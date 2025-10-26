"""
Ortak yardımcı fonksiyonlar ve renklendirme sistemi
"""
import os
import json
from datetime import datetime
from colorama import init, Fore, Style, Back

# Colorama'yı başlat
init(autoreset=True)


class Colors:
    """Renk sınıfı - tüm renkli çıktılar için"""
    
    # Başarı mesajları
    SUCCESS = Fore.GREEN
    SUCCESS_BG = Back.GREEN + Fore.BLACK
    
    # Hata mesajları  
    ERROR = Fore.RED
    ERROR_BG = Back.RED + Fore.WHITE
    
    # Uyarı mesajları
    WARNING = Fore.YELLOW
    WARNING_BG = Back.YELLOW + Fore.BLACK
    
    # Bilgi mesajları
    INFO = Fore.CYAN
    INFO_BG = Back.CYAN + Fore.BLACK
    
    # Vurgu
    HIGHLIGHT = Fore.MAGENTA
    BOLD = Style.BRIGHT
    
    # Sıfırlama
    RESET = Style.RESET_ALL
    
    # Marka renkleri
    BERSHKA = Fore.MAGENTA
    HM = Fore.BLUE
    ZARA = Fore.RED
    MANGO = Fore.YELLOW
    MAVI = Fore.GREEN


def print_success(message):
    """Başarı mesajı yazdırır"""
    print(f"{Colors.SUCCESS}✅ {message}{Colors.RESET}")


def print_error(message):
    """Hata mesajı yazdırır"""
    print(f"{Colors.ERROR}❌ {message}{Colors.RESET}")


def print_warning(message):
    """Uyarı mesajı yazdırır"""
    print(f"{Colors.WARNING}⚠️  {message}{Colors.RESET}")


def print_info(message):
    """Bilgi mesajı yazdırır"""
    print(f"{Colors.INFO}ℹ️  {message}{Colors.RESET}")


def print_highlight(message):
    """Vurgulu mesaj yazdırır"""
    print(f"{Colors.HIGHLIGHT}{Colors.BOLD}{message}{Colors.RESET}")


def get_brand_color(brand_name):
    """Marka adına göre renk döndürür"""
    brand_colors = {
        'BERSHKA': Colors.BERSHKA,
        'H&M': Colors.HM,
        'ZARA': Colors.ZARA,
        'MANGO': Colors.MANGO,
        'MAVİ': Colors.MAVI
    }
    return brand_colors.get(brand_name.upper(), Colors.INFO)


def print_brand_header(brand_name):
    """Marka başlığını renkli yazdırır"""
    color = get_brand_color(brand_name)
    print(f"\n{color}{'═' * 65}{Colors.RESET}")
    print(f"{color}╔{' ' * 63}╗{Colors.RESET}")
    print(f"{color}║{' ' * 15}🛍️  {brand_name} BARKOD ARAMA SİSTEMİ{' ' * 15}║{Colors.RESET}")
    print(f"{color}║{' ' * 63}║{Colors.RESET}")
    print(f"{color}╚{'═' * 63}╝{Colors.RESET}")
    print(f"{color}{'═' * 65}{Colors.RESET}")


