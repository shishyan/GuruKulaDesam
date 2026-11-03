import math
from PIL import Image, ImageDraw

W, H = 1080, 1920

# 1. Base transparent overlay for Diyas
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

def draw_mini_diya(cx, cy, scale=1.0):
    bw = int(14 * scale)
    bh = int(8 * scale)
    base_color = (220, 140, 20, 235)
    border_color = (130, 70, 10, 240)
    rim_color = (255, 200, 50, 255)
    
    # Base bowl
    draw.pieslice([cx - bw, cy - bh, cx + bw, cy + bh], start=0, end=180, fill=base_color, outline=border_color, width=1)
    draw.line([cx - bw, cy, cx + bw, cy], fill=rim_color, width=1)
    
    # Flame
    flame_w = int(5 * scale)
    flame_h = int(11 * scale)
    # Glow outer
    draw.ellipse([cx - flame_w - 2, cy - flame_h - 2, cx + flame_w + 2, cy + 2], fill=(255, 170, 0, 90))
    # Outer flame
    draw.polygon([(cx - flame_w, cy), (cx, cy - flame_h), (cx + flame_w, cy), (cx, cy + 2)], fill=(255, 140, 0, 240))
    # Inner bright flame
    draw.polygon([(cx - int(flame_w * 0.5), cy), (cx, cy - int(flame_h * 0.8)), (cx + int(flame_w * 0.5), cy), (cx, cy + 1)], fill=(255, 255, 180, 255))

# Perimeter distribution:
# 18 Left Edge
left_x = 40
margin_top_y = 120
margin_bot_y = 1800
y_steps_18 = [(margin_top_y + i * (margin_bot_y - margin_top_y) / 17.0) for i in range(18)]
for y in y_steps_18:
    draw_mini_diya(left_x, int(y), scale=1.0)

# 18 Right Edge
right_x = W - 40
for y in y_steps_18:
    draw_mini_diya(right_x, int(y), scale=1.0)

# 6 Top Edge (evenly spaced between left_x and right_x, excluding corners)
top_y = 38
x_steps_6 = [(160 + i * (W - 320) / 5.0) for i in range(6)]
for x in x_steps_6:
    draw_mini_diya(int(x), top_y, scale=1.0)

# 6 Bottom Edge
# Leave center clear for the logo (logo at bottom center ~ cx=540)
# 3 on left of center, 3 on right of center
bottom_y = H - 38
bot_x_left = [120, 240, 360]
bot_x_right = [W - 360, W - 240, W - 120]
for x in (bot_x_left + bot_x_right):
    draw_mini_diya(int(x), bottom_y, scale=1.0)

# 2. Composite Logo at Bottom Center
# Target logo size: e.g. 150x150 or 160x160 px centered at X=540, Y around 1830 (bottom center safe zone)
logo_path = "/home/shishyan/GitHub/Shishyan/GuruKulaDesam/production/gurukuladesam_shorts_logo.png"
logo = Image.open(logo_path).convert("RGBA")
target_logo_dim = 156
logo = logo.resize((target_logo_dim, target_logo_dim), Image.Resampling.LANCZOS)

# Position logo: centered horizontally at W//2 = 540, bottom margin at 18
logo_x = (W - target_logo_dim) // 2
logo_y = H - target_logo_dim - 12
overlay.paste(logo, (logo_x, logo_y), logo)

overlay.save("/home/shishyan/GitHub/Shishyan/GuruKulaDesam/production/shorts_diyas_48_overlay.png", "PNG")
print(f"Generated 48-Diya + Bottom Center Logo Overlay: size={overlay.size}, saved to production/shorts_diyas_48_overlay.png")
