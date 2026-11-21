# Neden böyle?

Bu şablondaki her kural bir hatadan ya da bir dersten doğdu. Bu belge her kuralın nereden geldiğini ve yol boyunca
verdiğimiz kararları kayıt altına alır. Kural ağır geldiğinde önce buraya bak: kuralı esnetmek serbest, ama nedenini
bilerek ve bir Sapma yazarak.

Kaynak notlar (bu depoda, `docs/notlar/`):
- [Boşluğu önce ölç](notlar/bosluk-once-olc.html): BCSDM ve dünya modeli çalışmasından beş ders, artı yazılmayan iki ders.
- [Problemden başla](notlar/problemden-basla.html): bir makaleyi ilerletmenin sırası, kâhini kim belirler.
- [Claude ile okumak](notlar/claude-ile-okumak.html): okuma ve taramada yapay zekâyı doğru kullanmak.
- [Dört ayın karnesi](notlar/dort-ayin-karnesi.html): Temmuz–Kasım 2026 projelerinin değerlendirmesi, sekiz hata.
- [Araştırma pusulası](notlar/arastirma-pusulasi.html): hepsinin tek sayfalık özeti (20 Kasım 2026).
- [Skill haritası](skill-haritasi.html): hangi skill ne zaman, başlangıç akışı.

Notlar yazıldıkları günün fotoğrafıdır; sonradan eklenen skill modları (açık rapor, denetçi, alan taraması…) yalnız
skill haritasında ve bu belgede güncel.

## İki kök

**1. BCSDM ve dünya modeli (Kasım 2026).** "Kararlı hareket sistemine dünya modeli ekleyelim" diye başladık. Altı
deneyde her kapıyı basit kurallar kapattı:
- makalenin görevinde başarı zaten 25'te 25'ti; iyileştirilecek yer yoktu;
- gecikme deneyinde önceden yazılan kurala göre 6000 koşuda tek hata yoktu;
- süre deneyinde kural kâhinden 1,21 s gerideydi; kuralı biraz akıllandırınca fark 0,25 s'ye indi;
- algılayıcı deneyinde iyi algılayıcıda (S1) fark 1,68 s'ydi; denetçinin önerdiği sıfırlama (TARE) bunu 0,24 s'ye
  indirdi (2 tohum, bağımsız denetim yok). Kötü algılayıcılarda (S2, S3) boşluk duruyor.

Sonuç olumsuz bir bulgu olarak yayımlandı: https://burhanbarakli.github.io/before-world-models/

**2. Dört ayın karnesi.** Dokuz araştırma hattında aynı sekiz hata tekrar etti (aşağıdaki tablo). Ana teşhis: aletler
doğru, sıra yanlış. Ölçme aletleri yöntemi seçmek için değil, seçilmiş yöntemi savunmak için kullanıldı.

## Kural → neden

