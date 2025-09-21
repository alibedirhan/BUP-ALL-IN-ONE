# build/icon_converter.py
"""
PNG dosyasını ICO formatına çevirir.
Eğer orijinal ikon bulunamazsa basit bir placeholder ikon üretir.
"""

import os
from PIL import Image, ImageDraw

def main():
    png_path = os.path.join("icon", "bupilic_logo.png")
    ico_path = os.path.join("build", "app_icon.ico")
    os.makedirs("build", exist_ok=True)

    try:
        img = Image.open(png_path)
        if img.mode != "RGBA":
            img = img.convert("RGBA")

        sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
        img.save(ico_path, format="ICO", sizes=sizes)
        print(f"✅ ICON created: {ico_path}")
    except Exception as e:
        print(f"⚠️ ICON convert failed: {e}")
        print("Creating placeholder icon instead...")

        # placeholder ikon
        img = Image.new("RGBA", (64, 64), (42, 157, 143, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, 63, 63), fill=(42, 157, 143, 255))
        img.save(ico_path, format="ICO")
        print(f"✅ Placeholder icon created: {ico_path}")

if __name__ == "__main__":
    main()

