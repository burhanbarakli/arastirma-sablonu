# Araştırma şablonu

Her yeni araştırma projesi bu şablonla başlar. Amaç, tekrar eden hataları (önce yöntem, geç gelen basit rakip,
eşitsiz rakip, sonradan değişen kural, az tohum, durmayan dönüşler, yalnız benzetim, silinen sınırlılık, çok proje,
basit kuralın kazandığı koşula dönüş) yapı düzeyinde önlemek. Kurallar geneldir: belirli bir makaleye ya da koşula
bağlı değildir.

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

**Güncelleme (iki makinede de):** `git pull`, ardından `kur` betiğini yeniden çalıştır. Skill'lerde bir değişiklik yapacaksan bu
depodaki `skills/` klasöründe yap, sonra `kur` betiğini çalıştır ve commit et. Doğru kaynak bu depodur.

## Yeni proje açmak

Claude Code'da, projenin açılacağı klasörde:

```
/proje-baslat
```

ya da "yeni bir araştırma projesi başlat" demen yeterli. Yan iş (örneğin bir alan taraması) de böyle açılır.
`proje-baslat` skill'i:
1. odağı denetler: bir ana proje, bir yan iş; kayıt boşsa başka makinedeki projeleri sorar;
2. bu klasördeki dosyaları yeni projeye kopyalar (`kaynak.json` kopyalanmaz, okunur);
3. `git init` yapar ve `tools/karar_koruma.py`'ı commit kancası olarak kurar;
4. senden proje adını, temel yöntemi (ve koşmak için neye ihtiyaç duyduğunu), şüphelendiğin koşulu ve bu koşulun
   daha önce çalışılıp çalışılmadığını alır; `karar.json`'ı doldurur;
5. projeyi `~/.claude/arastirma/projeler.json` kaydına ekler ve `durum.html` panelini üretir;
6. ilk commit'ten sonra kilidin **engellediğini** sınar.

## Akış

```mermaid
flowchart TD
  B["Başlangıç: proje-baslat<br/>odak, aile sorusu, kilit testi"] --> Q{Makalen var mı?}
  Q -- evet --> R["zayif-nokta-raporu: rapor<br/>bağımsız okuyucu + denetçi"]
  Q -- hayır --> T["Alan taraması A / B"]
  T -- "A: temel makale" --> R
  T -- "B: alanı tanımak" --> K["Kör nokta adayları"]
  R --> S["Sen ilk üçten birini seçersin"]
  K --> S
  S --> K1["Kapı 1–2: kendi ölçtüğün düşüş, yeniden üretim"]
  K1 --> K3["Kapı 3: önce eşik, sonra üç sayı"]
  K3 -- "boşluk < eşik" --> F["Bulgu yaz, dönüş +1<br/>sınırda durma kuralı"]
  K3 -- "boşluk ≥ eşik" --> Y["Yöntem arama<br/>(alan taraması C burada)"]
  Y --> K45["Kapı 4–5: eşit rakip, kilitli protokol"]
  K45 --> A["Ana koşu + kör denetim"]
  A --> K67["Kapı 6–7: gerçek test, sınırlılıklar"]
```

Hangi işe hangi skill'le başlanır:

| İş | Başlangıç |
|---|---|
| Yeni çalışma, yan iş dahil | `proje-baslat` (odak ve aile kontrolü okumadan önce) |
| Elinde bir makale var | `zayif-nokta-raporu` rapor modu; tek tek dinlemek istersen "anlatımlı okuma" |
| Alanı tanımak ya da temel makale bulmak | `zayif-nokta-raporu` alan taraması, amaç B ya da A |
| "Bunu kim çözmüş?" | `arastirma-kapisi`: yalnız Kapı 3'ten sonra, yöntem arama ya da aktarım kontrolü içinden (alan taraması C). Önce istenirse DUR |
| Yöntem önerisi, yeni koşul, kural değişikliği, gönderim | `arastirma-kapisi` |

Aşamalar ve panelde görünenler:

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

