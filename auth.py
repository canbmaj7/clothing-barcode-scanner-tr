"""
Şifre Doğrulama Sistemi
Google Sheets'ten şifre okur ve doğrular
"""
import requests
import csv
from io import StringIO
from utils import Colors, print_success, print_error, print_warning, print_info
import sys
import getpass


# Google Sheets CSV Export URL
SHEET_ID = "1Eqq70Wb0DU9uZBQJe_MGLCq40jbDrodxDi467KUYkYY"
SHEET_GID = "0"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={SHEET_GID}"


def get_password_from_sheet():
    """
    Google Sheets'ten B4 hücresindeki şifreyi okur
    
    Returns:
        str or None: Şifre veya None (hata durumunda)
    """
    try:
        response = requests.get(CSV_URL, timeout=10)
        
        if response.status_code != 200:
            print_error(f"Google Sheets'e bağlanılamadı! HTTP {response.status_code}")
            return None
        
        # CSV'yi parse et
        csv_data = StringIO(response.text)
        reader = csv.reader(csv_data)
        
        # Satırları oku
        rows = list(reader)
        
        # B4 hücresi = rows[3][1] (0-indexed: satır 3, sütun 1)
        if len(rows) >= 4 and len(rows[3]) >= 2:
            password = rows[3][1].strip()
            return password
        else:
            print_error("B4 hücresi bulunamadı!")
            return None
            
    except requests.exceptions.ConnectionError:
        print_error("İnternet bağlantısı yok!")
        print_info("Şifre doğrulaması için internet gereklidir.")
        return None
    except requests.exceptions.Timeout:
        print_warning("Google Sheets zaman aşımı!")
        return None
    except Exception as e:
        print_error(f"Şifre okuma hatası: {e}")
        return None


def verify_password():
    """
    Kullanıcıdan şifre alır ve doğrular (3 deneme hakkı)
    
    Returns:
        bool: Şifre doğruysa True, yanlışsa False
    """
    # Ekranı temizle
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Büyük giriş ekranı
    print(f"\n{Colors.HIGHLIGHT}")
    print("═" * 70)
    print("║                                                                    ║")
    print("║                                                                    ║")
    print("║                 🔐  GİYİM BARKOD ARAMA SİSTEMİ                    ║")
    print("║                                                                    ║")
    print("║                          v1.0.0                                    ║")
    print("║                                                                    ║")
    print("║                    🛡️  GÜVENLİ GİRİŞ                             ║")
    print("║                                                                    ║")
    print("║                                                                    ║")
    print("═" * 70)
    print(f"{Colors.RESET}\n")
    
    # Google Sheets'ten şifreyi oku
    print(f"{Colors.INFO}┌{'─' * 68}┐{Colors.RESET}")
    print(f"{Colors.INFO}│  🔍 Şifre doğrulaması yapılıyor...{' ' * 33}│{Colors.RESET}")
    print(f"{Colors.INFO}└{'─' * 68}┘{Colors.RESET}\n")
    
    correct_password = get_password_from_sheet()
    
    if correct_password is None:
        print_error("Şifre sistemi çalışmıyor! Program kapatılıyor...")
        print_info("Lütfen internet bağlantınızı kontrol edin.")
        return False
    
    print_success("✓ Şifre sistemi hazır!")
    print(f"\n{Colors.INFO}{'─' * 70}{Colors.RESET}\n")
    
    # 3 deneme hakkı
    max_attempts = 3
    
    for attempt in range(1, max_attempts + 1):
        print(f"{Colors.WARNING}Deneme {attempt}/{max_attempts}{Colors.RESET}")
        
        try:
            # getpass kullan - şifre gizli olacak (Linux/Unix gibi)
            try:
                user_password = getpass.getpass(f"{Colors.HIGHLIGHT}Şifre: {Colors.RESET}").strip()
            except Exception:
                # getpass çalışmazsa (bazı IDE'lerde), normal input kullan
                print_warning("(Şifre gizleme devre dışı - terminal limitasyonu)")
                user_password = input(f"{Colors.HIGHLIGHT}Şifre: {Colors.RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print_warning("\nGiriş iptal edildi!")
            return False
        
        if user_password == correct_password:
            print(f"\n{Colors.SUCCESS}{'═' * 70}{Colors.RESET}")
            print(f"{Colors.SUCCESS}║{' ' * 68}║{Colors.RESET}")
            print_success("         🎉 Şifre doğru! Programa hoş geldiniz!")
            print(f"{Colors.SUCCESS}║{' ' * 68}║{Colors.RESET}")
            print(f"{Colors.SUCCESS}{'═' * 70}{Colors.RESET}\n")
            return True
        else:
            remaining = max_attempts - attempt
            if remaining > 0:
                print_error(f"❌ Yanlış şifre! Kalan deneme hakkı: {remaining}\n")
            else:
                print_error("❌ Yanlış şifre!")
    
    # 3 deneme tükendi
    print(f"\n{Colors.ERROR}{'═' * 70}{Colors.RESET}")
    print(f"{Colors.ERROR}║{' ' * 68}║{Colors.RESET}")
    print_error("           🚫 Deneme hakkınız tükendi!")
    print_info("     Program güvenlik nedeniyle kapatılıyor...")
    print(f"{Colors.ERROR}║{' ' * 68}║{Colors.RESET}")
    print(f"{Colors.ERROR}{'═' * 70}{Colors.RESET}\n")
    
    return False


def show_login_failed_screen():
    """Giriş başarısız ekranını gösterir"""
    print(f"\n{Colors.ERROR}")
    print("═" * 70)
    print("║                                                                    ║")
    print("║                        ⛔ ERİŞİM ENGELLENDİ                        ║")
    print("║                                                                    ║")
    print("║          Doğru şifreyi girmek için yetkiliye başvurun             ║")
    print("║                                                                    ║")
    print("═" * 70)
    print(f"{Colors.RESET}\n")

