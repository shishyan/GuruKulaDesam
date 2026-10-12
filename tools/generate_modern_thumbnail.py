# -*- coding: utf-8 -*-
"""
Guru Kula Desam - Modern Thumbnail Generator
Batch generates stunning, high-impact 16:9 thumbnails (1920x1080) for YouTube devotional tracks.
Uses native Windows DirectWrite/Uniscribe shaping for flawless Tamil script typography.
"""

import os
import sys
import json
import math
import random
import re
import ctypes
from ctypes import wintypes, byref, c_void_p, Structure, sizeof
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Default directory paths
REPO_DIR = Path(r"c:\GitHub\Gurukuladesam")
OUTPUT_DIR = REPO_DIR / "production" / "thumbnails"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Font configurations
FONT_TAMIL_FAMILY = "Nirmala UI"
FONT_SANS_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_SANS_SEMI = r"C:\Windows\Fonts\seguisb.ttf"

# Color themes adhering strictly to divine traditions
THEMES = {
    'murugan': {
        'name': 'Murugan / Skanda',
        'bg_start': (139, 0, 0),        # #8B0000 Royal Vermilion
        'bg_mid': (45, 2, 8),          # Deep Ruby Night
        'bg_end': (15, 2, 5),          # Midnight
        'accent_bright': (255, 69, 0), # #FF4500 Fiery Saffron-Red
        'accent_gold': (255, 215, 0),   # #FFD700 Divine Gold
        'glow_color': (255, 110, 20, 180),
        'halo_color': (255, 190, 40, 110),
        'pill_bg': (75, 6, 12, 220),
        'pill_border': (255, 215, 0, 240),
        'pill_text': (255, 245, 210),
        'sub_color': (255, 235, 175),
    },
    'vinayagar': {
        'name': 'Vinayagar / Ganesha',
        'bg_start': (184, 69, 0),       # #B84500 Deep Saffron
        'bg_mid': (50, 14, 5),         # Deep Crimson Earth
        'bg_end': (155, 17, 30),       # #9B111E Crimson
        'accent_bright': (230, 126, 34),# #E67E22 Amber
        'accent_gold': (255, 215, 0),   # #FFD700
        'glow_color': (255, 140, 20, 180),
        'halo_color': (255, 190, 40, 110),
        'pill_bg': (95, 28, 6, 220),
        'pill_border': (255, 215, 0, 240),
        'pill_text': (255, 250, 220),
        'sub_color': (255, 240, 190),
    },
    'shiva': {
        'name': 'Shiva / Thiruvempavai',
        'bg_start': (11, 12, 16),       # #0B0C10 Cosmic Indigo
        'bg_mid': (31, 40, 51),        # #1F2833 Silver Charcoal
        'bg_end': (75, 0, 130),        # #4B0082 Deep Violet
        'accent_bright': (100, 181, 246),# Silver Blue Glow
        'accent_gold': (224, 235, 255), # Radiant Silver
        'glow_color': (100, 181, 246, 170),
        'halo_color': (140, 160, 255, 100),
        'pill_bg': (22, 28, 60, 220),
        'pill_border': (144, 202, 249, 240),
        'pill_text': (240, 248, 255),
        'sub_color': (220, 235, 255),
    },
    'perumal': {
        'name': 'Perumal / Thiruppavai / Vishnu',
        'bg_start': (10, 25, 47),       # #0A192F Deep Ocean Blue
        'bg_mid': (0, 77, 64),         # #004D40 Deep Sacred Emerald
        'bg_end': (5, 15, 30),         # Cosmic Abyss
        'accent_bright': (0, 229, 255), # Luminous Cyan
        'accent_gold': (212, 175, 55),  # #D4AF37 Peethambaram Gold
        'glow_color': (0, 200, 230, 160),
        'halo_color': (212, 175, 55, 110),
        'pill_bg': (0, 55, 65, 220),
        'pill_border': (212, 175, 55, 240),
        'pill_text': (255, 250, 225),
        'sub_color': (255, 242, 195),
    },
    'thirukkural': {
        'name': 'Thirukkural / Classical Tamil',
        'bg_start': (44, 0, 30),        # #2C001E Regal Antique Maroon
        'bg_mid': (91, 20, 38),        # #5B1426 Antique Sangria
        'bg_end': (18, 2, 12),         # Deep Obsidian
        'accent_bright': (225, 112, 85),# Warm Terracotta
        'accent_gold': (212, 175, 55),  # #D4AF37 Dark Bronze / Gold
        'glow_color': (255, 160, 60, 160),
        'halo_color': (212, 175, 55, 110),
        'pill_bg': (75, 14, 30, 220),
        'pill_border': (212, 175, 55, 240),
        'pill_text': (255, 245, 220),
        'sub_color': (255, 238, 195),
    },
    'amman': {
        'name': 'Amman / Devi',
        'bg_start': (74, 14, 23),       # #4A0E17 Sacred Kumkum
        'bg_mid': (128, 0, 32),        # #800020 Deep Magenta
        'bg_end': (25, 2, 8),          # Deep Night
        'accent_bright': (255, 64, 129),# Radiant Rose
        'accent_gold': (255, 193, 7),   # #FFC107 Gold
        'glow_color': (255, 64, 129, 160),
        'halo_color': (255, 193, 7, 110),
        'pill_bg': (100, 12, 38, 220),
        'pill_border': (255, 193, 7, 240),
        'pill_text': (255, 245, 230),
        'sub_color': (255, 235, 220),
    }
}


