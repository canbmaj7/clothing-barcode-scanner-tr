"""
Mavi Barkod Scraper
"""
from curl_cffi import requests
from bs4 import BeautifulSoup


def detect_input_type(user_input):
    """Kullanıcı girişinin barkod mu yoksa ürün kodu mu olduğunu algılar"""
    cleaned_input = user_input.strip().replace(" ", "").replace("-", "")
    
    if not cleaned_input.isdigit():
        return None, "Hata: Sadece rakam girilmelidir!"
    
    length = len(cleaned_input)
    
    if cleaned_input.startswith('8') and length == 13:
        return 'barcode', cleaned_input
    elif length == 10:
        return 'product_code', cleaned_input
    elif length >= 11:
        formatted = f"{cleaned_input[:-5]}-{cleaned_input[-5:]}"
        return 'product_code', formatted
    else:
        return None, f"Hata: Geçersiz uzunluk ({length} hane). En az 10 haneli olmalıdır!"


def get_product_name(search_value):
    """Mavi sitesinden barkod veya ürün kodu ile ürün adını çeker"""
    url = f"https://www.mavi.com/search/?text={search_value}"
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }
    
    try:
        response = requests.get(
            url, 
            headers=headers, 
            impersonate="chrome",
            timeout=15
        )
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            product_link = soup.find('a', class_='product-card-info')
            
            if product_link and product_link.get('title'):
                product_name = product_link.get('title')
                return product_name
            else:
                return None
        else:
            return None
            
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None


def run_mavi():
    """
    Mavi scraper'ı çalıştırır
    
    Returns:
        tuple: (found_products, not_found_products)
    """
    found_products = []
    not_found_products = []
    
    print("\n" + "═" * 70)
    print("║                                                                    ║")
    print("║                🛍️  MAVİ BARKOD ARAMA SİSTEMİ                     ║")
    print("║                                                                    ║")
    print("═" * 70)
    print()
    
    print(f"┌{'─' * 68}┐")
    print(f"│{' ' * 23}📋 BARKOD FORMATLARI{' ' * 26}│")
    print(f"├{'─' * 68}┤")
    print(f"│  • Barkod      →  8682067592678 (8 ile başlayan 13 haneli){' ' * 5}│")
    print(f"│  • Ürün Kodu   →  1234567890 (10 haneli, tire yok){' ' * 14}│")
    print(f"│  • Ürün Kodu   →  06580929743 → 065809-29743{' ' * 20}│")
    print(f"└{'─' * 68}┘\n")
    
    print(f"┌{'─' * 68}┐")
    print(f"│{' ' * 27}⌨️  KOMUTLAR{' ' * 29}│")
    print(f"├{'─' * 68}┤")
    print(f"│  q  →  Ana menüye dön ve sonuçları kaydet{' ' * 24}│")
    print(f"│  s  →  Bulunamayan ürünü atla (düzenleme modunda){' ' * 15}│")
    print(f"└{'─' * 68}┘\n")
    
    print("⚡ Sistem hazır! Barkod girmeye başlayabilirsiniz...")
    print("─" * 70)
    print()
    
    while True:
        user_input = input("Barkod/Ürün kodu giriniz: ").strip()
        
        if user_input.lower() == 'q':
            break
        
        if not user_input:
            print("Lütfen bir değer giriniz!\n")
            continue
        
        input_type, formatted_value = detect_input_type(user_input)
        
        if input_type is None:
            print(f"\n❌ {formatted_value}\n")
            continue
        
        print(f"\n📋 Kod/Barkod: {formatted_value}")
        print("🔍 Ürün bilgisi sorgulanıyor...")
        
        product_name = get_product_name(formatted_value)
        
        if product_name:
            result_line = f"{formatted_value} MAVİ {product_name}"
            found_products.append(result_line)
            print(f"✅ {result_line}")
        else:
            result_line = f"{formatted_value} MAVİ Ürün Bulunamadı"
            not_found_products.append(result_line)
            print(f"❌ {result_line}")
        
        print("✅ Tamamlandı!\n")
    
    return found_products, not_found_products

