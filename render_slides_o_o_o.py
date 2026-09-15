from PIL import Image, ImageDraw, ImageFont
import os
import math

FRAMES_DIR = "/home/quang/video_ai/frames_o"
os.makedirs(FRAMES_DIR, exist_ok=True)

W, H = 1920, 1080

FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

def get_fonts():
    return {
        "title": ImageFont.truetype(FONT_BOLD, 46),
        "subtitle": ImageFont.truetype(FONT_REG, 24),
        "h2": ImageFont.truetype(FONT_BOLD, 36),
        "h3": ImageFont.truetype(FONT_BOLD, 28),
        "big_letter": ImageFont.truetype(FONT_BOLD, 140),
        "huge_letter": ImageFont.truetype(FONT_BOLD, 200),
        "hero_letter": ImageFont.truetype(FONT_BOLD, 260),
        "word_vn": ImageFont.truetype(FONT_BOLD, 54),
        "word_en": ImageFont.truetype(FONT_REG, 26),
        "body": ImageFont.truetype(FONT_REG, 24),
        "body_bold": ImageFont.truetype(FONT_BOLD, 24),
        "badge": ImageFont.truetype(FONT_BOLD, 20),
        "sub_vi": ImageFont.truetype(FONT_BOLD, 26),
        "sub_en": ImageFont.truetype(FONT_REG, 22),
        "small": ImageFont.truetype(FONT_REG, 18)
    }

