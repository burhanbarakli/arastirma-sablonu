# Örnek: GDA çalışması için arama cümleleri

README'deki "Makale arama (alan taraması)" bölümünün gerçek bir projeye uygulanmış hâli (20 Kasım 2026).

**Bağlam** ("Dört ayın karnesi" özetinden; ayrıntılar proje deposunda doğrulanmalı):
- soru: az gerçek, bol benzetim verisiyle öğrenen robot görmediği koşullarda nasıl başarılı olur;
- hedef alan: yeniden boyanmış benzetim masaları;
- GDA'nın kazancı gürültü içinde (52'ye 48);
- asıl etki hizalamadan değil, kapsamdan geliyor;
- aynı konum bilgisini alan EDI köprüsü yöntemle berabere.

## Kötü örnekler

| Cümle | Sorun |
|---|---|
| "GDA makaleleri" | Arama yönteme kilitlenir; yalnız GDA'yı kullananlar gelir. |
| "Domain adaptation robot manipulation" | Çok geniş, binlerce makale; koşul yok. |
| "Hizalama yerine kapsamın önemli olduğunu gösteren makaleler" | Bulgu cümleye girmiş; arama onu doğrulamaya çalışır, karşı kanıtı getirmez. |

## Amaca göre iyi cümleler

### A. Zorlanacak temel makale

> "Az sayıda gerçek gösterim ve bol benzetim verisiyle eğitilen görsel manipülasyon politikaları; hedef ortamın
> görünümü (doku, ışık, kamera) değiştiğinde başarı."

Bu ortamda bugün en çok kullanılan yöntemi bulmak için. Zorlanacak koşul cümlenin içinde: görünüm değişimi.

### B. Alanı tanımak

> "Hedef ortamdan az veri varken benzetimden gerçeğe aktarılan görsel robot politikaları."

Cümlede bilerek hipotez yok. Eleme tablosu bu alan için şöyle uyarlanır:

| Makale | Görev | Hedef alan neyle değişiyor | Hedef veri miktarı | Basit rakip var mı | Gerçek robot mu | Tohum | Kod |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

"Basit rakip var mı" sütununda üç rakibe bakılır:
- yalnız rastgeleleştirme (domain randomization);
- az gerçek veriyle ince ayar;
- gerçek ve benzetim verisini karıştırarak eğitmek.

"Hedef alan neyle değişiyor" sütununda hepsi yalnız dokuyu değiştiriyorsa, kör nokta orada olabilir. GDA'daki
"yeniden boyanmış masa" kurgusu da bu gruba girer.

### C. Kim çözmüş (yalnız ölçülmüş bir bulgudan sonra)

Ölçülmüş bulgu: "kazanç hizalamadan değil, kapsamdan". Bulgu cümleye girebilir, ama yöntem adıyla değil, özellik
olarak:

> "Az sayıda hedef örnekle, bir eğitim kümesinin hedef dağılımı ne kadar kapsadığını önceden tahmin etmek."

Bu cümle robotiğin dışından da makale getirir: dağılım kayması (covariate shift) istatistiği, dağılım dışı örnek
tespiti (OOD detection), aktif öğrenme, deney tasarımı. Hangi alanın aracının uyduğunu aktarım kontrolü
(`arastirma-kapisi`) söyler. Kapsamı ölçen basit bir araç bulunursa, Tez 1 makalesinde güçlü bir rakip ya da analiz
aleti olur.

## Hangisi şimdi?

"Dört ayın karnesi"nin tavsiyesi: yeni hat açma, GDA Tez 1'i bitir. Bu yüzden en işe yarayanı **C**: tez omurgası
olarak düşünülen "kapsam" bulgusunu destekleyecek ya da sınayacak araçları bulur. A ve B yeni bir hat açmaya daha yakın.

Yeni oturumda başlangıç:

```
alan taraması: amaç C. Özellik cümlesi: "Az sayıda hedef örnekle, bir eğitim kümesinin hedef dağılımı ne kadar kapsadığını önceden tahmin etmek." Bağlam: GDA Tez 1.
```
