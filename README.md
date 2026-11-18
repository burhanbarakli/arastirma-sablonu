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

## Dosyalar

- `CLAUDE.md`: Claude'a bu yapıyı her oturumda kullanmasını söyler.
- `karar.json`: projenin durumu (tek doğru kaynak).
- `KARAR.md`: insan için okunur kayıt.
- `tools/durum.py`: `durum.html` panelini üretir (`python3 tools/durum.py`).
- `tools/karar_koruma.py`: dondurulmuş bir kural sapma yazılmadan değişirse commit'i durdurur.

## Haftalık alışkanlık

Her hafta paneli aç ve üç soruya bak: hangi aşamadayım, açık uyarı var mı, dönüş sayacı nerede? Danışmanla
görüşmeden önce paneli paylaş.
