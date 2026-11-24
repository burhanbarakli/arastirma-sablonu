# Kişisel klasör

Bu klasör şablonun değil, senindir. İçindekiler:

- `kaynak.json`: kaynak sınırların (makinen, GPU belleği; "izin yok", "ilk tercih değil" ve "izin verilen" listeleri).
- `kapali_kapilar.json`: kapalı kapıların; aile kontrolü buradan okur.
- `gecmis.md`: amacın, kendi hataların ve örnekleri; kapı kararlarında örnek buradan gelir, DUR'dan sonra amacın hatırlatılır.

`kur.sh` / `kur.ps1` bu klasörün yolunu `~/.claude/arastirma/kisisel_yolu.txt`'ye yazar ve eksik dosyaları
şablondaki `kisisel-ornek/`'ten oluşturur; var olan dosyaya dokunmaz.

Birden çok bilgisayarda çalışıyorsan bu klasörü özel bir git deposu yap (örneğin GitHub'da `arastirma-kisisel`).
Öbür bilgisayarda önce depoyu klonla, sonra kur betiğini klasörün yoluyla çalıştır:

    ./kur.sh ~/CALISMALAR/_arastirma-kisisel
    powershell -ExecutionPolicy Bypass -File kur.ps1 -Kisisel $HOME\CALISMALAR\_arastirma-kisisel
