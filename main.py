"""
GİYİM BARKOD ARAMA SİSTEMİ
Ana Menü ve Sistem Yöneticisi
"""
import os
import sys
import tempfile
import shutil
from datetime import datetime
from excel_manager import ExcelManager, parse_product_line
from utils import (
    Colors, print_success, print_error, print_warning, print_info, 
    print_highlight, print_brand_header, Statistics, handle_error, 
    clear_screen, print_loading
)
from auth import verify_password, show_login_failed_screen

# PyInstaller için stdin kontrolü
if not hasattr(sys, 'stdin') or sys.stdin is None:
    import io
    sys.stdin = io.StringIO()
    
# PyInstaller için chromedriver yolu
def get_chromedriver_path():
    """ChromeDriver'ın doğru yolunu döndürür"""
    if getattr(sys, 'frozen', False):
        # EXE modunda - geçici klasöre çıkar
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller'ın geçici klasörü
            chromedriver_bundled = os.path.join(sys._MEIPASS, 'chromedriver.exe')
            
            # Geçici klasöre kopyala (yazılabilir olması için)
            temp_dir = tempfile.gettempdir()
            chromedriver_temp = os.path.join(temp_dir, 'chromedriver.exe')
            
            if not os.path.exists(chromedriver_temp):
                shutil.copy2(chromedriver_bundled, chromedriver_temp)
            
            return chromedriver_temp
        else:
            # Eski PyInstaller veya farklı paketleyici
            return os.path.join(os.path.dirname(sys.executable), 'chromedriver.exe')
    else:
        # Normal Python modunda
        return os.path.join(os.path.dirname(__file__), 'chromedriver.exe')

# Global değişken olarak kaydet
CHROMEDRIVER_PATH = get_chromedriver_path()


