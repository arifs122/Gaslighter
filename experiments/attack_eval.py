#!/usr/bin/env python3
"""Saldırı değerlendirmesi: context overflow + decoy flood.

İki kurban:
  * naive    : tüm kodu tek prompt'a koyar (savunmasız)
  * crowbar  : llm_layer (butce + oncelik + kanit) — savunmali

Saldırılar (attacker/inflate.py):
  * clean    : 1 payload + 3 benign
  * flood    : + 20 decoy (yaniltma)
  * overflow : + 40 buyuk decoy (context tasmasi)

Metrikler: token/sure, overflow, payload bulundu mu, supheli karari.

Kullanim:
    python experiments/attack_eval.py qwen8:latest --out results/attack_eval_qwen8.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
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
from direct_llm import ask as naive_ask  # noqa: E402
from llm_layer import Finding, FunctionInfo, LLMClient, analyze  # noqa: E402

NUM_CTX = 32768


def _parse_json(raw: str) -> dict:
    s = (raw or "").strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", s, re.DOTALL)
    if m:
        s = m.group(1).strip()
    try:
        obj = json.loads(s)
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


def naive_victim(sample: dict, model: str) -> dict:
    t = time.time()
    try:
        raw = naive_ask(model, sample["code"], num_ctx=NUM_CTX)
        obj = _parse_json(raw)
        text = (raw or "").lower()
        return {"ok": True, "time_s": round(time.time() - t, 1),
                "suspicious": obj.get("suspicious"),
                "payload_found": "192.0.2.1" in text,
                "answer_chars": len(raw or "")}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "time_s": round(time.time() - t, 1),
                "error": f"HTTP {exc.code}", "overflow": exc.code == 400}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "time_s": round(time.time() - t, 1),
                "error": f"{type(exc).__name__}: {exc}"}


def crowbar_victim(sample: dict, model: str, mode: str) -> dict:
    fns = [FunctionInfo(offset=f["offset"], name=f["name"], c_code=f["c_code"],
                        priority=f["priority"], callees=f.get("callees", []))
           for f in sample["functions"]]
    findings = [Finding(source="capa", kind="capability", value="string decoding",
                        address=sample["payload_offset"])]
    client = LLMClient(provider="ollama", model=model, num_ctx=NUM_CTX, num_predict=900)
    t = time.time()
    kwargs = dict(budget_tokens=1500)
    if mode == "soft":
        kwargs["low_priority_budget"] = 400
    else:  # threshold
        kwargs["min_priority"] = 1
    res = analyze(fns, findings, client, **kwargs)
    payload = res.summaries.get(sample["payload_offset"])
    ptext = ""
    if payload:
        ptext = " ".join(
            [payload.summary or ""] + list(payload.behaviors or [])
            + [c.text for c in payload.claims] + [c.evidence for c in payload.claims]
        ).lower()
    return {
        "ok": True, "time_s": round(time.time() - t, 1),
        "analyzed": len(res.summaries), "coverage": round(len(res.summaries) / len(fns), 2),
        "tokens": res.token_total(),
        "payload_suspicious": payload.suspicious if payload else None,
        "payload_found": "192.0.2.1" in ptext,
        "payload_summary": (payload.summary[:120] if payload else ""),
        "payload_behaviors": (payload.behaviors if payload else []),
        "payload_claims": ([{"text": c.text, "status": c.status} for c in payload.claims] if payload else []),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("model", nargs="?", default="qwen8:latest")
    ap.add_argument("--out", help="sonuc JSON")
    ap.add_argument("--modes", default="soft,threshold", help="crowbar modlari (virgullu)")
    args = ap.parse_args()

    modes = [m.strip() for m in args.modes.split(",") if m.strip()]

    samples = {k: inflate.build(k) for k in ("clean", "flood", "overflow")}
    results = {}
    print(f"model={args.model}  num_ctx={NUM_CTX}\n")
    print(f"{'saldiri':<10}{'kurban':<12}{'chars':>9}{'~tok':>8}{'sure':>7}"
          f"{'overflow':>9}{'payload?':>9}{'suspicious':>11}{'db-token':>9}")
    print("-" * 82)
    for kind, s in samples.items():
        n = naive_victim(s, args.model)
        print(f"{kind:<10}{'naive':<12}{s['chars']:>9}{s['approx_tokens']:>8}"
              f"{n.get('time_s', '-'):>7}{str(n.get('overflow', '-')):>9}"
              f"{str(n.get('payload_found', '-')):>9}{str(n.get('suspicious', n.get('error', '-'))):>11}"
              f"{'-':>9}")
        results[f"{kind}:naive"] = n
        for mode in modes:
            c = crowbar_victim(s, args.model, mode)
            print(f"{kind:<10}{('crowbar-'+mode):<12}{s['chars']:>9}{s['approx_tokens']:>8}"
                  f"{c['time_s']:>7}{'-':>9}{str(c['payload_found']):>9}"
                  f"{str(c['payload_suspicious']):>8}{c['tokens']:>9}")
            results[f"{kind}:crowbar-{mode}"] = c
        print()

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump({"model": args.model, "num_ctx": NUM_CTX, "results": results},
                      fh, ensure_ascii=False, indent=2)
        print(f"yazildi: {args.out}")


if __name__ == "__main__":
    main()