# Windows GDI Text Shaping Structures
class BITMAPINFOHEADER(Structure):
    _fields_ = [
        ('biSize', wintypes.DWORD), ('biWidth', wintypes.LONG), ('biHeight', wintypes.LONG),
        ('biPlanes', wintypes.WORD), ('biBitCount', wintypes.WORD), ('biCompression', wintypes.DWORD),
        ('biSizeImage', wintypes.DWORD), ('biXPelsPerMeter', wintypes.LONG), ('biYPelsPerMeter', wintypes.LONG),
        ('biClrUsed', wintypes.DWORD), ('biClrImportant', wintypes.DWORD)
    ]

class BITMAPINFO(Structure):
    _fields_ = [('bmiHeader', BITMAPINFOHEADER), ('bmiColors', wintypes.DWORD * 3)]


def render_shaped_text(text: str, font_name: str, font_size: int, text_color=(255, 255, 255), max_w=1850, max_h=300):
    """
    Renders complex Tamil script with 100% accurate ligatures and vowel placement 
    using Windows native DirectWrite / Uniscribe text shaping engine.
    """
    gdi32 = ctypes.windll.gdi32
    user32 = ctypes.windll.user32
    
    hdc_screen = user32.GetDC(0)
    hdc = gdi32.CreateCompatibleDC(hdc_screen)
    
    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = max_w
    bmi.bmiHeader.biHeight = -max_h
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    bmi.bmiHeader.biCompression = 0
    
    p_bits = c_void_p()
    hbitmap = gdi32.CreateDIBSection(hdc, byref(bmi), 0, byref(p_bits), None, 0)
    gdi32.SelectObject(hdc, hbitmap)
    
    # FW_BOLD = 700, CLEARTYPE_QUALITY = 5
    hfont = gdi32.CreateFontW(-font_size, 0, 0, 0, 700, 0, 0, 0, 1, 0, 0, 5, 0, font_name)
    gdi32.SelectObject(hdc, hfont)
    
    # Fill background with white
    rect = wintypes.RECT(0, 0, max_w, max_h)
    white_brush = gdi32.CreateSolidBrush(0xFFFFFF)
    user32.FillRect(hdc, byref(rect), white_brush)
    gdi32.DeleteObject(white_brush)
    
    gdi32.SetBkMode(hdc, 1) # TRANSPARENT
    gdi32.SetTextColor(hdc, 0x00000000) # Draw solid black text
    
    # Calculate exact bounding rect
    calc_rect = wintypes.RECT(0, 0, max_w, max_h)
    DT_CALCRECT = 0x00000400
    DT_SINGLELINE = 0x00000020
    user32.DrawTextW(hdc, text, -1, byref(calc_rect), DT_CALCRECT | DT_SINGLELINE)
    text_w = max(calc_rect.right - calc_rect.left + 8, 10)
    text_h = max(calc_rect.bottom - calc_rect.top + 8, 10)
    
    draw_rect = wintypes.RECT(4, 4, text_w + 4, text_h + 4)
    user32.DrawTextW(hdc, text, -1, byref(draw_rect), DT_SINGLELINE)
    
    buf = (ctypes.c_char * (max_w * max_h * 4)).from_address(p_bits.value)
    raw = bytes(buf)
    
    gdi32.DeleteObject(hfont)
    gdi32.DeleteObject(hbitmap)
    gdi32.DeleteDC(hdc)
    user32.ReleaseDC(0, hdc_screen)
    
    full_img = Image.frombuffer('RGBA', (max_w, max_h), raw, 'raw', 'BGRA', 0, 1).convert('L')
    alpha = ImageOps.invert(full_img).crop((0, 0, min(text_w + 16, max_w), min(text_h + 16, max_h)))
    
    bbox = alpha.getbbox()
    if bbox:
        p = 3
        crop_box = (max(0, bbox[0]-p), max(0, bbox[1]-p), min(alpha.width, bbox[2]+p), min(alpha.height, bbox[3]+p))
        alpha = alpha.crop(crop_box)
    
    final = Image.new('RGBA', alpha.size, (0, 0, 0, 0))
    color_img = Image.new('RGBA', alpha.size, (*text_color, 255))
    final.paste(color_img, (0, 0), mask=alpha)
    return final, alpha