def ensure_directories():
    """Gerekli klasörleri oluşturur"""
    directories = [
        os.path.join("outputs", "txt"),
        os.path.join("outputs", "excel")
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print_success(f"Klasör oluşturuldu: {directory}")


def show_main_menu(stats):
    """Ana menüyü gösterir"""
    clear_screen()
    
    # Başlık - 70 karakter genişlik
    print(f"\n{Colors.HIGHLIGHT}")
    print("═" * 70)
    print("║                                                                    ║")
    print("║             🛍️  GİYİM BARKOD ARAMA SİSTEMİ  v1.0.0              ║")
    print("║                                                                    ║")
    print("═" * 70)
    print(f"{Colors.RESET}")
    
    # İstatistik paneli
    stats.print_daily_summary()
    
    # Markalar - 70 karakter genişlik
    print(f"\n{Colors.INFO}┌{'─' * 68}┐{Colors.RESET}")
    print(f"{Colors.INFO}│{' ' * 26}MARKALAR{' ' * 34}│{Colors.RESET}")
    print(f"{Colors.INFO}├{'─' * 68}┤{Colors.RESET}")
    print(f"{Colors.INFO}│  1. {Colors.BERSHKA}🛍️   Bershka{Colors.INFO}{' ' * 51}│{Colors.RESET}")
    print(f"{Colors.INFO}│  2. {Colors.HM}👕  H&M{Colors.INFO}{' ' * 54}│{Colors.RESET}")
    print(f"{Colors.INFO}│  3. {Colors.ZARA}👗  Zara{Colors.INFO}{' ' * 53}│{Colors.RESET}")
    print(f"{Colors.INFO}│  4. {Colors.MANGO}🧥  Mango{Colors.INFO}{' ' * 52}│{Colors.RESET}")
    print(f"{Colors.INFO}│  5. {Colors.MAVI}👖  Mavi{Colors.INFO}{' ' * 53}│{Colors.RESET}")
    print(f"{Colors.INFO}└{'─' * 68}┘{Colors.RESET}")
    
    # Araçlar - 70 karakter genişlik
    print(f"\n{Colors.INFO}┌{'─' * 68}┐{Colors.RESET}")
    print(f"{Colors.INFO}│{' ' * 27}ARAÇLAR{' ' * 34}│{Colors.RESET}")
    print(f"{Colors.INFO}├{'─' * 68}┤{Colors.RESET}")
    print(f"{Colors.INFO}│  6. 📊  Bugünkü Excel Dosyasını Aç{' ' * 31}│{Colors.RESET}")
    print(f"{Colors.INFO}│  7. 📁  Outputs Klasörünü Aç{' ' * 37}│{Colors.RESET}")
    print(f"{Colors.INFO}│  8. ❌  Çıkış{' ' * 51}│{Colors.RESET}")
    print(f"{Colors.INFO}└{'─' * 68}┘{Colors.RESET}")
    print()


def manual_edit_mode(not_found_products, brand_name):
    """
    Bulunamayan ürünler için manuel düzenleme modu
    
    Args:
        not_found_products (list): Bulunamayan ürünler listesi
        brand_name (str): Marka adı (BERSHKA, H&M, vb.)
    
    Returns:
        tuple: (düzenlenen_ürünler, kalan_bulunamayan_ürünler)
    """
    if not not_found_products:
        return [], []
    
    print(f"\n{Colors.WARNING}{'═' * 70}{Colors.RESET}")
    print(f"{Colors.WARNING}║{' ' * 68}║{Colors.RESET}")
    print(f"{Colors.WARNING}║{' ' * 16}⚠️  BULUNAMAYAN ÜRÜNLER DÜZENLENİYOR{' ' * 16}║{Colors.RESET}")
    print(f"{Colors.WARNING}║{' ' * 68}║{Colors.RESET}")
    print(f"{Colors.WARNING}{'═' * 70}{Colors.RESET}\n")
    print_info(f"{len(not_found_products)} bulunamayan ürün var\n")
    
    edited_products = []
    to_remove = []
    
    for not_found_item in not_found_products[:]:
        # Barkodu çıkar
        barcode_part = not_found_item.split(f" {brand_name} ")[0]
        
        while True:
            product_name_input = input(f"{Colors.INFO}{barcode_part}{Colors.RESET} - Ürün adını girin (veya 's' atla, 'q' kaydet ve çık): ").strip()
            
            if product_name_input.lower() == 'q':
                print_success("Kayıt ediliyor ve çıkılıyor...")
                break
            
            if product_name_input.lower() == 's':
                print_warning("Atlandı\n")
                break
            
            if product_name_input:
                formatted_product_name = product_name_input.title()
                new_result_line = f"{barcode_part} {brand_name} {formatted_product_name}"
                
                edited_products.append(new_result_line)
                to_remove.append(not_found_item)
                print_success(f"Eklendi: {new_result_line}\n")
                break
            else:
                print_error("Ürün adı boş olamaz!")
        
        if product_name_input.lower() == 'q':
            break
    
    # Düzenlenen ürünleri listeden kaldır
    for item in to_remove:
        not_found_products.remove(item)
    
    print_success("Düzenleme tamamlandı!")
    print_info(f"• {len(edited_products)} ürün eklendi")
    print_info(f"• {len(not_found_products)} ürün bulunamayan listesinde kaldı\n")
    
    return edited_products, not_found_products


def save_to_txt(found_products, not_found_products, brand_name):
    """
    Sonuçları TXT dosyasına kaydeder (append mode)
    
    Args:
        found_products (list): Bulunan ürünler
        not_found_products (list): Bulunamayan ürünler
        brand_name (str): Marka adı (küçük harf, dosya adı için)
    """
    txt_file = os.path.join("outputs", "txt", f"{brand_name.lower()}_urunler.txt")
    
    try:
        with open(txt_file, 'a', encoding='utf-8') as f:
            # Tarih başlığı
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"\n{'=' * 60}\n")
            f.write(f"Arama Tarihi: {timestamp}\n")
            f.write(f"{'=' * 60}\n\n")
            
            # Bulunan ürünler
            if found_products:
                f.write("=== BULUNAN ÜRÜNLER ===\n\n")
                for result in found_products:
                    f.write(result + '\n')
                f.write(f"\nToplam: {len(found_products)} ürün\n")
            
            # Boş satır
            if found_products and not_found_products:
                f.write("\n")
            
            # Bulunamayan ürünler
            if not_found_products:
                f.write("=== BULUNAMAYAN ÜRÜNLER ===\n\n")
                for result in not_found_products:
                    f.write(result + '\n')
                f.write(f"\nToplam: {len(not_found_products)} ürün\n")
            
            f.write("\n")
        
        print_success(f"TXT dosyasına kaydedildi: {txt_file}")
        return True
    except Exception as e:
        handle_error(e, "TXT kayıt")
        return False


