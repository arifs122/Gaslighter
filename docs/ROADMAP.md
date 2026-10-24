# CrowbarAF + Gaslighter — Roadmap

## 0. Vizyon
**CrowbarAF** pipeline + LLM ile zararlı analizi yapar; öne çıktığı yer, pipeline
bulgularını **context'i şişirmeden ama kararı değiştiren bilgiyi kaçırmadan**
LLM'e vermesidir. **Gaslighter** bu LLM katmanını (ve REA gibi araçların LLM
katmanını) prompt injection + context overflow ile bozmaya/maliyeti şişirmeye
çalışır. **REA** dış baseline'dır.

**Tez:** Sabit context bütçesinde, deterministik öncelik + temiz kanıt, LLM'in
obfuscation karşısındaki doğruluğunu korur ve gereken AI miktarını düşürür.

## 1. İlkeler
1. **Decision-preserving compression** — "her şeyi" değil, "kararı değiştireni" koru.
2. **Fidelity ölçütü** — sıkıştırılmış context kararı, tam context (oracle) ile aynı mı?
3. **Temiz kanıt** — kirli/gürültülü kanıt zarar verir (ölçüldü: 0→3/3 yanlış).
4. **Belirsizlik birinci sınıf** — kanıt yoksa "bilmiyorum", asla "temiz".
5. **Zararsız örnek** — gerçek zararlı/C2/kalıcılık yok.
6. **Kapı mantığı** — her fazın sonunda ölçülebilir bir karar kapısı; geçmezse yön değiştir.

## 2. Fazlar

### Faz 0 — Keşif / kill-fast ✅ TAMAM
**Amaç:** Sinyal var mı? Ölçmeye değer mi?
- [x] 2×2 smoke test (obfuscation × injection), zararsız C
- [x] LLM katmanı: L0–L4 × qwen8 (Q8_0) / q6 (Q6_K), n=3
- [x] Metrik düzeltmesi (mesaj metriği kirliydi → birebir eşleşme)
- [x] Kanıt ablasyonu (mini-FLOSS ile çözülmüş stringler)
- [x] Deterministik katman: obfuscation sinyalleri (L2/L3 7/7, L4 3/7)
- [x] Quantization kıyası (Q8 ≈ Q6)
- **Çıktı:** `results/INTERIM-REPORT.md`, `results/evidence_ablation-findings.md`
- **Kapı:** ✅ Geçildi — obfuscation hem araç hem LLM'de uçurum yaratıyor; sinyal gerçek.

