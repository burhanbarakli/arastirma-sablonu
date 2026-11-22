# Neden böyle?

Bu şablondaki her kural bir hatadan ya da bir dersten doğdu. Bu belge her kuralın nereden geldiğini ve yol boyunca
verdiğimiz kararları kayıt altına alır. Kural ağır geldiğinde önce buraya bak: kuralı esnetmek serbest, ama nedenini
bilerek ve bir Sapma yazarak.

**Örnek vakalar hakkında:** bu belgedeki proje adları (BCSDM, GDA, dcovf, SETONET, V2G…) şablonu yazan araştırmacının
2026 projeleridir. Kuralların nereden çıktığını gösterirler; şablonu kullanan başka birinin geçmişi değildir. Skill'ler
bunları yalnız "örnek vaka" diye anar. Her kullanıcının kendi geçmişi kişisel klasöründeki `gecmis.md`'dedir.

Kaynak notlar:
- [Boşluğu önce ölç](vakalar/bosluk-once-olc.html) (vaka): BCSDM ve dünya modeli çalışmasından beş ders, artı yazılmayan iki ders.
- [Problemden başla](notlar/problemden-basla.html) (rehber): bir makaleyi ilerletmenin sırası, kâhini kim belirler.
- [Claude ile okumak](notlar/claude-ile-okumak.html) (rehber): okuma ve taramada yapay zekâyı doğru kullanmak.
- [Dört ayın karnesi](vakalar/dort-ayin-karnesi.html) (vaka): Temmuz–Kasım 2026 projelerinin değerlendirmesi, sekiz hata.
- [Araştırma pusulası](vakalar/arastirma-pusulasi.html) (vaka): hepsinin tek sayfalık özeti (20 Kasım 2026).
- [Skill haritası](skill-haritasi.html): hangi skill ne zaman, başlangıç akışı.

Notlar yazıldıkları günün fotoğrafıdır; sonradan eklenen skill modları (açık rapor, denetçi, alan taraması…) yalnız
skill haritasında ve bu belgede güncel.