class Statistics:
    """İstatistik yönetimi"""
    
    def __init__(self):
        self.stats_file = os.path.join("outputs", "statistics.json")
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.stats = self.load_stats()
    
    def load_stats(self):
        """İstatistikleri yükle"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # Varsayılan istatistikler
        return {
            "daily": {},
            "total": {
                "searches": 0,
                "found": 0,
                "not_found": 0,
                "brands": {}
            },
            "last_search": None
        }
    
    def save_stats(self):
        """İstatistikleri kaydet"""
        try:
            os.makedirs(os.path.dirname(self.stats_file), exist_ok=True)
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print_warning(f"İstatistik kaydedilemedi: {e}")
    
    def add_search(self, brand_name, found_count, not_found_count):
        """Arama sonucunu ekle"""
        # Günlük istatistikler
        if self.today not in self.stats["daily"]:
            self.stats["daily"][self.today] = {
                "searches": 0,
                "found": 0,
                "not_found": 0,
                "brands": {}
            }
        
        # Günlük güncelle
        self.stats["daily"][self.today]["searches"] += 1
        self.stats["daily"][self.today]["found"] += found_count
        self.stats["daily"][self.today]["not_found"] += not_found_count
        
        if brand_name not in self.stats["daily"][self.today]["brands"]:
            self.stats["daily"][self.today]["brands"][brand_name] = 0
        self.stats["daily"][self.today]["brands"][brand_name] += 1
        
        # Toplam güncelle
        self.stats["total"]["searches"] += 1
        self.stats["total"]["found"] += found_count
        self.stats["total"]["not_found"] += not_found_count
        
        if brand_name not in self.stats["total"]["brands"]:
            self.stats["total"]["brands"][brand_name] = 0
        self.stats["total"]["brands"][brand_name] += 1
        
        # Son arama
        self.stats["last_search"] = {
            "brand": brand_name,
            "time": datetime.now().strftime("%H:%M"),
            "found": found_count,
            "not_found": not_found_count
        }
        
        self.save_stats()
    
    def get_today_stats(self):
        """Bugünkü istatistikleri getir"""
        if self.today not in self.stats["daily"]:
            return {
                "searches": 0,
                "found": 0,
                "not_found": 0,
                "brands": {}
            }
        return self.stats["daily"][self.today]
    
    def get_most_searched_brand_today(self):
        """Bugün en çok aranan marka"""
        today_stats = self.get_today_stats()
        if not today_stats["brands"]:
            return None
        
        return max(today_stats["brands"].items(), key=lambda x: x[1])
    
    def print_daily_summary(self):
        """Günlük özeti yazdır"""
        today_stats = self.get_today_stats()
        total_searches = today_stats["searches"]
        found = today_stats["found"]
        not_found = today_stats["not_found"]
        
        if total_searches == 0:
            print_info("Bugün henüz arama yapılmamış.")
            return
        
        success_rate = (found / (found + not_found) * 100) if (found + not_found) > 0 else 0
        most_brand = self.get_most_searched_brand_today()
        
        print(f"\n{Colors.INFO}┌{'─' * 68}┐{Colors.RESET}")
        print(f"{Colors.INFO}│{' ' * 25}📊 BUGÜNKÜ ÖZET{' ' * 30}│{Colors.RESET}")
        print(f"{Colors.INFO}├{'─' * 68}┤{Colors.RESET}")
        print(f"{Colors.INFO}│  • Toplam Arama    : {Colors.BOLD}{total_searches}{Colors.RESET} barkod{' ' * (39 - len(str(total_searches)))}│{Colors.RESET}")
        print(f"{Colors.INFO}│  • Bulunan         : {Colors.SUCCESS}{found}{Colors.RESET} ürün ({success_rate:.1f}%){' ' * (32 - len(str(found)) - len(f'{success_rate:.1f}'))}│{Colors.RESET}")
        print(f"{Colors.INFO}│  • Bulunamayan     : {Colors.ERROR}{not_found}{Colors.RESET} ürün ({100-success_rate:.1f}%){' ' * (32 - len(str(not_found)) - len(f'{100-success_rate:.1f}'))}│{Colors.RESET}")
        
        if most_brand:
            brand_name, count = most_brand
            color = get_brand_color(brand_name)
            brand_text = f"{brand_name} ({count} barkod)"
            spaces = 45 - len(brand_text)
            print(f"{Colors.INFO}│  • En Çok Aranan   : {color}{brand_text}{Colors.INFO}{' ' * spaces}│{Colors.RESET}")
        
        if self.stats["last_search"]:
            last = self.stats["last_search"]
            color = get_brand_color(last["brand"])
            last_text = f"{last['time']} ({last['brand']})"
            spaces = 48 - len(last_text)
            print(f"{Colors.INFO}│  • Son Arama       : {last_text}{' ' * spaces}│{Colors.RESET}")
        
        print(f"{Colors.INFO}└{'─' * 68}┘{Colors.RESET}")


def handle_error(error, context=""):
    """Hata yönetimi - detaylı hata mesajları"""
    error_type = type(error).__name__
    
    if "ConnectionError" in error_type or "ConnectTimeout" in error_type:
        print_error("İnternet bağlantısı yok!")
        print_info("Lütfen internet bağlantınızı kontrol edin ve tekrar deneyin.")
        
    elif "WebDriverException" in error_type or "ChromeDriver" in str(error):
        print_error("Chrome tarayıcı hatası!")
        print_info("chromedriver.exe dosyasını kontrol edin.")
        print_info("Chrome tarayıcının güncel olduğundan emin olun.")
        
    elif "TimeoutException" in error_type or "Timeout" in str(error):
        print_warning("Zaman aşımı!")
        print_info("İnternet bağlantınız yavaş olabilir. Lütfen tekrar deneyin.")
        
    elif "FileNotFoundError" in error_type:
        print_error("Dosya bulunamadı!")
        print_info(f"Eksik dosya: {str(error)}")
        
    elif "PermissionError" in error_type:
        print_error("Dosya erişim hatası!")
        print_info("Excel dosyası açık olabilir. Lütfen kapatıp tekrar deneyin.")
        
    else:
        print_error(f"Beklenmeyen hata: {error_type}")
        print_info(f"Detay: {str(error)}")
    
    if context:
        print_info(f"Konum: {context}")


def clear_screen():
    """Ekranı temizle"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_loading(message="Yükleniyor", dots=3):
    """Yükleme animasyonu"""
    import time
    for i in range(dots):
        print(f"\r{Colors.INFO}{message}{'.' * (i + 1)}{' ' * (dots - i - 1)}{Colors.RESET}", end='', flush=True)
        time.sleep(0.5)
    print()
