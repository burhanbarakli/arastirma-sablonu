# Araştırma şablonu

Her yeni araştırma projesi bu şablonla başlar. Amaç, tekrar eden hataları (önce yöntem, geç gelen basit rakip,
eşitsiz rakip, sonradan değişen kural, az tohum, durmayan dönüşler, yalnız benzetim, silinen sınırlılık) yapı
düzeyinde önlemek.

## Kurulum (her bilgisayarda bir kez)

```bash
git clone https://github.com/burhanbarakli/arastirma-sablonu.git ~/CALISMALAR/_arastirma-sablonu
sh ~/CALISMALAR/_arastirma-sablonu/kur.sh
```

Windows'ta (PowerShell):

```powershell
git clone https://github.com/burhanbarakli/arastirma-sablonu.git $HOME\CALISMALAR\_arastirma-sablonu
powershell -ExecutionPolicy Bypass -File $HOME\CALISMALAR\_arastirma-sablonu\kur.ps1
```

`kur` betiği üç skill'i (`zayif-nokta-raporu`, `arastirma-kapisi`, `proje-baslat`) `~/.claude/skills/` altına kurar
ve şablonun yerini `~/.claude/arastirma/sablon_yolu.txt` dosyasına yazar.

**Güncelleme:** `git pull`, ardından `kur` betiğini yeniden çalıştır. Skill'lerde bir değişiklik yapacaksan bu
depodaki `skills/` klasöründe yap, sonra `kur` betiğini çalıştır ve commit et. Doğru kaynak bu depodur.

## Yeni proje açmak

Claude Code'da, projenin açılacağı klasörde:

```
/proje-baslat
```

ya da "yeni bir araştırma projesi başlat" demen yeterli. `proje-baslat` skill'i:
1. bu klasördeki dosyaları yeni projeye kopyalar;
2. `git init` yapar ve `tools/karar_koruma.py`'ı commit kancası olarak kurar;
3. projeyi `~/.claude/arastirma/projeler.json` kaydına ekler (aktif ana proje sayısı için);
4. senden temel yöntemi ve ilk soruyu alır, `karar.json`'ı doldurur;
5. `durum.html` panelini üretir.

## Akış

| Aşama | Skill | Panelde |
|---|---|---|
| 0. Okuma | `zayif-nokta-raporu` | Raporun yolu |
| 1. Soru | `arastirma-kapisi` | Ölçülmüş bozulma, tez cümlesi |
| 2. Yeniden üretim | `arastirma-kapisi` | Makalenin sayısına karşı bizimki |
| 3. Üç sayı | `arastirma-kapisi` | Taban, basit çare, adil kâhin, boşluk |
| 4. Rakip adaleti | `arastirma-kapisi` | Bütçe, ayar, bilgi eşitliği |
| 5. Protokol | `arastirma-kapisi` | Karar kuralı, tohum, durma kuralı |
| Ana koşu | | Tohum planı / koşulan |
| 6. Gerçeklik ve tavan | `arastirma-kapisi` | Benzetim kusursuzlukları, gerçek test |
| Kör denetim | | Sonucu bilmeyen yeniden hesap |
| 7. Yazım | `arastirma-kapisi` | Sınırlılıklar |

## Nasıl başlarım, nasıl devam ederim

1. **Projeyi kur.** Yeni klasörde Claude Code'da `/proje-baslat`. Üç soruyu cevapla (proje adı ve amacı, temel makale
   ve kodu, şüphelendiğin koşul). `durum.html` paneli açılır.
2. **Makalen yoksa alanı tara.** "alan taraması: konu". Önce amaç (temel makale / alanı tanımak / kim çözmüş) ve
   yöntem adı geçmeyen bir arama cümlesi; sonra kartopu, eleme tablosu, doğrulama, durma kuralı.
   Ayrıntı: aşağıdaki "Makale arama (alan taraması)" bölümü.
3. **Makaleyi ver.** "zayıf nokta raporu: makale.pdf". Ayrı bir ajan okur, denetçi ajan kontrol eder;
   açık rapor ve "Değerlendirilecek iddialar" gelir. Bulguları tek tek, okunacak yeriyle dinlemek istersen
   "anlatımlı okuma" (ya da "şurayı oku de").
4. **Gösterilen yerleri oku.** İddiaları yargılamak isteğe bağlı: doğru / yanlış / abartılı / emin değilim diye
   işaretleyip getirirsen kontrol edilir, `okuma-gunlugu.md`'ye işlenir. "Ajanın kendi çıkarımı" etiketli bulgular
   ölçülecek hipotezdir, bozulma değil.