def create_base_canvas():
    # Premium Editorial Dark Obsidian background (#08090D) with subtle royal indigo depth
    im = Image.new("RGB", (W, H), "#08090D")
    draw = ImageDraw.Draw(im)
    
    # Soft ambient glows
    draw.ellipse([-200, -200, 600, 600], fill="#0F172A")
    draw.ellipse([W - 600, -200, W + 200, 600], fill="#111B38")
    draw.ellipse([W//2 - 500, H - 400, W//2 + 500, H + 400], fill="#0A1124")
    
    # Ultra-thin safe-zone boundary hairline
    draw.rounded_rectangle([20, 20, W - 20, H - 20], radius=20, outline="#1E293B", width=1)
    return im

def draw_top_nav(draw, fonts, current_step=1):
    steps = [
        (1, "I. Khởi động (Lim)"),
        (2, "II. Chữ O (Nhung)"),
        (3, "III. Chữ Ô (Nhung)"),
        (4, "IV. Chữ Ơ (Nhung)"),
        (5, "V. So sánh (Nhung)"),
        (6, "VI. Luyện tập (Ý)"),
        (7, "VII. Tổng kết (Thủy)")
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
        
        bg = "#0284C7" if is_active else ("#1E293B" if is_past else "#0D1527")
        border = "#38BDF8" if is_active else ("#334155" if is_past else "#172554")
        txt_col = "#FFFFFF" if is_active else ("#94A3B8" if is_past else "#475569")
        
        draw.rounded_rectangle([sx, y, ex, y + 38], radius=8, fill=bg, outline=border, width=1)
        draw.text(((sx + ex) // 2, y + 19), s_name, font=fonts["small"], fill=txt_col, anchor="mm")

def draw_subtitles(draw, fonts, vi_text, en_text):
    # Subtitle bar at bottom - clean editorial design, NO emojis, 0% overflow
    box = [100, 895, 1820, 1030]
    draw.rounded_rectangle(box, radius=14, fill="#0B1224", outline="#0284C7", width=1)
    
    # Tag badge
    draw.rounded_rectangle([125, 915, 235, 948], radius=6, fill="#0369A1")
    draw.text((180, 931), "PHỤ ĐỀ", font=fonts["small"], fill="#FFFFFF", anchor="mm")
    
    # Line 1: Vietnamese primary spoken text
    draw.text((255, 931), vi_text, font=fonts["sub_vi"], fill="#F8FAFC", anchor="lm")
    # Line 2: English translation
    draw.text((255, 982), f"[EN] {en_text}", font=fonts["sub_en"], fill="#38BDF8", anchor="lm")

def draw_editorial_card(draw, box, bg="#0E162B", border="#1E293B", border_width=1, radius=16):
    draw.rounded_rectangle(box, radius=radius, fill=bg, outline=border, width=border_width)

def draw_lip_shape(draw, fonts, cx, cy, lip_type="o"):
    # Clean vector diagram of lip aperture (Độ tròn và mở của môi)
    draw.rounded_rectangle([cx - 150, cy - 80, cx + 150, cy + 80], radius=14, fill="#080E1E", outline="#334155", width=1)
    draw.text((cx, cy - 55), "HÌNH DÁNG MÔI (LIP SHAPE)", font=fonts["small"], fill="#94A3B8", anchor="mm")
    
    if lip_type == "o": # Open-mid rounded (Tròn to, mở rộng)
        # Big circular open lips
        draw.ellipse([cx - 50, cy - 25, cx + 50, cy + 35], fill="#F43F5E", outline="#FECDD3", width=3)
        draw.ellipse([cx - 30, cy - 12, cx + 30, cy + 22], fill="#080E1E")
        draw.text((cx, cy + 55), "Môi mở rộng, tròn to (/ɔ/)", font=fonts["small"], fill="#FDE047", anchor="mm")
    elif lip_type == "oe": # Close-mid rounded (Tròn chúm, nhô ra)
        # Small tight circular puckered lips
        draw.ellipse([cx - 35, cy - 20, cx + 35, cy + 30], fill="#F59E0B", outline="#FEF08A", width=3)
        draw.ellipse([cx - 18, cy - 8, cx + 18, cy + 18], fill="#080E1E")
        # Protrusion lines
        draw.line([cx - 50, cy + 5, cx - 40, cy + 5], fill="#F59E0B", width=2)
        draw.line([cx + 40, cy + 5, cx + 50, cy + 5], fill="#F59E0B", width=2)
        draw.text((cx, cy + 55), "Môi khép vừa, nhô ra trước (/o/)", font=fonts["small"], fill="#FDE047", anchor="mm")
    else: # Close-mid unrounded (Môi dẹt ngang)
        # Wide flat unrounded ellipse
        draw.ellipse([cx - 55, cy - 12, cx + 55, cy + 22], fill="#38BDF8", outline="#BAE6FD", width=3)
        draw.ellipse([cx - 35, cy - 5, cx + 35, cy + 15], fill="#080E1E")
        draw.text((cx, cy + 55), "Môi không tròn, dẹt ngang (/ɤ/)", font=fonts["small"], fill="#FDE047", anchor="mm")

# -------------------------------------------------------------
# SCENE 1: KHỞI ĐỘNG (Thí Thuỳ Lim)
# -------------------------------------------------------------
def make_frame_s1(fonts):
    im = create_base_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_nav(draw, fonts, current_step=1)
    
    # Title Tag
    draw.rounded_rectangle([720, 95, 1200, 135], radius=10, fill="#0F1B36", outline="#38BDF8", width=1)
    draw.text((960, 115), "KHÓA HỌC TIẾNG VIỆT SƠ CẤP • TRÌNH ĐỘ A1", font=fonts["badge"], fill="#38BDF8", anchor="mm")
    
    draw.text((960, 175), "BÀI TẬP NGỮ ÂM: BỘ BA NGUYÊN ÂM O — Ô — Ơ", font=fonts["title"], fill="#F8FAFC", anchor="mm")
    draw.text((960, 225), "Phụ trách phần Khởi động: Thí Thuỳ Lim", font=fonts["subtitle"], fill="#94A3B8", anchor="mm")
    
    # Center Ca dao Card
    draw_editorial_card(draw, [150, 270, 1770, 520], bg="#0D162B", border="#0284C7", border_width=1)
    draw.text((960, 310), "CÂU THƠ DÂN GIAN GHI NHỚ MẶT CHỮ:", font=fonts["badge"], fill="#FDE047", anchor="mm")
    draw.text((960, 375), "“O tròn như quả trứng gà,”", font=fonts["h2"], fill="#FFFFFF", anchor="mm")
    draw.text((960, 440), "“Ô thì đội mũ — Ơ thì thêm râu.”", font=fonts["h2"], fill="#38BDF8", anchor="mm")
    
    # 3 Big Hero Letters Showcase
    letters = [
        ("O", "O tròn trứng", "#60A5FA", 420),
        ("Ô", "Ô đội mũ", "#FBBF24", 960),
        ("Ơ", "Ơ thêm râu", "#34D399", 1500)
    ]
    for ch, tag, col, cx in letters:
        draw_editorial_card(draw, [cx - 210, 550, cx + 210, 750], bg="#091122", border=col, border_width=1)
        draw.text((cx, 630), ch, font=fonts["huge_letter"], fill=col, anchor="mm")
        draw.text((cx, 715), tag, font=fonts["body_bold"], fill="#CBD5E1", anchor="mm")
        
    # Goal Banner
    draw.rounded_rectangle([300, 780, 1620, 850], radius=14, fill="#064E3B", outline="#10B981", width=1)
    draw.text((960, 815), "MỤC TIÊU: Sau video, người học có thể phát âm, viết đúng nguyên âm O, Ô và Ơ", font=fonts["body_bold"], fill="#A7F3D0", anchor="mm")
    
    draw_subtitles(draw, fonts, 
                   "Xin chào các em! O tròn như quả trứng gà, Ô thì đội mũ, Ơ thì thêm râu. Hôm nay chúng ta học O, Ô, Ơ!",
                   "Welcome! Plain is O like an egg, with a hat is Ô, with a hook is Ơ. Today we explore O, Ô, and Ơ!")
    
    im.save(os.path.join(FRAMES_DIR, "s1_lim_intro.png"))

# -------------------------------------------------------------
# SCENE 2: PHÁT ÂM & CÁCH VIẾT (Dương Thị Nhung)
# -------------------------------------------------------------
# Cảnh 1: Chữ O ban đầu
def make_frame_s2_o(fonts, sub_idx=1):
    im = create_base_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_nav(draw, fonts, current_step=2)
    
    draw.text((100, 100), "BÀI HỌC 1: NGUYÊN ÂM 'O' — NHÂN VẬT BAN ĐẦU", font=fonts["title"], fill="#60A5FA")
    draw.text((100, 145), "Phụ trách: Dương Thị Nhung  |  Ký hiệu IPA: /ɔ/ (Nguyên âm hàng sau, mở rộng, tròn môi)", font=fonts["subtitle"], fill="#94A3B8")
    
    # Left Hero Letter (Width 820px)
    draw_editorial_card(draw, [100, 195, 920, 850], bg="#091122", border="#3B82F6", border_width=1)
    draw.text((510, 360), "O", font=fonts["hero_letter"], fill="#60A5FA", anchor="mm")
    
    draw.rounded_rectangle([250, 520, 770, 580], radius=10, fill="#1E3A8A")
    draw.text((510, 550), "CHỮ GỐC: KHÔNG DẤU PHỤ", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    
    draw.text((510, 630), "Nét bút: Một nét cong tròn khép kín mềm mại", font=fonts["body"], fill="#CBD5E1", anchor="mm")
    draw.text((510, 680), "Phát âm: Môi mở to, tròn vành môi: 'O'", font=fonts["h3"], fill="#FDE047", anchor="mm")
    draw.text((510, 740), "Ví dụ A1: BÒ (Con bò / Cow)", font=fonts["body_bold"], fill="#93C5FD", anchor="mm")
    
    # Right Column: Diagram & Articulatory Guide (Width 860px)
    draw_editorial_card(draw, [960, 195, 1820, 510], bg="#091122", border="#334155", border_width=1)
    draw.text((1390, 235), "CÁCH VIẾT VÀ CẤU ÂM CHỮ O", font=fonts["badge"], fill="#38BDF8", anchor="mm")
    
    steps = [
        "1. Đặt bút ở đường kẻ trên, đưa nét cong sang trái.",
        "2. Vòng xuống đường kẻ dưới, lượn cong lên tạo hình tròn khép kín.",
        "3. Khi phát âm, hạ thấp hàm dưới, hai môi mở tròn to: /ɔ/."
    ]
    for idx, s in enumerate(steps):
        draw.text((1000, 290 + idx * 60), s, font=fonts["body"], fill="#F8FAFC")
        
    # Lip Shape Box
    draw_lip_shape(draw, fonts, 1390, 680, lip_type="o")
    
    subs = {
        1: ("Đây là O. Một chữ cái rất quen thuộc. Trong tiếng Việt, chỉ cần thêm dấu hiệu nhỏ, O có thể thay đổi!",
            "This is O, a very familiar letter. In Vietnamese, just adding a small mark can transform O!"),
        2: ("O ... O ... Môi mở rộng, tròn vành môi: O.",
            "O ... O ... Lips wide open, fully rounded: O.")
    }
    vi_s, en_s = subs.get(sub_idx, subs[1])
    draw_subtitles(draw, fonts, vi_s, en_s)
    
    im.save(os.path.join(FRAMES_DIR, f"s2_nhung_o_{sub_idx}.png"))

# Cảnh 2: O biến thành Ô
def make_frame_s2_oe(fonts, sub_idx=1):
    im = create_base_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_nav(draw, fonts, current_step=3)
    
    draw.text((100, 100), "BÀI HỌC 2: O BIẾN THÀNH 'Ô' — CHIẾC MŨ XUẤT HIỆN", font=fonts["title"], fill="#FBBF24")
    draw.text((100, 145), "Phụ trách: Dương Thị Nhung  |  Ký hiệu IPA: /o/ (Nguyên âm hàng sau, nửa khép, tròn môi nhô)", font=fonts["subtitle"], fill="#94A3B8")
    
    # Left Hero Letter (Width 820px)
    draw_editorial_card(draw, [100, 195, 920, 850], bg="#14111E", border="#F59E0B", border_width=1)
    
    # Hat floating above O -> Ô
    draw.polygon([(460, 200), (510, 160), (560, 200)], fill="#FBBF24", outline="#FEF08A", width=2)
    draw.text((510, 380), "Ô", font=fonts["hero_letter"], fill="#FBBF24", anchor="mm")
    
    draw.rounded_rectangle([250, 520, 770, 580], radius=10, fill="#B45309")
    draw.text((510, 550), "DẤU PHỤ: CHIẾC MŨ (HAT)", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    
    draw.text((510, 630), "Biến đổi: Một chiếc mũ nhỏ hạ xuống đỉnh chữ O", font=fonts["body"], fill="#CBD5E1", anchor="mm")
    draw.text((510, 680), "Phát âm: Môi khép vừa, nhô ra trước tròn hơn: 'Ô'", font=fonts["h3"], fill="#FDE047", anchor="mm")
    draw.text((510, 740), "Ví dụ A1: CÔ (Cô giáo / Teacher)", font=fonts["body_bold"], fill="#FDE047", anchor="mm")
    
    # Right Column: Guide
    draw_editorial_card(draw, [960, 195, 1820, 510], bg="#14111E", border="#334155", border_width=1)
    draw.text((1390, 235), "CÁCH VIẾT VÀ CẤU ÂM CHỮ Ô", font=fonts["badge"], fill="#F59E0B", anchor="mm")
    
    steps = [
        "1. Viết chữ O tròn chuẩn ban đầu.",
        "2. Thêm dấu mũ (^) cân đối ở chính giữa đỉnh chữ O.",
        "3. Khi phát âm, nâng hàm cao hơn âm O, hai môi chúm tròn nhô ra: /o/."
    ]
    for idx, s in enumerate(steps):
        draw.text((1000, 290 + idx * 60), s, font=fonts["body"], fill="#F8FAFC")
        
    # Lip Shape Box
    draw_lip_shape(draw, fonts, 1390, 680, lip_type="oe")
    
    subs = {
        1: ("Một chiếc mũ nhỏ xuất hiện từ trên hạ xuống chữ O. O đã trở thành Ô!",
            "A small hat appears and lands on O. O has now transformed into Ô!"),
        2: ("Ô ... Ô ... Môi chúm tròn nhô ra phía trước: Ô.",
            "Ô ... Ô ... Lips close-mid rounded and protruded: Ô.")
    }
    vi_s, en_s = subs.get(sub_idx, subs[1])
    draw_subtitles(draw, fonts, vi_s, en_s)
    
    im.save(os.path.join(FRAMES_DIR, f"s2_nhung_oe_{sub_idx}.png"))

# Cảnh 3: O biến thành Ơ
def make_frame_s2_ow(fonts, sub_idx=1):
    im = create_base_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_nav(draw, fonts, current_step=4)
    
    draw.text((100, 100), "BÀI HỌC 3: O BIẾN THÀNH 'Ơ' — CHIẾC RÂU XUẤT HIỆN", font=fonts["title"], fill="#34D399")
    draw.text((100, 145), "Phụ trách: Dương Thị Nhung  |  Ký hiệu IPA: /ɤ/ (Nguyên âm hàng sau/giữa, nửa khép, không tròn môi)", font=fonts["subtitle"], fill="#94A3B8")
    
    # Left Hero Letter (Width 820px)
    draw_editorial_card(draw, [100, 195, 920, 850], bg="#09141D", border="#10B981", border_width=1)
    
    # Hook mark indicator
    draw.arc([560, 200, 630, 280], start=180, end=360, fill="#34D399", width=6)
    draw.text((510, 380), "Ơ", font=fonts["hero_letter"], fill="#34D399", anchor="mm")
    
    draw.rounded_rectangle([250, 520, 770, 580], radius=10, fill="#065F46")
    draw.text((510, 550), "DẤU PHỤ: CHIẾC MÓC RÂU (HOOK)", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    
    draw.text((510, 630), "Biến đổi: Một chiếc râu nhỏ xuất hiện ở góc trên bên phải", font=fonts["body"], fill="#CBD5E1", anchor="mm")
    draw.text((510, 680), "Phát âm: Giống Ô nhưng môi không tròn, mở dẹt ngang: 'Ơ'", font=fonts["h3"], fill="#6EE7B7", anchor="mm")
    draw.text((510, 740), "Ví dụ A1: BƠ (Quả bơ / Avocado)", font=fonts["body_bold"], fill="#A7F3D0", anchor="mm")
    
    # Right Column: Guide
    draw_editorial_card(draw, [960, 195, 1820, 510], bg="#09141D", border="#334155", border_width=1)
    draw.text((1390, 235), "CÁCH VIẾT VÀ CẤU ÂM CHỮ Ơ", font=fonts["badge"], fill="#34D399", anchor="mm")
    
    steps = [
        "1. Viết chữ O tròn chuẩn ban đầu.",
        "2. Thêm một nét móc râu nhỏ ở góc trên bên phải của chữ O.",
        "3. Khi phát âm, nâng hàm như âm Ô nhưng mở dẹt khóe miệng: /ɤ/."
    ]
    for idx, s in enumerate(steps):
        draw.text((1000, 290 + idx * 60), s, font=fonts["body"], fill="#F8FAFC")
        
    # Lip Shape Box
    draw_lip_shape(draw, fonts, 1390, 680, lip_type="ow")
    
    subs = {
        1: ("Nhưng nếu dấu hiệu thay đổi thì sao? Một chiếc râu nhỏ xuất hiện: O đã trở thành Ơ!",
            "What if the mark changes? A small hook appears on the right: O has become Ơ!"),
        2: ("Ơ ... Ơ ... Khẩu hình như Ô nhưng môi không tròn, mở dẹt ngang: Ơ.",
            "Ơ ... Ơ ... Same tongue height as Ô but with unrounded, spread lips: Ơ.")
    }
    vi_s, en_s = subs.get(sub_idx, subs[1])
    draw_subtitles(draw, fonts, vi_s, en_s)
    
    im.save(os.path.join(FRAMES_DIR, f"s2_nhung_ow_{sub_idx}.png"))

# Cảnh 4: Máy quét so sánh O - Ô - Ơ
def make_frame_s2_scanner(fonts):
    im = create_base_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_nav(draw, fonts, current_step=5)
    
    draw.text((100, 100), "CẢNH BÁO: ĐỪNG ĐỂ DẤU ĐÁNH LỪA BẠN!", font=fonts["title"], fill="#F8FAFC")
    draw.text((100, 145), "Phụ trách: Dương Thị Nhung  |  Máy quét nhận diện dấu phụ", font=fonts["subtitle"], fill="#38BDF8")
    
    # 3 Comparison Columns
    cols = [
        ("O", "KHÔNG CÓ DẤU PHỤ", "Tròn to như quả trứng", "/ɔ/ (Open rounded)", "#60A5FA", 100, 640),
        ("Ô", "CÓ DẤU MŨ (^)", "Đội chiếc mũ trên đầu", "/o/ (Close-mid rounded)", "#FBBF24", 660, 1200),
        ("Ơ", "CÓ DẤU MÓC RÂU", "Thêm chiếc râu bên phải", "/ɤ/ (Close-mid unrounded)", "#34D399", 1220, 1820)
    ]
    
    for ch, rule, desc, ipa, col, x0, x1 in cols:
        draw_editorial_card(draw, [x0, 200, x1, 740], bg="#0D1527", border=col, border_width=2)
        cx = (x0 + x1) // 2
        draw.text((cx, 320), ch, font=fonts["hero_letter"], fill=col, anchor="mm")
        
        draw.rounded_rectangle([x0 + 40, 440, x1 - 40, 495], radius=10, fill="#1E293B")
        draw.text((cx, 467), rule, font=fonts["badge"], fill="#FFFFFF", anchor="mm")
        
        draw.text((cx, 550), desc, font=fonts["body_bold"], fill="#CBD5E1", anchor="mm")
        draw.text((cx, 610), ipa, font=fonts["body"], fill=col, anchor="mm")
        
    # Scanning Light Beam overlay
    draw.rounded_rectangle([100, 770, 1820, 850], radius=14, fill="#1E1B4B", outline="#A855F7", width=2)
    draw.text((960, 810), "[MÁY QUÉT]: Không dấu phụ -> O  |  Có dấu mũ -> Ô  |  Có dấu móc râu -> Ơ", font=fonts["h3"], fill="#E9D5FF", anchor="mm")
    
    draw_subtitles(draw, fonts, 
                   "Đừng để dấu đánh lừa bạn! Hãy nhớ: Không dấu là O; có mũ là Ô; có móc là Ơ!",
                   "Don't let marks trick you! Remember: Plain is O; with a hat is Ô; with a hook is Ơ!")
    
    im.save(os.path.join(FRAMES_DIR, "s2_nhung_scanner.png"))

# -------------------------------------------------------------
# SCENE 3: LUYỆN TẬP THỰC HÀNH (Mạc Như Ý)
# -------------------------------------------------------------
def make_frame_s3_drill(fonts, active_char=None, is_repeat=False):
    im = create_base_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_nav(draw, fonts, current_step=6)
    
    draw.text((100, 100), "PHẦN 3: LUYỆN TẬP THỰC HÀNH (SHADOWING)", font=fonts["title"], fill="#F8FAFC")
    draw.text((100, 145), "Phụ trách: Mạc Như Ý  |  Quy trình: 1. Nghe mẫu  ->  2. Cảm nhận độ tròn môi  ->  3. Lặp lại to rõ", font=fonts["subtitle"], fill="#38BDF8")
    
    words = [
        ("o", "O", "BÒ", "/bɔ̌/", "Con bò (Cow)", "#60A5FA", 200),
        ("oe", "Ô", "CÔ", "/ko/", "Cô giáo (Teacher)", "#FBBF24", 370),
        ("ow", "Ơ", "BƠ", "/bɤ/", "Quả bơ (Avocado)", "#34D399", 540)
    ]
    
    for tag, ch, word, ipa, meaning, col, y in words:
        is_active = (active_char == tag)
        bg = "#172554" if (is_active and not is_repeat) else ("#064E3B" if (is_active and is_repeat) else "#0D1527")
        border = "#60A5FA" if is_active else "#1E293B"
        
        draw_editorial_card(draw, [100, y, 1820, y + 145], bg=bg, border=border, border_width=2 if is_active else 1)
        
        # Letter pill
        draw.text((190, y + 72), ch, font=fonts["h2"], fill=col, anchor="mm")
        
        # Big Word
        draw.text((360, y + 72), word, font=fonts["word_vn"], fill="#FFFFFF", anchor="lm")
        draw.text((620, y + 72), ipa, font=fonts["h3"], fill=col, anchor="lm")
        draw.text((850, y + 72), meaning, font=fonts["body"], fill="#CBD5E1", anchor="lm")
        
        if is_active and not is_repeat:
            draw.rounded_rectangle([1500, y + 45, 1750, y + 100], radius=8, fill="#0284C7")
            draw.text((1625, y + 72), "ĐANG NGHE", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
        elif is_active and is_repeat:
            draw.rounded_rectangle([1450, y + 45, 1770, y + 100], radius=8, fill="#047857")
            draw.text((1610, y + 72), "LẶP LẠI NGAY!", font=fonts["badge"], fill="#A7F3D0", anchor="mm")
            
    # Bottom Action Bar
    if is_repeat:
        draw.rounded_rectangle([100, 715, 1820, 850], radius=14, fill="#064E3B", outline="#10B981", width=2)
        draw.text((960, 782), "[MIC ON] ĐẾN LƯỢT BẠN: BẬT MIC VÀ LẶP LẠI TO RÕ TRONG 2.5 GIÂY!", font=fonts["h2"], fill="#34D399", anchor="mm")
        vi_sub = "Đến lượt bạn: Hãy mở mic và lặp lại thật to rõ trong khoảng dừng này!"
        en_sub = "Your turn: Repeat out loud now during the pause!"
    else:
        draw.rounded_rectangle([100, 715, 1820, 850], radius=14, fill="#0F172A", outline="#0284C7", width=1)
        draw.text((960, 782), "LẮNG NGHE NGƯỜI BẢN XỨ VÀ CẢM NHẬN KHẨU HÌNH", font=fonts["h3"], fill="#38BDF8", anchor="mm")
        vi_sub = "Hãy lắng nghe người bản xứ và cảm nhận sự chuyển động của bờ môi!"
        en_sub = "Listen to native speaker and notice the lip shape transition!"
        
    draw_subtitles(draw, fonts, vi_sub, en_sub)
    
    fn = f"s3_y_{active_char if active_char else 'idle'}_{'rep' if is_repeat else 'lis'}.png"
    im.save(os.path.join(FRAMES_DIR, fn))

# -------------------------------------------------------------
# SCENE 4: TỔNG KẾT & CỦNG CỐ (Nông Thị Lệ Thuỷ)
# -------------------------------------------------------------
def make_frame_s4_quiz(fonts, state="question"):
    im = create_base_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_nav(draw, fonts, current_step=7)
    
    draw.text((100, 100), "PHẦN 4: TỔNG KẾT & THỬ THÁCH THÍNH GIÁC", font=fonts["title"], fill="#F8FAFC")
    draw.text((100, 145), "Phụ trách: Nông Thị Lệ Thuỷ  |  Chọn đáp án đúng trong 3 giây", font=fonts["subtitle"], fill="#38BDF8")
    
    draw_editorial_card(draw, [150, 200, 1770, 720], bg="#0D1527", border="#38BDF8", border_width=2)
    
    draw.rounded_rectangle([200, 230, 1720, 330], radius=14, fill="#0B1224", outline="#0284C7", width=1)
    draw.text((960, 260), "CÂU HỎI: BẠN VỪA NGHE THẤY TỪ NÀO DƯỚI ĐÂY?", font=fonts["h2"], fill="#F8FAFC", anchor="mm")
    draw.text((960, 300), "Which word did the teacher just pronounce?", font=fonts["subtitle"], fill="#94A3B8", anchor="mm")
    
    # Choice A: CÔ
    is_a_correct = (state == "answer")
    bg_a = "#064E3B" if is_a_correct else "#080E1E"
    bd_a = "#10B981" if is_a_correct else "#F59E0B"
    draw.rounded_rectangle([250, 360, 930, 600], radius=16, fill=bg_a, outline=bd_a, width=3 if is_a_correct else 1)
    draw.text((340, 420), "[A]", font=fonts["h2"], fill="#FBBF24", anchor="mm")
    draw.text((590, 450), "CÔ", font=fonts["huge_letter"], fill="#FFFFFF", anchor="mm")
    draw.text((590, 560), "/ko/ (Teacher / Aunt)", font=fonts["body"], fill="#94A3B8", anchor="mm")
    if is_a_correct:
        draw.rounded_rectangle([440, 370, 740, 410], radius=8, fill="#047857")
        draw.text((590, 390), "DAP AN CHINH XAC!", font=fonts["badge"], fill="#A7F3D0", anchor="mm")
        
    # Choice B: BƠ
    draw.rounded_rectangle([990, 360, 1670, 600], radius=16, fill="#080E1E", outline="#34D399", width=1)
    draw.text((1080, 420), "[B]", font=fonts["h2"], fill="#34D399", anchor="mm")
    draw.text((1330, 450), "BƠ", font=fonts["huge_letter"], fill="#FFFFFF", anchor="mm")
    draw.text((1330, 560), "/bɤ/ (Avocado / Butter)", font=fonts["body"], fill="#94A3B8", anchor="mm")
    
    if state == "question":
        draw.rounded_rectangle([250, 630, 1670, 690], radius=10, fill="#1E293B", outline="#F59E0B", width=1)
        draw.text((960, 660), "3... 2... 1... HÃY SUY NGHĨ VÀ CHỌN A HOẶC B!", font=fonts["h3"], fill="#FDE047", anchor="mm")
        vi_sub = "Thử thách thính giác nào! Bạn vừa nghe thấy từ nào dưới đây?"
        en_sub = "Listening challenge! Which word did you just hear?"
    else:
        draw.rounded_rectangle([250, 630, 1670, 690], radius=10, fill="#047857", outline="#34D399", width=1)
        draw.text((960, 660), "BINGO! ĐÁP ÁN ĐÚNG LÀ [A]: CÔ!", font=fonts["h3"], fill="#FFFFFF", anchor="mm")
        vi_sub = "Ba, hai, một. Chính xác! Đó là đáp án A: CÔ!"
        en_sub = "Three, two, one. Correct! It is choice A: CÔ!"
        
    draw_subtitles(draw, fonts, vi_sub, en_sub)
    im.save(os.path.join(FRAMES_DIR, f"s4_thuy_quiz_{state}.png"))

def make_frame_s4_summary(fonts):
    im = create_base_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_nav(draw, fonts, current_step=7)
    
    draw.text((100, 100), "QUY TẮC VÀNG GHI NHỚ VĨNH VIỄN", font=fonts["title"], fill="#34D399")
    draw.text((100, 145), "Phụ trách: Nông Thị Lệ Thuỷ  |  Tóm tắt ghi nhớ trọn đời", font=fonts["subtitle"], fill="#94A3B8")
    
    cols = [
        ("O", "TRÒN QUẢ TRỨNG", "Môi mở rộng, tròn to", "Ví dụ: BÒ (Con bò)", "#60A5FA", 100, 640),
        ("Ô", "ĐỘI CHIẾC MŨ (^)", "Môi khép vừa, nhô ra", "Ví dụ: CÔ (Cô giáo)", "#FBBF24", 660, 1200),
        ("Ơ", "THÊM CHIẾC RÂU", "Môi dẹt ngang tự nhiên", "Ví dụ: BƠ (Quả bơ)", "#34D399", 1220, 1820)
    ]
    
    for ch, rule, mouth, eg, col, x0, x1 in cols:
        draw_editorial_card(draw, [x0, 200, x1, 720], bg="#0D1527", border=col, border_width=1)
        cx = (x0 + x1) // 2
        draw.text((cx, 310), ch, font=fonts["hero_letter"], fill=col, anchor="mm")
        
        draw.rounded_rectangle([x0 + 30, 420, x1 - 30, 480], radius=10, fill="#1E293B")
        draw.text((cx, 450), rule, font=fonts["body_bold"], fill="#FFFFFF", anchor="mm")
        
        draw.text((cx, 540), mouth, font=fonts["body"], fill="#CBD5E1", anchor="mm")
        draw.text((cx, 620), eg, font=fonts["h3"], fill=col, anchor="mm")
        
    draw.rounded_rectangle([100, 750, 1820, 850], radius=14, fill="#064E3B", outline="#10B981", width=1)
    draw.text((960, 800), "CHÚC MỪNG BẠN ĐÃ LÀM CHỦ NGUYÊN ÂM O — Ô — Ơ!", font=fonts["h2"], fill="#FFFFFF", anchor="mm")
    
    draw_subtitles(draw, fonts, 
                   "Hãy luôn nhớ: O tròn trứng, Ô đội mũ, Ơ thêm râu. Cảm ơn các em và hẹn gặp lại! Tạm biệt!",
                   "Always remember: O egg, Ô hat, Ơ hook. Thank you and see you in the next lesson!")
    
    im.save(os.path.join(FRAMES_DIR, "s4_thuy_summary.png"))

def generate_all():
    fonts = get_fonts()
    print("Rendering Editorial O-Ô-Ơ slides with 0% tofu boxes and clean typography...")
    make_frame_s1(fonts)
    
    # Scene 2 (Nhung)
    make_frame_s2_o(fonts, sub_idx=1)
    make_frame_s2_o(fonts, sub_idx=2)
    make_frame_s2_oe(fonts, sub_idx=1)
    make_frame_s2_oe(fonts, sub_idx=2)
    make_frame_s2_ow(fonts, sub_idx=1)
    make_frame_s2_ow(fonts, sub_idx=2)
    make_frame_s2_scanner(fonts)
    
    # Scene 3 (Ý)
    make_frame_s3_drill(fonts, active_char=None, is_repeat=False)
    make_frame_s3_drill(fonts, active_char="o", is_repeat=False)
    make_frame_s3_drill(fonts, active_char="o", is_repeat=True)
    make_frame_s3_drill(fonts, active_char="oe", is_repeat=False)
    make_frame_s3_drill(fonts, active_char="oe", is_repeat=True)
    make_frame_s3_drill(fonts, active_char="ow", is_repeat=False)
    make_frame_s3_drill(fonts, active_char="ow", is_repeat=True)
    
    # Scene 4 (Thủy)
    make_frame_s4_quiz(fonts, state="question")
    make_frame_s4_quiz(fonts, state="answer")
    make_frame_s4_summary(fonts)
    print("All O-Ô-Ơ slides generated successfully!")

if __name__ == "__main__":
    generate_all()
