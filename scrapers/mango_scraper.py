"""
Mango Barkod Scraper
"""
import re
import requests
from bs4 import BeautifulSoup


def extract_barcode_from_qr(qr_string):
    """QR kod string'inden 8 haneli barkod numarasını çıkarır"""
    match = re.search(r'\b(\d{8})\b', qr_string)
    if match:
        return match.group(1)
    
    parts = qr_string.split('.')
    for part in parts:
        if len(part) == 8 and part.isdigit():
            return part
    return None


def detect_input_type(user_input):
    """Kullanıcı girişinin barkod mu yoksa QR kod mu olduğunu algılar"""
    cleaned_input = user_input.strip()
    
    if cleaned_input.isdigit() and len(cleaned_input) == 8:
        return cleaned_input, None
    
    if "mango" in cleaned_input.lower() or "https" in cleaned_input.lower():
        barcode = extract_barcode_from_qr(cleaned_input)
        if barcode:
            return barcode, None
        else:
            return None, "Hata: QR koddan barkod çıkarılamadı!"
    
    barcode = extract_barcode_from_qr(cleaned_input)
    if barcode:
        return barcode, None
    
    return None, "Hata: Geçerli bir barkod veya QR kod giriniz! (8 haneli barkod)"


def extract_product_name_from_product_page(soup):
    """
    Ürün sayfasından ürün adını çıkarır
    
    Args:
        soup: BeautifulSoup objesi
        
    Returns:
        str or None: Ürün adı
    """
    # Strateji 1: h1 tag (Ana başlık)
    h1_title = soup.find('h1')
    if h1_title:
        title = h1_title.get_text().strip()
        if title and len(title) > 5:
            return title
    
    # Strateji 2: ProductDetail_title class
    product_title = soup.find('h1', class_=lambda x: x and 'ProductDetail_title' in x)
    if product_title:
        title = product_title.get_text().strip()
        if title and len(title) > 5:
            return title
    
    # Strateji 3: meta itemprop="name"
    meta_name = soup.find('meta', attrs={'itemprop': 'name'})
    if meta_name and meta_name.get('content'):
        title = meta_name.get('content').strip()
        if title and len(title) > 5:
            return title
    
    # Strateji 4: og:title meta tag
    og_title = soup.find('meta', property='og:title')
    if og_title and og_title.get('content'):
        title = og_title.get('content').strip()
        if title and len(title) > 5:
            return title
    
    return None


def search_other_categories(barcode, headers):
    """
    Diğer kategorilerde ürün arar
    
    Args:
        barcode (str): Barkod
        headers (dict): HTTP headers
        
    Returns:
        tuple: (product_name, error_message)
    """
    categories = ['erkek', 'teen', 'cocuk', 'home']
    
    for category in categories:
        try:
            url = f"https://shop.mango.com/tr/tr/search/{category}?q={barcode}"
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            
            if response.status_code == 200:
                final_url = response.url
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Ürün sayfasına yönlendirildi mi?
                if '/p/' in final_url:
                    product_name = extract_product_name_from_product_page(soup)
                    if product_name:
                        return product_name, None
                
                # Arama sonuçlarından ürün adını çıkar
                page_text = soup.get_text()
                if 'Sonuç bulunamadı' not in page_text:
                    product_title = soup.find('p', class_=lambda x: x and 'ProductTitle_productTitle' in x)
                    if product_title:
                        product_name = product_title.get_text().strip()
                        if product_name and len(product_name) > 5:
                            return product_name, None
        except:
            continue
    
    return None, "Ürün hiçbir kategoride bulunamadı"


