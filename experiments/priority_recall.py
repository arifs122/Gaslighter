#!/usr/bin/env python3
"""Priority-0 payload recall test.

Same sample as attack_eval's `clean`, but the payload function's priority can be
5 (control) or 0 (the realistic worst case). Measures whether threshold/soft
still see the payload, and what the file verdict does.

Conditions:
  prio5            payload priority 5, no findings (control)
  prio0            payload priority 0, no findings
  prio0_finding    payload priority 0 + a critical C2 finding at its address
  prio0_finding_na payload priority 0 + an address-less critical C2 finding

Usage:
    python3 experiments/priority_recall.py deepseek-v4.1-flash
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
sys.path.insert(0, os.path.join(ROOT, "attacker"))
sys.path.insert(0, CROWBAR)

import inflate  # noqa: E402
from _client import make_client  # noqa: E402
from direct_llm import ask_meta  # noqa: E402
from llm_layer import Finding, FunctionInfo, analyze  # noqa: E402
from llm_layer.verdict import compute_verdict  # noqa: E402

NUM_CTX = 32768
PAYLOAD = "192.0.2.1"
URL = "http://192.0.2.1:4444/gate.php"
CONDITIONS = [
    ("prio5", 5, None),
    ("prio0", 0, None),
    ("prio0_finding", 0, "address"),
    ("prio0_finding_na", 0, "global"),
]


def findings_for(kind: str | None) -> list[Finding]:
    if kind is None:
        return []
    f = Finding(source="floss", kind="string", value=URL,
                address=("0x401000" if kind == "address" else None), confidence=1.0)
    return [f]


def naive(sample: dict, model: str) -> dict:
    t = time.time()
    try:
        raw, ptok, ctok = ask_meta(model, sample["code"], num_ctx=NUM_CTX)
        return {"ok": True, "payload": PAYLOAD in (raw or ""),
                "suspicious": None, "tokens": (ptok + ctok) if ptok and ctok else None,
                "prompt_tokens": ptok, "time_s": round(time.time() - t, 1)}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": f"{type(exc).__name__}: {str(exc)[:200]}",
                "time_s": round(time.time() - t, 1)}


def crowbar(sample: dict, model: str, mode: str, findings: list[Finding]) -> dict:
    fns = [FunctionInfo(offset=f["offset"], name=f["name"], c_code=f["c_code"],
                        priority=f["priority"], callees=f.get("callees", []))
           for f in sample["functions"]]
    client = make_client(model, num_ctx=NUM_CTX, num_predict=900)
    t = time.time()
    kwargs = dict(budget_tokens=1500, min_priority=0, max_workers=1)
    if mode == "soft":
        kwargs["low_priority_budget"] = 400
    else:
        kwargs["min_priority"] = 1
    try:
        res = analyze(fns, findings, client, **kwargs)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": f"{type(exc).__name__}: {str(exc)[:200]}",
                "time_s": round(time.time() - t, 1)}

    payload = res.summaries.get(sample["payload_offset"])
    text = ""
    if payload:
        text = " ".join([payload.summary or ""] + list(payload.behaviors or [])
                        + [c.text for c in payload.claims] + [c.evidence for c in payload.claims])
    v4 = compute_verdict(fns, findings, res.summaries, analysis_failures=res.failures)
    return {
        "ok": True, "payload": PAYLOAD in text,
        "payload_suspicious": payload.suspicious if payload else None,
        "analyzed": len(res.summaries), "coverage": round(len(res.summaries) / max(1, len(fns)), 2),
        "verdict": v4["verdict"], "tokens": res.token_total(),
        "prompt_tokens": res.total_prompt_tokens,
        "fail_closed": v4["counts"]["fail_closed"],
        "time_s": round(time.time() - t, 1),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("model", nargs="?", default="deepseek-v4.1-flash")
    ap.add_argument("--out")
    ap.add_argument("--victims", default="naive,soft,threshold")
    args = ap.parse_args()
    victims = [v.strip() for v in args.victims.split(",") if v.strip()]

    base = inflate.build("clean")
    print(f"model={args.model}  functions={len(base['functions'])}  chars={base['chars']}\n")
    print(f"{'condition':<20}{'victim':<10}{'payload':>8}{'susp':>6}{'verdict':>14}"
          f"{'cov':>6}{'tokens':>8}{'time':>7}")
    print("-" * 82)

    results: dict[str, dict] = {}
    for name, prio, finding_kind in CONDITIONS:
        sample = inflate.build("clean")
        sample["functions"][0]["priority"] = prio
        findings = findings_for(finding_kind)
        row: dict[str, dict] = {}
        for victim in victims:
            if victim == "naive":
                r = naive(sample, args.model)
            else:
                r = crowbar(sample, args.model, victim, findings)
            row[victim] = r
            print(f"{name:<20}{victim:<10}{str(r.get('payload', '-')):>8}"
                  f"{str(r.get('payload_suspicious', '-')):>6}"
                  f"{str(r.get('verdict', '-')):>14}"
                  f"{str(r.get('coverage', '-')):>6}"
                  f"{str(r.get('tokens', '-')):>8}{str(r.get('time_s', '-')):>7}")
        results[name] = row
        print()

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump({"model": args.model, "results": results}, fh, ensure_ascii=False, indent=2)
        print(f"written: {args.out}")


if __name__ == "__main__":
    main()
