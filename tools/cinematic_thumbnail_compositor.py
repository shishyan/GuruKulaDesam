# -*- coding: utf-8 -*-
"""
Guru Kula Desam - Cinematic Blockbuster Thumbnail Compositor
Creates ultra high-CTR YouTube thumbnails matching devotional blockbuster poster style:
- High-res Left-third Deity / Sage artwork plate
- 3D Gold Embossed / Metallic Chiseled Tamil Typography with deep drop shadows
- Ornate filigree banner ribbon framing
- Category pill & 4K Ultra HD badge
- Crisp DirectWrite / Uniscribe Tamil ligatures
"""

import os
import sys
import math
import ctypes
from ctypes import wintypes, byref, c_void_p, Structure, sizeof
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

REPO_DIR = Path(r"c:\GitHub\Gurukuladesam")
STAGES_DIR = REPO_DIR / "production" / "thumbnail_stages"
OUTPUT_DIR = REPO_DIR / "production" / "thumbnails"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_TAMIL_FAMILY = "Nirmala UI"
FONT_SANS_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_SANS_SEMI = r"C:\Windows\Fonts\seguisb.ttf"

class BITMAPINFOHEADER(Structure):
    _fields_ = [
        ('biSize', wintypes.DWORD), ('biWidth', wintypes.LONG), ('biHeight', wintypes.LONG),
        ('biPlanes', wintypes.WORD), ('biBitCount', wintypes.WORD), ('biCompression', wintypes.DWORD),
        ('biSizeImage', wintypes.DWORD), ('biXPelsPerMeter', wintypes.LONG), ('biYPelsPerMeter', wintypes.LONG),
        ('biClrUsed', wintypes.DWORD), ('biClrImportant', wintypes.DWORD)
    ]

class BITMAPINFO(Structure):
    _fields_ = [('bmiHeader', BITMAPINFOHEADER), ('bmiColors', wintypes.DWORD * 3)]

def render_shaped_alpha(text: str, font_name: str, font_size: int, max_w=1600, max_h=300):
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
    
    hfont = gdi32.CreateFontW(-font_size, 0, 0, 0, 900, 0, 0, 0, 1, 0, 0, 5, 0, font_name)
    gdi32.SelectObject(hdc, hfont)
    
    rect = wintypes.RECT(0, 0, max_w, max_h)
    white_brush = gdi32.CreateSolidBrush(0xFFFFFF)
    user32.FillRect(hdc, byref(rect), white_brush)
    gdi32.DeleteObject(white_brush)
    
    gdi32.SetBkMode(hdc, 1)
    gdi32.SetTextColor(hdc, 0x00000000)
    
    calc_rect = wintypes.RECT(0, 0, max_w, max_h)
    DT_CALCRECT = 0x00000400
    DT_SINGLELINE = 0x00000020
    user32.DrawTextW(hdc, text, -1, byref(calc_rect), DT_CALCRECT | DT_SINGLELINE)
    text_w = max(calc_rect.right - calc_rect.left + 16, 10)
    text_h = max(calc_rect.bottom - calc_rect.top + 16, 10)
    
    draw_rect = wintypes.RECT(8, 8, text_w + 8, text_h + 8)
    user32.DrawTextW(hdc, text, -1, byref(draw_rect), DT_SINGLELINE)
    
    buf = (ctypes.c_char * (max_w * max_h * 4)).from_address(p_bits.value)
    raw = bytes(buf)
    
    gdi32.DeleteObject(hfont)
    gdi32.DeleteObject(hbitmap)
    gdi32.DeleteDC(hdc)
    user32.ReleaseDC(0, hdc_screen)
    
    full_img = Image.frombuffer('RGBA', (max_w, max_h), raw, 'raw', 'BGRA', 0, 1).convert('L')
    alpha = ImageOps.invert(full_img).crop((0, 0, min(text_w + 20, max_w), min(text_h + 20, max_h)))
    
    bbox = alpha.getbbox()
    if bbox:
        p = 4
        crop_box = (max(0, bbox[0]-p), max(0, bbox[1]-p), min(alpha.width, bbox[2]+p), min(alpha.height, bbox[3]+p))
        alpha = alpha.crop(crop_box)
    return alpha