def get_mango_product_name(barcode):
    """
    Mango sitesinden barkod numarasına göre ürün adını çeker
    Direkt ürün sayfası URL'lerini dener
    
    Args:
        barcode (str): Ürün barkod numarası (8 haneli)
        
    Returns:
        tuple: (product_name, error_message)
               Başarılıysa: (ürün_adı, None)
               Başarısızsa: (None, hata_mesajı)
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    # Strateji 1: Direkt ürün sayfası URL'lerini dene
    product_urls = [
        f"https://shop.mango.com/tr/tr/p/kadin/{barcode}",
        f"https://shop.mango.com/tr/tr/p/erkek/{barcode}",
        f"https://shop.mango.com/tr/tr/p/teen/{barcode}",
        f"https://shop.mango.com/tr/tr/p/cocuk/{barcode}",
        f"https://shop.mango.com/tr/tr/p/home/{barcode}",
    ]
    
    for url in product_urls:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Ürün sayfasından ürün adını çıkar
                product_name = extract_product_name_from_product_page(soup)
                if product_name:
                    return product_name, None
                    
        except:
            continue
    
    # Strateji 2: Arama sayfasından başla (eski yöntem)
    search_url = f"https://shop.mango.com/tr/tr/search/kadin?q={barcode}"
    
    try:
        # Redirect'i takip et (allow_redirects=True)
        response = requests.get(search_url, headers=headers, timeout=10, allow_redirects=True)
        
        if response.status_code != 200:
            return None, f"HTTP Hatası: {response.status_code}"
        
        # Final URL'i kontrol et - ürün sayfasına yönlendirildi mi?
        final_url = response.url
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Eğer ürün sayfasına yönlendirildiyse (/p/ içeriyorsa)
        if '/p/' in final_url:
            # Ürün sayfasından ürün adını çıkar
            product_name = extract_product_name_from_product_page(soup)
            if product_name:
                return product_name, None
        
        # Arama sayfasındaysa, arama sonuçlarını kontrol et
        page_text = soup.get_text()
        if 'Sonuç bulunamadı' in page_text:
            # Strateji 3: Diğer kategorilerde ara
            return search_other_categories(barcode, headers)
        
        # ProductTitle class'ını ara (Ana strateji)
        product_title = soup.find('p', class_=lambda x: x and 'ProductTitle_productTitle' in x)
        if product_title:
            product_name = product_title.get_text().strip()
            if product_name and len(product_name) > 5:
                return product_name, None
        
        # Alternatif: meta tag'leri kontrol et
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            content = og_title.get('content')
            if content and 'Sonuç bulunamadı' not in content and len(content) > 5:
                return content, None
        
        return None, "Ürün adı bulunamadı"
        
    except requests.exceptions.Timeout:
        return None, "İstek zaman aşımına uğradı"
    except requests.exceptions.RequestException as e:
        return None, f"Bağlantı hatası: {e}"
    except Exception as e:
        return None, f"Beklenmeyen hata: {e}"


def run_mango():
    """
    Mango scraper'ı çalıştırır
    
    Returns:
        tuple: (found_products, not_found_products)
    """
    found_products = []
    not_found_products = []
    
    print("\n" + "═" * 70)
    print("║                                                                    ║")
    print("║                🛍️  MANGO BARKOD ARAMA SİSTEMİ                    ║")
    print("║                                                                    ║")
    print("═" * 70)
    print()
    
    print(f"┌{'─' * 68}┐")
    print(f"│{' ' * 23}📋 BARKOD FORMATLARI{' ' * 26}│")
    print(f"├{'─' * 68}┤")
    print(f"│  • Barkod  →  17034103 (8 haneli){' ' * 32}│")
    print(f"│  • QR Kod  →  Otomatik olarak barkod çıkarılır{' ' * 19}│")
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
        user_input = input("Barkod/QR kod giriniz: ").strip()
        
        if user_input.lower() == 'q':
            break
        
        if not user_input:
            print("Lütfen bir değer giriniz!\n")
            continue
        
        barcode, error = detect_input_type(user_input)
        
        if barcode is None:
            print(f"\n❌ {error}\n")
            continue
        
        print(f"\n📋 Barkod: {barcode}")
        print("🔍 Ürün bilgisi sorgulanıyor...")
        
        product_name, error = get_mango_product_name(barcode)
        
        if product_name:
            formatted_product_name = product_name.title()
            result_line = f"{barcode} MANGO {formatted_product_name}"
            found_products.append(result_line)
            print(f"✅ {result_line}")
        else:
            result_line = f"{barcode} MANGO Ürün Bulunamadı"
            not_found_products.append(result_line)
            print(f"❌ {result_line}")
        
        print("✅ Tamamlandı!\n")
    
    return found_products, not_found_products

