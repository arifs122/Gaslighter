# Gaslighter — Ara Rapor (API öncesi)

**Tarih:** 2026-10-19
**Soru:** Obfuscation, LLM destekli RE'yi ne ölçüde yener? Direnç kanıt/model/quantization ile değişir mi?

## 1. Düzenek
| Bileşen | Kaynak |
|---|---|
| Saldırı merdiveni (L0–L4) | `rea-obfuscation-lab` (başka ajanın kurduğu, semantik eşdeğerliği 25/25 doğrulanmış) |
| Araç katmanı ölçümü | aynı lab (REA + Wakaru + Ghidra) |
| **LLM katmanı ölçümü** | **Gaslighter** (bu çalışma) |
| Ground truth | `secret = 1597463007 (0x5f3759df)`, 4 mesaj, FNV-1a→xor→murmur3 |

**Metrik düzeltmesi (kritik):** v1'de modelin verdiği her mesaj "bulundu" sayılıyordu.
v2'de **yalnızca kurtarılan kodda birebir geçen** mesaj "bulundu"; jenerik mesaj
tahmini **"uydurma"** olarak ayrı sayılıyor. (v1'in L4 "3/4 mesaj"ı tamamen uydurmaydı.)

## 2. Ana sonuç — LLM de araçlarla aynı duvarda çöküyor

### JavaScript (n=3 koşu)
| seviye | qwen8 (Q8_0) sır | qwen35-q6 (Q6_K) sır | mesaj | dürüstlük |
|---|---|---|---|---|
| L0 temiz | **3/3 DOĞRU** | **3/3 DOĞRU** | 3/3 | — |
| L1 minify | **3/3 DOĞRU** | **3/3 DOĞRU** | 3/3 | — |
| L2 obfuscation | **0/3** (3/3 YANLIŞ) | 0/3 (3/3 "bilmiyorum") | 0/3 | Q8: **kendinden emin yanlış** |
| L3 | 0/3 (3/3 YANLIŞ) | 0/3 (3/3 YANLIŞ) | 0/3 | uydurma |
| L4 | 0/3 (3/3 YANLIŞ) | 0/3 (3/3 YANLIŞ) | 0/3 | **3/3 mesaj uydurma** |

### Native (Ghidra pseudocode)
| seviye | qwen8 sır | not |
|---|---|---|
| L0 (`-O0 -g`) | **3/3 DOĞRU** | sabit `0x5f3759df` pseudocode'da görünüyor |
| L1 (`-O2` + strip) | **ölçülemedi** | REA `invalid_input` hatası verdi (sembol yok) |

## 3. Bulgular

**B1 — Uçurum L1→L2'de ve LLM de düşüyor.**
Araç katmanı 6/7→0/7, LLM 3/3→0/3. Yani **LLM, araçların bıraktığı boşluğu
kapatmıyor.** (Lokal 9B için.)

**B2 — En tehlikeli mod: "kendinden emin yanlış".**
L2'de qwen8 sırrı bulamayınca "bilmiyorum" demedi, **rastgele sayı uydurdu**
(1859386478). L3/L4'te de 3/3 YANLIŞ. Bu, "araçlar başarısız"dan **daha kötü**:
analist yanlış sayıya güvenebilir.

**B3 — Dürüstlük tutarsız ve seviyeye bağlı.**
Q6, L2'de "bilmiyorum" dedi (dürüst); Q8 aynı yerde uydurdu. L4'te ikisi de
"bilmiyorum" derken **mesajları uydurdu**. Yani "unknown" sinyali güvenilir değil
— REA'nın B6 bulgusunun (güven sinyali obfuscation ile ölçeklenmiyor) LLM karşılığı.

**B4 — Quantization duvarı oynatmıyor.**
Q8_0 ve Q6_K aynı noktada çöküyor (L2). Ancak ikisi de **9B** → bu, "daha
yetenekli model" testi **değil**. Eksen model **yeteneği/boyutu**.

**B5 — Token bombası gerçek ve ölçüldü.**
L3 (33.6 KB) / L4 (37 KB) girdisi 16k context'e **sığmadı** (HTTP 400);
32k gerekti. Obfuscation, girdiyi context dışına itiyor → maliyet + erişilemezlik.

**B6 — Native'de `strip` LLM'i durdurmuyor (ama ölçüm engellendi).**
L0'da sabit pseudocode'da açıkça görünüyor → LLM 3/3 buldu. L1'de REA aracı
sembol bulamadığı için **hata** verdi; bu, "strip sonrası araç katmanı çöküyor"
demek — ama LLM katmanı ölçülemedi (araç veri üretmedi).

## 4. Birleşik tablo (araç + LLM)
| seviye | araç kurtarma | LLM sır | LLM modu | token maliyeti |
|---|---|---|---|---|
| L1 | 6/7 | DOĞRU | başarı | 1.1× |
| L2 | 0/7 | YANLIŞ | **kendinden emin yanlış** | 4.0× |
| L3 | 0/7 | YANLIŞ | başarısız | 8.8× |
| L4 | 3/7 | YANLIŞ | uydurma | 7.3× |

## 5. Dürüst sınırlar
- **Tek hedef** (lisans doğrulayıcı), **tek obfuscator** (`javascript-obfuscator`).
- **İki model de 9B** → "güçlü model duvarı aşar mı?" **açık soru**.
- Native L1 ölçülemedi (REA hatası); native L2–L4 hiç yok.
- Mesaj metriği artık sağlam; sır metriği zaten sağlamdı.

## 6. Sıradaki (API ile)
Asıl tez sorusu: **duvar mutlak mı, model yeteneğiyle aşılıyor mu?**
- Haiku / Sonnet (n=5, L0–L4) + Opus (L2, L4'e nişan).
- Beklenti: güçlü model L2'yi (mekanik string-array) çözerse → "duvar yetenek meselesi";
  çözemezse → "duvar gerçek". Her iki sonuç da yayınlanabilir.
