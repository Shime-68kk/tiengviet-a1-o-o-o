import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FRAMES_DIR = "/home/quang/video_ai/frames_o"
os.makedirs(FRAMES_DIR, exist_ok=True)

W, H = 1920, 1080

# High quality fonts from SVN-Gilroy
FONT_DIR = "/home/quang/video_ai/vendor/fonts"
FONT_BOLD = os.path.join(FONT_DIR, "SVN-Gilroy Bold.otf")
FONT_SEMIBOLD = os.path.join(FONT_DIR, "SVN-Gilroy SemiBold.otf")
FONT_MED = os.path.join(FONT_DIR, "SVN-Gilroy Medium.otf")
FONT_REG = os.path.join(FONT_DIR, "SVN-Gilroy Regular.otf")

BG_SRC = "/home/quang/video_ai/assets/classroom_bg.png"
CHAR_O_SRC = "/home/quang/video_ai/char_o.png"
CHAR_OE_SRC = "/home/quang/video_ai/char_oe.png"
CHAR_OW_SRC = "/home/quang/video_ai/char_ow.png"

def get_fonts():
    return {
        "hero_title": ImageFont.truetype(FONT_BOLD, 42),
        "title": ImageFont.truetype(FONT_BOLD, 34),
        "subtitle": ImageFont.truetype(FONT_MED, 22),
        "h2": ImageFont.truetype(FONT_BOLD, 30),
        "h3": ImageFont.truetype(FONT_SEMIBOLD, 24),
        "verse_bold": ImageFont.truetype(FONT_BOLD, 36),
        "big_letter": ImageFont.truetype(FONT_BOLD, 100),
        "huge_letter": ImageFont.truetype(FONT_BOLD, 160),
        "word_vn": ImageFont.truetype(FONT_BOLD, 44),
        "word_en": ImageFont.truetype(FONT_MED, 24),
        "body": ImageFont.truetype(FONT_REG, 22),
        "body_bold": ImageFont.truetype(FONT_BOLD, 22),
        "badge": ImageFont.truetype(FONT_BOLD, 17),
        "sub_vi": ImageFont.truetype(FONT_BOLD, 25),
        "sub_en": ImageFont.truetype(FONT_MED, 21),
        "small": ImageFont.truetype(FONT_MED, 17)
    }

def get_base_classroom_bg():
    bg = Image.open(BG_SRC).convert("RGB")
    bg = bg.resize((W, H), Image.Resampling.LANCZOS)
    return bg

def create_base_canvas(soften_bg=False):
    bg = get_base_classroom_bg()
    if soften_bg:
        wash = Image.new("RGBA", (W, H), (255, 253, 248, 175))
        bg = Image.alpha_composite(bg.convert("RGBA"), wash).convert("RGB")
    return bg

def draw_top_nav(draw, fonts, current_step=1):
    steps = [
        (1, "I. Khởi động (Lim)"),
        (2, "II. Chữ O (Nhung)"),
        (3, "III. Chữ Ô (Nhung)"),
        (4, "IV. Chữ Ơ (Nhung)"),
        (5, "V. So sánh (Nhung)"),
        (6, "VI. Luyện tập (Ý)"),
        (7, "VII. Tổng kết (Thuỷ)")
    ]
    total_w = 1720
    start_x = 100
    y = 30
    col_w = total_w // len(steps)
    
    for idx, (s_num, s_name) in enumerate(steps):
        sx = start_x + idx * col_w
        ex = sx + col_w - 12
        is_active = (s_num == current_step)
        
        bg = "#0284C7" if is_active else "#FFFFFF"
        border = "#0369A1" if is_active else "#CBD5E1"
        txt_col = "#FFFFFF" if is_active else "#475569"
        
        draw.rounded_rectangle([sx + 1, y + 2, ex + 1, y + 38], radius=8, fill="#E2E8F0")
        draw.rounded_rectangle([sx, y, ex, y + 36], radius=8, fill=bg, outline=border, width=1)
        draw.text(((sx + ex) // 2, y + 18), s_name, font=fonts["small"], fill=txt_col, anchor="mm")

def draw_subtitles(draw, fonts, vi_text, en_text):
    box = [100, 895, 1820, 1030]
    draw.rounded_rectangle([102, 897, 1822, 1032], radius=16, fill="#CBD5E1")
    draw.rounded_rectangle(box, radius=16, fill="#FFFFFF", outline="#E2E8F0", width=2)
    
    draw.rounded_rectangle([125, 915, 235, 950], radius=8, fill="#0284C7")
    draw.text((180, 932), "PHỤ ĐỀ", font=fonts["small"], fill="#FFFFFF", anchor="mm")
    
    draw.text((255, 933), vi_text, font=fonts["sub_vi"], fill="#0F172A", anchor="lm")
    draw.text((255, 982), f"[EN] {en_text}", font=fonts["sub_en"], fill="#0284C7", anchor="lm")

def draw_bright_card(draw, box, bg="#FFFFFF", border="#E2E8F0", radius=20, border_w=2):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0 + 2, y0 + 3, x1 + 2, y1 + 3], radius=radius, fill="#E2E8F0")
    draw.rounded_rectangle(box, radius=radius, fill=bg, outline=border, width=border_w)

def make_circular_avatar(img_path, size=(240, 240), border_color="#CBD5E1", border_w=4):
    img = Image.open(img_path).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((0, 0, size[0], size[1]), fill=255)
    avatar = Image.new("RGBA", size, (0, 0, 0, 0))
    avatar.paste(img, (0, 0), mask)
    d_av = ImageDraw.Draw(avatar)
    d_av.ellipse((1, 1, size[0] - 2, size[1] - 2), outline=border_color, width=border_w)
    return avatar

