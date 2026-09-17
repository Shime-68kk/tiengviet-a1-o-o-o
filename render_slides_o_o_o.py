import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FRAMES_DIR = "/home/quang/video_ai/frames_o"
ASSETS_DIR = "/home/quang/video_ai/assets"
os.makedirs(FRAMES_DIR, exist_ok=True)

W, H = 1920, 1080

FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

def get_fonts():
    return {
        "title": ImageFont.truetype(FONT_BOLD, 42),
        "subtitle": ImageFont.truetype(FONT_BOLD, 22),
        "h2": ImageFont.truetype(FONT_BOLD, 36),
        "h3": ImageFont.truetype(FONT_BOLD, 28),
        "big_letter": ImageFont.truetype(FONT_BOLD, 120),
        "huge_letter": ImageFont.truetype(FONT_BOLD, 160),
        "hero_letter": ImageFont.truetype(FONT_BOLD, 220),
        "word_vn": ImageFont.truetype(FONT_BOLD, 54),
        "word_en": ImageFont.truetype(FONT_REG, 26),
        "body": ImageFont.truetype(FONT_REG, 24),
        "body_bold": ImageFont.truetype(FONT_BOLD, 24),
        "badge": ImageFont.truetype(FONT_BOLD, 20),
        "sub_vi": ImageFont.truetype(FONT_BOLD, 26),
        "sub_en": ImageFont.truetype(FONT_REG, 22),
        "small": ImageFont.truetype(FONT_REG, 18),
        "quiz_opt": ImageFont.truetype(FONT_BOLD, 30)
    }

# Load Mascot Cards
CARD_O = Image.open(os.path.join(ASSETS_DIR, "card_o.png")).convert("RGBA")
CARD_OE = Image.open(os.path.join(ASSETS_DIR, "card_oe.png")).convert("RGBA")
CARD_OW = Image.open(os.path.join(ASSETS_DIR, "card_ow.png")).convert("RGBA")

# Load Classroom Background
BG_PATH = os.path.join(ASSETS_DIR, "bg_kindergarten_soft.png")
if not os.path.exists(BG_PATH):
    BG_PATH = os.path.join(ASSETS_DIR, "bg_kindergarten_1080p.png")

BASE_BG = Image.open(BG_PATH).convert("RGBA").resize((W, H), Image.Resampling.LANCZOS)

def create_kindergarten_canvas():
    canvas = BASE_BG.copy()
    overlay = Image.new("RGBA", (W, H), (255, 253, 248, 205))
    canvas = Image.alpha_composite(canvas, overlay)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle([20, 20, W - 20, H - 20], radius=24, outline="#E2E8F0", width=2)
    return canvas

