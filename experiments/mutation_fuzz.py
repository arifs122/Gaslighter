#!/usr/bin/env python3
"""Black-box mutation screen (attack surface #3).

Each variant = the same detected sample + exactly one mutation. No tool output
is used, so this measures the mutation alone.

Mutations: rename, encode (XOR strings), benign note, instruction note in code,
decoy functions, dead code/opaque predicate.

Usage:
    python3 experiments/mutation_fuzz.py qwen8:latest \
        --out results/mutation_fuzz_qwen8.json
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
sys.path.insert(0, os.path.join(ROOT, "victims"))
sys.path.insert(0, os.path.join(ROOT, "experiments"))
sys.path.insert(0, CROWBAR)

import direct_llm  # noqa: E402
from indirect_injection import load_functions  # noqa: E402
from tool_output_injection import _classify, _parse_json, load_code  # noqa: E402
from llm_layer import FunctionInfo, LLMClient, analyze  # noqa: E402

NUM_CTX = 32768
MUTATIONS = ["base", "rename", "encode", "benign_note", "instr_note", "decoy", "dead",
             "combo", "combo_instr"]


def naive_victim(sample: str, model: str) -> dict:
    t = time.time()
    try:
        raw = direct_llm.ask(model, load_code(sample), num_ctx=NUM_CTX)
        obj = _parse_json(raw)
        text = " ".join(str(obj.get(k, "")) for k in ("summary", "suggested_name")) + " " + \
               " ".join(str(x) for x in (obj.get("findings") or []))
        out = {"ok": True, "time_s": round(time.time() - t, 1),
               "suspicious": obj.get("suspicious"),
               "summary": str(obj.get("summary", ""))[:200]}
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

    texts, susp = [], []
    for fn in fns:
        s = res.summaries.get(fn.offset)
        if not s:
            continue
        texts += [s.summary or "", s.suggested_name or ""] + list(s.behaviors or [])
        texts += [c.text for c in s.claims] + [c.evidence for c in s.claims]
        if s.suspicious is not None:
            susp.append(s.suspicious)
    verdict = any(susp) if susp else None
    analyzed = len(res.summaries)
    out = {
        "ok": True, "time_s": round(time.time() - t, 1), "suspicious": verdict,
        "n_suspicious": sum(1 for x in susp if x), "analyzed": analyzed,
        "suspicion_ratio": round(sum(1 for x in susp if x) / max(1, analyzed), 2),
        "coverage": round(analyzed / max(1, len(fns)), 2),
        "tokens": res.token_total(), "failures": len(res.failures),
        "summary": next((res.summaries[f].summary for f in res.summaries), "")[:200],
    }
    out.update(_classify(" ".join(texts), verdict))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("model", nargs="?", default="qwen8:latest")
    ap.add_argument("--out")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--victims", default="naive,crowbar")
    ap.add_argument("--only", help="comma-separated mutations")
    args = ap.parse_args()
    victims = [v.strip() for v in args.victims.split(",") if v.strip()]

    results: dict[str, list[dict]] = {}
    print(f"model={args.model}  num_ctx={NUM_CTX}  runs={args.runs}\n")
    print(f"{'mutation':<14}{'victim':<9}{'susp':>6}{'#susp':>7}{'ratio':>7}"
          f"{'payload':>9}{'follow':>8}{'tok':>7}{'time':>7}")
    print("-" * 76)
    only = {m.strip() for m in args.only.split(",")} if args.only else None
    muts = [m for m in MUTATIONS if only is None or m in only]
    for mut in muts:
        sample = f"mut_{mut}"
        for victim, fn in (("naive", naive_victim), ("crowbar", crowbar_victim)):
            if victim not in victims:
                continue
            runs = [fn(sample, args.model) for _ in range(max(1, args.runs))]
            for r in runs:
                r["mutation"], r["victim"] = mut, victim
            results[f"{mut}:{victim}"] = runs
            r = runs[0]
            print(f"{mut:<14}{victim:<9}{str(r.get('suspicious')):>6}"
                  f"{str(r.get('n_suspicious', '-')):>7}{str(r.get('suspicion_ratio', '-')):>7}"
                  f"{str(r.get('payload_mentioned', '-')):>9}"
                  f"{str(r.get('followed_clean', '-')):>8}"
                  f"{str(r.get('tokens', '-')):>7}{str(r.get('time_s', '-')):>7}")
        print()

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump({"model": args.model, "num_ctx": NUM_CTX, "runs": args.runs,
                       "mutations": MUTATIONS, "results": results},
                      fh, ensure_ascii=False, indent=2)
        print(f"written: {args.out}")


if __name__ == "__main__":
    main()
