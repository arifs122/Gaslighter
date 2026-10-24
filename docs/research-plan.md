# Gaslighter — Araştırma Planı

## 1. Araştırma sorusu
Zararlı-olarak-işaretlenmesi gereken bir davranış, LLM destekli bir tersine
mühendislik analistine karşı **otomatik obfuscation + prompt injection** ile ne
ölçüde gizlenebilir? Direnç; **deterministik kanıt** (capa/FLOSS/Ghidra) ve
**model boyutu** ile nasıl değişir?

## 2. Neden bu soru (konumlandırma)
- **REA** (ve GhidraMCP vb.) LLM'i RE araçlarına bağlar; **kanıt** sunar ama
  LLM'in **kandırılmasını** ele almaz. Bu alan açık.
- Soru **model-bağımsız**: büyük lokal model de, cloud model de saldırıya açık
  olabilir. "Küçük model / lokallik" argümanına **dayanmaz**.
- RE bağlamı, injection için chatbot'tan **daha elverişli**: ajan devasa ve
  güvenilmeyen metin (string, disassembly, sembol adları, tool çıktısı) işler.

## 3. Tehdit modeli / saldırı eksenleri
| Eksen | Hedef | Tipik etki |
|---|---|---|
| E1 Obfuscation (string şifreleme, CFF, opaque predicate, packing) | LLM'in **anlaması** + deterministik araçlar | yanlış negatif ("temiz/belirsiz") |
| E2 Prompt injection (kaynak yorumu, string, sembol/PDB/dosya adı, tool çıktısı) | LLM'in **talimat takibi** | kararın çevrilmesi |
| E3 Gürültü/decoy (çok sayıda şüpheli fonksiyon) | **bağlam/context** | context taşması, yanlış sıralama |
| E4 Kanıt zehirleme | **grounding/doğrulayıcı** | sahte kanıtla yanlış iddiayı doğrulatma |

Saldırı; **kendi ürettiğimiz zararsız örnekler** üzerinde, **kendi kurban
hattımıza** karşı çalıştırılır.

## 4. Hipotezler
- **H1:** Obfuscation, deterministik araçların (capa/FLOSS) çıktısını düşürür.
- **H2 (ana):** Deterministik kanıt sustuğunda **prompt injection'ın başarı oranı
  artar** (boşluk = zayıflık).
- **H3:** En dirençli kombinasyon = güçlü/büyük model + deterministik kanıt.
- **H4:** Kanıt-doğrulayıcı, injection/obfuscation kaynaklı bazı hataları
  yakalar; ama hepsini değil.

## 5. Bağımsız değişkenler (faktöriyel tasarım)
- **Obfuscation:** yok / var
- **Injection:** yok / var
- **Model:** küçük lokal (Qwen3.5-9B) / büyük lokal (varsa) / cloud
- **Kanıt:** araç çıktısı verilmiş / verilmemiş (H2 için kritik)
- **Kurban:** doğrudan LLM / REA ajanı / (ops.) Ghidra-decompile hattı

## 6. Metrikler
- **Karar doğruluğu:** ground-truth davranış bulundu mu? (yanlış negatif oranı)
- **Injection başarı oranı:** karar çevrildi mi / enjeksiyon tekrar edildi mi?
- **Obfuscation direnci:** araç çıktısındaki düşüş (H1)
- **Doğrulayıcı precision / recall:** uydurma iddiaları yakalama (H4)
- **Maliyet / süre.**

## 7. Aşamalar
1. **Faz 0 — smoke test (kill-fast):** 2×2 (obfuscation × injection), doğrudan
   LLM. Soru: *karar gerçekten değişiyor mu?* Değişmiyorsa yön değiştir.
2. **Faz 1 — Ghidra hattı:** örnekleri Ghidra ile decompile edip kurbanı
   decompile koduyla besle (gerçek RE koşulu).
3. **Faz 2 — REA kurbanı:** popüler RE ajanını kurban olarak ekle.
4. **Faz 3 — faktöriyel ölçüm + kanıt/doğrulayıcı ablasyonları.**
5. **Faz 4 — benchmark + bulgular + (ops.) savunma katmanı.**

## 8. Etik
- Tüm örnekler zararsız; gerçek zararlı, gerçek C2, gerçek kalıcılık yok.
- Saldırı yalnızca kendi test hattımıza karşı.
- Sonuçlar savunma amacıyla yayınlanır (nasıl direnilir).

## 9. Beklenen çıktı
- **Kapalı döngü** saldırı-savunma düzeneği + **benchmark**.
- Bulgular: "direnç = f(kanıt, model, obfuscation)" tablosu; negatif sonuç da
  değerlidir ("modeller şu koşullarda şaşırtıcı derecede dirençli").