def draw_top_nav(draw, fonts, current_step=1):
    steps = [
        (1, "I. Khởi Động"),
        (2, "II. Bé O Tròn"),
        (3, "III. Bé Ô Mũ"),
        (4, "IV. Bé Ơ Râu"),
        (5, "V. Phép Biến Hình"),
        (6, "VI. Luyện Tập"),
        (7, "VII. Đố Vui & Tổng Kết")
    ]
    
    total_w = 1720
    start_x = 100
    y = 35
    col_w = total_w // len(steps)
    
    for idx, (s_num, s_name) in enumerate(steps):
        sx = start_x + idx * col_w
        ex = sx + col_w - 12
        is_active = (s_num == current_step)
        is_past = (s_num < current_step)
        
        bg = "#EF4444" if (is_active and s_num in (1,2)) else \
             ("#10B981" if (is_active and s_num in (3,5)) else \
             ("#F59E0B" if (is_active and s_num in (4,7)) else \
             ("#3B82F6" if is_active else \
             ("#F1F5F9" if is_past else "#FFFFFF"))))
             
        border = bg if is_active else ("#CBD5E1" if is_past else "#E2E8F0")
        txt_col = "#FFFFFF" if is_active else ("#475569" if is_past else "#94A3B8")
        
        draw.rounded_rectangle([sx, y, ex, y + 42], radius=12, fill=bg, outline=border, width=2)
        draw.text(((sx + ex) // 2, y + 21), s_name, font=fonts["subtitle"], fill=txt_col, anchor="mm")

def draw_subtitles(draw, fonts, vi_text, en_text):
    box = [100, 895, 1820, 1035]
    draw.rounded_rectangle(box, radius=18, fill=(255, 255, 255, 245), outline="#CBD5E1", width=2)
    draw.rounded_rectangle([130, 915, 260, 955], radius=10, fill="#EF4444")
    draw.text((195, 935), "LỜI THOẠI", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    draw.text((285, 935), vi_text, font=fonts["sub_vi"], fill="#0F172A", anchor="lm")
    draw.text((285, 990), f"[EN] {en_text}", font=fonts["sub_en"], fill="#0284C7", anchor="lm")

def draw_card(draw, box, bg=(255, 255, 255, 245), border="#E2E8F0", border_width=2, radius=20):
    draw.rounded_rectangle(box, radius=radius, fill=bg, outline=border, width=border_width)

def draw_lip_shape(draw, fonts, cx, cy, lip_type="o"):
    draw.rounded_rectangle([cx - 195, cy - 130, cx + 195, cy + 130], radius=18, fill="#F8FAFC", outline="#E2E8F0", width=2)
    draw.text((cx, cy - 90), "HÌNH DÁNG KHẨU HÌNH", font=fonts["badge"], fill="#64748B", anchor="mm")
    
    if lip_type == "o":
        draw.ellipse([cx - 65, cy - 40, cx + 65, cy + 40], fill="#EF4444", outline="#FCA5A5", width=4)
        draw.ellipse([cx - 38, cy - 22, cx + 38, cy + 22], fill="#FFFFFF")
        draw.text((cx, cy + 85), "Môi mở to, tròn vành (/ɔ/)", font=fonts["body_bold"], fill="#DC2626", anchor="mm")
    elif lip_type == "oe":
        draw.ellipse([cx - 48, cy - 32, cx + 48, cy + 32], fill="#10B981", outline="#6EE7B7", width=4)
        draw.ellipse([cx - 24, cy - 16, cx + 24, cy + 16], fill="#FFFFFF")
        draw.line([cx - 68, cy, cx - 54, cy], fill="#10B981", width=3)
        draw.line([cx + 54, cy, cx + 68, cy], fill="#10B981", width=3)
        draw.text((cx, cy + 85), "Môi khép vừa, chu nhô (/o/)", font=fonts["body_bold"], fill="#059669", anchor="mm")
    else:
        draw.ellipse([cx - 75, cy - 20, cx + 75, cy + 20], fill="#F59E0B", outline="#FCD34D", width=4)
        draw.ellipse([cx - 45, cy - 9, cx + 45, cy + 9], fill="#FFFFFF")
        draw.text((cx, cy + 85), "Môi không tròn, dẹt ngang (/ɤ/)", font=fonts["body_bold"], fill="#D97706", anchor="mm")

# 1. SCENE 1: KHỞI ĐỘNG (Thí Thuỳ Lim)
def make_frame_s1(fonts):
    im = create_kindergarten_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_nav(draw, fonts, current_step=1)
    
    draw.rounded_rectangle([700, 95, 1220, 140], radius=12, fill="#FEF2F2", outline="#EF4444", width=2)
    draw.text((960, 117), "TIẾNG VIỆT SƠ CẤP A1 • BÀI HỌC VUI NHỘN", font=fonts["badge"], fill="#DC2626", anchor="mm")
    
    draw.text((960, 180), "KHÁM PHÁ BỘ BA BẠN THÂN: O — Ô — Ơ", font=fonts["title"], fill="#0F172A", anchor="mm")
    draw.text((960, 230), "Hướng dẫn khởi động: Thí Thuỳ Lim", font=fonts["subtitle"], fill="#64748B", anchor="mm")
    
    draw_card(draw, [150, 265, 1770, 420], bg="#FFFBEB", border="#FBBF24", border_width=2)
    draw.text((960, 295), "CÂU THƠ DÂN GIAN KỲ DIỆU", font=fonts["badge"], fill="#D97706", anchor="mm")
    draw.text((960, 345), "“O tròn như quả trứng gà,”", font=fonts["h2"], fill="#DC2626", anchor="mm")
    draw.text((960, 390), "“Ô thì đội mũ — Ơ thì thêm râu!”", font=fonts["h2"], fill="#059669", anchor="mm")
    
    im.paste(CARD_O, (280, 440), CARD_O)
    im.paste(CARD_OE, (790, 440), CARD_OE)
    im.paste(CARD_OW, (1300, 440), CARD_OW)
    
    draw_subtitles(draw, fonts, 
                   "O tròn như quả trứng gà, Ô thì đội mũ, Ơ thì thêm râu! Cùng khám phá với chúng mình nhé!",
                   "Plain is O like an egg, with a hat is Ô, with a hook is Ơ. Let's explore together!")
    im.convert("RGB").save(os.path.join(FRAMES_DIR, "s1_lim_intro.png"))
    print("Rendered s1_lim_intro.png")

# 2. SCENE 2: O - Ô - Ơ (Dương Thị Nhung)
def make_frame_s2_o(fonts, step=1):
    im = create_kindergarten_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_nav(draw, fonts, current_step=2)
    
    draw.text((100, 100), "BÀI HỌC 1: BÉ O TRÒN VO — NHÂN VẬT GỐC", font=fonts["title"], fill="#DC2626")
    draw.text((100, 145), "Phụ trách: Dương Thị Nhung  |  Ký hiệu IPA: /ɔ/ (Nguyên âm hàng sau, mở rộng, tròn môi)", font=fonts["subtitle"], fill="#64748B")
    
    # Left Hero Showcase Card [140, 195, 780, 850]
    draw_card(draw, [140, 195, 780, 850], bg="#FFFFFF", border="#EF4444", border_width=3)
    im.paste(CARD_O, (290, 220), CARD_O)
    draw.rounded_rectangle([220, 680, 700, 735], radius=12, fill="#FEF2F2", outline="#EF4444", width=2)
    draw.text((460, 707), "CHỮ GỐC: KHÔNG DẤU", font=fonts["badge"], fill="#DC2626", anchor="mm")
    draw.text((460, 765), "Nét bút: Một nét cong tròn khép kín", font=fonts["body_bold"], fill="#1E293B", anchor="mm")
    draw.text((460, 805), "Môi mở tròn to như quả trứng gà", font=fonts["body"], fill="#64748B", anchor="mm")
    
    # Right Top Card: Rules & Guidelines [820, 195, 1780, 500]
    draw_card(draw, [820, 195, 1780, 500], bg="#FFFFFF", border="#CBD5E1", border_width=2)
    draw.text((1300, 235), "CÁCH PHÁT ÂM CHUẨN XỨNG DANH BÉ O", font=fonts["badge"], fill="#DC2626", anchor="mm")
    steps = [
        "1. Hạ thấp quai hàm, mở rộng hai môi tròn to thành hình chữ O.",
        "2. Luồng hơi đi ra tự do, ngân vang trong trẻo: /ɔ/.",
        "3. Ví dụ kinh điển: BÒ (B - O - BO - HUYỀN - BÒ)."
    ]
    for idx, s in enumerate(steps):
        draw.text((860, 290 + idx * 65), s, font=fonts["body"], fill="#1E293B")
        
    # Right Bottom Left: Lip Shape [820, 535, 1280, 850]
    draw_lip_shape(draw, fonts, 1050, 690, lip_type="o")
    
    # Right Bottom Right: Word Card [1320, 535, 1780, 850]
    draw_card(draw, [1320, 535, 1780, 850], bg="#FEF2F2", border="#EF4444", border_width=2)
    draw.text((1550, 580), "TỪ VỰNG TIÊU BIỂU", font=fonts["badge"], fill="#DC2626", anchor="mm")
    draw.text((1550, 680), "BÒ", font=fonts["huge_letter"], fill="#DC2626", anchor="mm")
    draw.text((1550, 785), "Con bò • The cow", font=fonts["body_bold"], fill="#1E293B", anchor="mm")
    
    subs = {
        1: ("Tớ là O tròn vo nè! Tớ là chữ cái đầu tiên, tròn xoe như quả trứng gà vậy đó!",
            "I am round O! I am the base letter, as round as a chicken egg!"),
        2: ("Cùng mở to môi và phát âm O thật vang với tớ nào: O ... O ... Bò ... Con bò!",
            "Open your lips wide and say O with me: O ... O ... Bò ... Con bò!")
    }
    vi, en = subs[step]
    draw_subtitles(draw, fonts, vi, en)
    
    fname = f"s2_nhung_o_{step}.png"
    im.convert("RGB").save(os.path.join(FRAMES_DIR, fname))
    print(f"Rendered {fname}")

def make_frame_s2_oe(fonts, step=1):
    im = create_kindergarten_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_nav(draw, fonts, current_step=3)
    
    draw.text((100, 100), "BÀI HỌC 2: BÉ Ô ĐỘI MŨ — CHIẾC NÓN XINH", font=fonts["title"], fill="#059669")
    draw.text((100, 145), "Phụ trách: Dương Thị Nhung  |  Ký hiệu IPA: /o/ (Nguyên âm hàng sau, khép vừa, tròn môi)", font=fonts["subtitle"], fill="#64748B")
    
    # Left Hero Showcase Card [140, 195, 780, 850]
    draw_card(draw, [140, 195, 780, 850], bg="#FFFFFF", border="#10B981", border_width=3)
    im.paste(CARD_OE, (290, 220), CARD_OE)
    draw.rounded_rectangle([220, 680, 700, 735], radius=12, fill="#ECFDF5", outline="#10B981", width=2)
    draw.text((460, 707), "THÊM MŨ: NÓN CHÓP (^)", font=fonts["badge"], fill="#059669", anchor="mm")
    draw.text((460, 765), "Biến đổi: O + Mũ chóp nhọn = Ô", font=fonts["body_bold"], fill="#1E293B", anchor="mm")
    draw.text((460, 805), "Môi khép vừa và chu nhô ra trước", font=fonts["body"], fill="#64748B", anchor="mm")
    
    # Right Top Card: Rules & Guidelines [820, 195, 1780, 500]
    draw_card(draw, [820, 195, 1780, 500], bg="#FFFFFF", border="#CBD5E1", border_width=2)
    draw.text((1300, 235), "CÁCH PHÁT ÂM CHUẨN XỨNG DANH BÉ Ô", font=fonts["badge"], fill="#059669", anchor="mm")
    steps = [
        "1. Nâng cao quai hàm hơn chữ O một chút, hai môi khép vừa.",
        "2. Chu môi nhô nhẹ ra phía trước, phát âm dứt khoát: /o/.",
        "3. Ví dụ kinh điển: CÔ (C - Ô - CÔ - CÔ GIÁO)."
    ]
    for idx, s in enumerate(steps):
        draw.text((860, 290 + idx * 65), s, font=fonts["body"], fill="#1E293B")
        
    # Right Bottom Left: Lip Shape [820, 535, 1280, 850]
    draw_lip_shape(draw, fonts, 1050, 690, lip_type="oe")
    
    # Right Bottom Right: Word Card [1320, 535, 1780, 850]
    draw_card(draw, [1320, 535, 1780, 850], bg="#ECFDF5", border="#10B981", border_width=2)
    draw.text((1550, 580), "TỪ VỰNG TIÊU BIỂU", font=fonts["badge"], fill="#059669", anchor="mm")
    draw.text((1550, 680), "CÔ", font=fonts["huge_letter"], fill="#059669", anchor="mm")
    draw.text((1550, 785), "Cô giáo • The teacher", font=fonts["body_bold"], fill="#1E293B", anchor="mm")
    
    subs = {
        1: ("Còn tớ là Ô đây! Nhìn xem, tớ có chiếc mũ chóp nhọn thật xinh trên đầu này!",
            "And I am Ô! Look, I have a cute pointy hat on my head!"),
        2: ("Chu môi nhô ra trước và nói Ô nhé: Ô ... Ô ... Cô ... Cô giáo!",
            "Pucker lips forward and say Ô: Ô ... Ô ... Cô ... Cô giáo!")
    }
    vi, en = subs[step]
    draw_subtitles(draw, fonts, vi, en)
    
    fname = f"s2_nhung_oe_{step}.png"
    im.convert("RGB").save(os.path.join(FRAMES_DIR, fname))
    print(f"Rendered {fname}")

def make_frame_s2_ow(fonts, step=1):
    im = create_kindergarten_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_nav(draw, fonts, current_step=4)
    
    draw.text((100, 100), "BÀI HỌC 3: BÉ Ơ THÊM RÂU — NÉT MÓC ĐÁNG YÊU", font=fonts["title"], fill="#D97706")
    draw.text((100, 145), "Phụ trách: Dương Thị Nhung  |  Ký hiệu IPA: /ɤ/ (Nguyên âm hàng sau, khép vừa, KHÔNG tròn môi)", font=fonts["subtitle"], fill="#64748B")
    
    # Left Hero Showcase Card [140, 195, 780, 850]
    draw_card(draw, [140, 195, 780, 850], bg="#FFFFFF", border="#F59E0B", border_width=3)
    im.paste(CARD_OW, (290, 220), CARD_OW)
    draw.rounded_rectangle([220, 680, 700, 735], radius=12, fill="#FFFBEB", outline="#F59E0B", width=2)
    draw.text((460, 707), "THÊM RÂU: NÉT MÓC CONG", font=fonts["badge"], fill="#D97706", anchor="mm")
    draw.text((460, 765), "Biến đổi: O + Râu móc bên phải = Ơ", font=fonts["body_bold"], fill="#1E293B", anchor="mm")
    draw.text((460, 805), "Môi dẹt ngang mỉm cười, không tròn", font=fonts["body"], fill="#64748B", anchor="mm")
    
    # Right Top Card: Rules & Guidelines [820, 195, 1780, 500]
    draw_card(draw, [820, 195, 1780, 500], bg="#FFFFFF", border="#CBD5E1", border_width=2)
    draw.text((1300, 235), "CÁCH PHÁT ÂM CHUẨN XỨNG DANH BÉ Ơ", font=fonts["badge"], fill="#D97706", anchor="mm")
    steps = [
        "1. Quai hàm giữ ở độ mở vừa phải, TUYỆT ĐỐI KHÔNG tròn môi.",
        "2. Khóe miệng hơi kéo dẹt sang hai bên như đang mỉm cười: /ɤ/.",
        "3. Ví dụ kinh điển: BƠ (B - Ơ - BƠ - QUẢ BƠ)."
    ]
    for idx, s in enumerate(steps):
        draw.text((860, 290 + idx * 65), s, font=fonts["body"], fill="#1E293B")
        
    # Right Bottom Left: Lip Shape [820, 535, 1280, 850]
    draw_lip_shape(draw, fonts, 1050, 690, lip_type="ow")
    
    # Right Bottom Right: Word Card [1320, 535, 1780, 850]
    draw_card(draw, [1320, 535, 1780, 850], bg="#FFFBEB", border="#F59E0B", border_width=2)
    draw.text((1550, 580), "TỪ VỰNG TIÊU BIỂU", font=fonts["badge"], fill="#D97706", anchor="mm")
    draw.text((1550, 680), "BƠ", font=fonts["huge_letter"], fill="#D97706", anchor="mm")
    draw.text((1550, 785), "Quả bơ • The avocado", font=fonts["body_bold"], fill="#1E293B", anchor="mm")
    
    subs = {
        1: ("Tớ là Ơ đây! Tớ có một chiếc râu móc cong cong đáng yêu ở bên phải nè!",
            "I am Ơ! I have an adorable little curved whisker on the right side!"),
        2: ("Mỉm cười dẹt môi ngang và phát âm cùng tớ: Ơ ... Ơ ... Bơ ... Quả bơ!",
            "Smile with flat lips and pronounce with me: Ơ ... Ơ ... Bơ ... Quả bơ!")
    }
    vi, en = subs[step]
    draw_subtitles(draw, fonts, vi, en)
    
    fname = f"s2_nhung_ow_{step}.png"
    im.convert("RGB").save(os.path.join(FRAMES_DIR, fname))
    print(f"Rendered {fname}")

def make_frame_s2_scanner(fonts):
    im = create_kindergarten_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_nav(draw, fonts, current_step=5)
    
    draw.text((960, 105), "CỖ MÁY BIẾN HÌNH KỲ DIỆU: TỪ O SANG Ô VÀ Ơ", font=fonts["title"], fill="#0F172A", anchor="mm")
    draw.text((960, 148), "Bí kíp ghi nhớ ngữ âm học sư phạm của Dương Thị Nhung", font=fonts["subtitle"], fill="#64748B", anchor="mm")
    
    im.paste(CARD_O, (280, 220), CARD_O)
    im.paste(CARD_OE, (790, 220), CARD_OE)
    im.paste(CARD_OW, (1300, 220), CARD_OW)
    
    draw_card(draw, [280, 680, 620, 840], bg="#FEF2F2", border="#EF4444", border_width=2)
    draw.text((450, 715), "CHỮ GỐC: O", font=fonts["badge"], fill="#DC2626", anchor="mm")
    draw.text((450, 765), "Tròn xoe không dấu", font=fonts["body_bold"], fill="#1E293B", anchor="mm")
    draw.text((450, 805), "Môi mở to (/ɔ/)", font=fonts["body"], fill="#64748B", anchor="mm")
    
    draw_card(draw, [790, 680, 1130, 840], bg="#ECFDF5", border="#10B981", border_width=2)
    draw.text((960, 715), "THÊM MŨ (^): Ô", font=fonts["badge"], fill="#059669", anchor="mm")
    draw.text((960, 765), "O + Mũ chóp = Ô", font=fonts["body_bold"], fill="#1E293B", anchor="mm")
    draw.text((960, 805), "Chu môi nhô trước (/o/)", font=fonts["body"], fill="#64748B", anchor="mm")
    
    draw_card(draw, [1300, 680, 1640, 840], bg="#FFFBEB", border="#F59E0B", border_width=2)
    draw.text((1470, 715), "THÊM RÂU ( ' ): Ơ", font=fonts["badge"], fill="#D97706", anchor="mm")
    draw.text((1470, 765), "O + Râu móc = Ơ", font=fonts["body_bold"], fill="#1E293B", anchor="mm")
    draw.text((1470, 805), "Môi dẹt cười tươi (/ɤ/)", font=fonts["body"], fill="#64748B", anchor="mm")
    
    draw.text((705, 430), "➔", font=fonts["big_letter"], fill="#10B981", anchor="mm")
    draw.text((1215, 430), "➔", font=fonts["big_letter"], fill="#F59E0B", anchor="mm")
    
    draw_subtitles(draw, fonts,
                   "Nhìn 3 chúng mình này! O tròn xoe. Thêm mũ nhọn hóa thành Ô. Thêm râu cong hóa thành Ơ! Thật là kỳ diệu!",
                   "Look at the three of us! Plain O. Add a hat becomes Ô. Add a hook becomes Ơ! So magical!")
    im.convert("RGB").save(os.path.join(FRAMES_DIR, "s2_nhung_scanner.png"))
    print("Rendered s2_nhung_scanner.png")

# 3. SCENE 3: LUYỆN TẬP THỰC HÀNH (Đặng Thị Như Ý)
def make_frame_s3_idle(fonts, is_intro=True):
    im = create_kindergarten_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_nav(draw, fonts, current_step=6)
    
    draw.text((960, 105), "PHÒNG LUYỆN TẬP PHÁT ÂM: NHẠI LẠI (SHADOWING)", font=fonts["title"], fill="#0F172A", anchor="mm")
    draw.text((960, 148), "Huấn luyện viên phát âm: Đặng Thị Như Ý", font=fonts["subtitle"], fill="#64748B", anchor="mm")
    
    drills = [
        ("VÒNG 1: BÉ O", "BÒ", "Con bò (Cow)", CARD_O, "#EF4444", 280),
        ("VÒNG 2: BÉ Ô", "CÔ", "Cô giáo (Teacher)", CARD_OE, "#10B981", 790),
        ("VÒNG 3: BÉ Ơ", "BƠ", "Quả bơ (Avocado)", CARD_OW, "#F59E0B", 1300)
    ]
    for tag, word, desc, card_img, col, x in drills:
        im.paste(card_img, (x, 220), card_img)
        draw_card(draw, [x, 680, x + 340, 840], bg="#FFFFFF", border=col, border_width=2)
        draw.text((x + 170, 715), tag, font=fonts["badge"], fill=col, anchor="mm")
        draw.text((x + 170, 765), word, font=fonts["h2"], fill="#0F172A", anchor="mm")
        draw.text((x + 170, 805), desc, font=fonts["body"], fill="#64748B", anchor="mm")
        
    if is_intro:
        draw_subtitles(draw, fonts,
                       "Đến giờ luyện tập rồi! Các bạn hãy lắng nghe và nhắc lại thật to theo ba bạn nhỏ nhé!",
                       "Practice time! Listen carefully and repeat out loud after our three little friends!")
    else:
        draw_subtitles(draw, fonts,
                       "Hoan hô các bạn! Các bạn phát âm ba âm O, Ô, Ơ rất chuẩn và xuất sắc!",
                       "Bravo friends! You pronounced O, Ô, and Ơ so accurately and excellently!")
    im.convert("RGB").save(os.path.join(FRAMES_DIR, "s3_y_idle_lis.png"))
    print("Rendered s3_y_idle_lis.png")

def make_frame_s3_drill(fonts, char_code, mode="lis"):
    im = create_kindergarten_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_nav(draw, fonts, current_step=6)
    
    cfg = {
        "o": ("BÉ O TRÒN VO", "BÒ", "Con bò (Cow)", CARD_O, "#EF4444", "Bé O: Bò ... Con bò!", "Little O: Bò ... Cow!"),
        "oe": ("BÉ Ô ĐỘI MŨ", "CÔ", "Cô giáo (Teacher)", CARD_OE, "#10B981", "Bé Ô: Cô ... Cô giáo!", "Little Ô: Cô ... Teacher!"),
        "ow": ("BÉ Ơ CÓ RÂU", "BƠ", "Quả bơ (Avocado)", CARD_OW, "#F59E0B", "Bé Ơ: Bơ ... Quả bơ!", "Little Ơ: Bơ ... Avocado!")
    }[char_code]
    
    title_tag, word, en_desc, card_img, col, vi_s, en_s = cfg
    
    draw.text((960, 105), f"THỬ THÁCH PHÁT ÂM: {title_tag}", font=fonts["title"], fill=col, anchor="mm")
    
    im.paste(card_img, (220, 240), card_img)
    draw_card(draw, [620, 200, 1720, 840], bg="#FFFFFF", border=col, border_width=3)
    
    if mode == "lis":
        draw.rounded_rectangle([660, 240, 1680, 310], radius=12, fill=col)
        draw.text((1170, 275), "BƯỚC 1: HÃY LẮNG NGHE THẬT KỸ", font=fonts["h3"], fill="#FFFFFF", anchor="mm")
        draw.text((1170, 470), word, font=fonts["hero_letter"], fill=col, anchor="mm")
        draw.text((1170, 630), en_desc, font=fonts["h2"], fill="#334155", anchor="mm")
        draw.text((1170, 740), "Nhân vật đang phát âm mẫu...", font=fonts["body_bold"], fill="#64748B", anchor="mm")
        draw_subtitles(draw, fonts, vi_s, en_s)
    else:
        draw.rounded_rectangle([660, 240, 1680, 310], radius=12, fill="#D97706")
        draw.text((1170, 275), "BƯỚC 2: ĐẾN LƯỢT BẠN PHÁT ÂM TO NHÉ!", font=fonts["h3"], fill="#FFFFFF", anchor="mm")
        draw.text((1170, 470), word, font=fonts["hero_letter"], fill=col, anchor="mm")
        draw.ellipse([1100, 620, 1240, 760], fill="#FEF3C7", outline="#F59E0B", width=4)
        draw.text((1170, 690), "🎤", font=fonts["h2"], anchor="mm")
        draw.text((1170, 795), "[Hãy phát âm to theo nhịp!]", font=fonts["body_bold"], fill="#B45309", anchor="mm")
        draw_subtitles(draw, fonts, "[Đến lượt bạn nhắc lại] ... Giỏi lắm!", "[Your turn to repeat] ... Great job!")
        
    fname = f"s3_y_{char_code}_{mode}.png"
    im.convert("RGB").save(os.path.join(FRAMES_DIR, fname))
    print(f"Rendered {fname}")

# 4. SCENE 4: ĐỐ VUI & TỔNG KẾT (Nguyễn Thị Thu Thủy)
def make_frame_s4_quiz(fonts, answered=False):
    im = create_kindergarten_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_nav(draw, fonts, current_step=7)
    
    draw.text((960, 105), "THỬ THÁCH ĐỐ VUI: BẠN NÀO ĐỘI MŨ?", font=fonts["title"], fill="#0F172A", anchor="mm")
    draw.text((960, 148), "Người dẫn câu hỏi: Nguyễn Thị Thu Thủy", font=fonts["subtitle"], fill="#64748B", anchor="mm")
    
    draw_card(draw, [150, 190, 1770, 330], bg="#FEF2F2", border="#EF4444", border_width=2)
    draw.text((960, 230), "CÂU HỎI NHANH TRÍ:", font=fonts["badge"], fill="#DC2626", anchor="mm")
    draw.text((960, 280), "“Chữ cái nào trong ba bạn nhỏ đang ĐỘI CHIẾC MŨ trên đầu?”", font=fonts["h2"], fill="#0F172A", anchor="mm")
    
    options = [
        ("A", "Chữ O", CARD_O, 280, False),
        ("B", "Chữ Ô", CARD_OE, 790, True),
        ("C", "Chữ Ơ", CARD_OW, 1300, False)
    ]
    
    for tag, opt_name, card_img, x, is_correct in options:
        is_highlight = answered and is_correct
        col = "#10B981" if is_highlight else ("#CBD5E1" if answered else "#3B82F6")
        bg_col = "#ECFDF5" if is_highlight else "#FFFFFF"
        
        im.paste(card_img, (x, 360), card_img)
        draw_card(draw, [x, 810, x + 340, 875], bg=bg_col, border=col, border_width=3 if is_highlight else 2)
        label = f"{tag}. {opt_name}" + ("  [CHÍNH XÁC!]" if is_highlight else "")
        draw.text((x + 170, 842), label, font=fonts["quiz_opt"], fill="#059669" if is_highlight else "#1E293B", anchor="mm")
        
    if not answered:
        draw_subtitles(draw, fonts,
                       "Đố vui nhanh nha! Đố các bạn biết, chữ cái nào đang đội một chiếc mũ xinh trên đầu? A, B hay C nào?",
                       "Quick quiz! Do you know which letter wears a cute hat on its head? A, B, or C?")
        fname = "s4_thuy_quiz_question.png"
    else:
        draw_subtitles(draw, fonts,
                       "Hoan hô! Đáp án chính xác là B: Chữ Ô! Ô có chiếc mũ chóp nhọn trên đầu đấy!",
                       "Hooray! The correct answer is B: Letter Ô! Ô has a pointy hat on top!")
        fname = "s4_thuy_quiz_answer.png"
        
    im.convert("RGB").save(os.path.join(FRAMES_DIR, fname))
    print(f"Rendered {fname}")

def make_frame_s4_summary(fonts):
    im = create_kindergarten_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_nav(draw, fonts, current_step=7)
    
    draw.text((960, 105), "TỔNG KẾT BÀI HỌC: QUY TẮC VÀNG GHI NHỚ", font=fonts["title"], fill="#0F172A", anchor="mm")
    draw.text((960, 148), "Nguyễn Thị Thu Thủy tổng kết  |  Trưởng nhóm: Nguyễn Thị Hồng Thương", font=fonts["subtitle"], fill="#64748B", anchor="mm")
    
    draw_card(draw, [150, 190, 1770, 360], bg="#FFFBEB", border="#F59E0B", border_width=3)
    draw.text((960, 230), "QUY TẮC DÂN GIAN KHẮC SÂU TRÍ NHỚ", font=fonts["badge"], fill="#D97706", anchor="mm")
    draw.text((960, 280), "“O tròn như quả trứng gà,”", font=fonts["h2"], fill="#DC2626", anchor="mm")
    draw.text((960, 325), "“Ô thì đội mũ — Ơ thì thêm râu!”", font=fonts["h2"], fill="#059669", anchor="mm")
    
    im.paste(CARD_O, (280, 390), CARD_O)
    im.paste(CARD_OE, (790, 390), CARD_OE)
    im.paste(CARD_OW, (1300, 390), CARD_OW)
    
    draw.rounded_rectangle([400, 820, 1520, 875], radius=12, fill="#FEF2F2", outline="#EF4444", width=2)
    draw.text((960, 847), "CHÚC CÁC BẠN LUÔN HỌC TIẾNG VIỆT THẬT VUI VẺ VÀ TỰ TIN!", font=fonts["body_bold"], fill="#DC2626", anchor="mm")
    
    draw_subtitles(draw, fonts,
                   "Nhớ câu thần chú: O tròn trứng gà, Ô thì đội mũ, Ơ thì thêm râu! Chúc các bạn học thật vui!",
                   "Remember the rhyme: Round like an egg is O, with a hat is Ô, with a hook is Ơ! Have fun learning Vietnamese!")
    im.convert("RGB").save(os.path.join(FRAMES_DIR, "s4_thuy_summary.png"))
    print("Rendered s4_thuy_summary.png")

if __name__ == "__main__":
    fonts = get_fonts()
    print("Generating bright, joyful preschool slides with refined layout...")
    make_frame_s1(fonts)
    make_frame_s2_o(fonts, step=1)
    make_frame_s2_o(fonts, step=2)
    make_frame_s2_oe(fonts, step=1)
    make_frame_s2_oe(fonts, step=2)
    make_frame_s2_ow(fonts, step=1)
    make_frame_s2_ow(fonts, step=2)
    make_frame_s2_scanner(fonts)
    
    make_frame_s3_idle(fonts, is_intro=True)
    make_frame_s3_drill(fonts, "o", "lis")
    make_frame_s3_drill(fonts, "o", "rep")
    make_frame_s3_drill(fonts, "oe", "lis")
    make_frame_s3_drill(fonts, "oe", "rep")
    make_frame_s3_drill(fonts, "ow", "lis")
    make_frame_s3_drill(fonts, "ow", "rep")
    
    make_frame_s4_quiz(fonts, answered=False)
    make_frame_s4_quiz(fonts, answered=True)
    make_frame_s4_summary(fonts)
    print("All slides re-rendered successfully!")