def save_to_excel(found_products, not_found_products, brand_name):
    """
    Sonuçları Excel dosyasına kaydeder
    
    Args:
        found_products (list): Bulunan ürünler
        not_found_products (list): Bulunamayan ürünler
        brand_name (str): Marka adı (BÜYÜK HARF)
    """
    try:
        excel_manager = ExcelManager()
        
        # Tüm ürünleri parse et
        all_products = found_products + not_found_products
        products_to_add = []
        
        for product_line in all_products:
            parsed = parse_product_line(product_line, brand_name)
            if parsed:
                products_to_add.append(parsed)
        
        # Excel'e ekle
        excel_manager.add_products(products_to_add, brand_name)
        
        # Kaydet
        success, error = excel_manager.save_to_excel()
        
        if success:
            print_success(f"Excel dosyasına kaydedildi: {excel_manager.filename}")
            return True
        else:
            print_error(f"Excel kayıt hatası: {error}")
            # Eğer dosya açıksa, yeniden denemesini iste
            if "açık" in error.lower():
                while True:
                    retry = input(f"{Colors.WARNING}Excel dosyasını kapattıktan sonra 'e' ile yeniden deneyin (veya 'h' ile iptal): {Colors.RESET}").strip().lower()
                    if retry == 'e':
                        return save_to_excel(found_products, not_found_products, brand_name)
                    elif retry == 'h':
                        print_info("Excel kaydı iptal edildi.")
                        return False
                    else:
                        print_error("Geçersiz seçim! Lütfen 'e' (tekrar dene) veya 'h' (iptal) girin.")
            return False
    except Exception as e:
        handle_error(e, "Excel kayıt")
        return False


def run_brand_scraper(brand_choice, stats):
    """
    Seçilen marka scraper'ını çalıştırır
    
    Args:
        brand_choice (str): Marka seçimi (1-5)
        stats (Statistics): İstatistik objesi
    
    Returns:
        bool: Başarılı ise True
    """
    brand_map = {
        '1': ('BERSHKA', 'scrapers.bershka_scraper', 'run_bershka'),
        '2': ('H&M', 'scrapers.hm_scraper', 'run_hm'),
        '3': ('ZARA', 'scrapers.zara_scraper', 'run_zara'),
        '4': ('MANGO', 'scrapers.mango_scraper', 'run_mango'),
        '5': ('MAVİ', 'scrapers.mavi_scraper', 'run_mavi'),
    }
    
    if brand_choice not in brand_map:
        print_error("Geçersiz seçim!")
        return False
    
    brand_name, module_name, function_name = brand_map[brand_choice]
    
    try:
        # Modülü import et
        module = __import__(module_name, fromlist=[function_name])
        scraper_function = getattr(module, function_name)
        
        # Scraper'ı çalıştır
        print_loading(f"{brand_name} scraper başlatılıyor")
        found_products, not_found_products = scraper_function()
        
        # Manuel düzenleme modu
        if not_found_products:
            print(f"\n{Colors.WARNING}{'═' * 70}{Colors.RESET}")
            print(f"{Colors.WARNING}║{' ' * 68}║{Colors.RESET}")
            print_warning(f"{len(not_found_products)} ürün bulunamadı!")
            print(f"{Colors.WARNING}║{' ' * 68}║{Colors.RESET}")
            print(f"{Colors.WARNING}{'═' * 70}{Colors.RESET}")
            
            while True:
                edit_choice = input(f"{Colors.INFO}Manuel düzenleme yapmak ister misiniz? (e/h): {Colors.RESET}").strip().lower()
                
                if edit_choice == 'e':
                    edited, remaining = manual_edit_mode(not_found_products, brand_name)
                    found_products.extend(edited)
                    not_found_products = remaining
                    break
                elif edit_choice == 'h':
                    print_info("Manuel düzenleme atlandı.")
                    break
                else:
                    print_error("Geçersiz seçim! Lütfen 'e' (evet) veya 'h' (hayır) girin.")
        
        # Sonuçları kaydet
        total = len(found_products) + len(not_found_products)
        if total > 0:
            print(f"\n{Colors.INFO}{'═' * 70}{Colors.RESET}")
            print_loading("Sonuçlar kaydediliyor")
            print(f"{Colors.INFO}{'═' * 70}{Colors.RESET}\n")
            
            # TXT'ye kaydet
            txt_success = save_to_txt(found_products, not_found_products, brand_name)
            
            # Excel'e kaydet
            excel_success = save_to_excel(found_products, not_found_products, brand_name)
            
            # İstatistikleri güncelle
            stats.add_search(brand_name, len(found_products), len(not_found_products))
            
            print(f"\n{Colors.SUCCESS}{'═' * 70}{Colors.RESET}")
            print(f"{Colors.SUCCESS}║{' ' * 30}📊 ÖZET{' ' * 32}║{Colors.RESET}")
            print(f"{Colors.SUCCESS}{'═' * 70}{Colors.RESET}")
            print_success(f"Bulunan       : {len(found_products)} ürün")
            print_error(f"Bulunamayan   : {len(not_found_products)} ürün")
            print_info(f"Toplam        : {total} barkod")
            print(f"{Colors.SUCCESS}{'═' * 70}{Colors.RESET}\n")
        else:
            print_info("Hiç ürün aranmadı.")
        
        input(f"\n{Colors.SUCCESS}Ana menüye dönmek için Enter'a basın...{Colors.RESET}")
        return True
        
    except ImportError as e:
        handle_error(e, f"Scraper modülü: {module_name}")
        input(f"\n{Colors.INFO}Devam etmek için Enter'a basın...{Colors.RESET}")
        return False
    except Exception as e:
        handle_error(e, "Scraper çalıştırma")
        input(f"\n{Colors.INFO}Devam etmek için Enter'a basın...{Colors.RESET}")
        return False


