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
3. **Makaleyi ver.** "zayıf nokta raporu: makale.pdf". Ayrı bir ajan okur, denetçi ajan kontrol eder;
   açık rapor ve "Değerlendirilecek iddialar" gelir. Yeni alandaysan ya da takılıyorsan "rehberli oku".
4. **Kendin oku, iddiaları yargıla.** Kendi tablonu tut (Ne / Yeri / Şüphem). Her iddiayı doğru / yanlış / abartılı /
   emin değilim diye işaretle, makalede kontrol ettiğin yeri yaz. Getir; kontrol edilir, `okuma-gunlugu.md`'ye işlenir.
   "Ajanın kendi çıkarımı" etiketli iddiaları elle kontrol et.
5. **En umut veren zayıf noktayı seç.** Okuma, boşluk cümlesi yarı dolunca biter; rapor en ucuz deneyi önerir.
6. **Kapıya sor.** "kapı" / "doğru yolda mıyım?". Kapı 1 ölçülmüş bozulma ister: oyuncak versiyon ya da resmî kodla
   hedefli koşu.
7. **Boşluk kalırsa yöntem ara.** Kapı 3 geçildiyse "yeni yöntem bul": kâhin ne biliyor, basit çareler, boşluğun
   nedeni, gereken özellik, literatür, şeytanın avukatı, en küçük test.
8. **Kapıları sırayla geç.** Yeniden üretim, üç sayı, rakip adaleti, protokol, ana koşu, gerçeklik. Her karardan sonra
   panel güncellenir.
9. **Sonuçtan sonra.** Kör denetim, sonra yazım (`paper-critique`, `citation-check`, Kapı 7).

## Skill haritası

Mor sütundaki üç skill yolun kendisi; yardımcılar bir işi hızlandırır. Sayfa hâli: `docs/skill-haritasi.html`
(claude.ai'de: https://claude.ai/artifact/KYYD2wqtncysDKgH51Qz8F).

| Aşama | Ana skill | Yardımcı | Dikkat |
|---|---|---|---|
| 0. Başlangıç | `proje-baslat` | | Bir ana proje, bir küçük yan iş |
| 1. Okuma | `zayif-nokta-raporu` (ayrı ajan + denetçi, açık rapor, iddiaları sen yargılarsın; makale yoksa "alan taraması", takılırsan "rehberli oku") | `paper-search`, `research-litnote` | Yöntem fikrini yaz, peşine düşme |
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