def classify_track(raw_title: str):
    """Categorizes the video into theme, badge, primary tamil title, and english subtitle."""
    t_low = raw_title.lower()
    
    # 1. Classify Theme
    if any(k in t_low for k in ['திருப்புகழ்', 'கந்தர்', 'கந்த ', 'முருக', 'ஆறுமுகம்', 'நாத விந்து', 'முத்தைத்', 'உருவாய்', 'நாள் என் செய்யும்', 'thiruppugazh', 'kandhar', 'murugan']):
        theme = 'murugan'
        badge = 'திருப்புகழ்' if 'திருப்புகழ்' in raw_title else ('கந்த சஷ்டி' if 'கந்த சஷ்டி' in raw_title else 'முருகன் அருள்')
    elif any(k in t_low for k in ['விநாயகர்', 'கண நாதா', 'கைத்தல', 'திகட சக்கர', 'பிடியதன்', 'பாலும் தெளிதேனும்', 'ganesha', 'vinayagar', 'gana natha']):
        theme = 'vinayagar'
        badge = 'கந்தபுராணம்' if 'கந்தபுராணம்' in raw_title else ('ஔவையார் நல்வழி' if 'நல்வழி' in raw_title else 'விநாயகர் துதி')
    elif any(k in t_low for k in ['திருப்பாவை', 'ஹரே ராமா', 'கிருஷ்ண', 'பெருமாள்', 'ஆண்டாள்', 'thiruppavai', 'krishna', 'rama', 'vishnu', 'perumal']):
        theme = 'perumal'
        badge = 'திருப்பாவை' if 'திருப்பாவை' in raw_title else 'மகாவிஷ்ணு'
    elif any(k in t_low for k in ['திருக்குறள்', 'அதிகாரம்', 'நாடு', 'வினைத்திட்பம்', 'வினைத்தூய்மை', 'ஆள்வினையுடைமை', 'வெருவந்த செய்யாமை', 'சிற்றினஞ்சேராமை', 'குற்றங்கடிதல்', 'கல்வி', 'வாய்மை', 'பொறையுடைமை', 'அருளுடைமை', 'thirukkural']):
        theme = 'thirukkural'
        badge = 'திருக்குறள்'
    elif any(k in t_low for k in ['அம்மன்', 'காளி', 'துர்க்கை', 'மீனாட்சி', 'அபிராமி', 'லலிதா', 'மாதா', 'தாயின் மணிக்கொடி']):
        theme = 'amman'
        badge = 'அம்மன் அருள்'
    else:
        theme = 'shiva'
        if 'தேவாரம்' in raw_title:
            badge = 'தேவாரம்'
        elif 'திருவாசகம்' in raw_title:
            badge = 'திருவாசகம்'
        elif 'திருவருட்பா' in raw_title:
            badge = 'திருவருட்பா'
        elif 'திருமந்திரம்' in raw_title:
            badge = 'திருமந்திரம்'
        elif 'பெரியபுராணம்' in raw_title:
            badge = 'பெரியபுராணம்'
        elif 'சிவ நாமாவளி' in raw_title:
            badge = 'சிவ நாமாவளி'
        elif 'சிவ ஸ்தோத்திரம்' in raw_title:
            badge = 'சிவ ஸ்தோத்திரம்'
        else:
            badge = 'சிவ பக்தி'

    # 2. Extract Parts
    parts = [p.strip() for p in raw_title.split('|')]
    tamil_raw = parts[0]
    eng_raw = parts[1] if len(parts) > 1 else ''
    
    # If part 2 contains non-latin and part 3 is latin, use part 3
    if len(parts) > 2 and any(ord(c) > 127 for c in eng_raw) and not any(ord(c) > 127 for c in parts[2]):
        eng_raw = parts[2]

    # Clean English Subtitle
    eng = re.sub(r'\[.*?\]', '', eng_raw)
    eng = re.sub(r'\(.*?\)', '', eng)
    eng = re.sub(r'(Cinematic|Devotional|Film|Full|Song|Remix|Official|Video|Audio|Part\s*\d+|Guru\s*Kula\s*Desam).*', '', eng, flags=re.I)
    eng = eng.strip(' -:|,\t\r\n')
    
    if not eng or len(eng) < 2:
        eng = badge

    # Clean Tamil Title
    t_clean = tamil_raw
    prefixes_to_strip = [
        'திருக்குறள்:', 'திருக்குறள் -', 'தேவாரம்:', 'தேவாரம் -', 'திருவருட்பா:', 'திருவருட்பா -',
        'திருவாசகம்:', 'திருவாசகம் -', 'திருமந்திரம்:', 'திருமந்திரம் -', 'பெரியபுராணம்:', 'பெரியபுராணம் -',
        'சிவ பக்திப் பாடல்:', 'சிவ நாமாவளி:', 'சிவ ஸ்தோத்திரம்:', 'நாம சங்கீர்த்தனம்:', 'தேசிய கீதம்:',
        'திருப்பாவை -', 'திருப்பாவை 1 -', 'திருப்பாவை 2 -', 'திருப்பாவை 3 -'
    ]
    for pfx in prefixes_to_strip:
        if t_clean.startswith(pfx):
            t_clean = t_clean[len(pfx):].strip()
    
    t_clean = re.sub(r'\s*2026\b', '', t_clean)
    t_clean = re.sub(r'\s*\[.*?\]', '', t_clean)
    t_clean = re.sub(r'\s*\(ஆண்டாள்\)', '', t_clean)
    t_clean = re.sub(r'\s*\(வள்ளலார்\)', '', t_clean)
    t_clean = re.sub(r'\s*\(திருநாவுக்கரசர்\)', '', t_clean)
    t_clean = t_clean.strip(' -:|,\t\r\n')

    # Specific track polish
    if 'திகட சக்கர' in t_clean and 'காப்பு' not in t_clean:
        t_clean = 'திகட சக்கர விநாயகர் காப்பு'

    return {
        'theme': theme,
        'badge': badge,
        'tamil_title': t_clean,
        'subtitle': eng.upper()
    }


