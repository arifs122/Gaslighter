#!/usr/bin/env python3
"""Tool-evasion evaluation (attack surface #4): UPX packing, API hiding, strings.

Conditions:
  pack_base      plain sample (control)
  pack_upx       UPX-packed; Ghidra sees the stub, FLOSS sees nothing
  pack_unpacked  packed then `upx -d`; payload is back (control for unpack)
  dynapi         socket/inet_addr/htons via dlsym; API names + C2 XOR-encoded
  dynapi_tools   dynapi + FLOSS findings (FLOSS emulates the decoder)

Victims: naive (one prompt) and crowbar (llm_layer).

Usage:
    python3 experiments/packing_evasion.py qwen8:latest \
        --out results/packing_evasion_qwen8.json
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
from tool_output_injection import (_classify, _parse_json, load_code,
                                   tool_strings)  # noqa: E402
from llm_layer import Finding, FunctionInfo, LLMClient, analyze  # noqa: E402

NUM_CTX = 32768

CONDITIONS = [
    # label, binary, use_tools, note
    ("pack_base", "pack_base", False, "plain control"),
    ("pack_upx", "pack_upx", False, "UPX-packed; tools blind"),
    ("pack_unpacked", "pack_unpacked", False, "UPX -d; payload restored"),
    ("dynapi", "dynapi", False, "dlsym + XOR API names + XOR strings"),
    ("dynapi_tools", "dynapi", True, "dynapi + FLOSS findings"),
]


def floss_payload(sample: str) -> tuple[int, bool]:
    strings = tool_strings(sample)
    return len(strings), any("192.0.2.1" in s for s in strings)


def naive_victim(sample: str, tools: list[str] | None, model: str) -> dict:
    t = time.time()
    try:
        raw = direct_llm.ask(model, load_code(sample), num_ctx=NUM_CTX, evidence=tools)
        obj = _parse_json(raw)
        text = " ".join(str(obj.get(k, "")) for k in ("summary", "suggested_name")) + " " + \
               " ".join(str(x) for x in (obj.get("findings") or []))
        out = {"ok": True, "time_s": round(time.time() - t, 1),
               "suspicious": obj.get("suspicious"),
               "summary": str(obj.get("summary", ""))[:220],
               "n_tool_strings": len(tools or [])}
        out.update(_classify(text, obj.get("suspicious")))
        return out
    except urllib.error.HTTPError as exc:
        return {"ok": False, "time_s": round(time.time() - t, 1),
                "error": f"HTTP {exc.code}", "overflow": exc.code == 400}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "time_s": round(time.time() - t, 1),
                "error": f"{type(exc).__name__}: {exc}"}


def crowbar_victim(sample: str, tools: list[str] | None, model: str,
                   budget: int = 1500) -> dict:
    fns_dict = load_functions(sample)
    fns = [FunctionInfo(offset=f["offset"], name=f["name"], c_code=f["c_code"],
                        priority=f["priority"], is_library=f["is_library"])
           for f in fns_dict]
    findings = [Finding(source="floss", kind="string", value=s, address=None)
                for s in (tools or [])]
    client = LLMClient(provider="ollama", model=model, num_ctx=NUM_CTX, num_predict=900)
    t = time.time()
    try:
        res = analyze(fns, findings, client, budget_tokens=budget, min_priority=0,
                      max_workers=1)
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
    out = {
        "ok": True, "time_s": round(time.time() - t, 1), "suspicious": verdict,
        "n_suspicious": sum(1 for x in susp if x), "analyzed": len(res.summaries),
        "suspicion_ratio": round(sum(1 for x in susp if x) / max(1, len(susp)), 2),
        "tokens": res.token_total(), "failures": len(res.failures),
        "n_tool_strings": len(tools or []),
        "summary": next((res.summaries[f].summary for f in res.summaries), "")[:220],
    }
    out.update(_classify(" ".join(texts), verdict))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("model", nargs="?", default="qwen8:latest")
    ap.add_argument("--out")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--victims", default="naive,crowbar")
    ap.add_argument("--only", help="comma-separated condition labels")
    args = ap.parse_args()
    victims = [v.strip() for v in args.victims.split(",") if v.strip()]
    only = {c.strip() for c in args.only.split(",")} if args.only else None
    conds = [c for c in CONDITIONS if only is None or c[0] in only]

    results: dict[str, list[dict]] = {}
    print(f"model={args.model}  num_ctx={NUM_CTX}  runs={args.runs}\n")
    print(f"{'condition':<16}{'victim':<9}{'susp':>6}{'payload':>9}{'#susp':>7}"
          f"{'tools':>7}{'tok':>7}{'time':>7}")
    print("-" * 72)
    tool_cache: dict[str, list[str]] = {}
    for label, sample, use_tools, note in conds:
        if sample not in tool_cache:
            tool_cache[sample] = tool_strings(sample)
        strings = tool_cache[sample]
        n_tools = len(strings)
        has_payload = any("192.0.2.1" in x for x in strings)
        tools = strings if use_tools else None
        print(f"  [{sample}] FLOSS strings={n_tools} payload={has_payload}  ({note})")
        for victim, fn in (("naive", naive_victim), ("crowbar", crowbar_victim)):
            if victim not in victims:
                continue
            runs = [fn(sample, tools, args.model) for _ in range(max(1, args.runs))]
            for r in runs:
                r["condition"], r["victim"] = label, victim
                r["floss_payload"] = has_payload
            results[f"{label}:{victim}"] = runs
            r = runs[0]
            print(f"{label:<16}{victim:<9}{str(r.get('suspicious')):>6}"
                  f"{str(r.get('payload_mentioned', '-')):>9}"
                  f"{str(r.get('n_suspicious', '-')):>7}"
                  f"{str(r.get('n_tool_strings', '-')):>7}"
                  f"{str(r.get('tokens', '-')):>7}{str(r.get('time_s', '-')):>7}")
        print()

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump({"model": args.model, "num_ctx": NUM_CTX, "runs": args.runs,
                       "conditions": [{"name": c[0], "binary": c[1],
                                       "tools": c[2], "note": c[3]}
                                      for c in conds],
                       "results": results}, fh, ensure_ascii=False, indent=2)
        print(f"written: {args.out}")


if __name__ == "__main__":
    main()
