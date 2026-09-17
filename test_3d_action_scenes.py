import os
import math
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = "/home/quang/video_ai"
W, H = 1920, 1080

FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

fonts = {
    "title": ImageFont.truetype(FONT_BOLD, 36),
    "h2": ImageFont.truetype(FONT_BOLD, 30),
    "h3": ImageFont.truetype(FONT_BOLD, 24),
    "huge_letter": ImageFont.truetype(FONT_BOLD, 120),
    "badge": ImageFont.truetype(FONT_BOLD, 22),
    "sub_vi": ImageFont.truetype(FONT_BOLD, 28),
    "sub_en": ImageFont.truetype(FONT_REG, 22),
}

ASSETS = {
    "egg": Image.open("cartoon_assets/item_egg.png").convert("RGBA"),
    "cow": Image.open("cartoon_assets/item_cow.png").convert("RGBA"),
    "hat": Image.open("cartoon_assets/item_hat.png").convert("RGBA"),
    "teacher": Image.open("cartoon_assets/item_teacher.png").convert("RGBA"),
    "hook": Image.open("cartoon_assets/item_hook.png").convert("RGBA"),
    "avocado": Image.open("cartoon_assets/item_avocado.png").convert("RGBA"),
    "trophy": Image.open("cartoon_assets/item_trophy.png").convert("RGBA"),
    "confetti": Image.open("cartoon_assets/item_confetti.png").convert("RGBA"),
}

os.makedirs("test_3d_actions_preview", exist_ok=True)