def draw_rounded_pill(draw, xy, fill, border_color, border_width=2, radius=18):
    """Draws a smooth rounded pill container."""
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=border_color, width=border_width)


def create_background_gradient(W, H, c_start, c_mid, c_end):
    """Vectorized non-linear diagonal spiritual gradient."""
    y_coords, x_coords = np.ogrid[:H, :W]
    t = (0.55 * (x_coords / W) + 0.45 * (y_coords / H))
    seg1 = t < 0.48
    t1 = np.clip(t / 0.48, 0.0, 1.0)
    t2 = np.clip((t - 0.48) / 0.52, 0.0, 1.0)
    
    r = np.where(seg1, c_start[0] + (c_mid[0] - c_start[0]) * t1, c_mid[0] + (c_end[0] - c_mid[0]) * t2)
    g = np.where(seg1, c_start[1] + (c_mid[1] - c_start[1]) * t1, c_mid[1] + (c_end[1] - c_mid[1]) * t2)
    b = np.where(seg1, c_start[2] + (c_mid[2] - c_start[2]) * t1, c_mid[2] + (c_end[2] - c_mid[2]) * t2)
    
    arr = np.stack([r, g, b], axis=-1).astype(np.uint8)
    return Image.fromarray(arr, 'RGB')


def create_vignette(W, H, center_x, center_y):
    """Smooth deep corner vignette to focus viewer attention."""
    y_coords, x_coords = np.ogrid[:H, :W]
    dist = np.sqrt((x_coords - center_x)**2 + (y_coords - center_y)**2)
    max_d = math.sqrt(center_x**2 + center_y**2)
    vig_factor = np.clip((dist - max_d * 0.56) / (max_d * 0.44), 0.0, 1.0) ** 1.8
    alpha = (vig_factor * 165).astype(np.uint8)
    black = np.zeros((H, W, 3), dtype=np.uint8)
    rgba = np.dstack([black, alpha])
    return Image.fromarray(rgba, 'RGBA')