| Kural | Nerede | Neden (hangi hata, hangi ders) |
|---|---|---|
| Önce ölçülmüş bozulma: "M, C koşulunda Q'yu A'dan B'ye düşürüyor" | Kapı 1 | Hata 1: önce yöntem/makale, sonra ihtiyaç (V2G güvenli RL; BCSDM'de "kimse birleştirmemiş"). |
| Tez cümlesi ve "bozulma" alanı boş başlar, yalnız ölçümle dolar | `proje-baslat`, `karar.json` | Aynı hata; fikir kâğıda problemden önce yazılamasın. |
| Yeniden üretmeden yeni yöntem kodu yok | Kapı 2 | Üretemediğin şeyi ilerletemezsin; GDA'da yeniden üretim en sağlam bulguydu. |
| Üç sayı: taban, en güçlü basit çare, adil kâhin | Kapı 3 | Hata 2: basit rakip hep geç geldi ve berabere kaldı ya da kazandı (dcovf, measure-aware, SkyJEPA, V2G, BCSDM). |
| Kâhin adil olmalı: yalnız yöntemin göreceğini, gördüğü andan itibaren bilir | Kapı 3 | BCSDM'de ilk kâhin deliği dokunmadan biliyordu; 1,21 s'lik farkın yarısı erişilemezdi. |
| Rakibe eşit bütçe, eşit ayar, eşit bilgi | Kapı 4 | Hata 3: GDA'da rakip 100 epoch (özgünü 500), λ ayarsız, yönteme ayrıcalıklı bilgi. |
| Karar kuralı, eşik, tohum, durma kuralı ana koşudan önce yazılır | Kapı 5 | Hata 4: tez cümlesi, karar kuralı ve eşikler sonuçtan sonra seçildi (GDA, measure-aware). |
| Kural sessizce değişirse commit durur | `karar_koruma.py` | Aynı hata; değişiklik yasak değil, görünür olmalı ("Sapmalar" güvenilirlik belgesidir). |
| En az 3 tohum; "koşulu azalt, tohumu değil" | Kapı 5, sürekli kontrol | Hata 5: tek tohum ya da plandan az tohum (SETONET, V2G, SkyJEPA'da aynı ayarla 5/19/38 çarpışma). |
| Durma kuralı ve dönüş sayacı; üçüncü dönüşte danışman | Kapı 5, sürekli kontrol | Hata 6: GDA'da ~8, SETONET'te 6 dönüş; BCSDM'de altı kapı sonra durduk. |
| Benzetimin kusursuzlukları listelenir; tavan ve küçük gerçek test | Kapı 6 | Hata 7: hep benzetim, sonuçlar tavanda; BCSDM'de algılayıcıyı dört deney boyunca kusursuz ölçtük. |
| Sınırlılık silinmez; iddia ölçülen boşlukla aynı boyda | Kapı 7 | Hata 8: V2G conformal'da "tek saha" cümlesi çıkarıldı. |
| Kör denetim: sonucu bilmeyen ayrı ajan baştan hesaplar | Kör denetim | BCSDM'de denetimler üç kez işin seyrini değiştirdi; TARE fikrini de denetçi buldu. |
| Bir ana proje, bir küçük yan iş | `proje-baslat` odak kontrolü | Dört ayda dokuz hat; hız vardı, derinlik yoktu. |
| Aynı görev ailesine dönüş için "bu kez neden farklı?" ölçümü | Sürekli kontrol | BCSDM'ye dört kez dönüldü, dördünde basit yöntem yetti. |
| Yöntem araması yalnız Kapı 3'ten sonra; şeytanın avukatı kod yazmadan önce | Yöntem arama | Hata 1 ve 2'nin birleşimi: yöntem kurulup haftalar sonra basit kuralla berabere kalınması. |
| Başka alandan yöntem: önce bozulan parça, alandan bağımsız özellik cümlesi, o alanın basit aracı | Aktarım kontrolü | Dünya modeli (ML'den aktarım) işe yaramadı; TARE (kuvvet algılayıcı pratiğinden aktarım) yaradı. Fark: biri yöntemden, öbürü problemden başladı. |

## Okuma ve yapay zekâ kuralları

| Kural | Neden |
|---|---|
| Hafızadan değil kaynaktan; her iddiaya yer ve kısa alıntı | Yapay zekâ özetleri eksik ya da yanlış olabilir; alıntıyı açıp bakmak hataların çoğunu yakalar. |
| Kullanıcının hipotezi soru olarak verilmez ("nerede bozulur?", "X'te mi bozulur?" değil) | Hipotez verilen ajan onu doğrulamaya meyleder; bağımsız denetçinin işe yaramasının nedeni buydu. |
| Her makalenin varlığı doğrulanır, link verilir | Yapay zekâ var olmayan makale uydurabilir. |
| Makaleyi ayrı bir okuyucu ajan okur (sohbeti ve hipotezi görmeden) | Aynı neden; bağımsız göz. |
| Tek denetçi ajan: alıntı, akıl yürütme, kaçırılanlar | İkinci göz hataları azaltır; ama iki ajanın anlaşması kanıt değildir, son denetçiler kullanıcı ve deneydir. |
| "Ajanın kendi çıkarımı" etiketi | Makalede yazmayan türetmeler en riskli iddialar; elle kontrol edilmeleri gerekir. |
| Rapor açık; iddiaları yargılamak isteğe bağlı, yargılananlar okuma günlüğüne yazılır | Yapay zekâyı denetlemek de bir beceri; günlük, ajanın hangi tür iddiada yanıldığını ve kullanıcının ne kadar yakaladığını gösterir. 2026-11-21'den beri zorunlu değil (anlatımlı okuma). |
| Anlatımlı okumada da okuma bağımsız ajanın; sıralama kullanıcının şüphesine göre değil, bozma olasılığı × test ucuzluğuna göre; şüpheye karşı çıkan bulgu hep listede | Okumayı hipotezi bilen ajan yaparsa ve bulguları "sıradaki kapı" için sıralarsa, hipotez filtreye döner (hata 1). |
| Türetilmiş ya da doğrulanamamış bulgu ölçülecek bir hipotezdir, bozulma değildir | Ajanın denklemden çıkardığı bir sınır `karar.json`'a ölçülmüş bozulma gibi girerse Kapı 1 yanlış temelde geçer. |
| Alan taraması amaçla başlar, yöntem adı geçmeyen cümleyle arar, durma kuralıyla biter | Literatür taraması geçmişte "kimse yapmamış" sonucuna ve yeni yönteme kaydı. |
| Yayımlanmamış fikir dış servislere gönderilmez | Gizlilik; `claude-council` gibi araçlar soruyu dışarı yollar. |

## Kararlar günlüğü

| Tarih | Karar | Neden |
|---|---|---|
| 2026-11-18 | `zayif-nokta-raporu` skill'i ("0. adım") | Yeniden üretmeden önce makalenin nerede bozulabileceğini kaynakla görmek. |
| 2026-11-18 | `arastirma-kapisi` skill'i: yedi kapı, net DUR / KOŞULLU DEVAM / DEVAM | Kullanıcının isteği: "hayır, yanlış yoldasın; kararımız şu" diyen bir yapı. |
| 2026-11-18 | Şablon, `durum.html` paneli, commit kilidi, `proje-baslat`, özel depo | Kapıların her projede ilk günden hazır olması; kuralların sessizce değişememesi. |
| 2026-11-18 | Kapı kuralını genel `~/.claude/CLAUDE.md`'ye koymamak | Kullanıcı tercihi ("şimdilik böyle kalsın"); kapı skill tetikleyicileri ve şablonun CLAUDE.md'si üzerinden çalışıyor. |
| 2026-11-19 | İki fikir üretme skill'i ve `superpowers`, `research-superpowers` paketleri kaldırıldı | Fikirden başlamak 1 numaralı hatayı besliyor; research-superpowers teoloji/arkeoloji için yapılmış ve kapı akışıyla çakışıyor. |
| 2026-11-19 | `hypothesis-generation` tutuldu, yalnız ölçümden sonra | Rakip açıklama üretmek boşluğun nedenini anlamakta faydalı; ölçümden önce fikirden başlatır. |
| 2026-11-19 | Başka alandan aktarım kontrolü (Kapı 1–4 arası) | Problemden başlayan aktarım (TARE) işe yaradı, yöntemden başlayan (dünya modeli) yaramadı. |
| 2026-11-19 | Skill haritası (sayfa + README) | Hangi skill'in hangi aşamada kullanılacağını tek yerde görmek. |
| 2026-11-19 | Rehberli okuma modu (soru, ipucu merdiveni) | Raporu hazır almak öğretmiyor; kullanıcı zayıf nokta bulmayı öğrenmek istedi. |
| 2026-11-19 | Rapor mühürlü değil, açık; iddia blokları ve değerlendirme | Kullanıcı tercihi: raporu görmek de geliştirir; yargılama adımı öğrenmeyi sağlar. Bedeli: rapor kendi okumayı yönlendirebilir, bilerek kabul edildi. |
| 2026-11-19 | Bağımsız okuyucu ajan ve tek denetçi ajan | Hipotez taşımayan okuma; denetçi zinciri yerine son sözü kullanıcıya ve deneye bırakmak. |
| 2026-11-19 | Yöntem arama bölümü, yalnız Kapı 3'ten sonra | "Yeni yöntem, kâhinin bildiğini gözlemden tahmin etmenin yoludur"; basit çare ve şeytanın avukatı koddan önce. |
| 2026-11-20 | Alan taraması modu | Literatür aramasını amaçla, kartopuyla, doğrulamayla ve durma kuralıyla sınırlamak; yeni oturumlarda da aynı yolun izlenmesi. |
| 2026-11-20 | Notlar ve bu belge depoya kondu | Notların tek kopyası claude.ai'deydi; kaynak dosyalar geçici klasörde silinmişti. |
| 2026-11-20 | Windows düzeltmeleri: commit kilidi UTF-8 okur ve okuyamazsa durdurur; kanca `python3`'ün çalıştığını sınar; `kur.ps1` BOM'suz yazar | İlk Windows projesinde kilit hiç çalışmıyordu: Türkçe kod sayfası (cp1254) `karar.json`'ı okuyamıyor, hata yutuluyor ve her commit geçiyordu. Microsoft Store'un sahte `python3` kısayolu kancayı bozuyor, BOM'lu kayıt dosyası paneldeki Odak kartını gizliyordu. Bir koruma sessizce kapanmamalı. |
| 2026-11-21 | Rehberli okuma kaldırıldı, yerine anlatımlı okuma: ajan zayıf noktaları bulur, "şurayı oku" diye tek tek anlatır; soru ve ipucu merdiveni yok | Kullanıcı tercihi: rehberli okuma (SIMPLER) çok uzun sürdü. Bedeli: kullanıcı zayıf nokta bulmayı daha az pratik eder, ajanın çerçevesi onu daha çok yönlendirir. Bunu dengelemek için okuma yine bağımsız ajanda, sıralama hipotezden bağımsız, şüpheye karşı bulgu hep listede, kapanışta `?`'li boşluk cümlesi. İlk sürüm yalnız kurulu kopyada yapılmıştı; inceleme (bağımsız ajan dahil) bu açıkları bulunca depoya bu düzeltmelerle girdi. |

## Temel kavramlar, kısaca

- **Boşluk cümlesi:** "[Yöntem], [koşul] altında [ölçüt]'te [X] kadar düşüyor. Sorunun kaynağını bilen bir kâhin [Y]
  kazandırıyor. En iyi basit çare bunun [Z] kadarını kapatıyor. Geriye kalan [Y − Z] hedefimiz." Dolduramıyorsan
  henüz bir sorun yok, bir fikir var.
- **Adil kâhin:** yöntemin tahmin edeceği şeyi kusursuz bilen, ama yalnız yöntemin göreceği bilgiyi, gördüğü andan
  itibaren kullanan politika. Mutlak kâhin (her şeyi bilen) ayrıca ölçülebilir, karar adil kâhine göre verilir.
- **Kâhini kim belirler:** araştırmacı, sonuçlardan önce, protokolde. Gerçek değer üç yoldan gelir: benzetimde ya da
  etiketlerde zaten vardır; seçim problemiyse sonradan bakılmış en iyi seçimdir; yoksa daha iyi bir ölçümdür.
- **Basit çare:** bir mühendisin öğleden önce kuracağı çözüm (kural, ayar, klasik yöntem, yayımlanmış bir yöntem).
  Yöntemin hedefi kâhin değil, en güçlü basit çaredir.
- **Olumsuz sonuç bir bulgudur:** "burada yöntem için yer yok" kararı başarısızlık değil, erken öğrenilmiş bir sonuçtur.
