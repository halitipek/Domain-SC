# Proje Dökümantasyon Oluşturma Süreci

---

## İçindekiler

1. [Doküman Tanımları](#dok%C3%BCman-tan%C4%B1mları)
2. [Referans Dokümanlar ve Veriler](#referans-dok%C3%BCmanlar-ve-veriler)
3. [Ajanlar](#ajanlar)
4. [Süreç Akışı (Detaylı)](#s%C3%BCre%C3%A7-ak%C4%B1%C5%9F%C4%B1-detayl%C4%B1)
5. [Nihai Çıktı](#nihai-%C3%A7%C4%B1kt%C4%B1)

---

## Doküman Tanımları

### Sistem Mimarisi Ana Planı (**SMAP**)

* **Mimari Vizyon**: ESD'den alınan vizyonun mimariye yansıtılması
* **Mimari İlkeler**: Modüler tasarım, bağımsız dağıtılabilirlik, gevşek bağlantı gibi başlıca prensipler
* **Üst Düzey Sistem Diyagramı**: Tüm modüllerin ve aralarındaki etkileşimlerin görsel temsili
* **Veri Akış Modeli**: Sistemdeki ana veri akışlarının ve dönüşümlerinin tanımlanması
* **Performans ve Maliyet Hedefleri**: OR raporundaki kısıtların mimariye yansıtılması
* **Teknik Kısıtlar ve Varsayımlar**: TR raporundaki teknik gereksinimlerin mimariye etkileri

### API Tasarım Çerçevesi (**APIDF**)

* **API Tasarım Prensipleri**: REST, GraphQL veya başka bir yaklaşımın seçilmesi
* **API Taksonomisi**: API'lerin gruplandırılması ve isimlendirme konvansiyonları
* **Kontrat Şablonları**: Her API türü için temel kontrat şablonları
* **Versiyonlama Stratejisi**: API'lerin versiyonlanma yöntemi
* **Dokümantasyon Gereksinimleri**: API dokümantasyonunun hazırlanma yöntemi
* **Güvenlik ve Erişim Kontrolü**: API güvenliği için temel prensipler

### Modül Tanım Belgesi (**MDD**)

* **Modül Listesi**: RR raporundan çıkarılan gerekli modüllerin listesi ve kısa açıklamaları
* **Modül Sorumlulukları**: Her modülün temel sorumlulukları
* **Modül Bağımlılıkları**: Yüksek seviyeli bağımlılık ilişkileri
* **Teknik Gereksinimler**: Her modül için TR raporundaki teknik gereksinimler
* **Performans Kriterleri**: Her modül için OR raporundaki performans beklentileri
* **İş Kuralları Entegrasyonu**: KS'den alınan kuralların ilgili modüllere entegrasyonu

### Bağımlılık Analiz Yönergesi (**DAG**)

* **Analiz Kriterleri**: İncelenecek bağımlılık türleri
* **Çevrimsel Bağımlılık Tespiti**: Çevrimsel bağımlılıkların tespit kriterleri
* **Bağımlılık Optimizasyonu**: Gereksiz bağımlılıkların azaltılması için stratejiler
* **Sıkı / Gevşek Bağlantı Analizi**: Bağlantıların sıkılık–gevşeklik derecesinin analizi
* **Entegrasyon Noktaları**: Kritik entegrasyon noktalarının belirlenmesi

### Mimari Yol Haritası (**AR**)

* **Geliştirme Sırası**: Modüllerin hangi sırayla geliştirileceği
* **Kritik Yol Analizi**: Hangi modül ve API'lerin kritik yolda yer aldığı
* **Ara Dönüm Noktaları**: Mimari açıdan önemli dönüm noktaları
* **Prototip Planı**: İlk prototiplerin geliştirilme planı
* **Risk Analizi**: Mimari riskler ve azaltma stratejileri

---

## Referans Dokümanlar ve Veriler

* **PD** — Projeden Beklentileri Sunan Kısa Döküman
* **EC** — Örnek Dosya (*Example Case*)
* **DMD** — Dosya Meta Verileri
* **DMD-SUM** — Dosya Meta Verileri Özet
* **GAP** — Belirsiz/Karışabilir Terim–Kural–Doküman Tipleri
* **RR** — İhtiyaç Raporu
* **RR-SUM** — İhtiyaç Raporu Özet
* **TR** — Teknoloji Raporu
* **TR-SUM** — Teknoloji Raporu Özet
* **OR** — Optimizasyon Raporu
* **OR-SUM** — Optimizasyon Raporu Özet
* **KS** — Kural Seti

---

## Ajanlar

* **HALİT**
* **OA** — Orkestratör Ajanı
* **DDA** — Belge Keşif Ajanı
* **WA** — İşçi Ajan *(tek seferlik kullanılır, tamamlanınca kapatılır)*
* **TAA** — Teknoloji Analizi Ajanı
* **RAA** — İhtiyaç Analizi Ajanı
* **OAA** — Optimizasyon Analizi Ajanı
* **KAA** — Kural Analizi Ajanı
* **SAA** — Sistem Mimarı Ajanı
* **MTA** — Modül Tasarım Ajanı
* **AEA** — API Entegrasyon Ajanı
* **BAA** — Bağımlılık Analiz Ajanı
* **CAA** — Tutarlılık Analiz Ajanı

---

## Süreç Akışı (Detaylı)

Aşağıdaki iş akışı, her adımın **girdi** (*→*) ve **çıktı** (*↩*) bilgileri ile birlikte ayrıntılı olarak sunulmuştur. İşçi ajanlar görevlerini tamamladıktan sonra **kapatılır**.

### 1. Başlangıç

1. **Halit → OA** → `{PD path, EC path}`
2. **OA → DDA** → `{PD path, EC path}`

### 2. Belge Keşif Aşaması

* **DDA → WA.1** → `{EC path}`
  **WA.1 Görevleri**

  * Sıkıştırılmış dosyaları açarak klasöre ekle.
  * Tüm dosyaların meta verilerini çıkar (**DMD**).
  * **DMD** özetini çıkar (**DMD-SUM**).
  * **WA.1** -> Kaydet -> `{DMD}` -> path -> **DDA**
  * **WA.1** -> Kaydet -> `{DMD-SUM}` -> path -> **DDA**
    *WA.1 kapatılır.*

* **DDA → WA.2** → `{EC path, PD path, DMD path}`
  **WA.2 Görevleri (SMART)**

  * Tüm dosyaları oku ve tara.
  * **GAP** listesini oluştur.
  * **WA.2** -> Kaydet -> `{GAP listesi}` -> path -> **DDA**
    *WA.2 kapatılır.*

* **DDA → WA.3** → `{GAP listesi path}`
  **WA.3 Görevleri**

  * GAP listesindeki terimlerin anlamını araştır (internet kullanabilir).
  * Özetleri çıkar.
  * **WA.3** -> Kaydet -> `{GAP özetleri}` -> path -> **DDA**
    *WA.3 kapatılır.*

* **DDA Nihai Çıktıları** -> `{GAP özetleri}`

  * Sözlük oluştur (**DICT**).
  * **DDA** -> Kaydet -> `{DICT}` -> path -> **OA**
    *DDA kapatılır.*

### 3. Kural Analizi Aşaması

* **KAA** → `{PD, DICT, DMD-SUM}`
  **KAA Görevleri**

  * Sigorta Tahkim süreçlerinin güncel durumunu araştır.
  * Kod hâline gelmemiş mantıksal ifadelerden oluşan **KS**'yi oluştur.
  * KS'yi ikileme ve çelişkilere karşı gözden geçir.
  * **KAA** - Kaydet -> `{KS}` -> path -> **OA**
    *KAA kapatılır.*

* **OA Dahili Görevleri** → `{PD, DICT, DMD-SUM, KS}`

  * Vizyonu, amaçları ve başarı ölçütlerini belirle.
  * Kısa bir **Executive Summary Document (ESD)** hazırla.
  * ESD'nin, PD'deki tüm talepleri karşıladığını doğrula; gerekirse revize et.

### 4. İhtiyaç Analizi Aşaması

* **WA.4** → `{ESD, DICT, DMD-SUM, KS}`
  **WA.4 — SMART Sorguları**

  * Sistem ne yapmalı?
  * Sistem hangi kullanıcılar için tasarlanmalı?
  * Sistem hangi verileri kullanmalı?
  * Sistem hangi verileri üretmeli?
  * Sistem hangi verileri depolamalı?
  * Sistem hangi verileri dışarı aktarmalı?
  * Event listesi nedir?
  * Sistem, ham dosyadan nihai rapora/raporlara hangi başlıca adımlarla ilerlemeli?
  * Hangi dosya tipleri geliyor ve her biri için özel işlem (ör. OCR) gerekiyor mu?
  * Metin çıkarımı nerede zorunlu; hangi araç veya model kullanılacak?
  * Hangi karar noktaları var ve karar vermek için hangi veriler birleşecek?
  * Kullanıcı hangi çıktı formatlarını (PDF, JSON, özet vb.) ve hangi detay seviyesini bekliyor?
  * Performans hedefi nedir (dosya başı süre, eş‑zamanlı işlem sayısı)?
  * Hata veya istisna durumları nerede olası; sistem nasıl toparlanacak?
  * Gelecekte yeni belge tipleri/kurallar eklemek gerekirse, sistem buna nasıl modüler hazırlanacak?
  * **WA.4 ↩ RAA** `{yanıtlar}`
    *WA.4 kapatılır.*

* **RAA Görevleri** → `{ESD, DICT, DMD-SUM, KS, yanıtlar}`

  * Kapsam ve modül analizi yap.
  * Fonksiyonel modülleri ve modüller arası bağımlılıkları belirle.
  * Küçük fakat kapsayıcı bir örnek girdi ile planı test ederek doğruluğunu onayla; gerekirse tekrarla.
  * **RAA** - Kaydet -> `{RR}` -> path -> **OA**
  * **RAA** - Kaydet -> `{RR-SUM}` -> path -> **OA**
    *RAA kapatılır.*

### 5. Teknoloji Analizi Aşaması

* **TAA** → `{ESD, RR, DMD-SUM}`
  **TAA Görevleri**

  * Teknik gereksinimleri analiz et.
  * OCR, belge işleme, RAG ve diğer teknik gereksinimlere yönelik çözümleri araştır.
  * **TAA** - Kaydet -> `{TR}` -> path -> **OA**
  * **TAA** - Kaydet -> `{TR-SUM}` -> path -> **OA**
    *TAA kapatılır.*

### 6. Optimizasyon Analizi Aşaması

* **OAA** → `{ESD, RR, TR, DMD-SUM}`
  **OAA Görevleri**

  * Performans ve maliyet analizi yap.
  * LLM kullanımı için optimizasyon stratejileri geliştir.
  * **OAA** - Kaydet -> `{OR}` -> path -> **OA**
  * **OAA** - Kaydet -> `{OR-SUM}` -> path -> **OA**
    *OAA kapatılır.*

### 7. Mimari Tasarım Aşaması

#### 7.0 İlk Mimari Tasarım

* **SAA** → `{ESD, RR, TR, OR, KS, DMD-SUM}`
  **SAA Görevleri**

  * SMAP, APIDF, MDD, DAG, AR belgelerini oluştur, tümünü kaydet.

#### 7.1 Tutarlılık Kontrolü 

* **CAA** → `{ESD, SMAP, APIDF, MDD, DAG, AR}`
* **CAA ↩ SAA**: Tutarlılık analizi sonuçları (ESD hariç öneriler)

>**CAA** onaylayana kadar **SAA** revizyon eder. (CAA yapıcı ve sonuç almaya odaklıdır. Süreci uzatmak faydalı değil.)

#### 7.2 API ve Modül Tasarımı

* **AEA** → `{SMAP, APIDF, AR}`

  * **AEA Görevleri**: Temel API Kontratlarını oluştur (**TAK**); **AEA ↩ SAA** `{TAK}`
* **MTA** → `{SMAP, TAK, MDD, AR}`

  * **MTA Görevleri**: Tüm modüllerin tasarım planlarını oluştur (**MTP**); **MTA ↩ SAA** `{MTP}`
* **BAA** → `{SMAP, TAK, MTP, DAG, AR}`

  * **BAA Görevleri**: Bağımlılık Analiz Planlarını oluştur (**BAP**); **BAA ↩ SAA** `{BAP}`
* **AEA** → `{MTP, BAP}`: API kontratlarını güncelle; **AEA ↩ SAA** `{Güncel API Kontratları}`
* **MTA** → `{API Kontratları, BAP}`: Modül tasarımlarını revize et; **MTA ↩ SAA** `{Güncel MTP}`
    *AEA kapatılır.*
    *MTA kapatılır.*
    *BAA kapatılır.*

#### 7.3 Nihai Mimari

* **SAA**: Tüm API, modül ve bağımlılıkları kapsayan **ADD**'yi hazırla.
* **SAA → CAA** → `{ADD}`
* **CAA ↩ SAA**: Tutarlılık geri bildirimi; onaylanana kadar revizyon.
* **SAA ↩ OA** `{Onaylı ADD}`
  *SAA kapatılır.*

### 8. Kapanış

* **OA**: ADD'yi inceler; tüm raporları konsolide eder.
* **OA** → Halit: **docs.zip**

  * `docs.zip` içeriği: Nihai dökümanlar, **ADD, ESD, RR, TR, OR, KS, DICT**

---

## Nihai Çıktı

* **docs.zip** — Proje dokümantasyon paketi

  * **ADD** — Nihai Mimari Dokümanı
  * **ESD, RR, TR, OR, KS, DICT** ve diğer ekler
  