def render_thumbnail(video_id: str, raw_title: str, custom_info: dict = None) -> Path:
    """Renders a 1920x1080 modern devotional thumbnail and saves to disk."""
    info = custom_info or classify_track(raw_title)
    theme_key = info['theme']
    theme = THEMES.get(theme_key, THEMES['shiva'])
    
    badge_text = info['badge']
    tamil_title = info['tamil_title']
    subtitle_text = info['subtitle']

    W, H = 1920, 1080
    center_x, center_y = 960, 510

    # 1. Base Gradient Canvas (1920 x 1080)
    base_img = create_background_gradient(W, H, theme['bg_start'], theme['bg_mid'], theme['bg_end'])

    # 2. Divine Sacred Radiant Halo / Radial Glow
    glow_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)
    
    halo_color = theme['halo_color']
    glow_color = theme['glow_color']

    # Concentric multi-stop halo circles with gaussian blur
    for r in range(480, 40, -40):
        alpha_factor = (1.0 - (r / 480.0)) ** 1.8
        alpha = int(halo_color[3] * alpha_factor)
        c = (halo_color[0], halo_color[1], halo_color[2], alpha)
        glow_draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], fill=c)

    for r in range(180, 20, -25):
        alpha_factor = (1.0 - (r / 180.0)) ** 1.2
        alpha = int(glow_color[3] * alpha_factor)
        c = (glow_color[0], glow_color[1], glow_color[2], alpha)
        glow_draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], fill=c)

    glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(radius=55))

    # 3. Sacred Rays / Cosmic Starburst Pattern
    rays_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    rays_draw = ImageDraw.Draw(rays_layer)
    num_rays = 32
    ray_len = 1100
    for i in range(num_rays):
        angle = (2 * math.pi / num_rays) * i
        x2 = center_x + int(ray_len * math.cos(angle))
        y2 = center_y + int(ray_len * math.sin(angle))
        rays_draw.line([(center_x, center_y), (x2, y2)], fill=(255, 215, 0, 18), width=3)

    for radius in [260, 390, 520]:
        rays_draw.ellipse(
            [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
            outline=(255, 215, 0, 28),
            width=2
        )

    # Subtle celestial sparkle stars (seeded for reproducibility)
    rng = random.Random(sum(ord(c) for c in video_id))
    for _ in range(60):
        sx = rng.randint(40, W - 40)
        sy = rng.randint(40, H - 40)
        s_size = rng.randint(2, 5)
        s_alpha = rng.randint(40, 180)
        s_col = (255, 245, 200, s_alpha)
        rays_draw.line([(sx - s_size * 2, sy), (sx + s_size * 2, sy)], fill=s_col, width=1)
        rays_draw.line([(sx, sy - s_size * 2), (sx, sy + s_size * 2)], fill=s_col, width=1)
        rays_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255, s_alpha + 40))

    composite = Image.alpha_composite(base_img.convert('RGBA'), glow_overlay)
    composite = Image.alpha_composite(composite, rays_layer)

    # 4. Corner Vignette Shading
    vignette = create_vignette(W, H, center_x, center_y)
    composite = Image.alpha_composite(composite, vignette)

    # 5. Regal Temple Framing / Golden Double Border
    draw = ImageDraw.Draw(composite)
    gold = theme['accent_gold']
    
    draw.rectangle([36, 36, W - 36, H - 36], outline=(gold[0], gold[1], gold[2], 90), width=2)
    draw.rectangle([48, 48, W - 48, H - 48], outline=(gold[0], gold[1], gold[2], 140), width=1)
    
    b_len = 45
    # Top-Left
    draw.line([(36, 36), (36 + b_len, 36)], fill=gold, width=4)
    draw.line([(36, 36), (36, 36 + b_len)], fill=gold, width=4)
    # Top-Right
    draw.line([(W - 36, 36), (W - 36 - b_len, 36)], fill=gold, width=4)
    draw.line([(W - 36, 36), (W - 36, 36 + b_len)], fill=gold, width=4)
    # Bottom-Left
    draw.line([(36, H - 36), (36 + b_len, H - 36)], fill=gold, width=4)
    draw.line([(36, H - 36), (36, H - 36 - b_len)], fill=gold, width=4)
    # Bottom-Right
    draw.line([(W - 36, H - 36), (W - 36 - b_len, H - 36)], fill=gold, width=4)
    draw.line([(W - 36, H - 36), (W - 36, H - 36 - b_len)], fill=gold, width=4)

    # 6. Top Left Category Pill (with shaped Tamil text)
    badge_img, badge_alpha = render_shaped_text(badge_text, FONT_TAMIL_FAMILY, 32, theme['pill_text'], max_w=700, max_h=80)
    bw = badge_img.width + 72
    bh = 58
    bx0, by0 = 80, 75
    draw_rounded_pill(draw, [bx0, by0, bx0 + bw, by0 + bh], fill=theme['pill_bg'], border_color=theme['pill_border'], border_width=2, radius=20)
    
    # Draw glowing sacred gold diamond icon inside pill
    dm_x, dm_y = bx0 + 26, by0 + (bh // 2)
    dr = 6
    draw.polygon([(dm_x, dm_y - dr), (dm_x + dr, dm_y), (dm_x, dm_y + dr), (dm_x - dr, dm_y)], fill=gold)
    # Paste shaped badge text
    composite.paste(badge_img, (bx0 + 44, by0 + (bh - badge_img.height) // 2), mask=badge_alpha)

    # 7. Top Right Quality / Format Pill
    font_qual = ImageFont.truetype(FONT_SANS_BOLD, 22)
    qual_label = "●  4K ULTRA HD  |  DIVINE MASTER"
    bbox_q = draw.textbbox((0, 0), qual_label, font=font_qual)
    qw = bbox_q[2] - bbox_q[0] + 44
    qh = 54
    qx0 = W - 80 - qw
    qy0 = 77
    draw_rounded_pill(draw, [qx0, qy0, qx0 + qw, qy0 + qh], fill=(15, 15, 25, 210), border_color=(255, 215, 0, 200), border_width=2, radius=18)
    draw.text((qx0 + 22, qy0 + 12), qual_label, font=font_qual, fill=(255, 245, 215))

    # 8. Primary Tamil Title with Windows DirectWrite / Uniscribe Shaping
    # Wrap text into 1 or 2 lines if needed
    lines = [tamil_title]
    if len(tamil_title) > 22:
        if ' - ' in tamil_title:
            p = tamil_title.split(' - ', 1)
            lines = [p[0].strip(), p[1].strip()]
        elif ' : ' in tamil_title:
            p = tamil_title.split(' : ', 1)
            lines = [p[0].strip(), p[1].strip()]
        elif ': ' in tamil_title:
            p = tamil_title.split(': ', 1)
            lines = [p[0].strip(), p[1].strip()]
        elif ' (' in tamil_title:
            p = tamil_title.split(' (', 1)
            lines = [p[0].strip(), '(' + p[1].strip()]

    # Select font size based on length
    title_size = 88 if len(lines) > 1 or len(tamil_title) > 16 else 98

    rendered_lines = []
    for l in lines:
        t_img, t_alpha = render_shaped_text(l, FONT_TAMIL_FAMILY, title_size, (255, 255, 255), max_w=1700, max_h=180)
        # If line still exceeds 1550px, re-render smaller
        if t_img.width > 1550:
            scale_size = int(title_size * (1500 / t_img.width))
            t_img, t_alpha = render_shaped_text(l, FONT_TAMIL_FAMILY, scale_size, (255, 255, 255), max_w=1700, max_h=180)
        rendered_lines.append((t_img, t_alpha))

    total_text_h = sum(img.height for img, _ in rendered_lines) + (len(rendered_lines) - 1) * 20
    start_y = 500 - (total_text_h // 2)

    # Layer A: Ambient colored glow
    glow_txt = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cur_y = start_y
    for t_img, t_alpha in rendered_lines:
        lx = (W - t_img.width) // 2
        glow_color_img = Image.new('RGBA', t_img.size, theme['glow_color'])
        glow_txt.paste(glow_color_img, (lx, cur_y), mask=t_alpha)
        cur_y += t_img.height + 20
    glow_txt = glow_txt.filter(ImageFilter.GaussianBlur(radius=18))
    composite = Image.alpha_composite(composite, glow_txt)

    # Layer B: Deep Drop Shadow
    shadow_txt = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cur_y = start_y + 8
    for t_img, t_alpha in rendered_lines:
        lx = (W - t_img.width) // 2
        black_img = Image.new('RGBA', t_img.size, (0, 0, 0, 240))
        shadow_txt.paste(black_img, (lx, cur_y), mask=t_alpha)
        cur_y += t_img.height + 20
    shadow_txt = shadow_txt.filter(ImageFilter.GaussianBlur(radius=8))
    composite = Image.alpha_composite(composite, shadow_txt)

    # Layer C: Crisp Foreground Text with High-Contrast Dark Outline
    cur_y = start_y
    for t_img, t_alpha in rendered_lines:
        lx = (W - t_img.width) // 2
        # Outline for extreme contrast against bright halo
        outline_img = Image.new('RGBA', t_img.size, (10, 5, 5, 230))
        for ox, oy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            composite.paste(outline_img, (lx + ox, cur_y + oy), mask=t_alpha)
        # Foreground crisp white
        composite.paste(t_img, (lx, cur_y), mask=t_alpha)
        cur_y += t_img.height + 20

    # 9. Decorative Golden Center Divider (─── ◆ ───)
    draw = ImageDraw.Draw(composite)
    div_y = cur_y + 16
    div_w = 480
    div_x0 = (W - div_w) // 2
    div_x1 = div_x0 + div_w
    center_div_x = W // 2
    
    draw.line([(div_x0, div_y), (center_div_x - 30, div_y)], fill=(gold[0], gold[1], gold[2], 210), width=2)
    draw.line([(center_div_x + 30, div_y), (div_x1, div_y)], fill=(gold[0], gold[1], gold[2], 210), width=2)
    diam_r = 7
    draw.polygon([
        (center_div_x, div_y - diam_r),
        (center_div_x + diam_r, div_y),
        (center_div_x, div_y + diam_r),
        (center_div_x - diam_r, div_y)
    ], fill=gold)

    # 10. Secondary English / Transliteration Subtitle
    font_sub = ImageFont.truetype(FONT_SANS_BOLD, 38)
    bbox_sub = draw.textbbox((0, 0), subtitle_text, font=font_sub)
    sub_w = bbox_sub[2] - bbox_sub[0]
    
    # If subtitle is very long, scale font size
    if sub_w > 1500:
        font_sub = ImageFont.truetype(FONT_SANS_BOLD, 32)
        bbox_sub = draw.textbbox((0, 0), subtitle_text, font=font_sub)
        sub_w = bbox_sub[2] - bbox_sub[0]

    sub_x = (W - sub_w) // 2
    sub_y = div_y + 26
    
    draw.text((sub_x, sub_y + 3), subtitle_text, font=font_sub, fill=(0, 0, 0, 230))
    draw.text((sub_x, sub_y), subtitle_text, font=font_sub, fill=theme['sub_color'])

    # 11. Subtle Channel Emblem / Watermark at Bottom
    font_watermark = ImageFont.truetype(FONT_SANS_SEMI, 22)
    wm_text = "G U R U   K U L A   D E S A M"
    bbox_wm = draw.textbbox((0, 0), wm_text, font=font_watermark)
    wm_w = bbox_wm[2] - bbox_wm[0]
    wm_x = (W - wm_w) // 2
    wm_y = H - 85

    # Decorative golden diamonds beside watermark
    wm_dr = 5
    d1_x = wm_x - 30
    d2_x = wm_x + wm_w + 30
    draw.polygon([(d1_x, wm_y + 14 - wm_dr), (d1_x + wm_dr, wm_y + 14), (d1_x, wm_y + 14 + wm_dr), (d1_x - wm_dr, wm_y + 14)], fill=gold)
    draw.polygon([(d2_x, wm_y + 14 - wm_dr), (d2_x + wm_dr, wm_y + 14), (d2_x, wm_y + 14 + wm_dr), (d2_x - wm_dr, wm_y + 14)], fill=gold)
    
    draw.text((wm_x, wm_y + 2), wm_text, font=font_watermark, fill=(0, 0, 0, 180))
    draw.text((wm_x, wm_y), wm_text, font=font_watermark, fill=(gold[0], gold[1], gold[2], 210))

    # 12. Save final 1920x1080 PNG (ultra fast)
    out_path = OUTPUT_DIR / f"{video_id}.png"
    composite.convert('RGB').save(str(out_path), format='PNG')
    return out_path


# Verified 7 Master Tracks definition
MASTER_TRACKS = [
    {
        'id': 'Mata6vtnrjQ',
        'raw_title': 'திருக்குறள்: அதிகாரம் 61 - மடியின்மை | Madiyinmai [Film]',
        'custom_info': {
            'theme': 'thirukkural',
            'badge': 'திருக்குறள்  •  அதிகாரம் 61',
            'tamil_title': 'மடியின்மை',
            'subtitle': 'THIRUKKURAL 61 • OVERCOMING IDLENESS'
        }
    },
    {
        'id': 'KFtS403RfbY',
        'raw_title': 'திருக்குறள்: அதிகாரம் 125 - நெஞ்சறிவுறுத்தல் | Nenjari Vuruthal Part 1 Cinematic Film',
        'custom_info': {
            'theme': 'thirukkural',
            'badge': 'திருக்குறள்  •  அதிகாரம் 125',
            'tamil_title': 'நெஞ்சறிவுறுத்தல்',
            'subtitle': 'THIRUKKURAL 125 • NENJARI VURUTHAL'
        }
    },
    {
        'id': 'mQpQEuXiEZ4',
        'raw_title': 'திகட சக்கர | கந்தபுராணம் விநாயகர் காப்பு | Thigada Sakkara Cinematic Film',
        'custom_info': {
            'theme': 'vinayagar',
            'badge': 'கந்தபுராணம்  •  விநாயகர் காப்பு',
            'tamil_title': 'திகட சக்கர விநாயகர் காப்பு',
            'subtitle': 'THIGADA SAKKARA • KANDHA PURANAM'
        }
    },
    {
        'id': '31xVgvxoiUA',
        'raw_title': 'திருப்பாவை 3 - ஓங்கி உலகளந்த உத்தமன் (ஆண்டாள்) | Ongi Ulagalandha Cinematic Film',
        'custom_info': {
            'theme': 'perumal',
            'badge': 'திருப்பாவை  •  பாசுரம் 3',
            'tamil_title': 'ஓங்கி உலகளந்த உத்தமன்',
            'subtitle': 'THIRUPPAVAI 3 • ONGI ULAGALANDHA'
        }
    },
    {
        'id': 'AW4cljBWy2w',
        'raw_title': 'பாலும் தெளிதேனும் | ஔவையார் நல்வழி விநாயகர் துதி',
        'custom_info': {
            'theme': 'vinayagar',
            'badge': 'ஔவையார் நல்வழி',
            'tamil_title': 'பாலும் தெளிதேனும்',
            'subtitle': 'PAALUM THELITHENUM • VINAYAGAR THUTHI'
        }
    },
    {
        'id': 'QH-xL37NmGM',
        'raw_title': 'திருப்பாவை - 1 (மார்கழித் திங்கள்) | Thiruppavai 1 Cinematic Devotional Film',
        'custom_info': {
            'theme': 'perumal',
            'badge': 'திருப்பாவை  •  பாசுரம் 1',
            'tamil_title': 'மார்கழித் திங்கள்',
            'subtitle': 'THIRUPPAVAI 1 • MARGAZHI THINGAL'
        }
    },
    {
        'id': 'hm7_qUlTUiU',
        'raw_title': 'திருப்பாவை 2 - வையத்து வாழ்வீர்காள் | ஆண்டாள் அருளிய திருப்பாவை',
        'custom_info': {
            'theme': 'perumal',
            'badge': 'திருப்பாவை  •  பாசுரம் 2',
            'tamil_title': 'வையத்து வாழ்வீர்காள்',
            'subtitle': 'THIRUPPAVAI 2 • VAIYATHU VAAZHVEERGAAL'
        }
    }
]


def run_master_generation():
    """Generates thumbnails for the 7 verified master tracks."""
    print("🎨 Generating thumbnails for 7 verified master tracks...")
    results = []
    for item in MASTER_TRACKS:
        vid = item['id']
        path = render_thumbnail(vid, item['raw_title'], item.get('custom_info'))
        print(f"  ✅ [MASTER] {vid} -> {path.name} ({item['custom_info']['tamil_title']})", flush=True)
        results.append((vid, path))
    return results


def run_batch_generation():
    """Batch generates thumbnails for remaining public tracks in remaining_bad_public_srts.json."""
    json_path = REPO_DIR / "production" / "remaining_bad_public_srts.json"
    if not json_path.exists():
        print(f"❌ Could not find {json_path}")
        return []

    with open(json_path, 'r', encoding='utf-8') as f:
        tracks = json.load(f)

    print(f"🎨 Batch generating modern thumbnails for {len(tracks)} tracks in {json_path.name}...", flush=True)
    results = []
    for idx, t in enumerate(tracks, 1):
        vid = t['id']
        raw_title = t.get('title', '')
        path = render_thumbnail(vid, raw_title)
        results.append((vid, path))
        if idx % 20 == 0 or idx == len(tracks):
            print(f"  ⚡ Progress: {idx}/{len(tracks)} thumbnails generated...", flush=True)

    print(f"🎉 Successfully batch generated {len(results)} thumbnails!", flush=True)
    return results


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if mode == 'master':
        run_master_generation()
    elif mode == 'batch':
        run_batch_generation()
    else:
        run_master_generation()
        run_batch_generation()
