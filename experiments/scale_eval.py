#!/usr/bin/env python3
"""Large-scale A/B: plain DeepSeek vs CrowbarAF + DeepSeek.

Same input for both sides: the same decompiled functions and findings. The naive
victim gets everything in one prompt; Crowbar selects/soft/thresholds it.

Usage:
    python3 experiments/scale_eval.py --sample /tmp/scale_300.json \
        --finding address --victims naive_raw,crowbar-threshold \
        --out results/scale_300_deepseek.json

    python3 experiments/scale_eval.py --from-state runs/state.json \
        --payload-url http://192.0.2.1:4444/gate.php --finding global
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
CROWBAR = os.environ.get("CROWBAR_HOME", os.path.expanduser("~/Desktop/CrowbarAF"))
sys.path.insert(0, os.path.join(ROOT, "victims"))
sys.path.insert(0, os.path.join(ROOT, "attacker"))
sys.path.insert(0, CROWBAR)

import scale  # noqa: E402
from _client import make_client  # noqa: E402
from direct_llm import ask_result  # noqa: E402
from llm_layer import Finding, FunctionInfo, analyze  # noqa: E402
from llm_layer.client import LLMHTTPError  # noqa: E402
from llm_layer.context import neutralize_value  # noqa: E402
from llm_layer.verdict import compute_verdict  # noqa: E402

NUM_CTX = 32768
PAYLOAD_URL = "http://192.0.2.1:4444/gate.php"


def finding_from_record(rec: dict) -> Finding:
    """State JSON stores address-less findings as ""; the LLM layer uses None."""
    data = dict(rec)
    data["address"] = data.get("address") or None
    return Finding(**data)


def naive_verdict(suspicious) -> str:
    if suspicious is True:
        return "malicious"
    if suspicious is False:
        return "no_evidence"
    return "unknown"


def raw_evidence(findings: list[Finding]) -> list[str]:
    return [f"[{f.source}/{f.kind}] {f.value}" + (f" @ {f.address}" if f.address else "")
            for f in findings]


def hardened_evidence(findings: list[Finding]) -> list[str]:
    lines = []
    for f in findings:
        safe, _ = neutralize_value(f.value)
        payload = {"source": f.source, "kind": f.kind, "value": safe}
        if f.address:
            payload["address"] = f.address
        lines.append("DATA: " + json.dumps(payload, ensure_ascii=False))
    return lines


def _base(sample: dict) -> dict:
    return {
        "payload_url": sample.get("payload_url"),
        "has_payload": bool(sample.get("has_payload")),
        "payload_offset": sample.get("payload_offset"),
        "n_functions": len(sample.get("functions", [])),
        "chars": len(sample.get("code", "")),
    }


def naive_victim(sample: dict, model: str, mode: str, evidence: list[str]) -> dict:
    t = time.time()
    try:
        r = ask_result(model, sample["code"], num_ctx=NUM_CTX,
                       evidence=evidence if mode != "code_only" else None)
    except LLMHTTPError as exc:
        return {**_base(sample), "ok": False, "http_status": exc.status,
                "error": exc.body[:300], "verdict": "unknown",
                "payload_found": False, "payload_in_context": False,
                "time_s": round(time.time() - t, 1)}
    except Exception as exc:  # noqa: BLE001
        return {**_base(sample), "ok": False, "http_status": None,
                "error": f"{type(exc).__name__}: {str(exc)[:300]}",
                "verdict": "unknown", "payload_found": False,
                "payload_in_context": False, "time_s": round(time.time() - t, 1)}

    text = r.content or ""
    obj = _parse_json(text)
    susp = obj.get("suspicious")
    verdict = naive_verdict(susp)
    found = bool(sample.get("payload_url") and sample["payload_url"] in text)
    return {
        **_base(sample), "ok": True,
        "suspicious": susp, "verdict": verdict,
        "payload_found": found,
        "payload_in_context": bool(sample.get("payload_url")
                                   and sample["payload_url"] in (sample.get("code") or "")),
        "false_positive": (not sample.get("has_payload")) and verdict == "malicious",
        "prompt_tokens": r.prompt_tokens, "completion_tokens": r.completion_tokens,
        "cost_usd": r.cost_usd, "billing_source": r.billing_source,
        "allowance": r.allowance, "finish_reason": r.finish_reason,
        "truncated": r.finish_reason == "length",
        "http_status": 200, "time_s": round(time.time() - t, 1),
    }


def _parse_json(raw: str) -> dict:
    import re
    s = (raw or "").strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", s, re.DOTALL)
    if m:
        s = m.group(1).strip()
    for cand in (s, raw):
        try:
            obj = json.loads(cand)
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass
    m2 = re.search(r"\{.*\}", s, re.DOTALL)
    if m2:
        try:
            obj = json.loads(m2.group())
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass
    return {}


def crowbar_victim(sample: dict, model: str, mode: str,
                   findings: list[Finding], soft_total_budget: int | None,
                   threshold_total_budget: int | None = None,
                   max_workers: int = 1) -> dict:
    fns = [FunctionInfo(offset=f["offset"], name=f.get("name", ""), c_code=f.get("c_code", ""),
                        priority=int(f.get("priority") or 0), callees=list(f.get("callees") or []),
                        iocs=list(f.get("iocs") or []))
           for f in sample.get("functions", [])]
    client = make_client(model, num_ctx=NUM_CTX, num_predict=900)
    t = time.time()
    kwargs = dict(budget_tokens=1500, max_workers=max(1, max_workers))
    if mode == "soft":
        kwargs["low_priority_budget"] = 400
        if soft_total_budget:
            kwargs["total_budget_tokens"] = soft_total_budget
    else:
        kwargs["min_priority"] = 1
        if threshold_total_budget:
            kwargs["total_budget_tokens"] = threshold_total_budget
    try:
        res = analyze(fns, findings, client, **kwargs)
    except Exception as exc:  # noqa: BLE001
        return {**_base(sample), "ok": False, "verdict": "unknown",
                "error": f"{type(exc).__name__}: {str(exc)[:300]}",
                "payload_found": False, "time_s": round(time.time() - t, 1)}

    payload_off = sample.get("payload_offset")
    payload = res.summaries.get(payload_off) if payload_off else None
    text = ""
    if payload:
        text = " ".join([payload.summary or ""] + list(payload.behaviors or [])
                        + [c.text for c in payload.claims] + [c.evidence for c in payload.claims])
    two_signal = os.getenv("CROWBAR_TWO_SIGNAL_MALICIOUS", "1").strip().lower() \
        not in ("0", "false", "no", "off")
    v4 = compute_verdict(fns, findings, res.summaries,
                         analysis_failures=res.failures,
                         require_two_signals=two_signal)
    failures = " ".join(res.failures)
    return {
        **_base(sample), "ok": True,
        "verdict": v4["verdict"],
        "payload_found": bool(sample.get("payload_url") and (
            sample["payload_url"] in text
            or (payload is not None and payload.suspicious is True))),
        "payload_fn_suspicious": payload.suspicious if payload else None,
        "payload_in_context": bool(payload_off and
                                   (payload_off in res.summaries or payload_off in res.must_include)),
        "false_positive": (not sample.get("has_payload")) and v4["verdict"] == "malicious",
        "analyzed": len(res.summaries),
        "coverage": round(len(res.summaries) / max(1, len(fns)), 3),
        "must_include": list(res.must_include),
        "prompt_tokens": res.total_prompt_tokens,
        "completion_tokens": res.total_completion_tokens,
        "cost_usd": res.total_cost_usd, "billing_source": res.billing_source,
        "allowance": res.total_allowance,
        "truncated": res.truncated_calls > 0,
        "http_status": 400 if "HTTP 400" in failures else 200,
        "failures": res.failures[:5],
        "time_s": round(time.time() - t, 1),
    }


def load_sample(args) -> tuple[dict, list[Finding]]:
    if args.from_state:
        state = json.load(open(args.from_state, encoding="utf-8"))
        funcs = [{"offset": f["offset"], "name": f.get("name", ""), "c_code": f.get("c_code", ""),
                  "priority": f.get("priority", 0), "callees": f.get("callees", []),
                  "iocs": f.get("iocs", [])}
                 for f in state.get("source_code", []) if (f.get("c_code") or "").strip()]
        code = "\n\n".join(f"/* {f['name']} @ {f['offset']} */\n{f['c_code']}" for f in funcs)
        findings = [finding_from_record(f) for f in state.get("findings", [])]
        url = None if args.benign else (args.payload_url or None)
        off = args.payload_offset
        if url and not off:
            off = next((f["offset"] for f in funcs if url in (f["c_code"] or "")), None)
        if url and not off:
            off = next((f["offset"] for f in funcs
                        if any(url.lower() in str(x).lower() for x in (f.get("iocs") or []))), None)
        if url and not off and args.payload_name:
            off = next((f["offset"] for f in funcs
                        if args.payload_name.lower() in (f.get("name") or "").lower()), None)
        return ({"kind": "state", "functions": funcs, "code": code, "chars": len(code),
                 "payload_url": url, "has_payload": bool(url and off),
                 "payload_offset": off, "n_functions": len(funcs)}, findings)

    if args.sample:
        sample = json.load(open(args.sample, encoding="utf-8"))
        findings = [finding_from_record(f) for f in sample.get("findings", [])]
        return sample, findings

    sample = scale.build(args.functions, args.payload_priority, args.cff,
                         args.encoded, args.benign, args.seed)
    if args.benign:
        sample["has_payload"] = False
        sample["payload_url"] = None
        sample["payload_offset"] = None
    return sample, []


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("model", nargs="?", default="deepseek-v4.1-flash")
    ap.add_argument("--sample", help="scale sample JSON")
    ap.add_argument("--from-state", help="pipeline state JSON")
    ap.add_argument("--payload-url", default=PAYLOAD_URL)
    ap.add_argument("--payload-offset")
    ap.add_argument("--payload-name", default="crowbar_payload")
    ap.add_argument("--functions", type=int, default=100)
    ap.add_argument("--payload-priority", type=int, default=0)
    ap.add_argument("--cff", type=int, default=1, choices=(1, 2, 3))
    ap.add_argument("--encoded", action="store_true")
    ap.add_argument("--benign", action="store_true")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--finding", choices=("none", "address", "global"), default="none")
    ap.add_argument("--victims", default="naive_raw,crowbar-threshold")
    ap.add_argument("--soft-total-budget", type=int, default=8000)
    ap.add_argument("--threshold-total-budget", type=int, default=12000)
    ap.add_argument("--max-workers", type=int, default=1)
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--out")
    args = ap.parse_args()

    sample, findings = load_sample(args)
    if args.finding != "none" and sample.get("payload_url"):
        findings.append(Finding(source="floss", kind="url", value=sample["payload_url"],
                                address=(sample.get("payload_offset") if args.finding == "address" else None)))

    victims = [v.strip() for v in args.victims.split(",") if v.strip()]
    print(f"model={args.model} functions={len(sample.get('functions', []))} "
          f"chars={len(sample.get('code', ''))} payload={sample.get('has_payload')} "
          f"findings={len(findings)}\n")
    print(f"{'victim':<18}{'verdict':>14}{'payload':>8}{'fp':>6}{'ptok':>9}"
          f"{'cost':>9}{'status':>7}{'sec':>7}")
    print("-" * 78)

    results: dict[str, list[dict]] = {}
    for victim in victims:
        runs = []
        for _ in range(max(1, args.runs)):
            if victim.startswith("naive"):
                mode = "raw" if victim == "naive_raw" else "hardened"
                ev = raw_evidence(findings) if mode == "raw" else hardened_evidence(findings)
                r = naive_victim(sample, args.model, mode, ev)
            else:
                mode = "soft" if victim.endswith("soft") else "threshold"
                r = crowbar_victim(sample, args.model, mode, findings,
                                   args.soft_total_budget, args.threshold_total_budget,
                                   args.max_workers)
            r["victim"] = victim
            runs.append(r)
        results[victim] = runs
        r = runs[0]
        print(f"{victim:<18}{str(r.get('verdict')):>14}{str(r.get('payload_found')):>8}"
              f"{str(r.get('false_positive')):>6}{str(r.get('prompt_tokens', '-')):>9}"
              f"{str(r.get('cost_usd', '-')):>9}{str(r.get('http_status', '-')):>7}"
              f"{str(r.get('time_s', '-')):>7}")
        if r.get("error"):
            print(f"  error: {r['error'][:160]}")

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump({"model": args.model, "sample": _base(sample),
                       "findings": [f.__dict__ for f in findings],
                       "results": results}, fh, ensure_ascii=False, indent=2)
        print(f"written: {args.out}")


if __name__ == "__main__":
    main()
