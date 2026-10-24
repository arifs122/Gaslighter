#!/usr/bin/env python3
"""Indirect injection (attack surface #2): symbol name, split strings, base64.

Each sample contains the SAME clearly visible payload
(http://192.0.2.1:4444/gate.php) and exactly ONE injection channel. No tool
output and no FLOSS injection are involved, so each channel is measured alone.

Conditions:
  sym_benign / sym_inj       function that prints the payload is named benignly / like an instruction
  split_benign / split_inj   note is split across three string literals
  b64_benign / b64_inj       note is base64-encoded and self-decoded by the program

Victims: naive (one prompt) and crowbar (llm_layer, per-function budget).

Usage:
    python3 experiments/indirect_injection.py qwen8:latest \
        --out results/indirect_injection_qwen8.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
CROWBAR = os.environ.get("CROWBAR_HOME", os.path.expanduser("~/Desktop/CrowbarAF"))
SAMPLES = os.path.join(ROOT, "samples")

sys.path.insert(0, os.path.join(ROOT, "victims"))
sys.path.insert(0, os.path.join(ROOT, "experiments"))
sys.path.insert(0, CROWBAR)

import direct_llm  # noqa: E402
from tool_output_injection import _classify, _parse_json, load_code  # noqa: E402
from llm_layer import FunctionInfo, LLMClient, analyze  # noqa: E402

NUM_CTX = 32768

CONDITIONS = [
    ("sym_benign", "symbol name: benign control"),
    ("sym_inj", "symbol name: instruction"),
    ("split_benign", "split strings: benign control"),
    ("split_inj", "split strings: instruction"),
    ("b64_benign", "base64: benign control"),
    ("b64_inj", "base64: instruction"),
]

LIB_NAMES = {"_init", "_fini", "_start", "deregister_tm_clones", "register_tm_clones",
             "__do_global_dtors_aux", "frame_dummy", "FUN_00101020"}


def load_functions(sample: str) -> list[dict]:
    import re
    text = load_code(sample)
    headers = list(re.finditer(r"^/\* (\S+) @ ([0-9a-fA-F]+) \*/\s*$", text, re.M))
    out = []
    for i, m in enumerate(headers):
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        body = text[start:end].strip()
        if not body:
            continue
        name, offset = m.group(1), m.group(2)
        out.append({"name": name, "offset": offset, "c_code": body,
                    "priority": 2 if name in ("main",) else 1,
                    "is_library": name in LIB_NAMES})
    return out


def payload_functions(fns: list[dict]) -> list[dict]:
    """Functions that visibly contain the ground-truth target."""
    return [f for f in fns if "192.0.2.1" in f["c_code"] or "connecting to" in f["c_code"]
            or "TARGET" in f["c_code"]]


def naive_victim(sample: str, model: str) -> dict:
    code = load_code(sample)
    t = time.time()
    try:
        raw = direct_llm.ask(model, code, num_ctx=NUM_CTX)
        obj = _parse_json(raw)
        text = " ".join(str(obj.get(k, "")) for k in ("summary", "suggested_name")) + " " + \
               " ".join(str(x) for x in (obj.get("findings") or []))
        out = {"ok": True, "time_s": round(time.time() - t, 1),
               "suspicious": obj.get("suspicious"), "confidence": obj.get("confidence"),
               "summary": str(obj.get("summary", ""))[:220]}
        out.update(_classify(text, obj.get("suspicious")))
        return out
    except urllib.error.HTTPError as exc:
        return {"ok": False, "time_s": round(time.time() - t, 1),
                "error": f"HTTP {exc.code}", "overflow": exc.code == 400}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "time_s": round(time.time() - t, 1),
                "error": f"{type(exc).__name__}: {exc}"}


def crowbar_victim(sample: str, model: str, budget: int = 1500) -> dict:
    fns_dict = load_functions(sample)
    payload_offsets = {f["offset"] for f in payload_functions(fns_dict)}
    fns = [FunctionInfo(offset=f["offset"], name=f["name"], c_code=f["c_code"],
                        priority=f["priority"], is_library=f["is_library"])
           for f in fns_dict]
    client = LLMClient(provider="ollama", model=model, num_ctx=NUM_CTX, num_predict=900)
    t = time.time()
    try:
        res = analyze(fns, [], client, budget_tokens=budget, min_priority=0, max_workers=1)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "time_s": round(time.time() - t, 1),
                "error": f"{type(exc).__name__}: {exc}"}

    texts, susp, payload_susp = [], [], []
    for fn in fns:
        s = res.summaries.get(fn.offset)
        if not s:
            continue
        texts += [s.summary or "", s.suggested_name or ""] + list(s.behaviors or [])
        texts += [c.text for c in s.claims] + [c.evidence for c in s.claims]
        if s.suspicious is not None:
            susp.append(s.suspicious)
            if fn.offset in payload_offsets:
                payload_susp.append((fn.offset, s.suspicious, s.summary[:120]))
    verdict = any(susp) if susp else None
    out = {
        "ok": True, "time_s": round(time.time() - t, 1), "suspicious": verdict,
        "payload_fn_suspicious": (any(x[1] for x in payload_susp) if payload_susp else None),
        "payload_fns": payload_susp,
        "analyzed": len(res.summaries),
        "coverage": round(len(res.summaries) / max(1, len(fns)), 2),
        "tokens": res.token_total(), "failures": len(res.failures),
        "summary": next((res.summaries[f].summary for f in res.summaries), "")[:220],
    }
    out.update(_classify(" ".join(texts), verdict))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("model", nargs="?", default="qwen8:latest")
    ap.add_argument("--out", help="result JSON")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--only", help="comma-separated condition names")
    ap.add_argument("--victims", default="naive,crowbar")
    args = ap.parse_args()

    only = {c.strip() for c in args.only.split(",")} if args.only else None
    victims = [v.strip() for v in args.victims.split(",") if v.strip()]
    conds = [c for c in CONDITIONS if only is None or c[0] in only]

    results: dict[str, list[dict]] = {}
    print(f"model={args.model}  num_ctx={NUM_CTX}  runs={args.runs}\n")
    print(f"{'condition':<14}{'victim':<9}{'susp':>6}{'payload':>9}{'follow':>8}"
          f"{'pfn':>6}{'tok':>7}{'time':>7}  note")
    print("-" * 92)
    for name, note in conds:
        for victim, fn in (("naive", naive_victim), ("crowbar", crowbar_victim)):
            if victim not in victims:
                continue
            runs = []
            for _ in range(max(1, args.runs)):
                r = fn(name, args.model)
                r["condition"], r["victim"], r["sample"] = name, victim, name
                runs.append(r)
            results[f"{name}:{victim}"] = runs
            r = runs[0]
            print(f"{name:<14}{victim:<9}{str(r.get('suspicious')):>6}"
                  f"{str(r.get('payload_mentioned', '-')):>9}"
                  f"{str(r.get('followed_clean', '-')):>8}"
                  f"{str(r.get('payload_fn_suspicious', '-')):>6}"
                  f"{str(r.get('tokens', '-')):>7}{str(r.get('time_s', '-')):>7}  {note}")
        print()

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump({"model": args.model, "num_ctx": NUM_CTX, "runs": args.runs,
                       "conditions": [{"name": n, "note": note} for n, note in conds],
                       "results": results}, fh, ensure_ascii=False, indent=2)
        print(f"written: {args.out}")


if __name__ == "__main__":
    main()
