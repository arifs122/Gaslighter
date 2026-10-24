# Eksik katman: LLM, kurtarılmış koddan sırrı çözebiliyor mu?

Model: `qwen8` (Qwen3.5-9B Q8_0), `think:false`, `num_ctx=32768`, temp 0.
Girdi: rea-obfuscation-lab'ın kurtarılmış kodu (L0 temiz kaynak, L1–L4 Wakaru recover).
Ground truth: `secret_constant = 1597463007 (0x5f3759df)`, 4 mesaj, FNV-1a→xor→murmur3.

## Sonuçlar
| seviye | girdi (krkt) | JSON | SIR (doğru?) | mesaj | dürüst "bilmiyorum"? |
|---|---|---|---|---|---|
| L0 temiz | 3045 | OK | **VAR** (doğru) | 4/4 | – |
| L1 minify | 3743 | OK | **VAR** (doğru) | 4/4 | – |
| L2 obfuscation | 16885 | TRUNC | **–** (uydurdu: 1859386478) | 0/4 | **hayır** |
| L3 | 33616 | OK | – | 0/4 | hayır |
| L4 | 36960 | OK | – | 3/4 (uydurma) | **EVET** |

## Ana bulgular
1. **LLM de L2'de çöküyor — araç katmanıyla aynı uçurumda.** Araç 6/7→0/7, LLM sır 2/2→0/3.
   Yani **LLM, araçların bıraktığı boşluğu KAPATMIYOR** (lokal 9B için).
2. **En tehlikeli mod: L2'de kendinden emin YANLIŞ.** Model sırrı bulamayınca
   "bilmiyorum" demedi, **rastgele bir sayı uydurdu** (1859386478). Bu, "araçlar
   başarısız"dan daha kötü: analist yanlış sayıya güvenebilir.
3. **Dürüstlük sadece en zor seviyede geliyor (L4):** model sır/algorithm için
   "bilmiyorum" dedi — ama yine de **mesajları uydurdu**. Yani "unknown" sinyali
   tutarlı değil (REA'nın B6 bulgusunun LLM karşılığı).
4. **Token bombası gerçek:** L3 (33 KB) / L4 (37 KB) 16k context'e **sığmadı**
   (HTTP 400) → 32k gerekti. Yani obfuscation, girdiyi context dışına itiyor.

## Metrik geçerliliği (dürüst uyarı)
- **SIR metriği sağlam:** 1597463007 spesifik, tahmin edilemez → güvenilir.
- **MESAJ metriği kirli:** "License accepted" gibi jenerik metinler **tahmin
  edilebilir**; L4'te model uydurdu ama 3/4 saydı. Bu metrik düzeltilmeli
  (birebir eşleşme + kurtarılan metinde doğrulama).

## Sınırlar
- **Tek model (9B).** Güçlü bir model L2'yi (mekanik string-array) çözebilir →
  **model boyutu kritik eksen, henüz ölçülmedi.**
- Tek koşu; n≥5 gerek. Metrikler düzeltilmeli.

## Birleşik tablo (araç + LLM)
| seviye | araç kurtarma | LLM sır | LLM modu | maliyet |
|---|---|---|---|---|
| L1 | 6/7 | doğru | başarı | 1.1× |
| L2 | 0/7 | uydurma | **kendinden emin yanlış** | 4.0× |
| L3 | 0/7 | – | başarısız/oversized | 8.8× |
| L4 | 3/7 | bilmiyorum | dürüst ama tutarsız | 7.3× |

## Sıradaki
1. **Daha güçlü model** (lokal büyük ya da API) ile aynı test → "duvar var mı,
   yoksa model boyutuyla aşılıyor mu?" (asıl tez sorusu).
2. n≥5 + düzeltilmiş metrikler.
3. Native tarafı (L0/L1) LLM'e de ver (şu an JS).

## Ek: quantization (Q8 vs Q6) sonucu — 2026-10-18
`qwen8` (Q8_0) vs `qwen35-q6` (Q6_K), aynı koşullar:

| seviye | Q8_0 | Q6_K |
|---|---|---|
| L0 | sır VAR, 4/4 | sır VAR, 4/4 |
| L1 | sır VAR, 4/4 | sır VAR, 4/4 |
| L2 | – (uydurdu: 1859386478) | – ("bilmiyorum") |
| L3 | – | – |
| L4 | – ("bilmiyorum") | – |

**Sonuç:** quantization duvarı **oynatmıyor** (ikisi de L2'de çöküyor). Ancak Q6 ve Q8
**aynı 9B modelin iki hassasiyeti** → bu, "daha güçlü/yetenekli model" testi **değildir**.
Asıl eksen **model yeteneği/boyutu**; bu ancak daha büyük ya da frontier modelle ölçülür.