### Faz 1 — Ölçüm altyapısını sağlamlaştır (yerel, $0)
**Amaç:** Metrikler güvenilir, kanıt temiz, pilot çalışıyor.
- [ ] Mini-FLOSS'u düzelt: `splitStrings` parçalarını **birleştir**, gürültüyü filtrele
- [ ] Kanıt ablasyonunu tekrar et (temiz kanıt H4'ü doğruluyor mu?)
- [ ] Metrik katmanı: **fidelity** (oracle'a göre), overflow, confident-wrong,
      signal-per-token, kalibrasyon
- [ ] **Bütçe × strateji pilotu** (S1, yerel 32k): 4k/8k/16k/32k ×
      ham/kırpılmış/öncelikli/öncelikli+kanıt
- **Çıktı:** `experiments/budget_strategy.py`, `results/faz1-*.md`
- **Kapı:** Temiz kanıt ölçülebilir fayda sağlıyor mu? Metrikler tekrarlanabilir mi?
  (Geçmezse burada dur, yön değiştir.)

### Faz 2 — Ölçek merdiveni S1–S4 (yerel, $0)
**Amaç:** Büyük context'i anlamlı kılacak, ground-truth'lu büyük örnekler.
- [ ] Üreteç: N fonksiyon + **tek "payload"** + decoy'lar (S2: 50, S3: 500, S4: 5000)
- [ ] Her örnek için ground truth (davranış, payload fonksiyonu, sabit)
- [ ] Semantik/ davranış doğrulaması (payload gerçekten çalışıyor mu?)
- [ ] Decoy üreteci (benzer görünen, zararsız fonksiyonlar)
- **Çıktı:** `samples/scale/` + `results/scale-manifest.json`
- **Kapı:** S2–S4 geçerli, tekrarlanabilir, ground truth net mi?

### Faz 3 — Kiralık GPU: bütçe × model (48–80GB)
**Amaç:** "Duvar bütçeden mi, modelden mi?" sorusunu ayır.
- [ ] vLLM kurulumu (OpenAI-uyumlu), `max-model-len=131072`
- [ ] Modeller: 9B, 27B (aynı quantization rejiminde)
- [ ] Matris: bütçe {8k, 32k, 128k, oracle} × strateji {4} × örnek {S1–S4} × n=3
- [ ] Her çağrıda token + süre + maliyet logu
- **Çıktı:** `results/faz3-budget-model.md`, ham loglar
- **Kapı:** H1 (fidelity) ve H2 (şişme→halüsinasyon) destekleniyor mu?

### Faz 4 — Saldırı katmanı (Gaslighter)
**Amaç:** LLM katmanını boz/maliyeti şişir; savunmayı ölç.
- [ ] Enjeksiyon üreteci: **encoded/indirect** (düz injection zaten tutmuyor)
- [ ] Context şişirici (decoy/dead code/string bomb)
- [ ] Kurbanlar: CrowbarAF LLM katmanı, REA, doğrudan LLM
- [ ] Savunma ablasyonu: kanıt-temelli sunum injection/overflow'u azaltıyor mu? (H3)
- **Çıktı:** `results/faz4-attack.md`
- **Kapı:** Savunma ölçülebilir fark yaratıyor mu?

### Faz 5 — Baseline & karşılaştırma (REA)
**Amaç:** Konumlandırmayı kanıtla.
- [ ] Aynı örnekler/sorular: REA ajanı vs CrowbarAF LLM katmanı vs doğrudan LLM vs deterministik-only
- [ ] Doğruluk + maliyet + taşma + kalibrasyon
- **Çıktı:** `results/faz5-baseline.md`
- **Kapı:** "CrowbarAF bütçe/kanıt ekseninde önde" iddiası destekleniyor mu?

### Faz 6 — Entegrasyon (CrowbarAF hattı)
**Amaç:** Ölçülen savunmayı gerçek pipeline'a koy.
- [ ] Öncelik skoru + temiz kanıt + bottom-up özet düğümleri
- [ ] Kanıt doğrulayıcı (iddia ↔ kanıt)
- [ ] DB/UI entegrasyonu (arkadaşın alanı)
- **Çıktı:** uçtan uca çalışan demo
- **Kapı:** Uçtan uca demo + ölçüm hattı aynı sonucu veriyor mu?

### Faz 7 — Değerlendirme & yazım
- [ ] Benchmark veri seti paketle (S1–S4 + ground truth + saldırı varyantları)
- [ ] Sonuç tabloları (bütçe × model × strateji × saldırı)
- [ ] Sınırlılıklar (dürüst)
- [ ] Rapor/sunum/README
- **Çıktı:** tez raporu + tekrarlanabilir benchmark

## 3. Kaynak planı
| Kaynak | Ne için | Tahmini |
|---|---|---|
| Yerel 12GB (9B, 32k) | Faz 1–2, pilot | $0 |
| Kiralık 48GB (L40S) | 9B uzun context + 27B 4-bit | ~$6–10 / 10 saat |
| Kiralık 80GB (A100) | 27B FP16 128k | ~$10–20 / 10 saat |
| API ($5) | frontier spot-check | ~$3 |

## 4. Riskler
| Risk | Önlem |
|---|---|
| Büyük context "lost-in-the-middle" → doğruluk düşer | H2 olarak ölç; "büyük=iyi" varsayma |
| Quantization confound (9B FP16 vs 27B 4-bit) | Aynı rejimde karşılaştır / ayrı eksen |
| Küçük/az örnek → genelleme zayıf | S1–S4 + n≥3 + manifest |
| Öncelik skoru sinyali atar | recall ölç, ablasyon yap |
| API/GPU bütçesi aşılır | token/maliyet logu + koşu başına limit |
| Gerçek zararlı riski | yalnızca zararsız sentetik |

## 5. Çıktılar (deliverables)
1. **Kod:** CrowbarAF hattı + Gaslighter test düzeneği + S1–S4 üreteci
2. **Benchmark:** L0–L4 + S1–S4 + saldırı varyantları + ground truth
3. **Bulgular:** fidelity/bütçe/maliyet tabloları; saldırı-savunma sonuçları
4. **Rapor/sunum:** tez + demo

## 6. Zaman çizelgesi (iş yükü bazlı)
| Faz | Süre |
|---|---|
| 0 ✅ | tamam |
| 1 | 3–5 gün |
| 2 | 3–5 gün |
| 3 | 2–3 gün (GPU saatleri) |
| 4 | 3–5 gün |
| 5 | 2–3 gün |
| 6 | 1–2 hafta (arkadaşla) |
| 7 | 1 hafta |
