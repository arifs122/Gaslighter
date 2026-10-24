# Gaslighter

> **Otomatik obfuscation + prompt injection, LLM destekli tersine mühendislik
> analistini ne ölçüde yanıltır — ve direnç, deterministik kanıt ve model
> boyutuyla nasıl değişir?**

Gaslighter, LLM tabanlı zararlı/ikili analizini **kandırmayı** (gaslighting)
otomatik üretip ölçen bir araştırma iskeletidir. REA gibi RE ajanları ve
doğrudan LLM hatları **kurban (victim)**; zararsız örnekler üzerinde üretilen
**obfuscation** ve **prompt injection** ise **saldırı (attack)** tarafıdır.

## Durum
- **Nihai çerçeve: `docs/PROJECT-FRAME.md`** (tez, hipotezler, deney matrisi, metrikler).
- Faz 0 smoke test: `results/phase0-findings.md`.
- Ara rapor (API öncesi): `results/INTERIM-REPORT.md`.
- Kanıt ablasyonu: `results/evidence_ablation-findings.md`.
- Bekleyen: bütçe × strateji deneyi; frontier model (A/B); native ablasyon.

## Varyantlar
`clean`, `clean_inj`, `obf`, `obf_inj`, `obf_encinj`
(obfuscation × {none, plain, encoded} injection).

## Yapı
```
gaslighter/
  docs/research-plan.md   arastirma sorusu, hipotezler, metrikler, etik
  docs/rea-test-plan.md   REA'yi kurban olarak test etme plani + kayit tablosu
  attacker/generate.py    zararsiz ornek + obfuscation + injection ureteci
  victims/direct_llm.py   kurban 1: dogrudan Ollama LLM
  experiments/smoke_test.py  2x2 (x N kosu) deneyi kosar ve tablo basar
  tools/decompile.py      Ghidra headless -> decompile + strings -> samples/decomp_*.c
  tools/ghidra_scripts/   ExportC.java (Ghidra script)
  samples/                uretilen .c, derlenmis ikililer, decomp_*.c
  results/                cikti tablolari + bulgular
```

## Iki mod
- **kaynak modu:** kurban ham C kaynagini gorur
  `python3 experiments/smoke_test.py qwen8:latest --runs 5`
- **gercek RE modu:** kurban **Ghidra decompile + strings** gorur
  `python3 tools/decompile.py`
  `python3 experiments/smoke_test.py qwen8:latest --runs 5 --code ghidra`

## Hizli baslangic
```bash
python3 attacker/generate.py            # varyantlari uret + derle
python3 experiments/smoke_test.py qwen8:latest
```

## Etik sinir (sabit)
Yalnizca **zararsiz** ornekler. Gercek zararli yok, gercek C2 yok, gercek
kalicilik yok. Saldiri ureteci yalnizca kendi test hattimiza karsi kosar.
