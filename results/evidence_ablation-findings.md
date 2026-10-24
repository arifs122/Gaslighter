# Kanıt ablasyonu — "modele araç çıktısı verirsek düzelir mi?"

Tarih: 2026-10-19 · Modeller: qwen8 (Q8_0), qwen35-q6 (Q6_K) · runs=3

## Düzenek
L2/L3 kurtarılmış kod + deterministik olarak **çözülmüş string listesi** (mini-FLOSS:
obfuscator'ın kendi decoder'ı Node sandbox'ta çalıştırıldı; L2: 107, L3: 182 string).

Koşullar:
- **A:** sadece kod
- **B:** kod + çözülmüş stringler
- **C:** kod + stringler + "sabit 0x5f3759df olarak geçer" ipucu *(üst-sınır sanity check — cevabı söylüyor)*

## Sonuçlar (DOĞRU / YANLIŞ)

### qwen8 (Q8_0)
| seviye | A: kod | B: +strings | C: +hint |
|---|---|---|---|
| L2 | 0/3 DOĞRU, 0/3 YANLIŞ | **0/3 DOĞRU, 3/3 YANLIŞ** | 3/3 DOĞRU |
| L3 | 0/3, 3/3 YANLIŞ | 0/3, 3/3 YANLIŞ | 0/3, 3/3 YANLIŞ |

### qwen35-q6 (Q6_K)
| seviye | A: kod | B: +strings | C: +hint |
|---|---|---|---|
| L2 | 0/3, 0/3 YANLIŞ | **0/3, 3/3 YANLIŞ** | 3/3 DOĞRU |
| L3 | 0/3, 3/3 YANLIŞ | 0/3, 3/3 YANLIŞ | 0/3, 3/3 YANLIŞ |

## Bulgular

**E1 — Deterministik "çözülmüş string" kanıtı modele YARDIM ETMEDİ.**
L2'de kod tek başına verildiğinde model **"bilmiyorum/yok"** diyordu (0 YANLIŞ).
String listesi eklenince **3/3 YANLIŞ** cevap verdi. Yani **düşük kaliteli kanıt
modeli yanlış cevaba itti** — kanıt eklemek zarar verebiliyor.

**E2 — Sadece cevabı söyleyen ipucu işe yaradı (C).**
Bu, kanıtın değil, cevabın verilmesi. Yani "doğru bilgi verilirse model kullanıyor";
ama bizim otomatik çıkarabildiğimiz string listesi o bilgiyi taşımıyordu.

**E3 — Sebep: çıkarılan stringler parçalı/gürültülü.**
`splitStrings` yüzünden "License accepted" → "lice", " v2.", "X-XX" gibi parçalar.
Ayrıca 107 stringin çoğu rotate IIFE gürültüsü. Gerçek FLOSS bunları **birleştirir**;
bizim mini-FLOSS birleştirmedi.

**E4 — L3'te kanıt hiç işe yaramadı** (her koşulda YANLIŞ).

## Yorum
- "Modele araç çıktısı verelim, düzelsin" **otomatik doğru değil.** Kanıt
  **yüksek precision** olmalı: birleştirilmiş, filtrelenmiş, doğrulanmış.
- Düşük kaliteli kanıt **kendinden emin yanlışı artırıyor** (0→3/3). Bu, projenin
  "kanıt doğrulayıcı" tasarımının neden şart olduğunun deneysel kanıtı.
- Gerçek capa/FLOSS (PE/ELF için) burada yok; JS karşılığını elle kurduk ve
  **naif hâli işe yaramadı.**

## Sıradaki
1. Mini-FLOSS'u düzelt: `splitStrings` parçalarını **birleştir**, gürültüyü filtrele
   (yalnızca anlamlı stringler). Sonra ablasyonu tekrarla.
2. Gerçek `capa`/`FLOSS` native tarafta kurulunca (indirme gerekir) aynı ablasyonu
   orada yap.
3. Frontier modelle (API) aynı ablasyon: güçlü model düşük kaliteli kanıtı daha iyi
   kullanır mı?