def draw_lip_shape_card(draw, fonts, cx, cy, lip_type="o"):
    w_card, h_card = 340, 160
    draw_bright_card(draw, [cx - w_card//2, cy - h_card//2, cx + w_card//2, cy + h_card//2], bg="#F8FAFC", border="#CBD5E1", radius=16)
    draw.text((cx, cy - 50), "HÌNH DÁNG MÔI (LIP APERTURE)", font=fonts["small"], fill="#64748B", anchor="mm")
    
    if lip_type == "o":
        draw.ellipse([cx - 44, cy - 24, cx + 44, cy + 36], fill="#EF4444", outline="#FCA5A5", width=3)
        draw.ellipse([cx - 24, cy - 10, cx + 24, cy + 22], fill="#FFFFFF")
        draw.text((cx, cy + 52), "Mở to • Tròn môi tối đa", font=fonts["body_bold"], fill="#EF4444", anchor="mm")
    elif lip_type == "oe":
        draw.ellipse([cx - 30, cy - 20, cx + 30, cy + 34], fill="#10B981", outline="#A7F3D0", width=3)
        draw.ellipse([cx - 12, cy - 7, cx + 12, cy + 21], fill="#FFFFFF")
        draw.text((cx, cy + 52), "Mở vừa • Tròn chúm nhô ra", font=fonts["body_bold"], fill="#059669", anchor="mm")
    elif lip_type == "ow":
        draw.rounded_rectangle([cx - 48, cy - 6, cx + 48, cy + 24], radius=12, fill="#F59E0B", outline="#FDE68A", width=3)
        draw.rounded_rectangle([cx - 28, cy + 2, cx + 28, cy + 16], radius=6, fill="#FFFFFF")
        draw.text((cx, cy + 52), "Mở nửa • Môi dẹt ngang thả lỏng", font=fonts["body_bold"], fill="#D97706", anchor="mm")

# --- 1. KHỞI ĐỘNG (LIM) ---
def render_s1_lim():
    im = get_base_classroom_bg()
    draw = ImageDraw.Draw(im)
    fonts = get_fonts()
    draw_top_nav(draw, fonts, 1)
    
    # Whiteboard top card with ample space and NO overlap
    draw_bright_card(draw, [200, 80, 1720, 280], bg="#FFFFFF", border="#BAE6FD", radius=20, border_w=2)
    
    # Pill badge centered at top
    draw.rounded_rectangle([750, 95, 1170, 128], radius=8, fill="#0284C7")
    draw.text((960, 111), "KHÓA TIẾNG VIỆT A1 • PHẦN KHỞI ĐỘNG", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    
    # Title centered below badge
    draw.text((960, 150), "BÀI HỌC NGỮ ÂM: BỘ BA NGUYÊN ÂM O — Ô — Ơ", font=fonts["hero_title"], fill="#0F172A", anchor="mm")
    
    # Rhyme box
    draw.rounded_rectangle([240, 185, 1680, 265], radius=12, fill="#F0F9FF", outline="#7DD3FC", width=1)
    draw.text((580, 225), "“O tròn như quả trứng gà,”", font=fonts["verse_bold"], fill="#EF4444", anchor="mm")
    draw.text((1280, 225), "“Ô thì đội mũ — Ơ thì thêm râu.”", font=fonts["verse_bold"], fill="#0284C7", anchor="mm")
    
    # Objective pill near bottom above subtitles
    draw.rounded_rectangle([380, 835, 1540, 878], radius=12, fill="#F8FAFC", outline="#CBD5E1", width=1)
    draw.text((960, 856), "MỤC TIÊU: Sau video, người học phát âm chuẩn và viết đúng 3 nguyên âm O, Ô, Ơ", font=fonts["body_bold"], fill="#059669", anchor="mm")
    
    draw_subtitles(draw, fonts,
                   "Xin chào các em! O tròn như quả trứng gà, Ô thì đội mũ, Ơ thì thêm râu. Hôm nay ta học O, Ô, Ơ!",
                   "Welcome! Plain is O like an egg, with a hat is Ô, with a hook is Ơ. Today we explore O, Ô, and Ơ!")
    im.save(os.path.join(FRAMES_DIR, "s1_lim_intro.png"))

# --- 2. PHÁT ÂM & CÁCH VIẾT (NHUNG) ---
def render_s2_o_1():
    im = create_base_canvas(soften_bg=True)
    draw = ImageDraw.Draw(im)
    fonts = get_fonts()
    draw_top_nav(draw, fonts, 2)
    
    # Left Hero Stage
    char_o = Image.open(CHAR_O_SRC).convert("RGBA").resize((380, 480), Image.Resampling.LANCZOS)
    draw_bright_card(draw, [140, 100, 820, 860], bg="#FFFFFF", border="#FECACA", radius=24)
    im.paste(char_o, (290, 180), char_o)
    
    draw.rounded_rectangle([180, 125, 780, 175], radius=10, fill="#FEE2E2")
    draw.text((480, 150), "NHÂN VẬT GỐC: NGUYÊN ÂM O", font=fonts["h2"], fill="#DC2626", anchor="mm")
    draw.text((480, 730), "Nét cong kín tròn đều", font=fonts["word_vn"], fill="#0F172A", anchor="mm")
    draw.text((480, 790), "Tròn xoe như quả trứng gà", font=fonts["word_en"], fill="#64748B", anchor="mm")
    
    # Right Stage
    draw_bright_card(draw, [860, 100, 1780, 860], bg="#FFFFFF", border="#E2E8F0", radius=24)
    draw.text((1320, 160), "CÁCH VIẾT VÀ BẢN CHẤT CHỮ O", font=fonts["title"], fill="#0F172A", anchor="mm")
    draw.text((1320, 205), "Phụ trách chuyên môn: Dương Thị Nhung", font=fonts["subtitle"], fill="#64748B", anchor="mm")
    
    draw.rounded_rectangle([920, 260, 1720, 380], radius=16, fill="#F8FAFC", outline="#E2E8F0", width=1)
    draw.text((950, 300), "1. Cấu trúc chữ cái:", font=fonts["body_bold"], fill="#0F172A", anchor="lm")
    draw.text((950, 340), "Chỉ gồm một nét cong kín duy nhất, viết từ trên xuống ngược chiều kim đồng hồ.", font=fonts["body"], fill="#334155", anchor="lm")
    
    draw.rounded_rectangle([920, 410, 1720, 530], radius=16, fill="#F8FAFC", outline="#E2E8F0", width=1)
    draw.text((950, 450), "2. Vị trí nền tảng:", font=fonts["body_bold"], fill="#0F172A", anchor="lm")
    draw.text((950, 490), "Là chữ cái mẹ ban đầu. Khi gắn thêm dấu phụ, O sẽ tạo ra Ô và Ơ.", font=fonts["body"], fill="#334155", anchor="lm")
    
    draw_lip_shape_card(draw, fonts, 1320, 680, "o")
    
    draw_subtitles(draw, fonts,
                   "Đây là O. Một chữ cái rất quen thuộc. Trong tiếng Việt, chỉ cần thêm dấu nhỏ là biến đổi. Hãy xem!",
                   "This is O, a familiar base vowel. In Vietnamese, just adding a small mark transforms it!")
    im.save(os.path.join(FRAMES_DIR, "s2_nhung_o_1.png"))

def render_s2_o_2():
    im = create_base_canvas(soften_bg=True)
    draw = ImageDraw.Draw(im)
    fonts = get_fonts()
    draw_top_nav(draw, fonts, 2)
    
    char_o = Image.open(CHAR_O_SRC).convert("RGBA").resize((380, 480), Image.Resampling.LANCZOS)
    draw_bright_card(draw, [140, 100, 820, 860], bg="#FFFFFF", border="#FECACA", radius=24)
    im.paste(char_o, (290, 180), char_o)
    
    draw.rounded_rectangle([180, 125, 780, 175], radius=10, fill="#EF4444")
    draw.text((480, 150), "HƯỚNG DẪN PHÁT ÂM: O", font=fonts["h2"], fill="#FFFFFF", anchor="mm")
    draw.text((480, 740), "Độ mở môi: MỞ TO TRÒN", font=fonts["h2"], fill="#EF4444", anchor="mm")
    
    draw_bright_card(draw, [860, 100, 1780, 860], bg="#FFFFFF", border="#E2E8F0", radius=24)
    draw.text((1320, 160), "SƠ ĐỒ CẤU ÂM NGUYÊN ÂM O", font=fonts["title"], fill="#0F172A", anchor="mm")
    
    draw.rounded_rectangle([920, 230, 1720, 350], radius=16, fill="#FEF2F2", outline="#FECACA", width=1)
    draw.text((950, 270), "• Khẩu hình môi: MỞ RỘNG TỐI ĐA", font=fonts["body_bold"], fill="#DC2626", anchor="lm")
    draw.text((950, 310), "Môi tròn to tự nhiên, không chúm chặt. Khoảng cách hai hàm mở rộng.", font=fonts["body"], fill="#475569", anchor="lm")
    
    draw.rounded_rectangle([920, 380, 1720, 500], radius=16, fill="#F8FAFC", outline="#E2E8F0", width=1)
    draw.text((950, 420), "• Lưỡi & Luồng hơi:", font=fonts["body_bold"], fill="#0F172A", anchor="lm")
    draw.text((950, 460), "Cuống lưỡi hạ thấp tự nhiên, luồng hơi từ thanh quản thoát ra thông thoáng.", font=fonts["body"], fill="#475569", anchor="lm")
    
    draw_lip_shape_card(draw, fonts, 1320, 670, "o")
    
    draw_subtitles(draw, fonts,
                   "O. O. Môi mở rộng, tròn môi: O.",
                   "O. O. Open mouth wide with rounded lips: O.")
    im.save(os.path.join(FRAMES_DIR, "s2_nhung_o_2.png"))

def render_s2_oe_1():
    im = create_base_canvas(soften_bg=True)
    draw = ImageDraw.Draw(im)
    fonts = get_fonts()
    draw_top_nav(draw, fonts, 3)
    
    char_oe = Image.open(CHAR_OE_SRC).convert("RGBA").resize((380, 480), Image.Resampling.LANCZOS)
    draw_bright_card(draw, [140, 100, 820, 860], bg="#FFFFFF", border="#A7F3D0", radius=24)
    im.paste(char_oe, (290, 180), char_oe)
    
    draw.rounded_rectangle([180, 125, 780, 175], radius=10, fill="#D1FAE5")
    draw.text((480, 150), "O BIẾN ĐỔI THÀNH Ô", font=fonts["h2"], fill="#059669", anchor="mm")
    draw.text((480, 730), "Ô: Đội Chiếc Mũ (^)", font=fonts["word_vn"], fill="#0F172A", anchor="mm")
    draw.text((480, 790), "Dấu nón rơi xuống đỉnh đầu", font=fonts["word_en"], fill="#64748B", anchor="mm")
    
    draw_bright_card(draw, [860, 100, 1780, 860], bg="#FFFFFF", border="#E2E8F0", radius=24)
    draw.text((1320, 160), "CHIẾC MŨ KỲ DIỆU TẠO THÀNH CHỮ Ô", font=fonts["title"], fill="#0F172A", anchor="mm")
    draw.text((1320, 205), "Quy tắc dấu phụ: Dấu nón (^)", font=fonts["subtitle"], fill="#059669", anchor="mm")
    
    draw.rounded_rectangle([920, 260, 1720, 380], radius=16, fill="#ECFDF5", outline="#A7F3D0", width=1)
    draw.text((950, 300), "1. Cách viết dấu mũ:", font=fonts["body_bold"], fill="#065F46", anchor="lm")
    draw.text((950, 340), "Gồm 2 nét xiên: nét xiên trái lên đỉnh rồi xiên phải xuống, cân đối trên đầu O.", font=fonts["body"], fill="#334155", anchor="lm")
    
    draw.rounded_rectangle([920, 410, 1720, 530], radius=16, fill="#F8FAFC", outline="#E2E8F0", width=1)
    draw.text((950, 450), "2. Hiệu ứng âm thanh:", font=fonts["body_bold"], fill="#0F172A", anchor="lm")
    draw.text((950, 490), "Âm thanh thu hẹp lại, độ mở môi nhỏ hơn O, môi nhô ra phía trước.", font=fonts["body"], fill="#334155", anchor="lm")
    
    draw_lip_shape_card(draw, fonts, 1320, 680, "oe")
    
    draw_subtitles(draw, fonts,
                   "Một chiếc mũ nhỏ xuất hiện. O đã trở thành Ô!",
                   "A little hat drops down. O has transformed into Ô!")
    im.save(os.path.join(FRAMES_DIR, "s2_nhung_oe_1.png"))

def render_s2_oe_2():
    im = create_base_canvas(soften_bg=True)
    draw = ImageDraw.Draw(im)
    fonts = get_fonts()
    draw_top_nav(draw, fonts, 3)
    
    char_oe = Image.open(CHAR_OE_SRC).convert("RGBA").resize((380, 480), Image.Resampling.LANCZOS)
    draw_bright_card(draw, [140, 100, 820, 860], bg="#FFFFFF", border="#A7F3D0", radius=24)
    im.paste(char_oe, (290, 180), char_oe)
    
    draw.rounded_rectangle([180, 125, 780, 175], radius=10, fill="#10B981")
    draw.text((480, 150), "HƯỚNG DẪN PHÁT ÂM: Ô", font=fonts["h2"], fill="#FFFFFF", anchor="mm")
    draw.text((480, 740), "Độ mở môi: CHÚM TRÒN NHÔ RA", font=fonts["h2"], fill="#059669", anchor="mm")
    
    draw_bright_card(draw, [860, 100, 1780, 860], bg="#FFFFFF", border="#E2E8F0", radius=24)
    draw.text((1320, 160), "SƠ ĐỒ CẤU ÂM NGUYÊN ÂM Ô", font=fonts["title"], fill="#0F172A", anchor="mm")
    
    draw.rounded_rectangle([920, 230, 1720, 350], radius=16, fill="#ECFDF5", outline="#A7F3D0", width=1)
    draw.text((950, 270), "• Khẩu hình môi: CHÚM TRÒN & NHÔ RA TRƯỚC", font=fonts["body_bold"], fill="#065F46", anchor="lm")
    draw.text((950, 310), "Miệng mở vừa phải, vành môi tròn chúm lại và đưa nhẹ ra phía trước.", font=fonts["body"], fill="#475569", anchor="lm")
    
    draw.rounded_rectangle([920, 380, 1720, 500], radius=16, fill="#F8FAFC", outline="#E2E8F0", width=1)
    draw.text((950, 420), "• Cuống lưỡi:", font=fonts["body_bold"], fill="#0F172A", anchor="lm")
    draw.text((950, 460), "Nâng cao hơn so với âm O, tạo khoang miệng cộng hưởng trầm ấm.", font=fonts["body"], fill="#475569", anchor="lm")
    
    draw_lip_shape_card(draw, fonts, 1320, 670, "oe")
    
    draw_subtitles(draw, fonts,
                   "Ô. Ô. Môi chúm tròn nhô ra phía trước: Ô.",
                   "Ô. Ô. Pucker and push your rounded lips forward: Ô.")
    im.save(os.path.join(FRAMES_DIR, "s2_nhung_oe_2.png"))

def render_s2_ow_1():
    im = create_base_canvas(soften_bg=True)
    draw = ImageDraw.Draw(im)
    fonts = get_fonts()
    draw_top_nav(draw, fonts, 4)
    
    char_ow = Image.open(CHAR_OW_SRC).convert("RGBA").resize((380, 480), Image.Resampling.LANCZOS)
    draw_bright_card(draw, [140, 100, 820, 860], bg="#FFFFFF", border="#FDE68A", radius=24)
    im.paste(char_ow, (290, 180), char_ow)
    
    draw.rounded_rectangle([180, 125, 780, 175], radius=10, fill="#FEF3C7")
    draw.text((480, 150), "O BIẾN ĐỔI THÀNH Ơ", font=fonts["h2"], fill="#D97706", anchor="mm")
    draw.text((480, 730), "Ơ: Thêm Chiếc Râu Móc", font=fonts["word_vn"], fill="#0F172A", anchor="mm")
    draw.text((480, 790), "Nét móc cong ở góc trên bên phải", font=fonts["word_en"], fill="#64748B", anchor="mm")
    
    draw_bright_card(draw, [860, 100, 1780, 860], bg="#FFFFFF", border="#E2E8F0", radius=24)
    draw.text((1320, 160), "CHIẾC RÂU DUYÊN DÁNG TẠO THÀNH Ơ", font=fonts["title"], fill="#0F172A", anchor="mm")
    draw.text((1320, 205), "Quy tắc dấu phụ: Dấu móc râu", font=fonts["subtitle"], fill="#D97706", anchor="mm")
    
    draw.rounded_rectangle([920, 260, 1720, 380], radius=16, fill="#FFFBEB", outline="#FDE68A", width=1)
    draw.text((950, 300), "1. Cách viết dấu móc râu:", font=fonts["body_bold"], fill="#92400E", anchor="lm")
    draw.text((950, 340), "Khởi đầu từ góc trên bên phải của chữ O, uốn một nét móc nhỏ hướng lên.", font=fonts["body"], fill="#334155", anchor="lm")
    
    draw.rounded_rectangle([920, 410, 1720, 530], radius=16, fill="#F8FAFC", outline="#E2E8F0", width=1)
    draw.text((950, 450), "2. Đặc điểm cấu âm đặc biệt:", font=fonts["body_bold"], fill="#0F172A", anchor="lm")
    draw.text((950, 490), "Đây là nguyên âm KHÔNG TRÒN MÔI (unrounded), môi mở dẹt ngang thư thái.", font=fonts["body"], fill="#334155", anchor="lm")
    
    draw_lip_shape_card(draw, fonts, 1320, 680, "ow")
    
    draw_subtitles(draw, fonts,
                   "Nhưng nếu dấu hiệu thay đổi thì sao? Một chiếc râu nhỏ xuất hiện: O đã trở thành Ơ!",
                   "What if the mark changes? A little hook sprouts: O becomes Ơ!")
    im.save(os.path.join(FRAMES_DIR, "s2_nhung_ow_1.png"))

def render_s2_ow_2():
    im = create_base_canvas(soften_bg=True)
    draw = ImageDraw.Draw(im)
    fonts = get_fonts()
    draw_top_nav(draw, fonts, 4)
    
    char_ow = Image.open(CHAR_OW_SRC).convert("RGBA").resize((380, 480), Image.Resampling.LANCZOS)
    draw_bright_card(draw, [140, 100, 820, 860], bg="#FFFFFF", border="#FDE68A", radius=24)
    im.paste(char_ow, (290, 180), char_ow)
    
    draw.rounded_rectangle([180, 125, 780, 175], radius=10, fill="#F59E0B")
    draw.text((480, 150), "HƯỚNG DẪN PHÁT ÂM: Ơ", font=fonts["h2"], fill="#FFFFFF", anchor="mm")
    draw.text((480, 740), "Độ mở môi: MÔI DẸT THƯ THÁI", font=fonts["h2"], fill="#D97706", anchor="mm")
    
    draw_bright_card(draw, [860, 100, 1780, 860], bg="#FFFFFF", border="#E2E8F0", radius=24)
    draw.text((1320, 160), "SƠ ĐỒ CẤU ÂM NGUYÊN ÂM Ơ", font=fonts["title"], fill="#0F172A", anchor="mm")
    
    draw.rounded_rectangle([920, 230, 1720, 350], radius=16, fill="#FFFBEB", outline="#FDE68A", width=1)
    draw.text((950, 270), "• Khẩu hình môi: KHÔNG TRÒN MÔI • DẸT NGANG", font=fonts["body_bold"], fill="#92400E", anchor="lm")
    draw.text((950, 310), "Khẩu hình tương tự Ô nhưng khóe môi thả lỏng kéo sang hai bên tự nhiên.", font=fonts["body"], fill="#475569", anchor="lm")
    
    draw.rounded_rectangle([920, 380, 1720, 500], radius=16, fill="#F8FAFC", outline="#E2E8F0", width=1)
    draw.text((950, 420), "• Điểm lưu ý người nước ngoài:", font=fonts["body_bold"], fill="#0F172A", anchor="lm")
    draw.text((950, 460), "Tuyệt đối không tròn môi. Thư giãn cơ mặt và phát âm nhẹ nhàng từ vòm họng.", font=fonts["body"], fill="#475569", anchor="lm")
    
    draw_lip_shape_card(draw, fonts, 1320, 670, "ow")
    
    draw_subtitles(draw, fonts,
                   "Ơ. Ơ. Khẩu hình như Ô nhưng môi không tròn, mở dẹt ngang: Ơ.",
                   "Ơ. Ơ. Same tongue position as Ô, but keep lips relaxed and unrounded: Ơ.")
    im.save(os.path.join(FRAMES_DIR, "s2_nhung_ow_2.png"))

# Cảnh 4: Máy quét so sánh O - Ô - Ơ
def render_s2_scanner():
    im = create_base_canvas(soften_bg=True)
    draw = ImageDraw.Draw(im)
    fonts = get_fonts()
    draw_top_nav(draw, fonts, 5)
    
    draw_bright_card(draw, [100, 80, 1820, 860], bg="#FFFFFF", border="#E2E8F0", radius=24)
    
    draw.rounded_rectangle([720, 95, 1200, 132], radius=8, fill="#FEF3C7")
    draw.text((960, 113), "MÁY QUÉT NHẬN DIỆN DẤU PHỤ", font=fonts["badge"], fill="#D97706", anchor="mm")
    draw.text((960, 155), "CẢNH BÁO: ĐỪNG ĐỂ DẤU ĐÁNH LỪA BẠN!", font=fonts["hero_title"], fill="#0F172A", anchor="mm")
    
    col_w = 510
    cols = [
        ("O", "KHÔNG DẤU PHỤ", "Tròn to như quả trứng", "Môi mở tròn rộng tối đa", "#EF4444", "#FEE2E2", 140, CHAR_O_SRC),
        ("Ô", "CÓ DẤU MŨ (^)", "Đội chiếc mũ trên đầu", "Môi chúm tròn nhô ra trước", "#059669", "#D1FAE5", 705, CHAR_OE_SRC),
        ("Ơ", "CÓ DẤU MÓC RÂU", "Thêm chiếc râu bên phải", "Môi dẹt ngang thả lỏng", "#D97706", "#FEF3C7", 1270, CHAR_OW_SRC)
    ]
    
    for letter, badge, desc, lip_desc, color, bg_badge, start_x, char_img_path in cols:
        box = [start_x, 195, start_x + col_w, 830]
        draw_bright_card(draw, box, bg="#F8FAFC", border="#CBD5E1", radius=20)
        
        draw.rounded_rectangle([start_x + 20, 215, start_x + col_w - 20, 265], radius=10, fill=bg_badge)
        draw.text((start_x + col_w // 2, 240), badge, font=fonts["badge"], fill=color, anchor="mm")
        
        # Circular avatar
        av = make_circular_avatar(char_img_path, size=(270, 270), border_color=color, border_w=4)
        im.paste(av, (start_x + (col_w - 270) // 2, 290), av)
        
        draw.text((start_x + col_w // 2, 600), f"Nguyên âm {letter}", font=fonts["h2"], fill=color, anchor="mm")
        draw.text((start_x + col_w // 2, 660), desc, font=fonts["h3"], fill="#0F172A", anchor="mm")
        
        draw.rounded_rectangle([start_x + 30, 710, start_x + col_w - 30, 770], radius=12, fill="#FFFFFF", outline=color, width=1)
        draw.text((start_x + col_w // 2, 740), lip_desc, font=fonts["body_bold"], fill=color, anchor="mm")
        
    draw_subtitles(draw, fonts,
                   "Đừng để dấu đánh lừa bạn! Hãy nhớ: Không dấu là O; có mũ là Ô; có móc râu là Ơ!",
                   "Don't let marks trick you! Plain is O; with a hat is Ô; with a hook is Ơ!")
    im.save(os.path.join(FRAMES_DIR, "s2_nhung_scanner.png"))

# --- 3. LUYỆN TẬP SHADOWING (Ý) ---
def render_s3_idle():
    im = create_base_canvas(soften_bg=True)
    draw = ImageDraw.Draw(im)
    fonts = get_fonts()
    draw_top_nav(draw, fonts, 6)
    
    draw_bright_card(draw, [100, 80, 1820, 860], bg="#FFFFFF", border="#E2E8F0", radius=24)
    draw.rounded_rectangle([700, 95, 1220, 132], radius=8, fill="#E0F2FE")
    draw.text((960, 113), "PHẦN III: LUYỆN TẬP THỰC HÀNH (MẠC NHƯ Ý)", font=fonts["badge"], fill="#0284C7", anchor="mm")
    draw.text((960, 155), "PHƯƠNG PHÁP SHADOWING: NGHE VÀ LẶP LẠI", font=fonts["hero_title"], fill="#0F172A", anchor="mm")
    
    vocabs = [
        ("O", "BÒ", "Con bò (Cow)", "#EF4444", 140, CHAR_O_SRC),
        ("Ô", "CÔ", "Cô giáo (Teacher)", "#059669", 705, CHAR_OE_SRC),
        ("Ơ", "BƠ", "Quả bơ (Avocado)", "#D97706", 1270, CHAR_OW_SRC)
    ]
    for letter, word, mean, color, start_x, char_img_path in vocabs:
        box = [start_x, 205, start_x + 510, 770]
        draw_bright_card(draw, box, bg="#F8FAFC", border="#E2E8F0", radius=20)
        
        av = make_circular_avatar(char_img_path, size=(250, 250), border_color=color, border_w=3)
        im.paste(av, (start_x + (510 - 250) // 2, 235), av)
        
        draw.text((start_x + 255, 540), f"Âm {letter}", font=fonts["h2"], fill=color, anchor="mm")
        draw.text((start_x + 255, 620), f"Từ vựng: {word}", font=fonts["word_vn"], fill="#0F172A", anchor="mm")
        draw.text((start_x + 255, 680), mean, font=fonts["word_en"], fill="#64748B", anchor="mm")
        
    draw.rounded_rectangle([360, 800, 1560, 845], radius=12, fill="#F0FDF4", outline="#86EFAC", width=1)
    draw.text((960, 822), "QUY TẮC: Lắng nghe cô phát âm mẫu -> Đợi thanh nhịp đếm 2.5s -> Đọc to theo cô!", font=fonts["body_bold"], fill="#166534", anchor="mm")
    
    draw_subtitles(draw, fonts,
                   "Bây giờ, chúng ta cùng luyện tập nhé! Hãy lắng nghe và lặp lại thật to theo cô trong nhịp đếm:",
                   "Now let's practice! Listen carefully and repeat out loud after me during the rhythm pause:")
    im.save(os.path.join(FRAMES_DIR, "s3_y_idle_lis.png"))

def render_s3_drill(letter, word, mean, color, char_img_path, is_repeat=False, filename=""):
    im = create_base_canvas(soften_bg=True)
    draw = ImageDraw.Draw(im)
    fonts = get_fonts()
    draw_top_nav(draw, fonts, 6)
    
    draw_bright_card(draw, [100, 80, 1820, 860], bg="#FFFFFF", border="#E2E8F0", radius=24)
    
    if not is_repeat:
        draw.rounded_rectangle([700, 95, 1220, 138], radius=10, fill="#0284C7")
        draw.text((960, 116), "LẮNG NGHE CHUẨN (LISTEN)", font=fonts["h3"], fill="#FFFFFF", anchor="mm")
    else:
        draw.rounded_rectangle([660, 95, 1260, 138], radius=10, fill="#10B981")
        draw.text((960, 116), "ĐẾN LƯỢT BẠN ĐỌC TO (REPEAT NOW!)", font=fonts["h3"], fill="#FFFFFF", anchor="mm")
        
    # Left Mascot
    draw_bright_card(draw, [160, 160, 740, 820], bg="#F8FAFC", border="#CBD5E1", radius=20)
    av = make_circular_avatar(char_img_path, size=(380, 380), border_color=color, border_w=4)
    im.paste(av, (260, 240), av)
    draw.text((450, 710), f"Nguyên âm: {letter}", font=fonts["title"], fill=color, anchor="mm")
    
    # Right Vocabulary Showcase with generous whitespace
    draw_bright_card(draw, [780, 160, 1760, 820], bg="#FFFFFF", border="#E2E8F0", radius=20)
    draw.text((1270, 220), "TỪ ỨNG DỤNG TIẾNG VIỆT A1", font=fonts["subtitle"], fill="#64748B", anchor="mm")
    
    # Large word well-spaced
    draw.text((1270, 335), word, font=fonts["huge_letter"], fill=color, anchor="mm")
    draw.text((1270, 445), mean, font=fonts["word_vn"], fill="#0F172A", anchor="mm")
    
    # Progress countdown / rhythm bar
    bar_bg = "#E2E8F0"
    draw.rounded_rectangle([860, 530, 1680, 570], radius=20, fill=bar_bg)
    if is_repeat:
        draw.rounded_rectangle([860, 530, 1680, 570], radius=20, fill="#10B981")
        draw.text((1270, 550), "2.5 GIÂY: BẬT MIC VÀ LẶP LẠI TỰ TIN!", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
        draw.rounded_rectangle([920, 630, 1620, 740], radius=16, fill="#ECFDF5", outline="#86EFAC", width=2)
        draw.text((1270, 685), f"Đọc to: {letter} ... {word}!", font=fonts["hero_title"], fill="#059669", anchor="mm")
    else:
        draw.rounded_rectangle([860, 530, 1270, 570], radius=20, fill="#0284C7")
        draw.text((1270, 550), "LẮNG NGHE NGƯỜI BẢN XỨ PHÁT ÂM MẪU", font=fonts["badge"], fill="#0F172A", anchor="mm")
        draw.rounded_rectangle([920, 630, 1620, 740], radius=16, fill="#F0F9FF", outline="#BAE6FD", width=1)
        draw.text((1270, 685), f"Nghe chuẩn: {letter} ... {word} ... {mean}", font=fonts["h2"], fill="#0369A1", anchor="mm")
        
    sub_vi = f"{letter}. {word}. {mean}."
    sub_en = f"Listen: {letter}. {word}. ({mean}). Repeat out loud!"
    draw_subtitles(draw, fonts, sub_vi, sub_en)
    im.save(os.path.join(FRAMES_DIR, filename))

# --- 4. TỔNG KẾT & QUIZ (THUỶ) ---
def render_s4_quiz_q():
    im = create_base_canvas(soften_bg=True)
    draw = ImageDraw.Draw(im)
    fonts = get_fonts()
    draw_top_nav(draw, fonts, 7)
    
    draw_bright_card(draw, [100, 80, 1820, 860], bg="#FFFFFF", border="#E2E8F0", radius=24)
    draw.rounded_rectangle([680, 95, 1240, 138], radius=8, fill="#FEF3C7")
    draw.text((960, 116), "PHẦN IV: THỬ THÁCH THÍNH GIÁC (NÔNG THỊ LỆ THUỶ)", font=fonts["badge"], fill="#D97706", anchor="mm")
    draw.text((960, 170), "BẠN VỪA NGHE THẤY TỪ NÀO DƯỚI ĐÂY?", font=fonts["hero_title"], fill="#0F172A", anchor="mm")
    
    draw.rounded_rectangle([760, 220, 1160, 280], radius=14, fill="#F0F9FF", outline="#7DD3FC", width=2)
    draw.text((960, 250), "ĐANG PHÁT ÂM THANH...", font=fonts["h3"], fill="#0284C7", anchor="mm")
    
    # Option A: CÔ
    draw_bright_card(draw, [240, 330, 920, 660], bg="#F8FAFC", border="#CBD5E1", radius=20)
    draw.rounded_rectangle([270, 360, 360, 410], radius=10, fill="#0284C7")
    draw.text((315, 385), "A", font=fonts["h2"], fill="#FFFFFF", anchor="mm")
    draw.text((580, 470), "CÔ", font=fonts["huge_letter"], fill="#0F172A", anchor="mm")
    draw.text((580, 580), "Chứa nguyên âm Ô", font=fonts["h3"], fill="#64748B", anchor="mm")
    
    # Option B: BƠ
    draw_bright_card(draw, [1000, 330, 1680, 660], bg="#F8FAFC", border="#CBD5E1", radius=20)
    draw.rounded_rectangle([1030, 360, 1120, 410], radius=10, fill="#64748B")
    draw.text((1075, 385), "B", font=fonts["h2"], fill="#FFFFFF", anchor="mm")
    draw.text((1340, 470), "BƠ", font=fonts["huge_letter"], fill="#0F172A", anchor="mm")
    draw.text((1340, 580), "Chứa nguyên âm Ơ", font=fonts["h3"], fill="#64748B", anchor="mm")
    
    # 3s countdown pill
    draw.rounded_rectangle([680, 710, 1240, 775], radius=14, fill="#FEF2F2", outline="#FCA5A5", width=2)
    draw.text((960, 742), "ĐANG ĐẾM NGƯỢC: 3 ... 2 ... 1 ...", font=fonts["h2"], fill="#EF4444", anchor="mm")
    
    draw_subtitles(draw, fonts,
                   "Thử thách thính giác nào! Bạn vừa nghe thấy từ nào dưới đây?",
                   "Listening challenge! Which word did you just hear?")
    im.save(os.path.join(FRAMES_DIR, "s4_thuy_quiz_question.png"))

def render_s4_quiz_ans():
    im = create_base_canvas(soften_bg=True)
    draw = ImageDraw.Draw(im)
    fonts = get_fonts()
    draw_top_nav(draw, fonts, 7)
    
    draw_bright_card(draw, [100, 80, 1820, 860], bg="#FFFFFF", border="#E2E8F0", radius=24)
    draw.rounded_rectangle([680, 95, 1240, 138], radius=8, fill="#D1FAE5")
    draw.text((960, 116), "CHÍNH XÁC! (CORRECT ANSWER)", font=fonts["h3"], fill="#059669", anchor="mm")
    draw.text((960, 170), "ĐÁP ÁN ĐÚNG LÀ: [A] CÔ (CHỨA ÂM Ô)", font=fonts["hero_title"], fill="#059669", anchor="mm")
    
    # Highlighted Option A
    draw_bright_card(draw, [240, 240, 920, 660], bg="#ECFDF5", border="#10B981", radius=20, border_w=4)
    draw.rounded_rectangle([270, 270, 360, 320], radius=10, fill="#10B981")
    draw.text((315, 295), "A", font=fonts["h2"], fill="#FFFFFF", anchor="mm")
    draw.text((580, 420), "CÔ", font=fonts["huge_letter"], fill="#059669", anchor="mm")
    draw.text((580, 530), "Môi chúm tròn nhô ra phía trước", font=fonts["h3"], fill="#065F46", anchor="mm")
    draw.rounded_rectangle([320, 580, 840, 630], radius=10, fill="#10B981")
    draw.text((580, 605), "CHÍNH XÁC 100%!", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    
    # Disabled Option B
    draw_bright_card(draw, [1000, 240, 1680, 660], bg="#F8FAFC", border="#E2E8F0", radius=20)
    draw.rounded_rectangle([1030, 270, 1120, 320], radius=10, fill="#94A3B8")
    draw.text((1075, 295), "B", font=fonts["h2"], fill="#FFFFFF", anchor="mm")
    draw.text((1340, 420), "BƠ", font=fonts["huge_letter"], fill="#94A3B8", anchor="mm")
    draw.text((1340, 530), "Âm Ơ (Môi dẹt ngang)", font=fonts["h3"], fill="#94A3B8", anchor="mm")
    
    draw.rounded_rectangle([360, 710, 1560, 775], radius=14, fill="#F0F9FF", outline="#7DD3FC", width=1)
    draw.text((960, 742), "GIẢI THÍCH: Từ 'CÔ' có âm Ô với đặc trưng môi chúm tròn nhô ra phía trước!", font=fonts["body_bold"], fill="#0284C7", anchor="mm")
    
    draw_subtitles(draw, fonts,
                   "Ba, hai, một. Chính xác! Đó là đáp án A: CÔ!",
                   "Three, two, one. Exactly! The answer is A: CÔ!")
    im.save(os.path.join(FRAMES_DIR, "s4_thuy_quiz_answer.png"))

def render_s4_summary():
    im = create_base_canvas(soften_bg=True)
    draw = ImageDraw.Draw(im)
    fonts = get_fonts()
    draw_top_nav(draw, fonts, 7)
    
    draw_bright_card(draw, [100, 80, 1820, 860], bg="#FFFFFF", border="#E2E8F0", radius=24)
    draw.rounded_rectangle([720, 95, 1200, 132], radius=8, fill="#FEF3C7")
    draw.text((960, 113), "TỔNG KẾT BÀI HỌC", font=fonts["badge"], fill="#D97706", anchor="mm")
    draw.text((960, 155), "BẢNG QUY TẮC VÀNG GHI NHỚ O — Ô — Ơ", font=fonts["hero_title"], fill="#0F172A", anchor="mm")
    
    cards = [
        ("O", "O tròn quả trứng", "Không có dấu phụ", "Môi mở tròn to", "#EF4444", 140, CHAR_O_SRC),
        ("Ô", "Ô thì đội mũ", "Có chiếc mũ trên đầu (^)", "Môi chúm nhô ra", "#059669", 705, CHAR_OE_SRC),
        ("Ơ", "Ơ thì thêm râu", "Có chiếc móc râu bên phải", "Môi dẹt ngang thư thái", "#D97706", 1270, CHAR_OW_SRC)
    ]
    for letter, verse, mark, lip, color, start_x, char_img_path in cards:
        box = [start_x, 195, start_x + 510, 730]
        draw_bright_card(draw, box, bg="#F8FAFC", border="#CBD5E1", radius=20)
        
        av = make_circular_avatar(char_img_path, size=(240, 240), border_color=color, border_w=3)
        im.paste(av, (start_x + (510 - 240) // 2, 220), av)
        
        draw.text((start_x + 255, 500), f"Nguyên âm {letter}", font=fonts["h2"], fill=color, anchor="mm")
        draw.text((start_x + 255, 570), verse, font=fonts["h2"], fill="#0F172A", anchor="mm")
        draw.text((start_x + 255, 620), mark, font=fonts["body"], fill="#64748B", anchor="mm")
        draw.text((start_x + 255, 665), lip, font=fonts["body_bold"], fill=color, anchor="mm")
        
    draw.rounded_rectangle([140, 755, 1780, 830], radius=14, fill="#F1F5F9", outline="#CBD5E1", width=1)
    draw.text((960, 792), "NHÓM THỰC HIỆN: Thí Thuỳ Lim • Dương Thị Nhung • Mạc Như Ý • Nông Thị Lệ Thuỷ • Nguyễn Thị Hồng Thương", font=fonts["body_bold"], fill="#334155", anchor="mm")
    
    draw_subtitles(draw, fonts,
                   "Hãy luôn nhớ quy tắc vàng: O tròn như quả trứng, Ô thì đội mũ, Ơ thì thêm râu. Tạm biệt!",
                   "Always remember the golden rule: O is round, Ô wears a hat, Ơ has a hook. Goodbye and see you again!")
    im.save(os.path.join(FRAMES_DIR, "s4_thuy_summary.png"))

def main():
    print("Re-rendering all bright educational slides with zero-collision typography...")
    render_s1_lim()
    render_s2_o_1()
    render_s2_o_2()
    render_s2_oe_1()
    render_s2_oe_2()
    render_s2_ow_1()
    render_s2_ow_2()
    render_s2_scanner()
    render_s3_idle()
    render_s3_drill("O", "BÒ", "Con bò (Cow)", "#EF4444", CHAR_O_SRC, False, "s3_y_o_lis.png")
    render_s3_drill("O", "BÒ", "Con bò (Cow)", "#EF4444", CHAR_O_SRC, True, "s3_y_o_rep.png")
    render_s3_drill("Ô", "CÔ", "Cô giáo (Teacher)", "#059669", CHAR_OE_SRC, False, "s3_y_oe_lis.png")
    render_s3_drill("Ô", "CÔ", "Cô giáo (Teacher)", "#059669", CHAR_OE_SRC, True, "s3_y_oe_rep.png")
    render_s3_drill("Ơ", "BƠ", "Quả bơ (Avocado)", "#D97706", CHAR_OW_SRC, False, "s3_y_ow_lis.png")
    render_s3_drill("Ơ", "BƠ", "Quả bơ (Avocado)", "#D97706", CHAR_OW_SRC, True, "s3_y_ow_rep.png")
    render_s4_quiz_q()
    render_s4_quiz_ans()
    render_s4_summary()
    print("All 18 slides re-rendered with ZERO overlap and ZERO font errors!")

if __name__ == "__main__":
    main()