## İki kök (örnek vakalar)

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
| Eşik ölçümden önce; yoksa Kapı 3 DUR, panel boşluğu yorumlamaz; ölçümden sonra ilk kez yazılan kural da sapma ister | Kapı 3, `karar_koruma.py`, `durum.py` | Hata 4'ün en kolay yolu boş bırakılan eşiği sonradan doldurmaktı; eski kilit yalnız dolu alanı koruyordu. |
| Karar kuralı, ölçüt, kilitli test ve durma kuralı `karar.json > protokol`'de ve kilitli | Kapı 5, `karar_koruma.py` | Bu kuralların JSON'da alanı yoktu; değişmeleri görünmüyordu (GDA'daki kural değişiklikleri gibi). |
| Sapmalar, dönüş kaydı ve aşılan kararlar yalnız büyür; sapmada tarih, ne ve gerekçe zorunlu; `karar.json` silinemez; alt klasör de denetlenir | `karar_koruma.py` | Kırmızı takım: kuralı sapmayla değiştirip sapmayı sonra silmek, boş sapma eklemek ya da dönüş kaydını silmek eski kilitten geçiyordu. |
| Kilit, Türkçe harfli yoldaki `karar.json`'ı da görür; eşik ilk ölçümle aynı commit'te de yazılamaz; eşiğin birimi kilitli; sapma yeni, tarihli ve gerçek gerekçeli olmalı (kopya, boş kayıt, "doldurulacak" geçmez; eksik kayıt `duzeltir` alanlı yeni kayıtla tamamlanır); yinelenen anahtar reddedilir | `karar_koruma.py`, `arastirma-kapisi`, şablon `CLAUDE.md` | Windows kırmızı takımı (2026-11-22): `çalışma/karar.json` hiç denetlenmiyordu; eski bir sapmanın kopyası ya da başa eklenen `{}` her değişikliği aklıyordu; "doldurulacak" gerekçe geçiyor ama sonra düzeltilemiyordu. Hepsi geçici depoda yeniden üretildi. |
| Uzak depo varsa `pre-push` kancası gönderilen her commit'i ve uzak ucu yeni uçla karşılaştırır | `karar_koruma.py --push`, `proje-baslat` | `git revert` ve `rebase` commit kancasını çalıştırmaz; ölçüm satırı, sapma ve dönüş kaydı revert ile sessizce siliniyordu. Uzak deposu olmayan projede bu açık kalır; README'de yazılı. |
| Kancalar BOM'suz ve LF yazılır; alt klasördeki projede betik yolu depo köküne göre verilir; `python3` çalışmıyorsa `python` (kancada, skill'lerde ve şablon belgelerinde) | `proje-baslat`, `arastirma-kapisi`, şablon `CLAUDE.md` | BOM'lu kancayı Git hiç çalıştırmıyor, alt klasörde betik bulunamıyor; ikisi de her commit'i durdurup `--no-verify`'a itiyor. Skill'deki `python3 tools/durum.py` PowerShell'de rc 9009 veriyordu. |
| Kurulum testi kilidin **engellediğini** sınar; her oturum kancanın kurulu olduğuna bakar | `proje-baslat`, şablon `CLAUDE.md` | Yalnız "geçen commit"i sınamak, her şeyi geçiren bir kilidi de geçirir (Windows'taki hata buydu). Klonlanan depoda kanca yoktur. |
| Benzetimde doğrulanan sonuçtan sonra gerçek test ya da "iddia benzetimle sınırlı" Sapması; Kapı 7 bunlar olmadan DUR | Kapı 6, Kapı 7 | Hata 7: gerçek test planlanıp hiç yapılmadı (GDA Dobot); "planlandı" kapıdan geçmeye yetiyordu. |
| Aile kontrolü yapıya göre: bu koşulda daha önce basit bir kural kazandıysa "bu kez neden farklı?" ölçülebilir cevap ister, kazanan kuralın karşılığı ilk ölçüme girer, dönüş sayacı taşınır | Adım 0, `proje-baslat` | Hata 10 yalnız proje adına bakılarak yakalanıyordu; yeni proje açmak aynı koşula dönüşü ve dönüş sayacını gizliyordu. |
| Her yeni koşul dönüştür, sonuç olumlu olsa da | Tanımlar, sürekli kontrol | Hata 6: "başka koşula geç" sayacı artırmıyordu; olumlu sonuçtan sonraki geçişler hiç sayılmıyordu. |
| 3'ten az tohum pilottur: kapı geçirmez, sınırlılık olarak yazılır; kullanıcının tohum sınırına uyulur | Tanımlar, şablon `CLAUDE.md` | Kullanıcının 2 tohum sınırı ile "≥ 3" çatışıyordu; ya sessiz uyum ya her koşuda override çıkıyordu. 2 tohumlu bir sonuç yayımlanmış bir "ders" olmuştu. |
| Kapı 1'deki düşüş kullanıcının kendi koşusundan, resmî ya da yeniden üretilmiş kodda, koşul yöntemden önce yazılmış ve tohum dağılımından büyük; literatürden ya da oyuncaktan gelen düşüş hipotezdir | Kapı 1 | Kırmızı takım: başkasının düşüşü, yöntemi bozmak için kurulmuş oyuncak ya da yöntemi beğendikten sonra seçilen koşul Kapı 1'den geçiyordu. |
| Basit çare adayları yöntemi bilmeyen bir ajandan; en az üçü ölçülür; en güçlüsüne yönteme verilecek ayar taraması verilir | Kapı 3 | Hata 2 ve 3: zayıf rakip (BCSDM'de MOMENT) ve gözden kaçan çare (TARE'yi ancak denetçi buldu). |
| Aşılan kapı kararları `overrides`'a yazılır; ikincisinde danışman | Overrides | `son_karar` her kararda üzerine yazıldığından aşılan bir DUR kayıttan kayboluyordu. |
| Okumada zayıf noktayı kullanıcı seçer (ilk üç), oyuncak kâhin adil, varsayım tablosu sütunları okumadan önce, yöntem fikirleri park edilir | `zayif-nokta-raporu` | Ajanın tek "en umut verici" seçimi ve kullanıcının şüphesiyle tohumlanmış sütunlar problemi ajana seçtiriyordu; adil olmayan kâhin boşluğu şişiriyordu. |
| Kaynak uyumu: `kaynak.json`'daki "ilk tercih değil" maddelerine uyan çalışma dışlanmaz, temel makale ve deney sıralamasında sona gider; yine de seçilirse Sapma | `zayif-nokta-raporu`, Kapı 2, `proje-baslat` | Kullanıcının makinesi 16 GB VRAM; 16 GB'tan fazlasını ya da Linux'u isteyen çalışma haftalarca kurulumda takılır, araştırma sorusuna hiç gelinmez. Değerler ayrı dosyada, skill'ler genel kalsın diye. |
| Sapma bilgi olarak gösterilir, uyarı değil; kâhin tanımlanamazsa gerekçeyle KOŞULLU DEVAM | `durum.py`, Kapı 3 | Aşırı engelleme de başarısızlıktır: dürüst kaydı cezalandıran ya da hiç geçilemeyen kural atlanmayı öğretir. |
| Aynı görev ailesine dönüş için "bu kez neden farklı?" ölçümü | Sürekli kontrol | BCSDM'ye dört kez dönüldü, dördünde basit yöntem yetti. |
| Yöntem araması yalnız Kapı 3'ten sonra; şeytanın avukatı kod yazmadan önce | Yöntem arama | Hata 1 ve 2'nin birleşimi: yöntem kurulup haftalar sonra basit kuralla berabere kalınması. |
| Başka alandan yöntem: önce bozulan parça, alandan bağımsız özellik cümlesi, o alanın basit aracı | Aktarım kontrolü | Dünya modeli (ML'den aktarım) işe yaramadı; TARE (kuvvet algılayıcı pratiğinden aktarım) yaradı. Fark: biri yöntemden, öbürü problemden başladı. |
| Aile kontrolü her soruda yapılır: eşleşme yoksa "yok" ve taranan kaynaklar; eşik altı kalan koşul da kapalı kapıdır; koşul fiziksel büyüklükle eşlenir; eşleşmede "bu kez neden farklı" sayılı bir öngörüdür | Adım 0.4, `kapali_kapilar.json`, `proje-baslat` | Hata 10: kontrol yalnız "basit kural kazandı mı?" diye soruyordu; bir koşulun eşiğin altında kalması kontrolü "temiz" geçiriyordu. Boş alan "bakılmadı" ile "baktım, yok"u ayırmıyordu. Kayıt makineye özel olduğu için kapalı kapılar şablon deposunda tutulur. Anahtar kelime eşlemesi gürültülü: aynı kelime iki projede başka anlama gelebiliyor. |
| Kapı 1'in sorusu, koşul düzeyleri, eşiği ve tek ölçütü bozulmadan önce commit'lenir; kilit ilk bozulmayı bunlarsız durdurur; bulut koşusu karar.json commit'ini çıktısına yazar | Kapı 1, `karar_koruma.py` | Hata 4: "başarı ya da sıralama" gibi iki ölçütlü soru sonuca göre ölçüt seçtiriyordu; kilit "ölçüm var"ı yalnız üç sayı satırlarından anlıyordu, Kapı 1 eşiği ölçümden sonra sessizce yazılabiliyordu. `bozulma` genel ölçüm sayımına yine katılmadı (Kapı 3 eşiği sapma istemesin); yalnız Kapı 1 alanlarına bağlandı. |
| Ölçümü olan eski projeye boş alan eklemek engellenmez | `karar_koruma.py` | Şema eşitlemesi kural yazmak değildir; aksi hâlde her yeni alan eski projelerde sapma isterdi. |
| Eğitim yoksa tohum = değerlendirme tohumu (başlangıç kümesi), eşli test şart; önce iki tohumun gerçekten farklı sonuç verdiği sınanır; tek eğitim koşusu sınırlılık | Tanımlar, `tohum.tanim`, şablon `CLAUDE.md` | Kaynak kuralı yalnız hazır checkpoint'e izin verirken "≥ 3 tohum" eğitim tohumu sayıyordu: hiçbir sonuç kapı geçemezdi. Belirlenimci bir politikada tohum yayılımı sıfır çıkar ve "dağılımdan büyük" anlamsızlaşır. |
| Gerçek test platformu Kapı 2'de sorulur (platform, erişim, eşleşme); yoksa sonuçtan önce sınırlılık olarak yazılır, Sapma değil | Kapı 2, 6, 7 | Hata 7: platform ancak Kapı 6'da, ana koşudan sonra soruluyordu. Sonuç görülmeden yazılan bir sınır plandır; ona Sapma demek orantılılık kuralıyla çelişiyordu. "Eşleşme" tanımlı, çünkü benzetimdeki kol ile eldeki kol farklı olabilir. |
| Kapı 7 bu projenin hafıza klasörlerini ve karar notlarını da tarar; bulunanlar "kontrol et" listesine girer | Kapı 7 | Hata 8: bazı sınırlılıklar ve rakip ayarı farkları yalnız hafızada duruyordu. Başka projelerin hafızası okunmaz (gürültü ve bilgi sızıntısı); eski not doğrudan DUR'a çevrilmez. |
| Kararlarını kendi düzeninde tutan projede kökte KARAR.md açılmaz; dönüşler o kayıttan tanıma göre listelenir, kullanıcı bir kez onaylar; panel karar.json yokken çökmez | Adım 0.1, `proje-baslat`, `durum.py` | Kayıtlı bir proje kendi `karar/` klasörünü kullanıyordu: skill ikinci bir kayıt açıp dönüş sayısını 0 görüyordu, panel çöküyordu. Dönüşleri ajan tek başına sayarsa ya her kartı sayar ya hiçbirini; liste kullanıcıya gösterilir. |
| Odak klasör değil hat sayar (`hatlar`); son 14 günün commit'leri oturumda bir kez bilgi olarak gösterilir, hat sayısını kullanıcı söyler; kayıt okunamazsa panel uyarır | Adım 0.3, `durum.py` | Hata 9: tek klasörde iki hat (makale bitişi ve yeni tez) tek proje sayılıyordu; bozuk kayıtta panel sessiz kalıyordu. Commit başlıklarından hat çıkarmak tahmine dayalı olduğu için karar kullanıcıda. |
| Durma kuralını doldurmuş yan iş yeni soru açarsa dönüştür, türü yeniden sorulur; panel tamamlanmamış sapmayı uyarı olarak gösterir; dondurulmuş bir alanın sonuçtan önce değişmesi de kısa bir "planlama" sapması ister | Sürekli kontrol, `durum.py`, `karar_koruma.py` | Bir tarama yan işi, kendi durma kuralı dolduktan sonra aynı kayıt altında Kapı 1 çalışmasına dönmüştü; dönüş sayılmamıştı. "doldurulacak" gerekçeli eski sapma panelde yalnız sayı olarak görünüyordu. Kilit git dışında neyin görüldüğünü bilemez. |

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

## Skill'deki örnekler

`arastirma-kapisi` kurallarını genel yazar; proje adları skill'de geçmez. Bir kapı kararında "senin şu projendeki
gibi" demek gerektiğinde ajan örneği kullanıcının kişisel klasöründen alır (`gecmis.md`, `kapali_kapilar.json`).
Şablonu yazanın kendi örnekleri 2026-11-22'de buradan onun kişisel klasörüne taşındı; vakalar `docs/vakalar/`'da.

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
| 2026-11-21 | Rehberli okuma kaldırıldı, yerine anlatımlı okuma: ajan zayıf noktaları bulur, "şurayı oku" diye tek tek anlatır; soru ve ipucu merdiveni yok | Kullanıcı tercihi: rehberli okuma çok uzun sürdü. Bedeli: kullanıcı zayıf nokta bulmayı daha az pratik eder, ajanın çerçevesi onu daha çok yönlendirir. Bunu dengelemek için okuma yine bağımsız ajanda, sıralama hipotezden bağımsız, şüpheye karşı bulgu hep listede, kapanışta `?`'li boşluk cümlesi. İlk sürüm yalnız kurulu kopyada yapılmıştı; inceleme (bağımsız ajan dahil) bu açıkları bulunca depoya bu düzeltmelerle girdi. |
| 2026-11-21 | İki ajanlı inceleme (geçmiş hatalar ve kırmızı takım) sonrası düzeltmeler: kilit, panel, `karar.json` (`protokol`, `aile_kontrolu`, `overrides`), üç skill ve şablon `CLAUDE.md` | İki bağımsız ajan 15 açık buldu, hepsi dosyada doğrulandı; ayrıntı "Kural → neden" tablosundaki yeni satırlarda. Kurallar genel tutuldu: belirli bir makalenin ya da koşulun adı geçmez. Bedeli: daha çok DUR; bunu sapmanın bilgi sayılması ve tanımlanamayan kâhin istisnası dengeler. |
| 2026-11-21 | Kaynak tercihi: 16 GB'tan fazla VRAM isteyen ve Linux isteyen çalışmalar ilk tercih değil (`kaynak.json`) | Kullanıcının isteği. Önceki "16 GB kuralı" yalnız robot kol taramasındaydı; artık bütün okuma ve seçimlerde geçerli. Dışlama değil, sıralama: alanın haritası eksik kalmasın. |
| 2026-11-22 | Windows'ta iki ajanlı inceleme sonrası kilit ve Windows düzeltmeleri (10 bulgu): Türkçe harfli yol, sapma kopyası ve boş kayıt, eşik ile ilk ölçüm aynı commit'te, `birim`, yer tutucu gerekçe, yinelenen anahtar, Git Bash'te bozuk mesaj, `pre-push` kancası, BOM'suz/LF kanca ve alt klasör yolu, `python3` yedeği | Devir belgesinin 5. bölümü. Bulgular ana oturumda geçici depolarda yeniden üretildi; yeni kilit 17 senaryonun 17'sinde beklenen sonucu verdi. Kullanıcı önce yalnız kilit ve Windows bulgularını seçti; skill içeriğine dokunan bulgular (aile kontrolü, kayıtsız proje, Kapı 1 alanları, odak, tohum tanımı, Kapı 6–7) ayrıca konuşulacak. "Ölçüm var" sayımına `bozulma` katılmadı: Kapı 1 düşüşü ölçer, eşik Kapı 3'te yazılır; katılsaydı her projede Kapı 3 sapma isterdi. |
| 2026-11-22 | Skill içeriği düzeltmeleri (bulgu 11–17 ve üç ek açık): aile kontrolü ve `kapali_kapilar.json`, kendi karar düzeni olan proje, Kapı 1 alanları ve kilidi, odak hatları, değerlendirme tohumu, Kapı 2'de platform, Kapı 7 hafıza taraması, yan işten dönüş, eksik sapma uyarısı, boş alan eşitlemesi | Öneriler iki bağımsız ajana (etkililik; maliyet ve yan etki) okutuldu, kanıtları dosyada doğrulandı; kullanıcı hepsini önerilen sırayla seçti. Ajanların ayrıştığı yerde: boş aile kontrolü yalnız soru açılırken DUR (eski projelerde bir kez uyarı); dönüşler tanıma göre listelenip kullanıcıya onaylatılır; odakta hat sayısını kullanıcı söyler; platform Kapı 2'de sorulur. `kapali_kapilar.json` doğrulanmış dört kayıtla başlatıldı (NEDEN.md'deki BCSDM sonuçları ve bir başka projenin eşik altı sonucu). 17 eski ve 29 yeni senaryonun hepsi beklenen sonucu verdi. |
| 2026-11-22 | Eski projelerin adları `arastirma-kapisi`'den çıkarıldı, bu belgenin "Skill'deki örnekler" bölümüne taşındı; skill geçmiş örneği buradan ve `kapali_kapilar.json`'dan alır | Kullanıcının isteği: skill genel kalsın, kurallar eski çalışmalara atıf yapmasın. "Kullanıcının kendi örneğiyle uyar" özelliği kaybolmasın diye örnekler silinmedi, yer değiştirdi. |
| 2026-11-22 | Şablon paylaşılabilir hâle getirildi: kişisel veri (`kaynak.json`, `kapali_kapilar.json`, geçmiş örnekleri) şablondan çıkıp kişisel klasöre taşındı (yolu `~/.claude/arastirma/kisisel_yolu.txt`; `kur` betiği boş örneklerden oluşturur); vaka notları `docs/vakalar/`'a, devir belgesi silindi; skill'ler vakaları "örnek vaka" diye anar, kullanıcının geçmişi saymaz | Kullanıcının isteği: skill'ler öğrencisiyle de paylaşılacak, öğrenci aynı hataları yaşamasın, skill genel olsun. Kişisel veri şablonda kalsaydı başka bir kullanıcının aile kontrolü ve kaynak sıralaması şablonu yazanın projelerine göre çalışırdı. Bedeli: kişisel klasör ayrı eşitlenir (özel depo); kurulum bir adım uzadı. |

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
