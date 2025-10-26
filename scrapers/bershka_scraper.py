"""
Bershka Barkod Scraper (Selenium)
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import re
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import Colors, print_success, print_error, print_warning, print_info, print_highlight


def process_barcode(barcode):
    """Barkodu işler ve URL oluşturur"""
    if len(barcode) == 14:
        processed_barcode = barcode[1:-3]
    elif len(barcode) == 10:
        processed_barcode = barcode
    else:
        return None, None
    
    part1 = processed_barcode[:4]
    part2 = processed_barcode[4:7]  
    part3 = processed_barcode[7:]
    
    url = f"https://www.bershka.com/tr/q/{part1}%2F{part2}%2F{part3}"
    return url, f"{part1}/{part2}/{part3}"


def run_bershka():
    """
    Bershka scraper'ı çalıştırır
    
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
        
        print(f"\n{Colors.BERSHKA}")
        print("═" * 70)
        print("║                                                                    ║")
        print("║               🛍️  BERSHKA BARKOD ARAMA SİSTEMİ                   ║")
        print("║                                                                    ║")
        print("═" * 70)
        print(f"{Colors.RESET}\n")
        
        print(f"{Colors.INFO}┌{'─' * 68}┐{Colors.RESET}")
        print(f"{Colors.INFO}│{' ' * 23}📋 BARKOD FORMATLARI{' ' * 26}│{Colors.RESET}")
        print(f"{Colors.INFO}├{'─' * 68}┤{Colors.RESET}")
        print(f"{Colors.INFO}│  • 14 hane  →  07369498800046 (Tam barkod){' ' * 24}│{Colors.RESET}")
        print(f"{Colors.INFO}│  • 10 hane  →  2104644040 (İşlenmiş barkod){' ' * 21}│{Colors.RESET}")
        print(f"{Colors.INFO}└{'─' * 68}┘{Colors.RESET}\n")
        
        print(f"{Colors.INFO}┌{'─' * 68}┐{Colors.RESET}")
        print(f"{Colors.INFO}│{' ' * 27}⌨️  KOMUTLAR{' ' * 29}│{Colors.RESET}")
        print(f"{Colors.INFO}├{'─' * 68}┤{Colors.RESET}")
        print(f"{Colors.INFO}│  q  →  Ana menüye dön ve sonuçları kaydet{' ' * 24}│{Colors.RESET}")
        print(f"{Colors.INFO}│  s  →  Bulunamayan ürünü atla (düzenleme modunda){' ' * 15}│{Colors.RESET}")
        print(f"{Colors.INFO}└{'─' * 68}┘{Colors.RESET}\n")
        
        print_success("⚡ Tarayıcı hazır! Barkod girmeye başlayabilirsiniz...")
        print(f"{Colors.INFO}{'─' * 70}{Colors.RESET}\n")
        
        is_first_run = True
        
        while True:
            barcode = input("Barkod giriniz: ").strip()
            
            if barcode.lower() == 'q':
                break
            
            if len(barcode) not in [10, 14]:
                print_error("Barkod 10 veya 14 haneli olmalı!")
                continue
            
            if not barcode.isdigit():
                print_error("Barkod sadece rakamlardan oluşmalı!")
                continue
            
            url, processed = process_barcode(barcode)
            
            if url is None:
                print_error("Barkod işlenemedi!")
                continue
            
            print_info(f"İşlenen: {processed}")
            
            try:
                if is_first_run:
                    print_info("Sayfa yükleniyor... (İlk açılış, biraz bekleyin)")
                else:
                    print_info("Sayfa yükleniyor...")
                
                driver.get(url)
                
                if is_first_run:
                    wait_time = 40
                    extra_wait = 20
                    print_info(f"JavaScript yükleniyor... ({extra_wait} saniye)")
                else:
                    wait_time = 35
                    extra_wait = 15
                
                wait = WebDriverWait(driver, wait_time)
                
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
                    print_success("Sayfa yüklendi!")
                except:
                    print_warning("Sayfa yükleme sorunu...")
                
                time.sleep(extra_wait)
                
                if is_first_run:
                    is_first_run = False
                    print_success("İlk yükleme tamamlandı! Sonraki aramalar daha hızlı olacak.\n")
                
                page_source = driver.page_source
                
                has_no_results = "Sonuç yok" in page_source
                
                if has_no_results:
                    result_line = f"{processed} BERSHKA Ürün Bulunamadı"
                    not_found_products.append(result_line)
                    print_error(f"{result_line}")
                    print_success("Tamamlandı!\n")
                    continue
                
                selectors_to_try = [
                    "p.bds-typography-label-s",
                    ".product-text p",
                    ".content-block_info p", 
                    "[data-qa-anchor='productItemText'] p",
                    "p[class*='typography']"
                ]
                
                elements = []
                for selector in selectors_to_try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(elements) > 0:
                        break
                
                if len(elements) == 0:
                    result_line = f"{processed} BERSHKA Ürün Bulunamadı"
                    not_found_products.append(result_line)
                    print(f"❌ {result_line}")
                    print("✅ Tamamlandı!\n")
                    continue
                
                if len(elements) > 0:
                    unique_products = []
                    seen = set()
                    
                    for e in elements:
                        text = e.text.strip()
                        if text and len(text) > 2 and text not in seen:
                            unique_products.append(text)
                            seen.add(text)
                    
                    if len(unique_products) == 1:
                        product_name = unique_products[0].title()
                        result_line = f"{processed} BERSHKA {product_name}"
                        found_products.append(result_line)
                        print_success(f"{result_line}")
                    elif len(unique_products) > 1:
                        product_name = unique_products[0].title()
                        result_line = f"{processed} BERSHKA {product_name}"
                        found_products.append(result_line)
                        print_success(f"İlk ürün seçildi: {result_line}")
                    else:
                        result_line = f"{processed} BERSHKA Ürün Bulunamadı"
                        not_found_products.append(result_line)
                        print_error(f"{result_line}")
                else:
                    result_line = f"{processed} BERSHKA Ürün Bulunamadı"
                    not_found_products.append(result_line)
                    print_error(f"{result_line}")
                
                print_success("Tamamlandı!\n")
                
            except Exception as e:
                print_error(f"Hata: {e}")
                result_line = f"{processed} BERSHKA Ürün Bulunamadı (Hata)"
                not_found_products.append(result_line)
                print_success("Tamamlandı!\n")
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}⚠ Program kullanıcı tarafından durduruldu!{Colors.RESET}")
    finally:
        try:
            driver.quit()
            print_success("Tarayıcı kapatıldı.")
        except:
            pass
    
    return found_products, not_found_products

