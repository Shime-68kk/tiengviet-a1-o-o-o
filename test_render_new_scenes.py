import os
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

# Assets
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

os.makedirs("test_scenes_preview", exist_ok=True)

def draw_subtitle_bar(draw, vi_text, en_text, speaker_name, speaker_color):
    draw.rounded_rectangle([180, 910, 1740, 1040], radius=24, fill=(15, 23, 42, 230), outline="#475569", width=2)
    draw.rounded_rectangle([210, 930, 390, 975], radius=12, fill=speaker_color)
    draw.text((300, 952), speaker_name, font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    draw.text((420, 952), vi_text, font=fonts["sub_vi"], fill="#F8FAFC", anchor="lm")
    draw.text((420, 1005), en_text, font=fonts["sub_en"], fill="#94A3B8", anchor="lm")

# Test 1: Solo Bé O with Egg & Cow
im_o = Image.open("frames_1w/f_0180.png").resize((W, H), Image.Resampling.LANCZOS)
d_o = ImageDraw.Draw(im_o)
# Floating right card
d_o.rounded_rectangle([1220, 120, 1860, 860], radius=28, fill=(255, 255, 255, 245), outline="#EF4444", width=4)
d_o.text((1540, 180), "BÉ O TRÒN XOE", font=fonts["title"], fill="#DC2626", anchor="mm")
d_o.text((1540, 230), "Nguyên âm đơn /ɔ/ • Tròn môi mở", font=fonts["h3"], fill="#64748B", anchor="mm")
# Egg image
egg_resized = ASSETS["egg"].resize((200, 200))
im_o.paste(egg_resized, (1440, 280), egg_resized)
d_o.text((1540, 510), "Tròn như quả trứng gà!", font=fonts["h2"], fill="#D97706", anchor="mm")
# Cow card below
d_o.rounded_rectangle([1260, 570, 1820, 810], radius=20, fill="#FEF2F2", outline="#EF4444", width=3)
cow_resized = ASSETS["cow"].resize((180, 180))
im_o.paste(cow_resized, (1280, 600), cow_resized)
d_o.text((1600, 650), "TỪ VỰNG A1", font=fonts["badge"], fill="#EF4444", anchor="mm")
d_o.text((1600, 720), "CON BÒ 🐮", font=fonts["title"], fill="#1E293B", anchor="mm")
draw_subtitle_bar(d_o, "Tớ là Bé O! Tròn vo như quả trứng gà, có trong CON BÒ nè!", "I am Bé O! Round like an egg, found in CON BÒ!", "Bé O", "#EF4444")
im_o.save("test_scenes_preview/preview_scene_o.png")
print("Saved preview_scene_o.png")

# Test 2: Solo Bé Ô with Hat & Teacher
im_oe = Image.open("frames_1w/f_0380.png").resize((W, H), Image.Resampling.LANCZOS)
d_oe = ImageDraw.Draw(im_oe)
d_oe.rounded_rectangle([1220, 120, 1860, 860], radius=28, fill=(255, 255, 255, 245), outline="#10B981", width=4)
d_oe.text((1540, 180), "BÉ Ô ĐỘI MŨ", font=fonts["title"], fill="#059669", anchor="mm")
d_oe.text((1540, 230), "Nguyên âm đơn /o/ • Chu môi nhô", font=fonts["h3"], fill="#64748B", anchor="mm")
hat_resized = ASSETS["hat"].resize((200, 200))
im_oe.paste(hat_resized, (1440, 280), hat_resized)
d_oe.text((1540, 510), "Chiếc mũ chóp nhọn cực xinh!", font=fonts["h2"], fill="#059669", anchor="mm")
d_oe.rounded_rectangle([1260, 570, 1820, 810], radius=20, fill="#ECFDF5", outline="#10B981", width=3)
tch_resized = ASSETS["teacher"].resize((180, 180))
im_oe.paste(tch_resized, (1280, 600), tch_resized)
d_oe.text((1600, 650), "TỪ VỰNG A1", font=fonts["badge"], fill="#10B981", anchor="mm")
d_oe.text((1600, 720), "CÔ GIÁO 👩‍🏫", font=fonts["title"], fill="#1E293B", anchor="mm")
draw_subtitle_bar(d_oe, "Tớ là Bé Ô! Tớ đội chiếc mũ chóp nhọn, có trong CÔ GIÁO nè!", "I am Bé Ô! I wear a pointy hat, found in CÔ GIÁO!", "Bé Ô", "#10B981")
im_oe.save("test_scenes_preview/preview_scene_oe.png")
print("Saved preview_scene_oe.png")

# Test 3: Solo Bé Ơ with Hook & Avocado
im_ow = Image.open("frames_1w/f_0580.png").resize((W, H), Image.Resampling.LANCZOS)
d_ow = ImageDraw.Draw(im_ow)
# Left card because Bé Ơ is on right
d_ow.rounded_rectangle([60, 120, 700, 860], radius=28, fill=(255, 255, 255, 245), outline="#F59E0B", width=4)
d_ow.text((380, 180), "BÉ Ơ CÓ RÂU", font=fonts["title"], fill="#D97706", anchor="mm")
d_ow.text((380, 230), "Nguyên âm đơn /ɤ/ • Mép dẹt ngang", font=fonts["h3"], fill="#64748B", anchor="mm")
hook_resized = ASSETS["hook"].resize((200, 200))
im_ow.paste(hook_resized, (280, 280), hook_resized)
d_ow.text((380, 510), "Chiếc râu móc bên phải đáng yêu!", font=fonts["h2"], fill="#D97706", anchor="mm")
d_ow.rounded_rectangle([100, 570, 660, 810], radius=20, fill="#FFFBEB", outline="#F59E0B", width=3)
avo_resized = ASSETS["avocado"].resize((180, 180))
im_ow.paste(avo_resized, (120, 600), avo_resized)
d_ow.text((440, 650), "TỪ VỰNG A1", font=fonts["badge"], fill="#F59E0B", anchor="mm")
d_ow.text((440, 720), "QUẢ BƠ 🥑", font=fonts["title"], fill="#1E293B", anchor="mm")
draw_subtitle_bar(d_ow, "Tớ là Bé Ơ! Tớ có chiếc râu móc bên phải, có trong QUẢ BƠ nè!", "I am Bé Ơ! I have a hook on the right, found in QUẢ BƠ!", "Bé Ơ", "#F59E0B")
im_ow.save("test_scenes_preview/preview_scene_ow.png")
print("Saved preview_scene_ow.png")

print("All preview scenes rendered successfully!")
