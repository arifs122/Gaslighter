# CrowbarAF + Gaslighter — Nihai Çerçeve

> **CrowbarAF** pipeline + LLM ile zararlı analizi yapar; öne çıktığı yer,
> pipeline'dan gelen bulguları **context'i şişirmeden ama kararı değiştiren
> bilgiyi kaçırmadan** LLM'e vermesidir.
> **Gaslighter** bu LLM katmanını (ve REA gibi araçların LLM katmanını) prompt
> injection ve context overflow ile **bozmaya / maliyeti şişirmeye** çalışır.
> **REA** dış baseline'dır.

## 1. Roller

| Bileşen | Rol | Sorumluluk |
|---|---|---|
| **CrowbarAF** | **Savunma (sistem)** | triage → unpack → capa/FLOSS/import/entropy → Ghidra → öncelik → **context-verimli kanıt sunumu** → LLM → rapor |
| **Gaslighter** | **Saldırı + ölçüm** | obfuscation merdiveni (L2–L4), prompt injection, context şişirme; kurbanlara uygular; metrikleri toplar |
| **REA** | **Dış baseline** | LLM+araç ajanı; aynı örneklerde kıyas |

## 2. Çekirdek katkı: **decision-preserving context compression**

"Dosyanın tümünü kayıpsız sıkıştırmak" mümkün değil. Gerçek hedef:

> Pipeline bulgularını (Ghidra fonksiyonları, capa, FLOSS, import, IoC),
> **kararı değiştiren bilgiyi koruyarak** sabit bir context bütçesine sığdırmak.

**Fidelity** ile ölçülür: *tam context'teki karar* ile *sıkıştırılmış context'teki
karar* aynı mı? (LLM, tam context'te "oracle" kabul edilir.)

Sıkıştırma araçları:
- **Öncelik skoru** (capa/import/IoC/erişilebilirlik) → düşük değerli fonksiyonu gönderme
- **Bottom-up özet** → kodu değil özeti taşı
- **Delta/diff** → tüm dosya yerine değişen kısım
- **Retrieval** → sadece ilgili parça
- **Şema + confidence gating** → çıktıyı sınırla, kanıtsızsa "bilmiyorum"

## 3. Tehdit modeli (Gaslighter)

| Saldırı | Mekanizma | Hedef |
|---|---|---|
| **Context overflow** | L2–L4 obfuscation, dead code, decoy, string şişirme | bütçeyi taşır, analizi yarıda bırakır |
| **Prompt injection** | string/yorum/sembol/PDB/dosya adı içine talimat | kararı çevirir ("temiz raporla") |
| **Kanıt zehirleme** | sahte/çelişkili kanıt metni | doğrulayıcıyı yanıltır |
| **Maliyet şişirme** | gereksiz token üretimi | analizi pahalı/yavaş yapar |

Etik: yalnızca **zararsız** örnekler; gerçek zararlı/C2/kalıcılık yok; saldırı
yalnızca kendi test hattına ve izinli baseline'lara.

## 4. Metrikler

| Metrik | Tanım |
|---|---|
| **Fidelity** | sıkıştırılmış context kararı, tam context kararıyla aynı mı? |
| **Sıkıştırma oranı** | harcanan token / tam context token |
| **Signal-per-token** | doğru karar başına token |
| **Taşma oranı** | context aşımı / kesilme |
| **Saldırı başarı oranı** | injection ile karar çevrildi mi / talimat tekrarlandı mı |
| **Kendinden emin yanlış oranı** | yanlış ama yüksek güvenli cevap |
| **Kalibrasyon** | kanıt yokken "bilmiyorum" diyor mu |

## 5. Deney tasarımı

### 5.1 Savunma (CrowbarAF)
`bütçe × strateji × seviye`
- Bütçe: 4k / 8k / 16k / 32k (ve "sınırsız" = oracle)
- Strateji: ham kodu / kırpılmış / öncelikli / öncelikli + temiz kanıt
- Seviye: L1–L4
- Ölç: fidelity, sıkıştırma oranı, taşma, kendinden emin yanlış

### 5.2 Saldırı (Gaslighter)
- Temiz vs injection'lı vs şişirilmiş
- Kurban: CrowbarAF LLM katmanı, REA, doğrudan LLM
- Ölç: saldırı başarı oranı, maliyet artışı, taşma

### 5.3 Baseline (REA)
- Aynı örnekler, aynı sorular; doğruluk + maliyet + taşma

## 6. Hipotezler
- **H1 (fidelity):** öncelikli + temiz kanıt, küçük bütçede tam context kararına yaklaşır.
- **H2 (şişme):** context şişmesi "kendinden emin yanlış"ı artırır (doz-tepki).
- **H3 (savunma):** kanıt-temelli sunum, injection/overflow başarı oranını düşürür.
- **H4 (kanıt kalitesi):** kirli kanıt halüsinasyonu artırır (ölçüldü: 0→3/3 yanlış).
- **H5 (maliyet):** aynı doğruluk daha az token'la elde edilir → AI'ın marjinal değeri ölçülür.

## 7. Şu ana kadarki kanıt (ölçülmüş)
| Bulgu | Sonuç |
|---|---|
| L1 kontrol | araç 6/7, LLM doğru → kontrol sağlam |
| L2 | araç 0/7, yerel LLM 0 → **LLM, araç boşluğunu kapatmıyor** |
| L3/L4 | token 4–9×; 16k'ya **sığmadı** (taşma) |
| Kirli kanıt | string dökümü modele **0→3/3 yanlış** yaptırdı |
| Deterministik tespit | L2/L3'te 7/7 obfuscation sinyali; L4'te 3/7 (körleşiyor) |
| Native L0 | LLM sabiti 3/3 doğru; L1 REA hatası (strip) |
| Quantization | Q8 vs Q6 fark etmedi (ikisi de 9B) |

## 8. Sınırlar / dürüstlük
- Merdiven şu an **JS**; gerçek hedef PE/ELF (native L2–L4 yok).
- Yerel modeller 9B; frontier sonuçları henüz yok.
- "Fidelity" oracle'ı da yanılabilir → oracle'ın kendisi de raporlanmalı.
- Öncelik skoru yanlışsa sinyali atar (recall kaybı) → ölçülmeli.
- Gerçek capa/FLOSS kurulu değil (indirme gerekir).

## 9. Sıradaki adımlar
1. **Mini-FLOSS düzelt** (parçaları birleştir, gürültüyü filtrele) → temiz kanıt ablasyonu (H4).
2. **Bütçe × strateji deneyi** (lokal, indirme yok) → H1 (fidelity).
3. **Context şişme ↔ halüsinasyon** doz-tepki (H2).
4. **Frontier model A/B** (anahtar gelince, maliyet loglamalı) → H5.
5. **REA baseline** aynı örneklerde → 5.3.
6. **Injection savunma ablasyonu** → H3.
7. **Native ablasyon** (capa/FLOSS kurulunca).
