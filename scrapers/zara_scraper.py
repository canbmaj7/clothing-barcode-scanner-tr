"""
Zara Barkod Scraper
"""
import requests
import uuid


def validate_and_process_barcode(raw_barcode):
    """
    Barkodu kontrol eder ve işler
    
    Args:
        raw_barcode (str): Ham barkod (14 haneli olmalı)
    
    Returns:
        tuple: (işlenmiş_barkod, hata_mesajı) - Hata yoksa (barkod, None)
    """
    raw_barcode = raw_barcode.strip()
    
    if not raw_barcode.isdigit():
        return None, "Hata: Barkod sadece rakamlardan oluşmalıdır!"
    
    if len(raw_barcode) != 14:
        return None, f"Hata: Barkod 14 haneli olmalıdır! (Girilen: {len(raw_barcode)} hane)"
    
    processed_barcode = raw_barcode[1:-3]
    return processed_barcode, None


def get_product_name(barcode):
    """
    Zara API'sinden barkod numarasına göre ürün adını çeker
    
    Args:
        barcode (str): Ürün barkod numarası (örn: "4813858712")
    
    Returns:
        tuple: (ürün_adı, başarılı_mı) - Başarılıysa (ad, True), değilse (None, False)
    """
    base_url = "https://www.zara.com/itxrest/1/search/store/11766/reference"
    session_id = str(uuid.uuid4())
    
    params = {
        'reference': barcode,
        'locale': 'tr_TR',
        'session': session_id,
        'deviceType': 'mobile',
        'deviceOS': 'Windows',
        'deviceOSVersion': '10',
        'scope': 'mobileweb',
        'origin': 'search',
        'ajax': 'true'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.zara.com/tr/',
        'Origin': 'https://www.zara.com'
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'SUCCESS' and data.get('results'):
            product_name = data['results'][0]['content']['name']
            return product_name, True
        else:
            return None, False
            
    except Exception as e:
        print(f"⚠️ API hatası: {e}")
        return None, False


def run_zara():
    """
    Zara scraper'ı çalıştırır
    
    Returns:
        tuple: (found_products, not_found_products)
               Her biri ["barkod ZARA Ürün Adı", ...] formatında liste
    """
    found_products = []
    not_found_products = []
    
    print("\n" + "═" * 70)
    print("║                                                                    ║")
    print("║                🛍️  ZARA BARKOD ARAMA SİSTEMİ                     ║")
    print("║                                                                    ║")
    print("═" * 70)
    print()
    
    print(f"┌{'─' * 68}┐")
    print(f"│{' ' * 23}📋 BARKOD FORMATLARI{' ' * 26}│")
    print(f"├{'─' * 68}┤")
    print(f"│  • 14 hane  →  04813858712034 (Tam barkod){' ' * 24}│")
    print(f"│  • İşleme   →  Başındaki 0 ve son 3 hane çıkarılır{' ' * 15}│")
    print(f"└{'─' * 68}┘\n")
    
    print(f"┌{'─' * 68}┐")
    print(f"│{' ' * 27}⌨️  KOMUTLAR{' ' * 29}│")
    print(f"├{'─' * 68}┤")
    print(f"│  q  →  Ana menüye dön ve sonuçları kaydet{' ' * 24}│")
    print(f"│  s  →  Bulunamayan ürünü atla (düzenleme modunda){' ' * 15}│")
    print(f"└{'─' * 68}┘\n")
    
    print("⚡ API hazır! Barkod girmeye başlayabilirsiniz...")
    print("─" * 70)
    print()
    
    while True:
        raw_barcode = input("Barkod giriniz: ").strip()
        
        if raw_barcode.lower() == 'q':
            break
        
        if not raw_barcode:
            print("❌ Barkod boş olamaz!")
            continue
        
        print(f"📋 Ham Barkod: {raw_barcode}")
        
        processed_barcode, error = validate_and_process_barcode(raw_barcode)
        
        if error:
            print(f"❌ {error}")
            continue
        
        print(f"🔄 İşlenmiş Barkod: {processed_barcode}")
        print(f"   (Başındaki '0' ve son 3 hane çıkarıldı)")
        print("🔍 Ürün bilgisi sorgulanıyor...")
        
        product_name, success = get_product_name(processed_barcode)
        
        if success and product_name:
            formatted_product_name = product_name.title()
            result_line = f"{processed_barcode} ZARA {formatted_product_name}"
            found_products.append(result_line)
            print(f"✅ {result_line}")
        else:
            result_line = f"{processed_barcode} ZARA Ürün Bulunamadı"
            not_found_products.append(result_line)
            print(f"❌ {result_line}")
        
        print("✅ Tamamlandı!\n")
    
    return found_products, not_found_products