1. **Projeyi kur.** Yeni klasörde Claude Code'da `/proje-baslat`. Soruları cevapla: proje adı ve amacı; temel makale,
   kodu ve koşmak için ne istediği; şüphelendiğin koşul; bu koşul daha önce çalışıldı mı. Daha önce basit bir kural
   kazandıysa "bu kez neden farklı?" sorusuna ölçülebilir bir cevap gerekir. `durum.html` paneli açılır.
2. **Makalen yoksa alanı tara.** "alan taraması: konu". Amaç A (temel makale) ya da B (alanı tanımak); yöntem adı
   geçmeyen bir arama cümlesi; sonra kartopu, eleme tablosu (kaynak uyumu sütunuyla), doğrulama, durma kuralı.
   Ayrıntı: aşağıdaki "Makale arama (alan taraması)" bölümü.
3. **Makaleyi ver.** "zayıf nokta raporu: makale.pdf". Sohbeti ve şüpheni görmeyen bir ajan okur, denetçi ajan kontrol
   eder; açık rapor gelir. Bulguları tek tek, okunacak yeriyle dinlemek istersen "anlatımlı okuma" (ya da "şurayı oku
   de"). Okuma sırasında çıkan yöntem fikirleri "Fikirler (park edildi)" altına yazılır, geliştirilmez.
4. **Gösterilen yerleri oku.** İddiaları yargılamak isteğe bağlı; getirirsen kontrol edilir, `okuma-gunlugu.md`'ye
   işlenir. Literatürden, oyuncaktan ya da ajanın çıkarımından gelen düşüş ölçülecek bir hipotezdir, bozulma değil.
5. **Zayıf noktayı sen seç.** Rapor ilk üç zayıf noktayı en ucuz deneyleriyle verir; birini sen seçersin.
   16 GB'tan fazla VRAM ya da Linux isteyenler bu sıralamada sona gider (`kaynak.json`).
6. **Kapıya sor.** "kapı" / "doğru yolda mıyım?". Kapı 1 düşüşü senin ölçmeni ister: resmî ya da yeniden üretilmiş
   kodda, stres yokken sayı makaledekiyle yan yana, koşul yöntemden önce yazılmış, düşüş tohum dağılımından büyük.
7. **Kapı 3: önce eşik, sonra üç sayı.** Taban, en güçlü basit çare (en az üç aday, yöntemi bilmeyen bir ajandan;
   en güçlüsüne yönteme verilecek ayar taraması), adil kâhin. Boşluk eşiğin altındaysa bulgu yaz; başka koşula geçmek
   dönüştür.
8. **Boşluk kalırsa yöntem ara.** "yeni yöntem bul": kâhin ne biliyor, basit çareler, boşluğun nedeni, gereken
   özellik, kim çözmüş (alan taraması C), şeytanın avukatı, adil kâhinli en küçük test.
9. **Kapıları sırayla geç.** Rakip adaleti, protokol (`karar.json > protokol`, kilitli), ana koşu, kör denetim,
   gerçeklik. Benzetimde doğrulanan sonuçtan sonraki adım gerçek test ya da "iddia benzetimle sınırlı" Sapması.
10. **Yazım.** Kapı 7: gerçek test ya da Sapma, açık KOŞULLU yok, makaledeki sınırlılıklar kayıtla satır satır aynı,
    kör denetim yapılmış (`paper-critique`, `citation-check` yardımcı).

## Kurallar kısaca

- **Pilot:** `protokol.pilot_butcesi` içinde, kodu sınamak ya da protokolü boyutlamak için yapılan koşu. Sayıları
  kapı geçirmez. 3'ten az tohumla alınan her sonuç pilottur.
- **Tohum sınırı:** Bir sınır koyarsan (örneğin 2 tohum) ona uyulur; sonuç pilot sayılır ve sınırlılık olarak yazılır.
  Hazır bir checkpoint'in değerlendirme bölümleri tohum sayılmaz.
- **Dönüş:** yeni bir koşula, soruya, göreve ya da yönteme her geçiş; sonuç olumlu olsa da sayılır. Aynı koşulda
  açılan yeni proje sayacı devralır. Sınıra gelince durma kuralı devreye girer.
- **Sapma:** sonuç görüldükten sonra bir kural değişirse `sapmalar`'a tarih, ne değişti ve gerekçeyle yazılır.
  Dürüst kayıttır, başarısızlık değil; panel onu uyarı olarak göstermez.
- **Aşılan karar:** bir kapı kararını aşarsan yardım sürer, `overrides`'a yazılır; ikincisinde danışmanla konuşman
  önerilir.
- **Kilit:** eşik ve protokol ölçümden sonra (ya da ilk ölçümle aynı commit'te) ilk kez yazılamaz; eşiğin birimi de
  kilitli; ölçüm satırları değiştirilemez; sapmalar, dönüşler ve aşılan kararlar silinemez; `karar.json` silinemez.
  Sapma yeni, tarihli ve gerçek gerekçeli olmalı; eski bir sapmanın kopyası ya da "doldurulacak" geçmez. `git revert`
  ve `rebase` commit kancasını çalıştırmaz; uzak depo varsa `pre-push` kancası gönderilen her commit'i denetler.
  Her oturum kancaların kurulu olduğuna bakar.
- **Kaynak:** `kaynak.json`'daki "ilk tercih değil" maddelerine uyan çalışmalar dışlanmaz, sıralamada sona gider;
  yine de seçilirse Sapma yazılır.

## Makale arama (alan taraması)

Claude Code'da: **"alan taraması: <konu>"** (ya da "literatür tara", "bu konuda ne var", "temel makale bul"). Bu,
`zayif-nokta-raporu`'nun alan taraması modunu çalıştırır ve aşağıdaki yolu izler.

Önce bir soruyu netleştir: **makaleyi ne için arıyorsun?** "Konuya bak, boşluk bul, yöntem öner" sırası eski
hatalarımızdan biri; arama tam bu hataya kapı açabilir. Amaca göre üç yol var:

| Amaç | Ne ararsın | Çıktı |
|---|---|---|
| **A. Zorlanacak bir temel makale bulmak** | Görevin bugünkü en iyi ya da en yaygın yöntemi | 1–2 makale, sonra `zayif-nokta-raporu` |
| **B. Bir alanı tanımak** | O görev üzerine 5–10 temel makale | Varsayım tablosu ve alanın **kör noktası** |
| **C. Bir özelliği kim çözmüş** (yalnız Kapı 3'ten sonra, yöntem aramanın 5. adımı) | Alan adı geçmeyen bir özellik cümlesi | Başka alanlardan adaylar |

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

   | Makale | Görev | Neyi değiştirmiş | Basit rakip var mı | Gerçek robot mu | Tohum | Kod | Kaynak uyumu |
   |---|---|---|---|---|---|---|---|
   | | | | | | | | |

   "Kaynak uyumu": eğitim mi gerekiyor yoksa hazır checkpoint mi yetiyor, kaç GB GPU, hangi işletim sistemi.

5. **Çekirdeği seç ve derinleş.** 5–10 makale seçilir. Varsayım tablosunun sütunları okumadan önce, genel bir
   listeden sabitlenir (yalnız şüphelendiğin koşuldan değil). PDF'lerden doldurulur. Neredeyse bütün makalelerin aynı
   işaretlediği **her** sütun bir kör nokta adayıdır; adaylar sıralanır, birini sen seçersin. Mesela "hepsi kusursuz
   algı varsayıyor".
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
(claude.ai'de, akış şemasıyla: https://claude.ai/artifact/KYYD2wqtncysDKgH51Qz8F).

| Aşama | Ana skill | Yardımcı | Dikkat |
|---|---|---|---|
| 0. Başlangıç | `proje-baslat` | | Bir ana, bir yan iş; aile sorusu; kilit engelliyor mu |
| 1. Okuma | `zayif-nokta-raporu` (bağımsız okuyucu + denetçi; "anlatımlı okuma"; makale yoksa "alan taraması" A/B) | `paper-search`, `research-litnote` | Zayıf noktayı sen seç; fikirler park edilir; kaynak uyumu |
| Kapı 1: Soru | `arastirma-kapisi` | `hypothesis-generation` (sadece ölçümden sonra) | Düşüşü sen ölç; "kimse yapmamış" = DUR |
| Kapı 2: Yeniden üretim | `arastirma-kapisi` | | Henüz yeni yöntem kodu yok; koşu `kaynak.json`'a uyuyor mu |
| Kapı 3: Üç sayı | `arastirma-kapisi` (+ yöntem arama, aktarım kontrolü, alan taraması C) | `paper-compare`, `decision-matrix` | Önce eşik; basit çare yöntemden önce, eşit ayarla |
| Kapı 4–5: Adalet, protokol | `arastirma-kapisi` | | Protokol kilitli; sonradan yazılan kural da sapma |
| Ana koşu, Kapı 6: Gerçeklik | `arastirma-kapisi` | | Tohumu değil koşulu azalt; sonra gerçek test ya da Sapma |
| Kör denetim | `zayif-nokta-raporu` (kör denetim bölümü) | | Denetçi sonucu bilmez |
| Kapı 7: Yazım | `arastirma-kapisi` | `related-work`, `paper-critique`, `citation-check` | Sınırlılıklar makalede kayıtla aynı; açık KOŞULLU yok |

Her aşamada: kapı kararından sonra `durum.html` güncellenir. İkinci görüş için `llm-council` / `claude-council`;
`claude-council` soruyu dış servislere gönderir, yayımlanmamış fikir girmez.

## Belgeler

- [`docs/NEDEN.md`](docs/NEDEN.md): her kuralın hangi hatadan ya da dersten doğduğu ve tarihli kararlar günlüğü.
- [`docs/devir-2026-11-21.md`](docs/devir-2026-11-21.md): Mac'ten Windows'a devir: yapılanlar, hatalar, eski projeleri
  eşitleme ve Windows'taki iki ajanlı inceleme görevi.
- [`docs/skill-haritasi.html`](docs/skill-haritasi.html): hangi skill ne zaman, başlangıç akışı.
- [`docs/ornekler/arama-cumlesi-gda.md`](docs/ornekler/arama-cumlesi-gda.md): GDA çalışması için arama cümlesi örneği.
- [`docs/notlar/arastirma-pusulasi.html`](docs/notlar/arastirma-pusulasi.html): **Araştırma pusulası**, hepsinin özeti: hatalarım, yol, makale okuma, kâhin, yedi kapı, arama, komutlar.
- `docs/notlar/`: araştırma notları (Boşluğu önce ölç, Problemden başla, Claude ile okumak, Dört ayın karnesi).

HTML dosyalarını tarayıcıda açmak için depoyu klonla ve dosyayı çift tıkla (GitHub HTML'yi kod olarak gösterir).

## Dosyalar

- `CLAUDE.md`: Claude'a bu yapıyı her oturumda kullanmasını söyler.
- `karar.json`: projenin durumu (tek doğru kaynak).
- `KARAR.md`: insan için okunur kayıt.
- `tools/durum.py`: `durum.html` panelini üretir (`python3 tools/durum.py`; Windows'ta `python3` çalışmıyorsa
  `python`).
- `tools/karar_koruma.py`: dondurulmuş bir kural sapma yazılmadan değişirse commit'i durdurur.
- `kaynak.json`: kaynak tercihleri (şu an 16 GB'tan fazla VRAM isteyen ve Linux isteyen çalışmalar ilk tercih değil).
  Skill'ler buradan okur; projelere kopyalanmaz. Makine değişirse yalnız bu dosyayı düzelt.

## Haftalık alışkanlık

Her hafta paneli aç ve üç soruya bak: hangi aşamadayım, açık uyarı var mı, dönüş sayacı nerede? Danışmanla
görüşmeden önce paneli paylaş.