def create_gold_embossed_text(text: str, font_name: str, font_size: int):
    """Generates a 3D embossed metallic golden title with beveled highlights and deep shadow."""
    alpha = render_shaped_alpha(text, font_name, font_size)
    w, h = alpha.size
    
    # 1. Base Gold Gradient Layer
    gold_grad = Image.new('RGBA', (w, h))
    draw_g = ImageDraw.Draw(gold_grad)
    for y in range(h):
        ratio = y / max(h - 1, 1)
        # Metallic golden shine profile (bright top, warm amber center, deep gold bottom)
        if ratio < 0.25:
            r = int(255 - ratio * 40)
            g = int(245 - ratio * 80)
            b = int(180 - ratio * 200)
        elif ratio < 0.6:
            r = int(255 - (ratio - 0.25) * 60)
            g = int(210 - (ratio - 0.25) * 120)
            b = int(70 - (ratio - 0.25) * 100)
        else:
            r = int(230 - (ratio - 0.6) * 100)
            g = int(160 - (ratio - 0.6) * 90)
            b = int(35 - (ratio - 0.6) * 40)
        draw_g.line([(0, y), (w, y)], fill=(r, g, b, 255))
    
    # Apply alpha mask
    gold_text = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    gold_text.paste(gold_grad, (0, 0), mask=alpha)
    
    # 2. Beveled Highlight (Shifted Up-Left)
    highlight = Image.new('RGBA', (w, h), (255, 255, 230, 240))
    hi_mask = ImageOps.invert(alpha)
    hi_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    hi_layer.paste(highlight, (-2, -2), mask=alpha)
    
    # 3. Inner Dark Bevel (Shifted Down-Right)
    dark_bevel = Image.new('RGBA', (w, h), (80, 30, 0, 210))
    dark_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    dark_layer.paste(dark_bevel, (2, 3), mask=alpha)
    
    # 4. Outer Metallic Stroke (Dark Red-Bronze outline)
    stroke_w = 6
    outline_img = Image.new('RGBA', (w + stroke_w*2, h + stroke_w*2), (0, 0, 0, 0))
    stroke_color = Image.new('RGBA', (w, h), (45, 10, 5, 255))
    
    for ox in range(-stroke_w, stroke_w + 1):
        for oy in range(-stroke_w, stroke_w + 1):
            if ox*ox + oy*oy <= stroke_w*stroke_w:
                outline_img.paste(stroke_color, (ox + stroke_w, oy + stroke_w), mask=alpha)
    
    # Composite the 3D text
    comp = Image.new('RGBA', (w + stroke_w*2, h + stroke_w*2), (0, 0, 0, 0))
    comp.paste(outline_img, (0, 0))
    comp.paste(gold_text, (stroke_w, stroke_w), mask=alpha)
    comp.paste(hi_layer, (stroke_w, stroke_w), mask=hi_layer)
    comp.paste(dark_layer, (stroke_w, stroke_w), mask=dark_layer)
    
    return comp

def draw_ornate_banner(draw, box, fill=(50, 8, 12, 235), border=(255, 215, 0, 240)):
    """Draws a cinematic royal devotional banner ribbon with notched swallowtails and double gold border."""
    x0, y0, x1, y1 = box
    mid_y = (y0 + y1) // 2
    notch = 28
    
    # Points for notched ornamental ribbon
    pts = [
        (x0 + notch, y0),
        (x1 - notch, y0),
        (x1, mid_y),
        (x1 - notch, y1),
        (x0 + notch, y1),
        (x0, mid_y)
    ]
    draw.polygon(pts, fill=fill)
    draw.polygon(pts, outline=border, width=3)
    
    # Inner border
    in_pts = [
        (x0 + notch + 6, y0 + 5),
        (x1 - notch - 6, y0 + 5),
        (x1 - 8, mid_y),
        (x1 - notch - 6, y1 - 5),
        (x0 + notch + 6, y1 - 5),
        (x0 + 8, mid_y)
    ]
    draw.polygon(in_pts, outline=(border[0], border[1], border[2], 140), width=1)