def draw_subtitle_bar(draw, vi_text, en_text, speaker_name, speaker_color):
    draw.rounded_rectangle([180, 910, 1740, 1040], radius=24, fill=(15, 23, 42, 230), outline="#475569", width=2)
    draw.rounded_rectangle([210, 930, 400, 975], radius=12, fill=speaker_color)
    draw.text((305, 952), speaker_name, font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    draw.text((430, 952), vi_text, font=fonts["sub_vi"], fill="#F8FAFC", anchor="lm")
    draw.text((430, 1005), en_text, font=fonts["sub_en"], fill="#94A3B8", anchor="lm")

# Test 1: 3D Clip Zoomed on Bé O with Egg & Cow action
base_3d = Image.open("snaptik_frames/frame_0050.png").convert("RGBA")
# 16:9 crop on Bé O
crop_o = base_3d.crop((40, 140, 40 + 1422, 140 + 800)).resize((W, H), Image.Resampling.LANCZOS)
d_o = ImageDraw.Draw(crop_o)
# Floating glass card on right
d_o.rounded_rectangle([1180, 100, 1860, 870], radius=28, fill=(255, 255, 255, 245), outline="#EF4444", width=4)
d_o.text((1520, 160), "BÉ O TRÒN XOE", font=fonts["title"], fill="#DC2626", anchor="mm")
d_o.text((1520, 210), "Nguyên âm đơn /ɔ/ • Môi mở tròn to", font=fonts["h3"], fill="#64748B", anchor="mm")
# Bouncing Egg
egg_im = ASSETS["egg"].resize((180, 180))
crop_o.paste(egg_im, (1430, 250), egg_im)
d_o.text((1520, 460), "Tròn vo như quả trứng gà!", font=fonts["h2"], fill="#D97706", anchor="mm")
# Word Cow
d_o.rounded_rectangle([1220, 520, 1820, 810], radius=20, fill="#FEF2F2", outline="#EF4444", width=3)
cow_im = ASSETS["cow"].resize((180, 180))
crop_o.paste(cow_im, (1240, 570), cow_im)
d_o.text((1580, 610), "TỪ VỰNG A1", font=fonts["badge"], fill="#EF4444", anchor="mm")
d_o.text((1580, 680), "CON BÒ", font=fonts["title"], fill="#1E293B", anchor="mm")
d_o.text((1580, 750), "O ... O ... BÒ!", font=fonts["h2"], fill="#DC2626", anchor="mm")
# Halo & label directly above 3D character Bé O
d_o.rounded_rectangle([260, 80, 540, 140], radius=15, fill="#EF4444", outline="#FCA5A5", width=3)
d_o.text((400, 110), "Bé O Đang Nói", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
draw_subtitle_bar(d_o, "Tớ là Bé O! Tròn vo như quả trứng gà, có trong CON BÒ nè!", "I am Bé O! Round like an egg, found in CON BÒ!", "Bé O", "#EF4444")
crop_o.save("test_3d_actions_preview/preview_3d_o.png")
print("Saved preview_3d_o.png")

# Test 2: 3D Clip Zoomed on Bé Ô with Falling Magic Hat & Teacher action
crop_oe = base_3d.crop((249, 140, 249 + 1422, 140 + 800)).resize((W, H), Image.Resampling.LANCZOS)
d_oe = ImageDraw.Draw(crop_oe)
# Floating glass card on right
d_oe.rounded_rectangle([1180, 100, 1860, 870], radius=28, fill=(255, 255, 255, 245), outline="#10B981", width=4)
d_oe.text((1520, 160), "BÉ Ô ĐỘI MŨ", font=fonts["title"], fill="#059669", anchor="mm")
d_oe.text((1520, 210), "Nguyên âm đơn /o/ • Chu môi nhô trước", font=fonts["h3"], fill="#64748B", anchor="mm")
# Hat action
hat_im = ASSETS["hat"].resize((180, 180))
crop_oe.paste(hat_im, (1430, 250), hat_im)
d_oe.text((1520, 460), "Chiếc mũ chóp nhọn cực xinh!", font=fonts["h2"], fill="#059669", anchor="mm")
# Word Teacher
d_oe.rounded_rectangle([1220, 520, 1820, 810], radius=20, fill="#ECFDF5", outline="#10B981", width=3)
tch_im = ASSETS["teacher"].resize((180, 180))
crop_oe.paste(tch_im, (1240, 570), tch_im)
d_oe.text((1580, 610), "TỪ VỰNG A1", font=fonts["badge"], fill="#10B981", anchor="mm")
d_oe.text((1580, 680), "CÔ GIÁO", font=fonts["title"], fill="#1E293B", anchor="mm")
d_oe.text((1580, 750), "Ô ... Ô ... CÔ!", font=fonts["h2"], fill="#059669", anchor="mm")
# Sparkles on top of Bé Ô's head
d_oe.rounded_rectangle([260, 80, 540, 140], radius=15, fill="#10B981", outline="#6EE7B7", width=3)
d_oe.text((400, 110), "Bé Ô Đang Nói", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
draw_subtitle_bar(d_oe, "Còn tớ là Bé Ô! Tớ có chiếc mũ chóp nhọn, có trong CÔ GIÁO nè!", "And I am Bé Ô! I have a pointy hat, found in CÔ GIÁO!", "Bé Ô", "#10B981")
crop_oe.save("test_3d_actions_preview/preview_3d_oe.png")
print("Saved preview_3d_oe.png")

# Test 3: 3D Clip Zoomed on Bé Ơ with Hook & Avocado action
crop_ow = base_3d.crop((458, 140, 458 + 1422, 140 + 800)).resize((W, H), Image.Resampling.LANCZOS)
d_ow = ImageDraw.Draw(crop_ow)
# Floating glass card on left (since Bé Ơ is on right)
d_ow.rounded_rectangle([60, 100, 740, 870], radius=28, fill=(255, 255, 255, 245), outline="#F59E0B", width=4)
d_ow.text((400, 160), "BÉ Ơ CÓ RÂU", font=fonts["title"], fill="#D97706", anchor="mm")
d_ow.text((400, 210), "Nguyên âm đơn /ɤ/ • Mép dẹt ngang", font=fonts["h3"], fill="#64748B", anchor="mm")
# Hook action
hook_im = ASSETS["hook"].resize((180, 180))
crop_ow.paste(hook_im, (310, 250), hook_im)
d_ow.text((400, 460), "Chiếc râu móc bên phải đáng yêu!", font=fonts["h2"], fill="#D97706", anchor="mm")
# Word Avocado
d_ow.rounded_rectangle([100, 520, 700, 810], radius=20, fill="#FFFBEB", outline="#F59E0B", width=3)
avo_im = ASSETS["avocado"].resize((180, 180))
crop_ow.paste(avo_im, (120, 570), avo_im)
d_ow.text((460, 610), "TỪ VỰNG A1", font=fonts["badge"], fill="#F59E0B", anchor="mm")
d_ow.text((460, 680), "QUẢ BƠ", font=fonts["title"], fill="#1E293B", anchor="mm")
d_ow.text((460, 750), "Ơ ... Ơ ... BƠ!", font=fonts["h2"], fill="#D97706", anchor="mm")
# Label above Bé Ơ
d_ow.rounded_rectangle([1380, 80, 1660, 140], radius=15, fill="#F59E0B", outline="#FCD34D", width=3)
d_ow.text((1520, 110), "Bé Ơ Đang Nói", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
draw_subtitle_bar(d_ow, "Hihi, tớ là Bé Ơ! Tớ có chiếc râu móc bên phải, có trong QUẢ BƠ nè!", "Hihi, I am Bé Ơ! I have a hook on the right, found in QUẢ BƠ!", "Bé Ơ", "#F59E0B")
crop_ow.save("test_3d_actions_preview/preview_3d_ow.png")
print("Saved preview_3d_ow.png")

# Test 4: Wide 3D Stage with Magic Transformation
wide_3d = base_3d.copy()
d_w = ImageDraw.Draw(wide_3d)
d_w.rounded_rectangle([360, 50, 1560, 150], radius=25, fill=(255, 255, 255, 240), outline="#3B82F6", width=4)
d_w.text((960, 100), "CỖ MÁY BIẾN HÌNH CHỮ CÁI KỲ DIỆU", font=fonts["title"], fill="#1D4ED8", anchor="mm")
# Arrow pointing and hat above Bé Ô
hat_sm = ASSETS["hat"].resize((120, 120))
wide_3d.paste(hat_sm, (990, 240), hat_sm)
d_w.text((1050, 200), "BOONG! Thêm mũ = Ô", font=fonts["h3"], fill="#059669", anchor="mm")
# Hook above Bé Ơ
hook_sm = ASSETS["hook"].resize((120, 120))
wide_3d.paste(hook_sm, (1510, 240), hook_sm)
d_w.text((1570, 200), "VÍU! Thêm râu = Ơ", font=fonts["h3"], fill="#D97706", anchor="mm")
draw_subtitle_bar(d_w, "Thêm chiếc mũ nhọn là thành Ô! Thêm chiếc râu móc là thành Ơ!", "Add a pointy hat is Ô! Add a whisker hook is Ơ!", "Bộ Ba O - Ô - Ơ", "#3B82F6")
wide_3d.save("test_3d_actions_preview/preview_3d_magic.png")
print("Saved preview_3d_magic.png")