def open_excel_file():
    """Bugünkü Excel dosyasını açar"""
    today = datetime.now().strftime("%Y-%m-%d")
    excel_file = os.path.join("outputs", "excel", f"tum_urunler_{today}.xlsx")
    
    if not os.path.exists(excel_file):
        print_error(f"Bugünkü Excel dosyası bulunamadı: {excel_file}")
        input(f"\n{Colors.INFO}Devam etmek için Enter'a basın...{Colors.RESET}")
        return
    
    try:
        os.startfile(excel_file)
        print_success(f"Excel dosyası açılıyor: {excel_file}")
    except Exception as e:
        handle_error(e, "Excel dosyası açma")
    
    input(f"\n{Colors.INFO}Devam etmek için Enter'a basın...{Colors.RESET}")


def open_outputs_folder():
    """Outputs klasörünü açar"""
    outputs_dir = "outputs"
    
    if not os.path.exists(outputs_dir):
        print_error("Outputs klasörü bulunamadı!")
        input(f"\n{Colors.INFO}Devam etmek için Enter'a basın...{Colors.RESET}")
        return
    
    try:
        os.startfile(outputs_dir)
        print_success(f"Klasör açılıyor: {outputs_dir}")
    except Exception as e:
        handle_error(e, "Klasör açma")
    
    input(f"\n{Colors.INFO}Devam etmek için Enter'a basın...{Colors.RESET}")


def main():
    """Ana program döngüsü"""
    # Şifre kontrolü
    if not verify_password():
        show_login_failed_screen()
        input(f"{Colors.ERROR}Çıkmak için Enter'a basın...{Colors.RESET}")
        sys.exit(1)
    
    # Başlangıç kontrolü
    ensure_directories()
    
    # İstatistik objesi oluştur
    stats = Statistics()
    
    while True:
        # Ana menüyü göster
        show_main_menu(stats)
        
        # Kullanıcı seçimi
        try:
            choice = input(f"{Colors.HIGHLIGHT}Seçiminiz (1-8): {Colors.RESET}").strip()
        except (EOFError, RuntimeError):
            print_error("Input hatası! Program sonlandırılıyor...")
            sys.exit(1)
        
        if choice in ['1', '2', '3', '4', '5']:
            # Marka scraper'ını çalıştır
            run_brand_scraper(choice, stats)
        
        elif choice == '6':
            # Excel'i aç
            open_excel_file()
        
        elif choice == '7':
            # Outputs klasörünü aç
            open_outputs_folder()
        
        elif choice == '8':
            # Çıkış
            print(f"\n{Colors.SUCCESS}👋 Programdan çıkılıyor...{Colors.RESET}")
            print(f"{Colors.INFO}Teşekkürler!{Colors.RESET}\n")
            sys.exit(0)
        
        else:
            print_error("Geçersiz seçim! Lütfen 1-8 arasında bir sayı girin.")
            input(f"\n{Colors.INFO}Devam etmek için Enter'a basın...{Colors.RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}⚠️  Program kullanıcı tarafından durduruldu!{Colors.RESET}")
        print(f"{Colors.SUCCESS}👋 Güle güle!{Colors.RESET}\n")
        sys.exit(0)
    except Exception as e:
        handle_error(e, "Kritik hata")
        input(f"\n{Colors.ERROR}Programı kapatmak için Enter'a basın...{Colors.RESET}")
        sys.exit(1)

