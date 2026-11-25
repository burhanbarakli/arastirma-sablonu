# Skill'ler ne yapar

Sistemde üç skill var. Sırayla devreye girerler: **proje-baslat**, sonra **zayif-nokta-raporu**, sonra
**arastirma-kapisi**. Üçü de aynı dosyaları okuyup yazar: `karar.json`, `KARAR.md` ve kişisel klasördeki dosyalar.

Kısa harita: [`skill-haritasi.html`](skill-haritasi.html). Her kuralın gerekçesi: [`NEDEN.md`](NEDEN.md).

## 1. proje-baslat: projeyi kurar

"Yeni proje" dediğinde ya da kapı yapısı olmayan bir klasörde çalışırken devreye girer.

- **Odak kontrolü.** Kayıttaki (`projeler.json`) aktif projelere bakar. Kural bir ana proje ve bir küçük yan iş. Bu
  sınır doluysa önce hangisinin arşive kalkacağını sorar, cevap gelmeden ilerlemez.
- **Kopyalama.** Şablondan `CLAUDE.md`, `KARAR.md`, `karar.json`, `README.md` ve `tools/` klasörünü kopyalar. Var olan
  hiçbir dosyanın üzerine yazmaz.
- **Kancalar.** `git init` yapar, `pre-commit` ve `pre-push` kancalarını kurar. Kancalar, dondurulmuş bir kural sapma
  olarak yazılmadan değişirse commit'i ya da gönderimi durdurur.
- **Açılış soruları.**
  - Proje adı ve hedefi.
  - Temel makale ve kodu.
  - Koşmak için ne gerektiği: eğitim mi yalnız checkpoint mi, GPU belleği, işletim sistemi, sürücü.
  - Bozduğunu düşündüğün koşul.
  - Bu koşula daha önce çalışıp çalışmadığın.
- **Kaynak kontrolü.** Temel makale kişisel `kaynak.json`'daki `izin_yok` listesine uyarsa "bu makinede temel yöntem
  olamaz" der ve uygun bir makale arar. `ilk_tercih_degil` listesine uyarsa bunu söyler ve sorar.
- **Aile kontrolü.** Kapalı kapılara, hafızaya ve eski projelerin dosyalarına bakar, sonucu `aile_kontrolu` alanına
  yazar.
- **Kapanış.** Paneli (`durum.html`) üretir ve ilk commit'ten sonra kilidin gerçekten engellediğini sınar.

## 2. zayif-nokta-raporu: makaleyi çoğaltmadan önce zorlar ("0. adım")

Amaç, haftalarca çoğaltma yapmadan önce yöntemin en çok nerede kırılabileceğini bulmak. Üç modu var.

- **Rapor modu** (varsayılan):
  - **Makalenin içi.** Denenmeyen koşullar, açık ve örtük varsayımlar, elle seçilmiş sabitler, tavana dayanmış
    sonuçlar, ekler.
  - **Makalenin çevresi.** OpenReview'daki hakem yorumları, GitHub issue'ları, makaleyi rakip olarak kullanıp onu yenen
    çalışmalar, benchmark'ın doygun olup olmadığı.
  - **Ucuz denemeler.** Yalnız önerir, onay gelmeden koşmaz: kâğıt kalem analizi, öğleden sonra bitecek bir oyuncak
    sürüm, resmi kodla hedefli bir koşu.
  - **Rapor dosyası.** Sonuç `zayif-nokta-<ad>.md` dosyasına yazılır. İçinde her iddia yer, alıntı ve kaynak türüyle
    verilir. Boşluk cümlesinde ölçülmemiş sayılar "?" kalır.
- **Anlatımlı okuma:** Makaleyi ajan okur, bulguları birer birer "şurayı oku" diye gösterir. Sınamaz.
- **Alan taraması:** Bir konuda temel makale ya da kör nokta arar. Arama cümlesi bir yöntem adıyla değil, görev ve
  koşulla kurulur.

Değişmeyen kurallar:

- **Bağımsız okuma.** Okumayı ayrı bir ajan yapar ve araştırmacının hipotezini görmez. Böylece sezgiyi doğrulamaya
  kaymaz.
- **Denetim.** İkinci bir ajan alıntıları ve akıl yürütmeyi denetler.
- **Uydurma kaynak yok.** Dışarıdan anılan her makalenin var olduğu doğrulanır.
- **Yöntem fikirleri park edilir.** Okurken çıkan fikirler "Fikirler (park edildi)" altına tek satırla yazılır,
  geliştirilmez.
- **Seçim araştırmacının.** Rapor en zayıf üç noktayla, her biri için en ucuz denemeyle biter; hangisine geçileceğini
  araştırmacı seçer.
- **Kaynak uyumu.** `izin_yok` listesine uyan makale haritada kalır ama aday olarak önerilmez. `ilk_tercih_degil` olan
  sona gider.

## 3. arastirma-kapisi: kapı bekçisi

Yeni yöntem, dönüş, eşik değişikliği, sınırlılığı çıkarma ya da gönderim konusu açıldığında çalışır. Her seferinde açık
bir karar verir: **DUR**, **KOŞULLU DEVAM** ya da **DEVAM**. Kapılar sırayla işler; biri geçmezse sonrakilere bakılmaz.