def compose_cinematic_thumbnail(stage_path: Path, category_pill: str, main_title: str, subtitle: str, badge_quality="4K ULTRA HD"):
    """Composites stage plate with high-CTR 3D typography on the right two-thirds."""
    base = Image.open(stage_path).convert('RGBA').resize((1920, 1080), Image.Resampling.LANCZOS)
    W, H = base.size
    
    # Right-center text placement anchor
    center_text_x = 1320
    
    # 1. 4K Ultra HD Golden Badge (Top Right)
    draw = ImageDraw.Draw(base)
    font_4k = ImageFont.truetype(FONT_SANS_BOLD, 26)
    b_text = f"●  {badge_quality}"
    bbox_4k = draw.textbbox((0, 0), b_text, font=font_4k)
    bw = bbox_4k[2] - bbox_4k[0] + 40
    bh = 50
    bx0, by0 = W - 70 - bw, 60
    
    # Gold rounded badge
    draw.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=12, fill=(15, 10, 5, 220), outline=(255, 215, 0, 240), width=2)
    draw.text((bx0 + 20, by0 + 10), b_text, font=font_4k, fill=(255, 225, 120))
    
    # 2. Ornate Category Ribbon Banner
    alpha_cat = render_shaped_alpha(category_pill, FONT_TAMIL_FAMILY, 38)
    cat_w, cat_h = alpha_cat.size
    banner_w = max(cat_w + 120, 480)
    banner_h = 74
    bx0 = center_text_x - (banner_w // 2)
    by0 = 240
    draw_ornate_banner(draw, [bx0, by0, bx0 + banner_w, by0 + banner_h])
    
    cat_img = Image.new('RGBA', alpha_cat.size, (255, 245, 210, 255))
    base.paste(cat_img, (center_text_x - (cat_w // 2), by0 + (banner_h - cat_h) // 2), mask=alpha_cat)
    
    # 3. Main 3D Gold Embossed Tamil Title (Massive, high-impact)
    # Split if long
    lines = [main_title]
    if len(main_title) > 16:
        if ' - ' in main_title:
            lines = [p.strip() for p in main_title.split(' - ', 1)]
        elif ' : ' in main_title:
            lines = [p.strip() for p in main_title.split(' : ', 1)]
        elif ': ' in main_title:
            lines = [p.strip() for p in main_title.split(': ', 1)]
    
    title_size = 150 if len(lines) == 1 and len(main_title) <= 10 else (135 if len(lines) == 1 else 115)
    
    rendered_titles = []
    for l in lines:
        t_comp = create_gold_embossed_text(l, FONT_TAMIL_FAMILY, title_size)
        if t_comp.width > 1050:
            scale = 1000 / t_comp.width
            new_w = int(t_comp.width * scale)
            new_h = int(t_comp.height * scale)
            t_comp = t_comp.resize((new_w, new_h), Image.Resampling.LANCZOS)
        rendered_titles.append(t_comp)
    
    tot_h = sum(t.height for t in rendered_titles) + (len(rendered_titles) - 1) * 20
    start_y = 350 + (320 - tot_h) // 2
    
    # Deep ambient gold glow behind title
    glow_canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_canvas)
    glow_draw.ellipse([center_text_x - 520, start_y - 60, center_text_x + 520, start_y + tot_h + 100], fill=(255, 140, 20, 140))
    glow_canvas = glow_canvas.filter(ImageFilter.GaussianBlur(radius=60))
    base = Image.alpha_composite(base, glow_canvas)
    
    # Paste title lines with drop shadow
    curr_y = start_y
    for t_comp in rendered_titles:
        tx = center_text_x - (t_comp.width // 2)
        # Drop shadow
        shadow = Image.new('RGBA', t_comp.size, (0, 0, 0, 240))
        base.paste(shadow, (tx + 8, curr_y + 10), mask=t_comp)
        # Main text
        base.paste(t_comp, (tx, curr_y), mask=t_comp)
        curr_y += t_comp.height + 20
    
    # 4. Secondary Subtitle / Devotional Ribbon
    draw = ImageDraw.Draw(base)
    font_sub = ImageFont.truetype(FONT_SANS_BOLD, 42)
    bbox_sub = draw.textbbox((0, 0), subtitle, font=font_sub)
    sw = bbox_sub[2] - bbox_sub[0]
    if sw > 950:
        font_sub = ImageFont.truetype(FONT_SANS_BOLD, 34)
        bbox_sub = draw.textbbox((0, 0), subtitle, font=font_sub)
        sw = bbox_sub[2] - bbox_sub[0]
    
    sx = center_text_x - (sw // 2)
    sy = curr_y + 35
    
    # Draw dark glowing background plaque behind subtitle for extreme pop
    sub_pad_x = 36
    sub_pad_y = 12
    draw.rounded_rectangle(
        [sx - sub_pad_x, sy - sub_pad_y, sx + sw + sub_pad_x, sy + (bbox_sub[3] - bbox_sub[1]) + sub_pad_y + 6],
        radius=14,
        fill=(30, 5, 8, 230),
        outline=(255, 215, 0, 230),
        width=2
    )
    
    # Decorative filigree line above subtitle
    div_w = 460
    div_x0 = center_text_x - (div_w // 2)
    draw.line([(div_x0, sy - 14), (center_text_x - 25, sy - 14)], fill=(255, 215, 0, 220), width=2)
    draw.line([(center_text_x + 25, sy - 14), (div_x0 + div_w, sy - 14)], fill=(255, 215, 0, 220), width=2)
    draw.polygon([
        (center_text_x, sy - 14 - 6),
        (center_text_x + 6, sy - 14),
        (center_text_x, sy - 14 + 6),
        (center_text_x - 6, sy - 14)
    ], fill=(255, 215, 0, 255))
    
    # Subtitle text with high contrast shadow
    draw.text((sx + 3, sy + 3), subtitle, font=font_sub, fill=(0, 0, 0, 230))
    draw.text((sx, sy), subtitle, font=font_sub, fill=(255, 235, 175))
    
    # 5. Channel Emblem
    font_wm = ImageFont.truetype(FONT_SANS_SEMI, 22)
    wm = "G U R U   K U L A   D E S A M"
    bb_wm = draw.textbbox((0, 0), wm, font=font_wm)
    wm_w = bb_wm[2] - bb_wm[0]
    draw.text((center_text_x - (wm_w // 2), H - 80), wm, font=font_wm, fill=(255, 215, 0, 190))
    
    return base.convert('RGB')

if __name__ == '__main__':
    # Test generation on Kodungonmai 56
    stage = STAGES_DIR / "thirukkural_stage.png"
    out_img = compose_cinematic_thumbnail(
        stage_path=stage,
        category_pill="திருக்குறள்  •  அதிகாரம் 56",
        main_title="கொடுங்கோன்மை",
        subtitle="CRUEL TYRANNY  |  CLASSICAL DEVOTIONAL",
        badge_quality="4K ULTRA HD"
    )
    test_out = OUTPUT_DIR / "wzdoeFDq0iQ.png"
    out_img.save(str(test_out), format='PNG')
    print(f"Generated test thumbnail: {test_out}")
