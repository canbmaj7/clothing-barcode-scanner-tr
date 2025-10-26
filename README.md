# 🛍️ Giyim Barkod Arama Sistemi

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-Private-red.svg)

**Türkiye'deki popüler giyim markalarının barkod numaralarından ürün adlarını otomatik olarak bulan gelişmiş sistem**

[📍 Özellikler](#-özellikler) • [🚀 Kurulum](#-kurulum) • [💻 Kullanım](#-kullanım) • [📊 Çıktılar](#-çıktılar)

</div>

---

## 📖 Hakkında

Giyim Barkod Arama Sistemi, mağazalardan toplanan barkod numaralarından ürün bilgilerini otomatik olarak çeken profesyonel bir web scraping aracıdır. 5 farklı popüler marka için optimize edilmiş scraper'lar içerir ve sonuçları hem Excel hem de TXT formatında kaydeder.

## ✨ Özellikler

### 🎯 Temel Özellikler
- **🔐 Güvenli Giriş Sistemi**: Google Sheets entegrasyonu ile şifre doğrulama
- **🔍 Çoklu Marka Desteği**: 5 popüler giyim markası için otomatik arama
- **📊 Günlük İstatistik Paneli**: Detaylı başarı oranları ve arama geçmişi
- **🎨 Renkli Terminal Arayüzü**: Kolay takip için renklendirilmiş çıktılar
- **💾 Çift Format Çıktı**: Hem TXT hem de Excel formatında otomatik kayıt
- **✏️ Manuel Düzenleme Modu**: Bulunamayan ürünler için interaktif düzenleme
- **🎨 Özel Icon**: İkon oluşturucu ile özelleştirilmiş EXE icon'u

### 🛍️ Desteklenen Markalar

| Marka | Yöntem | Özellik |
|-------|--------|---------|
| 🛍️ **Bershka** | Selenium (Dinamik) | 10/14 haneli barkod |
| 👕 **H&M** | Selenium (Dinamik) | 10 haneli barkod |
| 👗 **Zara** | API | Hızlı arama |
| 🧥 **Mango** | Requests + BS4 | Optimize edilmiş |
| 👖 **Mavi** | curl_cffi | Gelişmiş bypass |

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- Chrome tarayıcı (güncel versiyon)
- ChromeDriver (Chrome ile uyumlu)
- İnternet bağlantısı

### 1️⃣ Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 2️⃣ ChromeDriver İndirin

1. [ChromeDriver İndirme Sayfası](https://chromedriver.chromium.org/)'na gidin
2. Chrome tarayıcınızın versiyonunu kontrol edin (Chrome menü → Yardım → Google Chrome Hakkında)
3. Uyumlu ChromeDriver'ı indirin
4. `chromedriver.exe` dosyasını proje klasörüne kopyalayın

### 3️⃣ Programı Çalıştırın

```bash
python main.py
```

## 💻 Kullanım

### Basit Kullanım

1. Programı başlatın (`python main.py`)
2. Şifrenizi girin (gizli giriş: ***)
3. Ana menüden marka seçin (1-5)
4. Barkod numaralarını girin (her satıra bir barkod)
5. Arama bitince `q` yazarak çıkın
6. Sonuçları Excel ve TXT olarak kaydedin

### Kullanılabilir Komutlar

| Komut | Açıklama |
|-------|----------|
| `q` | Aramayı bitir ve sonuçları kaydet |
| `s` | Bulunamayan ürünü atla (düzenleme modunda) |
| `e` | Manuel düzenleme moduna geç |
| `h` | Düzenleme işlemini iptal et |

### Günlük Menü Seçenekleri

```
╔══════════════════════════════════════════════╗
║  🛍️  GİYİM BARKOD ARAMA SİSTEMİ             ║
╠══════════════════════════════════════════════╣
║  1. 🛍️  Bershka                             ║
║  2. 👕  H&M                                  ║
║  3. 👗  Zara                                ║
║  4. 🧥  Mango                               ║
║  5. 👖  Mavi                                ║
║  6. 📊  Bugünkü Excel Dosyasını Aç          ║
║  7. 📁  Outputs Klasörünü Aç                ║
║  8. ❌  Çıkış                                ║
╚══════════════════════════════════════════════╝
```

## 📊 Çıktılar

### TXT Dosyası (Marka Bazlı)
Her marka için ayrı TXT dosyası oluşturulur:
- `outputs/txt/bershka_urunler.txt`
- `outputs/txt/h&m_urunler.txt`
- `outputs/txt/zara_urunler.txt`
- `outputs/txt/mango_urunler.txt`
- `outputs/txt/mavi_urunler.txt`

**Format:**
```
=== BULUNAN ÜRÜNLER ===
2104644040 BERSHKA Oversize Sweatshirt
4813858712 BERSHKA Denim Ceket

=== BULUNAMAYAN ÜRÜNLER ===
1188865002 BERSHKA Ürün Bulunamadı
```

### Excel Dosyası (Günlük - Tüm Markalar)
Günlük olarak tüm markalar tek Excel dosyasında birleştirilir:
- `outputs/excel/tum_urunler_2025-10-26.xlsx`

**Sütunlar:**
| Barkod | Marka | Ürün Adı | Tarih |
|--------|-------|----------|-------|
| 2104644040 | BERSHKA | Oversize Sweatshirt | 2025-10-26 |
| 4813858712 | ZARA | Denim Ceket | 2025-10-26 |

## 🎨 Icon Oluşturma

Projeye özel icon oluşturmak için:

```bash
python create_icon.py
```

Bu komut `app_icon.ico` dosyasını oluşturur. İsterseniz PyInstaller ile EXE dosyası oluştururken bu icon'u kullanabilirsiniz.

## 📦 Proje Yapısı

```
clothing-barcode-finder/
├── 📄 main.py                  # Ana program ve menü sistemi
├── 📄 auth.py                  # Google Sheets şifre doğrulama
├── 📄 excel_manager.py         # Excel işlemleri ve veri yönetimi
├── 📄 utils.py                 # Yardımcı fonksiyonlar (renk, istatistik)
├── 📄 create_icon.py           # Icon oluşturucu
├── 🔧 requirements.txt         # Python bağımlılıkları
├── 🚗 chromedriver.exe         # Selenium driver
│
├── 📁 scrapers/                # Marka scraper'ları
│   ├── __init__.py
│   ├── bershka_scraper.py      # Bershka scraper (Selenium)
│   ├── hm_scraper.py           # H&M scraper (Selenium)
│   ├── zara_scraper.py         # Zara scraper (API)
│   ├── mango_scraper.py        # Mango scraper (BS4)
│   └── mavi_scraper.py         # Mavi scraper (curl_cffi)
│
└── 📁 outputs/                 # Otomatik oluşturulan çıktılar
    ├── 📁 txt/                 # Marka bazlı TXT dosyaları
    ├── 📁 excel/               # Günlük Excel dosyaları
    └── statistics.json         # JSON formatında istatistikler
```

## ⚙️ Bağımlılıklar

```txt
# Web Scraping
selenium>=4.0.0           # Dinamik web scraping
requests>=2.28.0         # HTTP istekleri
beautifulsoup4>=4.11.0    # HTML parsing
curl-cffi>=0.5.0          # Gelişmiş bypass
lxml>=4.9.0               # XML/HTML parsing

# Excel
xlsxwriter>=3.0.0         # Excel yazma
openpyxl>=3.1.0           # Excel okuma/yazma

# Görsel
colorama>=0.4.6           # Renkli terminal çıktısı
pillow>=10.0.0           # Icon oluşturma
```

## 🔧 Yapılandırma

### Şifre Sistemi
Program Google Sheets'ten şifre okuyacak şekilde yapılandırılmıştır. `auth.py` dosyasındaki Sheet ID'yi kendi Sheet ID'niz ile değiştirin.

### Bekleme Süreleri
Her marka için optimize edilmiş bekleme süreleri:
- **Bershka**: 20-40 saniye (ilk aramada daha uzun)
- **H&M**: 10-20 saniye
- **Zara**: 2-5 saniye (API)
- **Mango**: 5-10 saniye
- **Mavi**: 5-10 saniye

## ⚠️ Önemli Notlar

1. **Chrome Gerekliliği**: Güncel Chrome tarayıcısı zorunludur
2. **ChromeDriver Uyumluluğu**: Chrome versiyonuyla uyumlu olmalı
3. **İnternet Bağlantısı**: Tüm aramalar için gerekli
4. **Rate Limiting**: Aşırı hızlı aramadan kaçının
5. **Gizlilik**: Google Sheets şifre sistemi geliştiricinin kendi hesabını kullanır

## 🐛 Karşılaşılabilecek Sorunlar

### ChromeDriver Hatası
**Sorun**: `chromedriver.exe bulunamadı`  
**Çözüm**: ChromeDriver'ı indirip proje klasörüne kopyalayın

### Chrome Uyumsuzluğu
**Sorun**: `Chrome tarayıcı hatası`  
**Çözüm**: Chrome'u güncelleyin ve uyumlu ChromeDriver indirin

### İnternet Problemi
**Sorun**: `İnternet bağlantısı yok`  
**Çözüm**: İnternet bağlantınızı kontrol edin

### Excel Açık
**Sorun**: `Excel dosyası açılamıyor`  
**Çözüm**: Excel dosyasını kapatıp tekrar deneyin

## 📈 Sürüm Geçmişi

### v1.0.0 (2025-10-26)
- ✅ 5 marka desteği (Bershka, H&M, Zara, Mango, Mavi)
- ✅ Renkli terminal arayüzü
- ✅ Günlük istatistik paneli
- ✅ Gelişmiş hata yönetimi
- ✅ Excel + TXT çift çıktı
- ✅ Manuel düzenleme modu
- ✅ Google Sheets şifre sistemi
- ✅ Icon oluşturucu
- ✅ Optimize edilmiş beklemeler
- ✅ PyInstaller EXE desteği

## 📄 Lisans

Bu proje özel kullanım içindir. Web sitelerinin kullanım şartlarına uygun kullanın.

## 👤 Geliştirici

**Ahmet Can Otlu**
- Email: ahmetcanotlu@gmail.com

---

<div align="center">

**⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! ⭐**

Made with ❤️ in Türkiye

</div>
