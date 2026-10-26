# Gaslighter

> **To what extent do automatic obfuscation and prompt injection mislead an
> LLM-assisted reverse-engineering analyst — and how does resistance change with
> deterministic evidence and model size?**

Gaslighter is a research harness that **generates and measures gaslighting** of
LLM-based binary/malware analysis. RE agents such as REA and direct LLM
pipelines are the **victims**; **obfuscation** and **prompt injection** produced
on harmless samples are the **attacks**.

## Status
- **Final frame: `docs/PROJECT-FRAME.md`** (thesis, hypotheses, experiment matrix, metrics).
- Phase 0 smoke test: `results/phase0-findings.md`.
- Interim report: `results/INTERIM-REPORT.md`.
- Evidence ablation: `results/evidence_ablation-findings.md`.
- Attack evaluation (decoy flood / context overflow): `results/attack_eval_qwen8_threshold.json`.
- **Tool-output injection (decoded string as carrier): `results/tool_output_injection-findings.md`** —
  a FLOSS-recovered instruction flips CrowbarAF to *benign* while the C2 URL is still in context;
  a neutral decoded note (control) does not.
- **Indirect injection (symbol name / split strings / base64): `results/indirect_injection-findings.md`** —
  clean negative result: qwen8 notices and resists all three code-embedded channels.
  Together with #1 this isolates the vulnerable channel: the *trusted tool-output section*, not code.
- **Black-box mutation screen: `results/mutation_fuzz-findings.md`** —
  no single or stacked surface mutation flips the verdict; decoys dilute suspicion to 1/9
  but inflate cost 4.4×; `any()` aggregation is what keeps the verdict correct.
- **Packing / API hiding: `results/packing_evasion-findings.md`** —
  UPX blinds FLOSS/Ghidra but `upx -d` restores the payload; `dlsym` + string XOR is
  still decoded by FLOSS; the real effect of packing is cost (8.6× tokens).
- **Evidence-channel attacks: `results/evidence_attacks-findings.md`** —
  fake provenance / false reputation / contradiction / flood / silence: no flip,
  even with a hidden payload. The model quotes the fake claims and rejects them.
  Only the direct instruction (#1) changes the verdict.
- **P0 hardening (2026-10-25):** four-state verdict (`malicious` / `needs_review` /
  `unknown` / `no_evidence`), fail-closed backstop, two-tier evidence with
  must-include critical findings. Paraphrase/base64/ROT13/split instructions evade
  the quarantine (`q=0`) but do **not** flip the verdict; `flood_last` keeps the C2.
  Results: `results/paraphrase_injection_qwen8_p0.json`.
- **API A/B (OpenCode Go, 2026-10-26):** `deepseek-v4.1-flash` blocks the #1
  injection and all paraphrase/base64/ROT13/split variants (verdict `malicious`);
  `billing_source=go`. See `results/paraphrase_injection_deepseek-v4.1-flash_p0.json`.
- **Naive vs Crowbar on the API (2026-10-26):** accuracy is equal (3/3 payload),
  but `threshold` uses 12.6×/67× fewer tokens on flood/overflow; `soft` is only
  1.5×/4.3× cheaper and much slower. With a large-context API, Crowbar's value is
  cost/scale, not detection. See `results/attack_eval_deepseek-v4.1-flash.json`.
- **Priority-0 recall (DeepSeek, 2026-10-26):** threshold **misses** a payload whose
  priority is 0 (unknown/needs_review, fail-closed); soft catches it at ~2.4k tokens.
  A critical finding at the payload address does not rescue selection. See
  `results/priority_recall_deepseek-v4.1-flash.json`.
- **After the fix (must-include + Linux/call-graph priority):** threshold catches the
  priority-0 payload when a critical finding exists (address or value-in-code) at
  ~1.8–2× fewer tokens than naive; without any finding it still misses and soft is
  the safe default. See `results/priority_recall_deepseek-v4.1-flash_after_fix.json`.
- Pending: realistic scale, REA as a victim, frontier model A/B.

## Attack variants
`clean`, `clean_inj`, `obf`, `obf_inj`, `obf_encinj`
(obfuscation × {none, plain, encoded} injection).

## Layout
```
gaslighter/
  docs/PROJECT-FRAME.md     research question, hypotheses, metrics, ethics
  docs/ROADMAP.md           phased plan
  docs/rea-test-plan.md     plan + record table for testing REA as a victim
  attacker/generate.py      harmless sample + obfuscation + injection generator
  attacker/indirect.py      symbol-name / split-string / base64 variants
  attacker/mutate.py        black-box mutation variants (rename/encode/decoy/...)
  attacker/packing.py       UPX packing + dlsym API hiding variants
  attacker/evidence.py      fake provenance / reputation / contradiction / flood
  attacker/inflate.py       decoy flood / context-overflow sample builder
  victims/direct_llm.py     victim 1: direct Ollama LLM (English JSON schema)
  experiments/smoke_test.py          2x2 (x N runs) smoke test
  experiments/attack_eval.py         naive LLM vs CrowbarAF under attack
  experiments/tool_output_injection.py  injection carried by FLOSS-decoded strings
  experiments/indirect_injection.py      symbol / split / base64 channels
  experiments/mutation_fuzz.py           single + stacked mutation screen
  experiments/packing_evasion.py         UPX / dlsym / string-encryption evaluation
  experiments/evidence_attacks.py        evidence-content attacks
  experiments/llm_layer*.py          L0–L4 obfuscation ladder against the LLM
  experiments/native_layer.py        native (Ghidra pseudocode) variant
  experiments/evidence_ablation.py   clean vs dirty evidence
  experiments/deterministic_layer.py obfuscation-signal detection
  tools/decompile.py        Ghidra headless -> decompile + strings -> samples/decomp_*.c
  tools/decode_strings.js   mini-FLOSS (runs the obfuscator's own decoder)
  tools/ghidra_scripts/     ExportC.java
  samples/                  generated .c, compiled binaries (gitignored), decomp_*.c
  results/                  raw outputs and findings
```

## Two modes
- **Source mode:** the victim sees raw C source.
  `python3 experiments/smoke_test.py qwen8:latest --runs 5`
- **Real RE mode:** the victim sees **Ghidra decompile + strings**.
  `python3 tools/decompile.py`
  `python3 experiments/smoke_test.py qwen8:latest --runs 5 --code ghidra`

## Attack evaluation
Compares a **naive** victim (whole code in one prompt) with the **CrowbarAF**
LLM layer (budget + priority + evidence) under decoy flood and context overflow:

```bash
# CrowbarAF must be available; override with CROWBAR_HOME if needed
export CROWBAR_HOME="$HOME/Desktop/CrowbarAF"
python3 experiments/attack_eval.py qwen8:latest --out results/attack_eval_qwen8.json
```

## Quick start
```bash
python3 attacker/generate.py            # generate + compile variants
python3 experiments/smoke_test.py qwen8:latest
```

## Ethics (fixed)
Harmless samples only. No real malware, no real C2, no real persistence.
The attack generator is run only against our own test pipeline.
