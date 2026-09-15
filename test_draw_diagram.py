from PIL import Image, ImageDraw, ImageFont
import numpy as np

W, H = 1920, 1080
FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

f_title = ImageFont.truetype(FONT_BOLD, 36)
f_h2 = ImageFont.truetype(FONT_BOLD, 28)
f_body = ImageFont.truetype(FONT_REG, 24)
f_bold = ImageFont.truetype(FONT_BOLD, 24)
f_badge = ImageFont.truetype(FONT_BOLD, 20)
f_small = ImageFont.truetype(FONT_REG, 18)

im = Image.new("RGB", (900, 480), "#0B1120")
draw = ImageDraw.Draw(im)

# Outer card border
draw.rounded_rectangle([10, 10, 890, 470], radius=20, fill="#0F172A", outline="#38BDF8", width=2)
draw.rounded_rectangle([30, 25, 340, 65], radius=10, fill="#0369A1")
draw.text((185, 45), "SO DO CAU AM (ARTICULATION)", font=f_badge, fill="#FFFFFF", anchor="mm")

# Anatomical cross section
cx = 360
cy = 240

# 1. Background skull/palate cavity
# Upper palate arch
draw.arc([cx - 160, cy - 140, cx + 220, cy + 100], start=180, end=350, fill="#475569", width=12)

# 2. Upper Lip & Gum (Alveolar Ridge)
# Gum tissue
draw.ellipse([cx - 130, cy - 60, cx - 40, cy + 10], fill="#BE123C") # Deep pink gum
# Alveolar ridge label target
draw.ellipse([cx - 65, cy - 45, cx - 35, cy - 15], fill="#EF4444", outline="#FECDD3", width=3)

# 3. Upper front tooth
draw.polygon([
    (cx - 115, cy - 15),
    (cx - 95, cy - 15),
    (cx - 98, cy + 45),
    (cx - 112, cy + 45)
], fill="#F8FAFC", outline="#94A3B8", width=2)
draw.text((cx - 170, cy + 35), "Rang tren", font=f_small, fill="#94A3B8")

# 4. Lower front tooth
draw.polygon([
    (cx - 115, cy + 85),
    (cx - 95, cy + 85),
    (cx - 98, cy + 135),
    (cx - 112, cy + 135)
], fill="#F8FAFC", outline="#94A3B8", width=2)
draw.text((cx - 170, cy + 105), "Rang duoi", font=f_small, fill="#94A3B8")

# 5. Tongue Muscle - for Đ (Tip touches alveolar ridge firmly)
tongue_pts = [
    (cx - 48, cy - 25),   # Tip firmly on alveolar ridge!
    (cx + 30, cy - 10),   # Tongue blade
    (cx + 120, cy + 40),  # Tongue dorsum
    (cx + 150, cy + 140), # Tongue root
    (cx + 60, cy + 150),
    (cx - 10, cy + 110),
    (cx - 60, cy + 40)
]
draw.polygon(tongue_pts, fill="#F43F5E", outline="#E11D48", width=3)
draw.text((cx + 50, cy + 70), "LUOI (Tongue)", font=f_badge, fill="#FFFFFF", anchor="mm")

# 6. Air blockage indicator
draw.arc([cx - 10, cy - 70, cx + 50, cy - 10], start=160, end=320, fill="#38BDF8", width=4)
draw.polygon([(cx - 10, cy - 40), (cx - 25, cy - 35), (cx - 15, cy - 20)], fill="#38BDF8")

# 7. Callouts & Explanation Cards on the right
draw.rounded_rectangle([540, 90, 860, 200], radius=12, fill="#1E293B", outline="#F43F5E", width=2)
draw.text((560, 115), "1. VI TRI TIEP XUC:", font=f_bold, fill="#FECDD3")
draw.text((560, 150), "Dau luoi AP CHAT vao", font=f_body, fill="#F8FAFC")
draw.text((560, 175), "nuou rang tren (Alveolar)", font=f_bold, fill="#38BDF8")

draw.rounded_rectangle([540, 220, 860, 330], radius=12, fill="#1E293B", outline="#38BDF8", width=2)
draw.text((560, 245), "2. LUONG KHI (AIR):", font=f_bold, fill="#93C5FD")
draw.text((560, 280), "Chan hoan toan luong hoi", font=f_body, fill="#F8FAFC")
draw.text((560, 305), "-> Bat ra manh nhu 'Door'", font=f_bold, fill="#FDE047")

# Target point pointer line
draw.line([cx - 35, cy - 30, 540, 140], fill="#EF4444", width=2)
draw.ellipse([537, 137, 543, 143], fill="#EF4444")

im.save("/home/quang/video_ai/test_diagram.png")
print("Saved test_diagram.png")
