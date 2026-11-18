# Bu proje araştırma kapısı yapısını kullanır

Bu klasördeki her araştırma işinde aşağıdaki yapı geçerlidir. Kullanıcıyla Türkçe konuş.

## Dosyalar

- `karar.json`: projenin makinece okunan durumu (aşamalar, üç sayı, protokol, tohum, dönüşler, sapmalar). Tek doğru
  kaynak budur.
- `KARAR.md`: aynı kararların insan için okunur kaydı ve tarihli kapı notları.
- `durum.html`: `python3 tools/durum.py` ile `karar.json`'dan üretilen durum paneli. Elle düzenlenmez.
- `tools/karar_koruma.py`: git kancası; dondurulmuş bir kural "sapmalar"a yazılmadan değişirse commit'i durdurur.

## Her oturumda

1. Önce `karar.json` ve `KARAR.md`'yi oku. Projenin hangi aşamada olduğunu ve son kararı bil.
2. Kullanıcı yeni bir yöntem, model, modül ya da yön önerirse; olumsuz sonuçtan sonra yeni bir koşul eklemek
   isterse; eşik, karar kuralı, tohum ya da rakip ayarını değiştirmek isterse; ya da yazıma ve gönderime geçerse,
   **`arastirma-kapisi` skill'ini çalıştır** ve kararını (DUR / KOŞULLU DEVAM / DEVAM) açıkça ver.
3. Yeni bir makale okunacaksa önce **`zayif-nokta-raporu`** skill'ini kullan; raporun yolunu
   `karar.json > asamalar.okuma.dosya`'ya yaz.
4. Her kapı kararından sonra `karar.json`'ı güncelle (aşama durumu, tarih, not, `son_karar`, gerekiyorsa dönüş ve
   sapma kaydı), `KARAR.md`'ye bir satır ekle ve `python3 tools/durum.py` çalıştırıp paneli yenile.

## Değişmez kurallar

- Yöntem kodu, üç sayı (taban, en güçlü basit çare, adil kâhin) ölçülmeden yazılmaz.
- Basit çare yöntemden önce kurulur ve rakiplere aynı bütçe, ayar ve bilgi verilir.
- Karar kuralı, eşik, tohum (≥ 3), kilitli test kümesi ve durma kuralı ana koşudan önce yazılır.
- Sonuç görüldükten sonra bir kural değişirse, bu bir sapmadır: tarih, ne değişti ve gerekçeyle `sapmalar`'a yazılır.
- Üçüncü dönüşte durma kuralı devreye girer.
- Gerçek bir sınırlılık metinden çıkarılmaz.
