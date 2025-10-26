"""
H&M Barkod Scraper (Selenium)
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys


def process_barcode(barcode):
    """Barkodu ayrıştırır ve H&M için gerekli kısmı çıkarır"""
    if len(barcode) == 10:
        return barcode
    elif len(barcode) == 29:
        return barcode[2:12]
    else:
        return barcode


def run_hm():
    """
    H&M scraper'ı çalıştırır
    
    Returns:
        tuple: (found_products, not_found_products)
    """
    found_products = []
    not_found_products = []
    
    # Chrome ayarları
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.7390.108 Safari/537.36")
    
    # ChromeDriver yolu (PyInstaller uyumlu)
    if getattr(sys, 'frozen', False):
        # EXE modunda
        import main
        chromedriver_path = main.CHROMEDRIVER_PATH
    else:
        # Normal Python modunda
        chromedriver_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chromedriver.exe")
        if not os.path.exists(chromedriver_path):
            chromedriver_path = "chromedriver"
    
    try:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("\n" + "═" * 70)
        print("║                                                                    ║")
        print("║                 🛍️  H&M BARKOD ARAMA SİSTEMİ                     ║")
        print("║                                                                    ║")
        print("═" * 70)
        print()
        
        print(f"┌{'─' * 68}┐")
        print(f"│{' ' * 23}📋 BARKOD FORMATLARI{' ' * 26}│")
        print(f"├{'─' * 68}┤")
        print(f"│  • 29 karakter  →  101188865002009202410877220ID{' ' * 18}│")
        print(f"│  • 10 karakter  →  1296051002{' ' * 35}│")
        print(f"└{'─' * 68}┘\n")
        
        print(f"┌{'─' * 68}┐")
        print(f"│{' ' * 27}⌨️  KOMUTLAR{' ' * 29}│")
        print(f"├{'─' * 68}┤")
        print(f"│  q  →  Ana menüye dön ve sonuçları kaydet{' ' * 24}│")
        print(f"│  s  →  Bulunamayan ürünü atla (düzenleme modunda){' ' * 15}│")
        print(f"└{'─' * 68}┘\n")
        
        print("⚡ Tarayıcı hazır! Barkod girmeye başlayabilirsiniz...")
        print("─" * 70)
        print()
        
        while True:
            barcode_input = input("Barkod giriniz: ").strip()
            
            if barcode_input.lower() == 'q':
                break
            
            if not barcode_input:
                print("❌ Barkod boş olamaz!")
                continue
            
            barcode_len = len(barcode_input)
            
            if barcode_len not in [10, 29]:
                print(f"❌ Barkod 10 veya 29 karakter olmalı! (Girilen: {barcode_len} karakter)")
                continue
            
            barcode = process_barcode(barcode_input)
            print(f"Orijinal: {barcode_input}")
            print(f"İşlenen: {barcode}")
            
            url = f"https://www2.hm.com/tr_tr/search-results.html?q={barcode}"
            print(f"URL: {url}")
            
            try:
                print("Sayfa yükleniyor...")
                driver.get(url)
                
                wait = WebDriverWait(driver, 15)
                
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".product-item, .item-heading, [class*='product'], h3")))
                    print("✓ Ürün bilgileri yüklendi!")
                except:
                    print("⚠ Ürün bilgileri bulunamadı, devam ediliyor...")
                
                time.sleep(3)
                
                print("Ürün kontrol ediliyor...")
                
                # data-articlecode attribute'u olan article elementlerini bul
                articles_with_articlecode = driver.find_elements(By.CSS_SELECTOR, "article[data-articlecode]")
                
                # Bu barkodla eşleşen article var mı?
                matching_articles = []
                for article in articles_with_articlecode:
                    articlecode = article.get_attribute("data-articlecode")
                    if articlecode == barcode:
                        matching_articles.append(article)
                        print(f"✓ Eşleşen ürün bulundu: {articlecode}")
                
                # Sonuçları işle ve kaydet
                if len(matching_articles) > 0:
                    # Ürün bulundu - ilk eşleşen articleden ürün adını al
                    first_article = matching_articles[0]
                    product_name_element = first_article.find_element(By.CSS_SELECTOR, "h3")
                    product_name = product_name_element.text.strip()
                    
                    # Format: barkod H&M ürün_ismi (baş harfleri büyük)
                    formatted_product_name = product_name.title()
                    result_line = f"{barcode} H&M {formatted_product_name}"
                    found_products.append(result_line)
                    print(f"✓ {result_line}")
                else:
                    # Ürün bulunamadı
                    result_line = f"{barcode} H&M Ürün Bulunamadı"
                    not_found_products.append(result_line)
                    print(f"❌ {result_line}")
                
                print("✅ Tamamlandı!\n")
                
            except Exception as e:
                print(f"❌ Hata: {e}")
                result_line = f"{barcode} H&M Ürün Bulunamadı (Hata)"
                not_found_products.append(result_line)
                print("✅ Tamamlandı!\n")
    
    except KeyboardInterrupt:
        print("\n\n⚠ Program kullanıcı tarafından durduruldu!")
    finally:
        try:
            driver.quit()
            print("Tarayıcı kapatıldı.")
        except:
            pass
    
    return found_products, not_found_products