5. **En umut veren zayıf noktayı seç.** Okuma, boşluk cümlesi yarı dolunca biter; rapor en ucuz deneyi önerir.
6. **Kapıya sor.** "kapı" / "doğru yolda mıyım?". Kapı 1 ölçülmüş bozulma ister: oyuncak versiyon ya da resmî kodla
   hedefli koşu.
7. **Boşluk kalırsa yöntem ara.** Kapı 3 geçildiyse "yeni yöntem bul": kâhin ne biliyor, basit çareler, boşluğun
   nedeni, gereken özellik, literatür, şeytanın avukatı, en küçük test.
8. **Kapıları sırayla geç.** Yeniden üretim, üç sayı, rakip adaleti, protokol, ana koşu, gerçeklik. Her karardan sonra
   panel güncellenir.
9. **Sonuçtan sonra.** Kör denetim, sonra yazım (`paper-critique`, `citation-check`, Kapı 7).

## Makale arama (alan taraması)

Claude Code'da: **"alan taraması: <konu>"** (ya da "literatür tara", "bu konuda ne var", "temel makale bul"). Bu,
`zayif-nokta-raporu`'nun alan taraması modunu çalıştırır ve aşağıdaki yolu izler.

Önce bir soruyu netleştir: **makaleyi ne için arıyorsun?** "Konuya bak, boşluk bul, yöntem öner" sırası eski
hatalarımızdan biri; arama tam bu hataya kapı açabilir. Amaca göre üç yol var:

| Amaç | Ne ararsın | Çıktı |
|---|---|---|
| **A. Zorlanacak bir temel makale bulmak** | Görevin bugünkü en iyi ya da en yaygın yöntemi | 1–2 makale, sonra `zayif-nokta-raporu` |
| **B. Bir alanı tanımak** | O görev üzerine 5–10 temel makale | Varsayım tablosu ve alanın **kör noktası** |
| **C. Bir özelliği kim çözmüş** (yöntem aramanın 5. adımı) | Alan adı geçmeyen bir özellik cümlesi | Başka alanlardan adaylar |

### Yol (özellikle A ve B için)

1. **Arama cümlesini yaz, yöntem adını değil.**
   - Kötü: "diffusion policy makaleleri".
   - İyi: "Gürültülü kuvvet algısıyla temaslı yerleştirme görevini öğrenen politikalar."

   Cümlede görev ve koşul olmalı. Yöntem adı girerse aramanın sonuçları o yönteme kilitlenir.
2. **Tohum makaleler bul.** Bildiğin 2–3 makale ya da bir derleme (survey) yeter. Hiç yoksa Claude cümlenle arar ve
   aday sunar.
3. **Kartopu.** Tohumların **kaynakçasına** (geriye doğru) ve onlara **atıf yapanlara** (ileriye doğru) bakılır. En
   verimli yöntem budur, çünkü alanın gerçekten konuştuğu makaleleri getirir. Araçlar:
   - `citation_neighbours` (OpenAlex): bir makalenin kaynakçasını ve ona atıf yapanları getirir;
   - `paper-search`: anahtar sözcükle arar;
   - `deep-research`: geniş bir tarama gerekirse.
4. **Hızlı eleme.** Başlık ve özetten küçük bir tablo doldurulur. Bu, varsayım tablosunun hafif bir hâli:

   | Makale | Görev | Neyi değiştirmiş | Basit rakip var mı | Gerçek robot mu | Tohum | Kod |
   |---|---|---|---|---|---|---|
   | | | | | | | |

5. **Çekirdeği seç ve derinleş.** 5–10 makale seçilir. `zayif-nokta-raporu`'nun varsayım tablosu moduyla PDF'lerden
   doldurulur. Sonunda neredeyse bütün makalelerin aynı şekilde işaretlediği sütun alanın **kör noktası** olarak çıkar.
   Mesela "hepsi kusursuz algı varsayıyor".
6. **Her makale gerçek mi, kontrol et.** Yapay zekâ var olmayan makale uydurabilir. Her makale OpenAlex'te, arXiv'de
   ya da DOI'siyle doğrulanır. Hafızadan gelen hiçbir makale doğrulanmadan kullanılmaz.
7. **Durma kuralı.** Aramaya bir süre koy, mesela 1–2 gün. Yeni makaleler tabloya yeni bir sütun ya da yeni bir bulgu
   eklemiyorsa arama doymuştur, dur.