| Kapı | Ne sorar | Geçmezse |
|---|---|---|
| **0. Kayıt** | `karar.json`, kancalar, aktif hat sayısı ve aile kontrolü: bu koşul daha önce kapandı mı? | Aile kontrolü boşsa DUR |
| **1. Soru** | "M yöntemi, C koşulunda, Q ölçütünü A'dan B'ye düşürüyor" araştırmacının kendi koşusunda ölçüldü mü? Soru, düzeyler, eşik ve tek ölçüt ölçümden önce commit'lendi mi? | "Bu bir çözüm, henüz bir problem değil" (DUR) |
| **2. Yeniden üretim** | Makalenin sayısı tutturuldu mu? Kaynak uygun mu? Gerçek test platformu var mı? | Henüz yöntem kodu yazılmaz. `izin_yok` ise DUR |
| **3. Üç sayı** | Taban, en güçlü basit çare ve adil kâhin, ≥ 3 tohumla. Basit çare adayları yöntemi görmeyen bir ajandan gelir | Kâhinle basit çare arasındaki fark eşiğin altındaysa "burada yöntem için yer yok" (bulgu ve kapalı kapı) |
| **4. Rakip adaleti** | Rakiplere aynı bütçe, ayar ve bilgi verildi mi? | Eşitlenene kadar sonuç sayılmaz |
| **5. Protokol** | Karar kuralı, kilitli test kümesi, varsayımlar ve durma kuralı ana koşudan önce yazıldı mı? | Ana koşu için DUR |
| **6. Gerçeklik** | Benzetimin kusursuzlukları ne? Gerçek dünya testi planlandı mı? Sonuçlar tavanda mı? | "İddia benzetimle sınırlı" ya da daha zor bir koşul |
| **7. Yazım** | Sınırlılıklar makalede eksiksiz mi? Hafıza tarandı mı? Kör denetim yapıldı mı? | DUR, eksiklerin listesiyle |

Kapıların dışında çalışan parçalar:

- **Yöntem arama.** Yalnız Kapı 3 geçtikten sonra çalışır. Kâhinin neyi bildiğini adlandırır, önce basit çareleri
  ölçer. Ardından gereken özelliği alandan bağımsız bir cümleyle yazar ve literatürde kimin çözdüğünü arar. Koddan önce
  "neden basit çareyle berabere kalır?" diye üç gerekçe ister.
- **Aktarım kontrolü.** Başka bir alandan bir parça getirilmek istendiğinde çalışır. "Bu alana kimse uygulamamış"
  gerekçe sayılmaz, DUR verilir.
- **Sürekli kontroller.**
  - Her yeni koşul ya da yöntem bir dönüş sayılır. Üçüncü dönüşte durma kuralı devreye girer.
  - Sonuç görüldükten sonra bir kural değişirse sapma olarak yazılır.
  - 3'ten az tohumla alınan sonuç pilottur.
  - Bir kapı kararı aşılırsa yardım sürer, ama `overrides`'a kaydedilir.

## 4. Aktarım türü: yeni yöntemi M'nin yerine koymak

`arastirma-kapisi`'nin ikinci çalışma türü (`calisma_turu: aktarim`). Amaç alternatif yöntem: güncel ya da başka
alandan bir yöntem X, var olan güçlü yöntem M'nin yerine konur. İki sonuç baştan yazılır: **A** (X, M kadar iyi ve
tek avantaj ekseninde en güçlü basit alternatiften önde) ya da **B** (basit alternatif yetiyor: "X gerekli mi?").

| Kapı | Ne sorar | Geçmezse |
|---|---|---|
| **A1. Darboğaz ve eksen** | M güçlü ve güncel mi? Darboğazı kendi koşunda ölçüldü mü? Eksen, ölçütü, δ ≤ ½·(M − taban), ε ve iki sonuç cümlesi aday adı geçmeden commit'lendi mi? | "Bu bir yöntem, henüz bir darboğaz değil" (DUR) |
| **2. Yeniden üretim** | Boşluk türüyle aynı | |
| **A3. Kollar** | Taban, M ve en az üç basit alternatif, biri "M + ilkenin ucuz eki" | Basit alternatif zaten yetiyorsa bulgu (B) ve kapalı kapı |
| **Aday seçimi** | Alandan bağımsız özellik cümlesi, aday havuzu (alan taraması D), gerekçe ve beklenen bozulma, şeytanın avukatı, en çok iki aday, oyuncak test | Gerekçesiz aday DUR; üçüncü aday dönüş |
| **4. Rakip adaleti** | Boşluk türüyle aynı | |
| **A5. Protokol** | İki sonuçlu karar kuralı (%90 aralıklar), `tools/aralik.py` ile hesaplanan tohum | Tohum yetmiyorsa sonuç pilot |
| **6. Gerçeklik** | Avantaj ekseni zor koşulda ya da gerçek testte | |
| **A7. Yazım** | A "eşdeğer ve eksende önde" diye, B B olarak yazılır; geride kalınan yerler metinde | DUR, eksiklerle |

Panel bu türde "Üç sayı" yerine "Kollar" ve "Karşılaştırmalar" tablolarını, boşluk cümlesi yerine sonuç cümlesini
gösterir; sonucu önceden yazılmış kuralla kendisi hesaplar.

## Akış ve kayıt

**Akış:** proje-baslat, sonra zayif-nokta-raporu, sonra arastirma-kapisi'nin Kapı 1–7'si. Yöntem arama ancak Kapı
3'ten sonra açılır. Aktarım türünde: Kapı A1, 2, A3, aday seçimi, 4, A5, ana koşu, 6, A7.

**Kayıt:** Her kapı kararından sonra `karar.json` ve `KARAR.md` güncellenir, panel yenilenir. Kapanan kapılar kişisel
klasördeki `kapali_kapilar.json` dosyasına gider. Böylece bir sonraki projede aynı koşula dönülürse aile kontrolü bunu
yakalar.
