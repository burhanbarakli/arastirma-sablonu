# Bu proje araştırma kapısı yapısını kullanır

Bu klasördeki her araştırma işinde aşağıdaki yapı geçerlidir. Kullanıcıyla Türkçe konuş.

## Dosyalar

- `karar.json`: projenin makinece okunan durumu (aşamalar, üç sayı, protokol, tohum, dönüşler, sapmalar). Tek doğru
  kaynak budur.
- `KARAR.md`: aynı kararların insan için okunur kaydı ve tarihli kapı notları.
- `durum.html`: `python3 tools/durum.py` ile `karar.json`'dan üretilen durum paneli. Elle düzenlenmez. Windows'ta
  `python3 -c ""` çalışmıyorsa (Microsoft Store kısayolu) bu dosyadaki `python3` yerine `python` kullan.
- `tools/karar_koruma.py`: git kancası (`pre-commit`, uzak depo varsa `pre-push`); dondurulmuş bir kural
  "sapmalar"a yazılmadan değişirse commit'i ya da gönderimi durdurur.

## Her oturumda

1. Önce `karar.json`'ı (tek doğru kaynak), sonra `KARAR.md`'yi oku. Projenin hangi aşamada olduğunu ve son kararı bil.
   `.git/hooks/pre-commit` dosyasının var olduğunu ve `tools/karar_koruma.py`'yi çağırdığını kontrol et; uzak depo
   varsa `.git/hooks/pre-push`'a da bak. Yoksa (örneğin depo yeni klonlandıysa) kullanıcıya söyle ve kurmayı öner.
2. Kullanıcı yeni bir yöntem, model, modül ya da yön önerirse ("hızlı bir deneme", "makaleye küçük bir ek", "hakem
   istedi" de buna girer); yeni bir koşul eklemek isterse; eşik, karar kuralı, tohum ya da rakip ayarını değiştirmek
   isterse; bir sınırlılığı çıkarmak isterse; ya da yazıma ve gönderime geçerse, **`arastirma-kapisi` skill'ini
   çalıştır** ve kararını (DUR / KOŞULLU DEVAM / DEVAM) açıkça ver.
3. Yeni bir makale okunacaksa önce **`zayif-nokta-raporu`** skill'ini kullan; raporun yolunu
   `karar.json > asamalar.okuma.dosya`'ya yaz.
4. Her kapı kararından sonra `karar.json`'ı güncelle (aşama durumu, tarih, not, `son_karar`, gerekiyorsa dönüş,
   sapma ve `overrides` kaydı), `KARAR.md`'ye bir satır ekle ve `python3 tools/durum.py` çalıştırıp paneli yenile.

## Değişmez kurallar

- Yöntem kodu, üç sayı (taban, en güçlü basit çare, adil kâhin) ölçülmeden yazılmaz.
- Basit çare yöntemden önce kurulur ve rakiplere aynı bütçe, ayar ve bilgi verilir.
- Eşik ölçümden önce; karar kuralı, ölçüt, kilitli test kümesi ve durma kuralı ana koşudan önce `karar.json >
  protokol`'e yazılır.
- Tohum ≥ 3. Daha az tohumla (kullanıcı sınır koyduysa da) alınan sonuç pilottur: kapı geçirmez, üç sayı tablosuna ve
  tez cümlesine girmez, sınırlılık olarak yazılır.
- Her yeni koşul, soru ya da yöntem bir dönüştür; sonuç olumlu da olsa sayılır.
- Benzetimde doğrulanmış bir sonuçtan sonraki adım gerçek dünya testidir; yapılmayacaksa iddianın benzetimle sınırlı
  olduğu Sapma olarak yazılır.
- Sonuç görüldükten sonra bir kural değişirse, bu bir sapmadır: tarih, ne değişti ve gerekçeyle `sapmalar`'a yazılır.
  Gerekçe yer tutucu olamaz ("doldurulacak"); eksik kalmış eski bir kayıt düzenlenmez, `"duzeltir": "<eski tarih>"`
  alanlı yeni bir kayıtla tamamlanır.
- Üçüncü dönüşte durma kuralı devreye girer.
- Gerçek bir sınırlılık metinden çıkarılmaz; ortaya çıktığı anda `sinirliliklar`'a yazılır.
- Kullanıcı bir kapı kararını aşarsa yardım sürer, ama `overrides`'a tarih, kapı, karar ve gerekçeyle yazılır.