Sonuç `alan-taramasi-<konu>.md` dosyasına yazılır.

**Örnek:** GDA çalışması için kötü ve iyi arama cümleleri, amaç A/B/C ve uyarlanmış eleme tablosu:
[`docs/ornekler/arama-cumlesi-gda.md`](docs/ornekler/arama-cumlesi-gda.md).

> **Dikkat:** Aramanın sonu "**bunu kimse yapmamış**" cümlesine çıkıyorsa, kapı orada DUR der. Kör nokta bir problem
> adayıdır, henüz problem değildir. Doğru sonraki adım: kör noktanın bozduğunu düşündüğün yöntemi seçip o koşulda
> bozulmayı ölçmek (Kapı 1).

## Skill haritası

Mor sütundaki üç skill yolun kendisi; yardımcılar bir işi hızlandırır. Sayfa hâli: `docs/skill-haritasi.html`
(claude.ai'de: https://claude.ai/artifact/KYYD2wqtncysDKgH51Qz8F).

| Aşama | Ana skill | Yardımcı | Dikkat |
|---|---|---|---|
| 0. Başlangıç | `proje-baslat` | | Bir ana proje, bir küçük yan iş |
| 1. Okuma | `zayif-nokta-raporu` (ayrı ajan + denetçi, açık rapor, bulgular tek tek "şurayı oku" diye anlatılabilir: "anlatımlı okuma"; makale yoksa "alan taraması") | `paper-search`, `research-litnote` | Yöntem fikrini yaz, peşine düşme |
| Kapı 1: Soru | `arastirma-kapisi` | `hypothesis-generation` (sadece ölçümden sonra) | "Kimse yapmamış" = DUR |
| Kapı 2: Yeniden üretim | `arastirma-kapisi` | | Henüz yeni yöntem kodu yok |
| Kapı 3: Üç sayı | `arastirma-kapisi` (+ yöntem arama, aktarım kontrolü) | `paper-compare`, `decision-matrix` | Basit çare yöntemden önce |
| Kapı 4–5: Adalet, protokol | `arastirma-kapisi` | | Kural sonradan değişirse commit durur |
| Kapı 6: Ana koşu, gerçeklik | `arastirma-kapisi` | | Tohumu değil koşulu azalt |
| Kör denetim | `zayif-nokta-raporu` (kör denetim bölümü) | | Denetçi sonucu bilmez |
| Kapı 7: Yazım | `arastirma-kapisi` | `related-work`, `paper-critique`, `citation-check` | Sınırlılık silinmez |

Her aşamada: kapı kararından sonra `durum.html` güncellenir. İkinci görüş için `llm-council` / `claude-council`;
`claude-council` soruyu dış servislere gönderir, yayımlanmamış fikir girmez.

## Belgeler

- [`docs/NEDEN.md`](docs/NEDEN.md): her kuralın hangi hatadan ya da dersten doğduğu ve tarihli kararlar günlüğü.
- [`docs/skill-haritasi.html`](docs/skill-haritasi.html): hangi skill ne zaman, başlangıç akışı.
- [`docs/ornekler/arama-cumlesi-gda.md`](docs/ornekler/arama-cumlesi-gda.md): GDA çalışması için arama cümlesi örneği.
- [`docs/notlar/arastirma-pusulasi.html`](docs/notlar/arastirma-pusulasi.html): **Araştırma pusulası**, hepsinin özeti: hatalarım, yol, makale okuma, kâhin, yedi kapı, arama, komutlar.
- `docs/notlar/`: araştırma notları (Boşluğu önce ölç, Problemden başla, Claude ile okumak, Dört ayın karnesi).

HTML dosyalarını tarayıcıda açmak için depoyu klonla ve dosyayı çift tıkla (GitHub HTML'yi kod olarak gösterir).

## Dosyalar

- `CLAUDE.md`: Claude'a bu yapıyı her oturumda kullanmasını söyler.
- `karar.json`: projenin durumu (tek doğru kaynak).
- `KARAR.md`: insan için okunur kayıt.
- `tools/durum.py`: `durum.html` panelini üretir (`python3 tools/durum.py`).
- `tools/karar_koruma.py`: dondurulmuş bir kural sapma yazılmadan değişirse commit'i durdurur.

## Haftalık alışkanlık

Her hafta paneli aç ve üç soruya bak: hangi aşamadayım, açık uyarı var mı, dönüş sayacı nerede? Danışmanla
görüşmeden önce paneli paylaş.
