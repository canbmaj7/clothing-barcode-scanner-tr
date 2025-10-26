"""
GİYİM BARKOD SİSTEMİ - İKON OLUŞTURUCU
Otomatik olarak app_icon.ico dosyası oluşturur
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Ana icon dosyasını oluşturur"""
    print("=" * 60)
    print("  GİYİM BARKOD - İKON OLUŞTURUCU")
    print("=" * 60)
    print()
    
    # Dosya adı
    output_file = "app_icon.ico"
    
    # Boyutlar (ICO formatı için birden fazla boyut gerekli)
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    for size in sizes:
        # Renkler: Pembe/Mor arka plan (#E91E63, #9C27B0)
        background_colors = [
            (233, 30, 99),   # Kırmızımsı pembe
            (156, 39, 176),  # Mor
            (186, 104, 200), # Açık mor
        ]
        
        # Gradient oluştur
        img = Image.new('RGB', (size, size), background_colors[0])
        draw = ImageDraw.Draw(img)
        
        # Gradient efekti ekle (basit yaklaşım)
        for y in range(size):
            # Gradient için renk karışımı
            ratio = y / size
            color = tuple(
                int(bg * (1 - ratio) + end * ratio)
                for bg, end in zip(background_colors[0], background_colors[1])
            )
            draw.rectangle([(0, y), (size, y + 1)], fill=color)
        
        # "GB" harflerini çiz
        try:
            # Sistem fontunu kullan
            if os.name == 'nt':  # Windows
                font_path = "arial.ttf"
            else:  # Linux/Mac
                font_path = "arial.ttf"
            
            # Font boyutunu hesapla
            font_size = int(size * 0.45)
            try:
                font = ImageFont.truetype(font_path, font_size)
            except:
                # Font bulunamazsa varsayılan font
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Metin rengi: Beyaz
        text_color = (255, 255, 255)
        
        # Metni ortala
        text = "GB"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2 - bbox[1]
        
        # Gölge efekti ekle
        shadow_offset = max(1, size // 50)
        draw.text((x + shadow_offset, y + shadow_offset), text, 
                 fill=(0, 0, 0, 128), font=font)
        
        # Ana metin
        draw.text((x, y), text, fill=text_color, font=font)
        
        # Kenar çizgisi ekle
        border_width = max(1, size // 40)
        draw.rectangle([(border_width, border_width), 
                       (size - border_width, size - border_width)], 
                      outline=text_color, width=border_width)
        
        images.append(img)
        print(f"✓ {size}x{size} boyutunda icon oluşturuldu")
    
    # ICO dosyası olarak kaydet
    img.save(output_file, format='ICO', sizes=[(s, s) for s in sizes])
    print()
    print("=" * 60)
    print(f"✓ BAŞARILI! Icon oluşturuldu: {output_file}")
    print("=" * 60)
    print()
    print("Kullanım:")
    print("1. create_icon.py'yi çalıştırın (bu script)")
    print("2. Oluşan app_icon.ico dosyasını kullanın")
    print("3. build_exe_fixed.bat ile EXE oluşturun")
    print()


def test_with_png():
    """Test için PNG olarak da kaydet"""
    output_file = "app_icon.png"
    
    img = Image.new('RGB', (256, 256), (233, 30, 99))
    draw = ImageDraw.Draw(img)
    
    # Gradient
    for y in range(256):
        ratio = y / 256
        color = tuple(
            int(bg * (1 - ratio) + end * ratio)
            for bg, end in zip((233, 30, 99), (156, 39, 176))
        )
        draw.rectangle([(0, y), (256, y + 1)], fill=color)
    
    # Font
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except:
        font = ImageFont.load_default()
    
    text = "GB"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (256 - text_width) // 2
    y = (256 - text_height) // 2 - bbox[1]
    
    # Gölge
    draw.text((x + 3, y + 3), text, fill=(0, 0, 0, 100), font=font)
    draw.text((x, y), text, fill=(255, 255, 255), font=font)
    
    # Kenar
    draw.rectangle([(5, 5), (251, 251)], outline=(255, 255, 255), width=5)
    
    img.save(output_file)
    print(f"✓ Test PNG oluşturuldu: {output_file}")


if __name__ == "__main__":
    try:
        create_icon()
        # test_with_png()  # İsteğe bağlı test
        print("\n✓ İşlem tamamlandı!")
        
    except ImportError:
        print()
        print("=" * 60)
        print("  ❌ HATA: Pillow kütüphanesi bulunamadı!")
        print("=" * 60)
        print()
        print("Çözüm:")
        print("  pip install pillow")
        print()
        print("Yüklendikten sonra tekrar çalıştırın:")
        print("  python create_icon.py")
        print()
    
    except Exception as e:
        print()
        print("=" * 60)
        print(f"  ❌ HATA: {str(e)}")
        print("=" * 60)
        print()
        import traceback
        traceback.print_exc()
