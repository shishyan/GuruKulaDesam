# -*- coding: utf-8 -*-
"""
tools/generate_pazhaimai_thumbnails.py

Generates modern 16:9 thumbnails (1920x1080) for the 2 new Pazhaimai tracks.
Aesthetic: Regal Antique Maroon / Dark Bronze with Tamil Classical typography and golden glow.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

os.makedirs("production/thumbnails", exist_ok=True)

W, H = 1920, 1080

def create_base_canvas():
    # Gradient: Antique Maroon (#2C001E) -> Deep Wine (#5B1426) -> Dark Bronze
    img = Image.new("RGBA", (W, H), (44, 0, 30, 255))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        r = int(44 + (91 - 44) * ratio)
        g = int(0 + (20 - 0) * ratio)
        b = int(30 + (38 - 30) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))
        
    # Divine radial halo in center
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    halo_draw = ImageDraw.Draw(halo)
    cx, cy = W // 2, H // 2
    for rad in range(600, 50, -25):
        alpha = int(45 * (1.0 - rad / 600))
        halo_draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(255, 215, 0, alpha))
    
    halo = halo.filter(ImageFilter.GaussianBlur(40))
    return Image.alpha_composite(img, halo)

def render_thumbnail(out_path, title_tamil, title_eng, badge_text):
    base = create_base_canvas()
    draw = ImageDraw.Draw(base)
    
    # Fonts
    font_tamil = ImageFont.truetype("C:/Windows/Fonts/NirmalaB.ttf", 92)
    font_tamil_sub = ImageFont.truetype("C:/Windows/Fonts/NirmalaB.ttf", 64)
    font_eng = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 46)
    font_badge = ImageFont.truetype("C:/Windows/Fonts/NirmalaB.ttf", 36)
    font_brand = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 32)
    
    # 1. Top Category Pill / Badge
    badge_w, badge_h = 420, 65
    bx, by = 100, 90
    draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=15, fill=(212, 175, 55, 240))
    draw.text((bx + 25, by + 8), badge_text, font=font_badge, fill=(20, 5, 10, 255))
    
    # 2. Main Title: அதிகாரம் 81
    draw.text((100, 320), "அதிகாரம் 81", font=font_tamil_sub, fill=(255, 215, 0, 255))
    
    # 3. Huge Primary Tamil Text: பழைமை
    # Soft shadow
    draw.text((104, 424), title_tamil, font=font_tamil, fill=(0, 0, 0, 200))
    draw.text((100, 420), title_tamil, font=font_tamil, fill=(255, 255, 255, 255))
    
    # 4. Secondary English Text
    draw.text((100, 570), title_eng, font=font_eng, fill=(230, 210, 180, 255))
    
    # 5. Aesthetic Decorative Accent Line
    draw.line([(100, 670), (750, 670)], fill=(212, 175, 55, 255), width=5)
    
    # 6. Bottom Brand Watermark
    draw.text((100, 950), "GURU KULA DESAM | 4K CINEMATIC RELEASE", font=font_brand, fill=(200, 180, 160, 220))
    
    base.convert("RGB").save(out_path, "PNG", quality=95)
    print(f"Generated Modern 16:9 Thumbnail -> {out_path}")

render_thumbnail(
    "production/thumbnails/pazhaimai_1F_golden_2026.png",
    "பழைமை — PAZHAIMAI",
    "Thirukkural: Ancient & Timeless Friendship [Film 2026]",
    "திருக்குறள் | 4K FILM"
)

render_thumbnail(
    "production/thumbnails/pazhaimai_1H_golden_pop.png",
    "பழைமை — PAZHAIMAI",
    "Thirukkural: Golden Pop & Classical Symphony",
    "திருக்குறள் | POP FILM"
)
