from PIL import Image, ImageDraw, ImageFont
import os

FRAMES_DIR = "/home/quang/video_ai/frames_v2"
os.makedirs(FRAMES_DIR, exist_ok=True)

W, H = 1920, 1080

FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

def get_fonts():
    return {
        "title": ImageFont.truetype(FONT_BOLD, 54),
        "subtitle": ImageFont.truetype(FONT_REG, 28),
        "h2": ImageFont.truetype(FONT_BOLD, 40),
        "h3": ImageFont.truetype(FONT_BOLD, 32),
        "big_letter": ImageFont.truetype(FONT_BOLD, 140),
        "huge_letter": ImageFont.truetype(FONT_BOLD, 180),
        "word_vn": ImageFont.truetype(FONT_BOLD, 56),
        "word_en": ImageFont.truetype(FONT_REG, 28),
        "body": ImageFont.truetype(FONT_REG, 26),
        "body_bold": ImageFont.truetype(FONT_BOLD, 26),
        "badge": ImageFont.truetype(FONT_BOLD, 22),
        "sub_en": ImageFont.truetype(FONT_BOLD, 28),
        "sub_vi": ImageFont.truetype(FONT_REG, 26),
        "small": ImageFont.truetype(FONT_REG, 22)
    }

def create_base_canvas():
    # Elegant deep gradient background with subtle radial depth
    im = Image.new("RGB", (W, H), "#070B19")
    draw = ImageDraw.Draw(im)
    
    # Subtle geometric tech glow circles
    draw.ellipse([-200, -200, 600, 600], fill="#0C1A3A")
    draw.ellipse([W - 500, -200, W + 300, 600], fill="#111B38")
    draw.ellipse([W//2 - 400, H - 300, W//2 + 400, H + 400], fill="#0B1630")
    
    # Subtle border around screen (safe zone 20px)
    draw.rectangle([20, 20, W - 20, H - 20], outline="#172554", width=2)
    return im

def draw_top_progress(draw, fonts, current_step=1):
    steps = [
        (1, "1. Khởi động"),
        (2, "2. Phụ âm Đ"),
        (3, "3. Phụ âm D"),
        (4, "4. Luyện tập"),
        (5, "5. Mini Quiz"),
        (6, "6. Quy tắc vàng")
    ]
    
    total_w = 1720
    start_x = 100
    y = 35
    col_w = total_w // len(steps)
    
    for idx, (s_num, s_name) in enumerate(steps):
        sx = start_x + idx * col_w
        ex = sx + col_w - 15
        is_active = (s_num == current_step)
        is_past = (s_num < current_step)
        
        bg = "#0284C7" if is_active else ("#1E293B" if is_past else "#0F172A")
        border = "#38BDF8" if is_active else ("#334155" if is_past else "#1E293B")
        txt_col = "#FFFFFF" if is_active else ("#94A3B8" if is_past else "#64748B")
        
        draw.rounded_rectangle([sx, y, ex, y + 42], radius=10, fill=bg, outline=border, width=2 if is_active else 1)
        draw.text(((sx + ex) // 2, y + 21), s_name, font=fonts["badge"], fill=txt_col, anchor="mm")

def draw_subtitle_box(draw, fonts, en_text, vi_text):
    # Subtitle container anchored at bottom (safe zone, perfectly padded)
    box = [100, 885, 1820, 1030]
    draw.rounded_rectangle(box, radius=16, fill="#0B1329", outline="#0284C7", width=2)
    
    # Subtitle badge tag
    draw.rounded_rectangle([120, 905, 230, 940], radius=8, fill="#0369A1")
    draw.text((175, 922), "SUBTITLES", font=fonts["small"], fill="#FFFFFF", anchor="mm")
    
    # Dual-line bilingual subtitles
    draw.text((250, 922), en_text, font=fonts["sub_en"], fill="#F8FAFC", anchor="lm")
    draw.text((250, 975), f"🇻🇳 {vi_text}", font=fonts["sub_vi"], fill="#38BDF8", anchor="lm")

def draw_card(draw, box, bg="#111C35", border="#1E3A8A", border_width=2, radius=18):
    draw.rounded_rectangle(box, radius=radius, fill=bg, outline=border, width=border_width)

def draw_anatomical_diagram(draw, fonts, x, y, w, h, sound_type="de"):
    # Card container
    draw_card(draw, [x, y, x + w, y + h], bg="#091024", border="#38BDF8", border_width=2, radius=16)
    
    draw.text((x + 25, y + 25), "SƠ ĐỒ CẤU ÂM (SAGITTAL SECTION)", font=fonts["badge"], fill="#38BDF8")
    
    cx = x + w // 2
    cy = y + h // 2 - 20
    
    if sound_type == "de": # Đ - Alveolar Stop
        # Palate arch
        draw.arc([cx - 160, cy - 130, cx + 160, cy + 90], start=180, end=350, fill="#CBD5E1", width=6)
        draw.text((cx + 100, cy - 100), "Vòm họng", font=fonts["small"], fill="#94A3B8")
        
        # Upper incisor tooth
        draw.rectangle([cx - 100, cy - 30, cx - 75, cy + 30], fill="#FFFFFF", outline="#64748B", width=2)
        draw.text((cx - 160, cy + 20), "Răng trên", font=fonts["small"], fill="#94A3B8")
        
        # Alveolar ridge (Target hotspot - Glowing Red)
        draw.ellipse([cx - 60, cy - 45, cx - 30, cy - 15], fill="#EF4444", outline="#FCA5A5", width=2)
        draw.text((cx - 30, cy - 65), "🎯 Nướu trên (Alveolar)", font=fonts["body_bold"], fill="#FCA5A5")
        
        # Tongue muscle pressing firmly against alveolar ridge
        draw.polygon([
            (cx - 50, cy - 25),
            (cx + 80, cy + 20),
            (cx + 60, cy + 90),
            (cx - 20, cy + 80)
        ], fill="#FB7185", outline="#F43F5E", width=2)
        
        # Stop air icon (Burst/Stop)
        draw.text((cx - 110, cy - 10), "🚫 STOP AIR", font=fonts["badge"], fill="#F87171")
        
        # Educational explanation text inside box
        draw.text((x + 25, y + h - 75), "1. Đầu lưỡi áp chặt chân răng hàm trên", font=fonts["body_bold"], fill="#FFFFFF")
        draw.text((x + 25, y + h - 40), "2. Chặn luồng hơi → Bật ra dứt khoát như 'Door'", font=fonts["body"], fill="#38BDF8")
        
    else: # D - Dental Fricative
        # Upper & lower incisors
        draw.rectangle([cx - 60, cy - 70, cx - 35, cy - 15], fill="#FFFFFF", outline="#64748B", width=2)
        draw.rectangle([cx - 60, cy + 5, cx - 35, cy + 60], fill="#FFFFFF", outline="#64748B", width=2)
        draw.text((cx - 160, cy), "Răng khép nhẹ", font=fonts["small"], fill="#94A3B8")
        
        # Friction air stream arrows (Buzzing waves)
        for offset in [-12, 0, 12]:
            yy = cy - 5 + offset
            draw.line([cx - 20, yy, cx + 110, yy], fill="#F59E0B", width=4)
            draw.polygon([(cx + 110, yy - 5), (cx + 125, yy), (cx + 110, yy + 5)], fill="#F59E0B")
            
        draw.text((cx + 30, cy - 50), "⚡ RUNG XÁT /z/", font=fonts["body_bold"], fill="#FBBF24")
        
        # Tongue positioned behind teeth
        draw.polygon([
            (cx - 10, cy - 5),
            (cx + 80, cy + 30),
            (cx + 60, cy + 90),
            (cx + 10, cy + 70)
        ], fill="#FB7185", outline="#F43F5E", width=2)
        
        # Educational explanation
        draw.text((x + 25, y + h - 75), "1. Hai hàm răng khép nhẹ, đầu lưỡi sát mặt sau răng", font=fonts["body_bold"], fill="#FFFFFF")
        draw.text((x + 25, y + h - 40), "2. Luồng hơi ma sát liên tục tạo âm rung xát như 'Zoo'", font=fonts["body"], fill="#FBBF24")

# -------------------------------------------------------------
# SCENE 1: INTRO & OBJECTIVE
# -------------------------------------------------------------
def make_frame_s1(fonts):
    im = create_base_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_progress(draw, fonts, current_step=1)
    
    # Title badge
    draw.rounded_rectangle([720, 95, 1200, 140], radius=12, fill="#0F172A", outline="#38BDF8", width=2)
    draw.text((960, 117), "PHÁT ÂM TIẾNG VIỆT • TRÌNH ĐỘ A1", font=fonts["badge"], fill="#38BDF8", anchor="mm")
    
    draw.text((960, 190), "Phân Biệt Phụ Âm 'D' và 'Đ'", font=fonts["title"], fill="#F8FAFC", anchor="mm")
    draw.text((960, 245), "Mastering Vietnamese D vs Đ in 2.5 Minutes", font=fonts["subtitle"], fill="#94A3B8", anchor="mm")
    
    # Left Card: Đ
    draw_card(draw, [180, 310, 840, 720], bg="#111E38", border="#3B82F6", border_width=3)
    draw.text((510, 430), "Đ", font=fonts["huge_letter"], fill="#60A5FA", anchor="mm")
    draw.rounded_rectangle([260, 530, 760, 590], radius=12, fill="#1D4ED8")
    draw.text((510, 560), "CÓ GẠCH NGANG (CROSSBAR)", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    draw.text((510, 640), "= English 'D' in 'DOOR' / 'DAY'", font=fonts["h3"], fill="#93C5FD", anchor="mm")
    
    # VS Circle
    draw.ellipse([890, 460, 1030, 600], fill="#EF4444", outline="#FCA5A5", width=3)
    draw.text((960, 530), "VS", font=fonts["h2"], fill="#FFFFFF", anchor="mm")
    
    # Right Card: D
    draw_card(draw, [1080, 310, 1740, 720], bg="#1A1829", border="#F59E0B", border_width=3)
    draw.text((1410, 430), "D", font=fonts["huge_letter"], fill="#FBBF24", anchor="mm")
    draw.rounded_rectangle([1160, 530, 1660, 590], radius=12, fill="#B45309")
    draw.text((1410, 560), "KHÔNG GẠCH NGANG (PLAIN)", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    draw.text((1410, 640), "= English 'Z' in 'ZOO' / 'ZERO'", font=fonts["h3"], fill="#FDE047", anchor="mm")
    
    # Target goal pill
    draw.rounded_rectangle([350, 760, 1570, 830], radius=16, fill="#064E3B", outline="#10B981", width=2)
    draw.text((960, 795), "🎯 MỤC TIÊU: Sau 2.5 phút, phân biệt vị trí đặt lưỡi & phát âm chuẩn 100%!", font=fonts["body_bold"], fill="#A7F3D0", anchor="mm")
    
    draw_subtitle_box(draw, fonts, 
                      "Welcome! Many English speakers confuse Vietnamese D and Đ. Let's master them in 2.5 minutes!", 
                      "Chào mừng bạn! Rất nhiều người học nhầm lẫn chữ D và Đ. Hãy cùng làm chủ chúng trong 2.5 phút!")
    
    im.save(os.path.join(FRAMES_DIR, "s1_intro.png"))

# -------------------------------------------------------------
# SCENE 2: LETTER Đ
# -------------------------------------------------------------
def make_frame_s2(fonts, sub_idx=1):
    im = create_base_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_progress(draw, fonts, current_step=2)
    
    # Header
    draw.text((100, 110), "BÀI HỌC 1: CHỮ 'Đ' (Có gạch ngang)", font=fonts["title"], fill="#60A5FA")
    draw.text((100, 165), "Ngữ âm: Âm Tắc - Đầu Lưỡi Chân Răng (Alveolar Stop) • Ký hiệu IPA: /ɗ/ hoặc [ʔd]", font=fonts["subtitle"], fill="#94A3B8")
    
    # Column 1: Big Letter & Mnemonic (Width 440px)
    draw_card(draw, [100, 220, 540, 840], bg="#111E38", border="#3B82F6", border_width=3)
    draw.text((320, 360), "Đ", font=fonts["huge_letter"], fill="#60A5FA", anchor="mm")
    
    draw.rounded_rectangle([130, 480, 510, 540], radius=10, fill="#1E3A8A")
    draw.text((320, 510), "IPA: /ɗ/ (Hữu thanh)", font=fonts["body_bold"], fill="#93C5FD", anchor="mm")
    
    # Mnemonic box
    draw.rounded_rectangle([130, 570, 510, 800], radius=14, fill="#0F172A", outline="#60A5FA", width=2)
    draw.text((320, 610), "🔑 MẸO GHI NHỚ:", font=fonts["badge"], fill="#FDE047", anchor="mm")
    draw.text((320, 665), "Đ = English 'D'", font=fonts["h3"], fill="#FFFFFF", anchor="mm")
    draw.text((320, 715), "Giống trong từ:", font=fonts["body"], fill="#94A3B8", anchor="mm")
    draw.text((320, 755), "DOOR / DAY", font=fonts["h3"], fill="#38BDF8", anchor="mm")
    
    # Column 2: Anatomical Diagram (Width 560px)
    draw_anatomical_diagram(draw, fonts, 570, 220, 560, 620, sound_type="de")
    
    # Column 3: Vocabulary List (Width 660px)
    draw_card(draw, [1160, 220, 1820, 840], bg="#111E38", border="#334155", border_width=2)
    draw.text((1490, 265), "TỪ VỰNG A1 MẪU (VOCABULARY)", font=fonts["badge"], fill="#38BDF8", anchor="mm")
    
    words = [
        ("🚶 Đi", "/ɗi/", "to go / walk"),
        ("🔴 Đỏ", "/ɗɔ̌/", "red color"),
        ("✨ Đẹp", "/ɗɛp̚/", "beautiful"),
        ("📏 Đo", "/ɗɔ/", "to measure")
    ]
    for idx, (vn, ipa, en) in enumerate(words):
        wy = 315 + idx * 105
        draw.rounded_rectangle([1190, wy, 1790, wy + 90], radius=12, fill="#091024", outline="#1D4ED8", width=2)
        draw.text((1220, wy + 45), vn, font=fonts["word_vn"], fill="#FFFFFF", anchor="lm")
        draw.text((1440, wy + 45), ipa, font=fonts["body_bold"], fill="#60A5FA", anchor="lm")
        draw.text((1580, wy + 45), en, font=fonts["word_en"], fill="#CBD5E1", anchor="lm")
        
    draw.rounded_rectangle([1190, 745, 1790, 815], radius=10, fill="#1E3A8A")
    draw.text((1490, 780), "🔊 Lắng nghe: Đờ ... Đ ... Đi ... Đỏ ... Đẹp", font=fonts["body_bold"], fill="#FDE047", anchor="mm")
    
    subs = {
        1: ("The letter Đ with crossbar is an alveolar stop, sounding like English D in Door.",
            "Chữ Đ có gạch ngang là âm tắc đầu lưỡi, phát âm giống chữ D tiếng Anh trong Door."),
        2: ("Listen carefully to native pronunciation: Đờ ... Đ ... Đi ... Đỏ ... Đẹp.",
            "Lắng nghe phát âm chuẩn người bản xứ: Đờ ... Đ ... Đi ... Đỏ ... Đẹp."),
        3: ("Awesome! Just remember: Crossbar Đ equals English Door.",
            "Tuyệt vời! Hãy nhớ quy tắc: Chữ Đ có gạch ngang giống từ Door.")
    }
    en_s, vi_s = subs.get(sub_idx, subs[1])
    draw_subtitle_box(draw, fonts, en_s, vi_s)
    
    im.save(os.path.join(FRAMES_DIR, f"s2_de_sub{sub_idx}.png"))

# -------------------------------------------------------------
# SCENE 3: LETTER D
# -------------------------------------------------------------
def make_frame_s3(fonts, sub_idx=1):
    im = create_base_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_progress(draw, fonts, current_step=3)
    
    # Header
    draw.text((100, 110), "BÀI HỌC 2: CHỮ 'D' (Không gạch ngang)", font=fonts["title"], fill="#FBBF24")
    draw.text((100, 165), "Ngữ âm: Âm Xát - Đầu Lưỡi Răng (Dental Fricative) • Ký hiệu IPA: /z/ (Bắc) hoặc /j/ (Nam)", font=fonts["subtitle"], fill="#94A3B8")
    
    # Column 1: Big Letter & Mnemonic (Width 440px)
    draw_card(draw, [100, 220, 540, 840], bg="#1F1824", border="#F59E0B", border_width=3)
    draw.text((320, 360), "D", font=fonts["huge_letter"], fill="#FBBF24", anchor="mm")
    
    draw.rounded_rectangle([130, 480, 510, 540], radius=10, fill="#78350F")
    draw.text((320, 510), "IPA: /z/ (Âm xát rung)", font=fonts["body_bold"], fill="#FDE047", anchor="mm")
    
    # Mnemonic box
    draw.rounded_rectangle([130, 570, 510, 800], radius=14, fill="#0F172A", outline="#F59E0B", width=2)
    draw.text((320, 610), "🔑 MẸO GHI NHỚ:", font=fonts["badge"], fill="#FDE047", anchor="mm")
    draw.text((320, 665), "D = English 'Z'", font=fonts["h3"], fill="#FFFFFF", anchor="mm")
    draw.text((320, 715), "Giống trong từ:", font=fonts["body"], fill="#94A3B8", anchor="mm")
    draw.text((320, 755), "ZOO / ZERO", font=fonts["h3"], fill="#F59E0B", anchor="mm")
    
    # Column 2: Anatomical Diagram (Width 560px)
    draw_anatomical_diagram(draw, fonts, 570, 220, 560, 620, sound_type="d")
    
    # Column 3: Vocabulary List (Width 660px)
    draw_card(draw, [1160, 220, 1820, 840], bg="#1F1824", border="#334155", border_width=2)
    draw.text((1490, 265), "TỪ VỰNG A1 MẪU (VOCABULARY)", font=fonts["badge"], fill="#F59E0B", anchor="mm")
    
    words = [
        ("✋ Da", "/za/", "skin"),
        ("👌 Dễ", "/ze˦ˀ˥/", "easy"),
        ("🍉 Dưa", "/zɨə/", "melon"),
        ("💡 Do", "/zɔ/", "because of")
    ]
    for idx, (vn, ipa, en) in enumerate(words):
        wy = 315 + idx * 105
        draw.rounded_rectangle([1190, wy, 1790, wy + 90], radius=12, fill="#091024", outline="#B45309", width=2)
        draw.text((1220, wy + 45), vn, font=fonts["word_vn"], fill="#FFFFFF", anchor="lm")
        draw.text((1440, wy + 45), ipa, font=fonts["body_bold"], fill="#FBBF24", anchor="lm")
        draw.text((1580, wy + 45), en, font=fonts["word_en"], fill="#CBD5E1", anchor="lm")
        
    draw.rounded_rectangle([1190, 745, 1790, 815], radius=10, fill="#78350F")
    draw.text((1490, 780), "🔊 Lắng nghe: Dờ ... D ... Da ... Dễ ... Dưa", font=fonts["body_bold"], fill="#FDE047", anchor="mm")
    
    subs = {
        1: ("The letter D without crossbar is a dental fricative, sounding like English Z in Zoo.",
            "Chữ D không gạch ngang là âm xát đầu lưỡi răng, phát âm như chữ Z tiếng Anh trong Zoo."),
        2: ("Listen carefully to native pronunciation: Dờ ... D ... Da ... Dễ ... Dưa.",
            "Lắng nghe phát âm chuẩn người bản xứ: Dờ ... D ... Da ... Dễ ... Dưa."),
        3: ("Buzz through your teeth! Note: In Southern Vietnam, it sounds like 'Y' in Yes.",
            "Rung luồng hơi qua kẽ răng! Lưu ý: Ở miền Nam, chữ D được đọc giống như 'Y' trong Yes.")
    }
    en_s, vi_s = subs.get(sub_idx, subs[1])
    draw_subtitle_box(draw, fonts, en_s, vi_s)
    
    im.save(os.path.join(FRAMES_DIR, f"s3_d_sub{sub_idx}.png"))

# -------------------------------------------------------------
# SCENE 4: MINIMAL PAIRS DRILL
# -------------------------------------------------------------
def make_frame_s4(fonts, pair_idx=0, active_sound=None, is_repeat=False):
    im = create_base_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_progress(draw, fonts, current_step=4)
    
    draw.text((100, 105), "LUYỆN TẬP CẶP TỪ TƯƠNG PHẢN (MINIMAL PAIRS)", font=fonts["title"], fill="#F8FAFC")
    draw.text((100, 160), "Mô hình: Nghe chuẩn người bản xứ ➔ Nhìn tín hiệu đếm ngược ➔ Bắt chước lặp lại to rõ", font=fonts["subtitle"], fill="#94A3B8")
    
    # Left Card: Đ
    draw_card(draw, [100, 210, 930, 750], bg="#111E38", border="#3B82F6", border_width=3)
    draw.rounded_rectangle([130, 235, 900, 305], radius=12, fill="#1D4ED8")
    draw.text((515, 270), "CỘT ÂM Đ (/ɗ/ - TẮC BẬT HƠI NHƯ 'DOOR')", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    
    # Right Card: D
    draw_card(draw, [990, 210, 1820, 750], bg="#1F1824", border="#F59E0B", border_width=3)
    draw.rounded_rectangle([1020, 235, 1790, 305], radius=12, fill="#B45309")
    draw.text((1405, 270), "CỘT ÂM D (/z/ - XÁT RUNG RĂNG NHƯ 'ZOO')", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    
    pairs = [
        (1, "Đi", "(to go)", "Da", "(skin)"),
        (2, "Đỏ", "(red)", "Dở", "(bad/unskilled)"),
        (3, "Đo", "(to measure)", "Do", "(because of)")
    ]
    
    for idx, (p_num, w_de, m_de, w_d, m_d) in enumerate(pairs):
        py = 330 + idx * 135
        is_cur_pair = (pair_idx == p_num)
        
        # Left item (Đ)
        hl_de = is_cur_pair and (active_sound == "de")
        bg_de = "#1E3A8A" if hl_de else "#091024"
        bd_de = "#60A5FA" if hl_de else "#334155"
        draw.rounded_rectangle([130, py, 900, py + 115], radius=14, fill=bg_de, outline=bd_de, width=3 if hl_de else 1)
        draw.text((220, py + 57), w_de, font=fonts["word_vn"], fill="#FFFFFF" if not hl_de else "#93C5FD", anchor="lm")
        draw.text((450, py + 57), m_de, font=fonts["body"], fill="#94A3B8" if not hl_de else "#FFFFFF", anchor="lm")
        if hl_de:
            draw.text((800, py + 57), "🔊 NGHE", font=fonts["badge"], fill="#38BDF8", anchor="mm")
            
        # Right item (D)
        hl_d = is_cur_pair and (active_sound == "d")
        bg_d = "#78350F" if hl_d else "#091024"
        bd_d = "#FBBF24" if hl_d else "#334155"
        draw.rounded_rectangle([1020, py, 1790, py + 115], radius=14, fill=bg_d, outline=bd_d, width=3 if hl_d else 1)
        draw.text((1110, py + 57), w_d, font=fonts["word_vn"], fill="#FFFFFF" if not hl_d else "#FDE047", anchor="lm")
        draw.text((1340, py + 57), m_d, font=fonts["body"], fill="#94A3B8" if not hl_d else "#FFFFFF", anchor="lm")
        if hl_d:
            draw.text((1690, py + 57), "🔊 NGHE", font=fonts["badge"], fill="#FBBF24", anchor="mm")
            
    # Bottom Action Bar
    if is_repeat:
        draw.rounded_rectangle([100, 770, 1820, 860], radius=16, fill="#064E3B", outline="#10B981", width=3)
        draw.text((960, 815), "🎙️ ĐẾN LƯỢT BẠN: BẬT MIC VÀ LẶP LẠI TO RÕ NGAY! (REPEAT NOW)", font=fonts["h2"], fill="#34D399", anchor="mm")
        en_sub = "Your turn: Repeat out loud now during the pause!"
        vi_sub = "Đến lượt bạn: Hãy mở mic và lặp lại thật to rõ trong khoảng dừng này!"
    else:
        draw.rounded_rectangle([100, 770, 1820, 860], radius=16, fill="#0F172A", outline="#0284C7", width=2)
        draw.text((960, 815), "🎧 LẮNG NGHE NGƯỜI BẢN XỨ VÀ CẢM NHẬN SỰ ĐỐI LẬP CẤU ÂM", font=fonts["h3"], fill="#38BDF8", anchor="mm")
        en_sub = "Listen to the native speaker, then repeat out loud during the countdown!"
        vi_sub = "Lắng nghe người bản xứ, sau đó lặp lại thật to theo nhịp đếm ngược!"
        
    draw_subtitle_box(draw, fonts, en_sub, vi_sub)
    
    fn = f"s4_p{pair_idx}_{active_sound if active_sound else 'idle'}_{'rep' if is_repeat else 'lis'}.png"
    im.save(os.path.join(FRAMES_DIR, fn))

# -------------------------------------------------------------
# SCENE 5: MINI QUIZ
# -------------------------------------------------------------
def make_frame_s5(fonts, q_num=1, state="question"):
    im = create_base_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_progress(draw, fonts, current_step=5)
    
    draw.text((100, 105), f"THỬ THÁCH THÍNH GIÁC: CÂU HỎI {q_num}/2", font=fonts["title"], fill="#38BDF8")
    draw.text((100, 160), "Quy tắc: Nghe âm thanh từ người bản xứ ➔ Chọn đáp án đúng trong 3 giây", font=fonts["subtitle"], fill="#94A3B8")
    
    # Question Card
    draw_card(draw, [150, 210, 1770, 750], bg="#111C35", border="#38BDF8", border_width=3)
    
    draw.rounded_rectangle([200, 240, 1720, 360], radius=16, fill="#091024", outline="#0284C7", width=2)
    draw.text((960, 280), f"🔊 CÂU HỎI {q_num}: Bạn vừa nghe thấy từ nào dưới đây?", font=fonts["h2"], fill="#F8FAFC", anchor="mm")
    draw.text((960, 325), "Which word did the native speaker just pronounce?", font=fonts["subtitle"], fill="#94A3B8", anchor="mm")
    
    if q_num == 1:
        opt_a = ("A", "Đi", "/ɗi/ (to go)")
        opt_b = ("B", "Di", "/zi/ (fricative)")
        correct = "A"
    else:
        opt_a = ("A", "Đa", "/ɗa/ (banyan)")
        opt_b = ("B", "Da", "/za/ (skin)")
        correct = "B"
        
    # Choice A
    is_a_correct = (correct == "A" and state == "answer")
    bg_a = "#064E3B" if is_a_correct else "#091024"
    bd_a = "#10B981" if is_a_correct else "#3B82F6"
    draw.rounded_rectangle([250, 390, 930, 640], radius=18, fill=bg_a, outline=bd_a, width=4 if is_a_correct else 2)
    draw.text((340, 460), "[A]", font=fonts["h2"], fill="#60A5FA", anchor="mm")
    draw.text((590, 480), opt_a[1], font=fonts["huge_letter"], fill="#FFFFFF", anchor="mm")
    draw.text((590, 590), opt_a[2], font=fonts["body"], fill="#94A3B8", anchor="mm")
    if is_a_correct:
        draw.text((590, 400), "⭐ ĐÁP ÁN CHÍNH XÁC!", font=fonts["badge"], fill="#34D399", anchor="mm")
        
    # Choice B
    is_b_correct = (correct == "B" and state == "answer")
    bg_b = "#064E3B" if is_b_correct else "#091024"
    bd_b = "#10B981" if is_b_correct else "#F59E0B"
    draw.rounded_rectangle([990, 390, 1670, 640], radius=18, fill=bg_b, outline=bd_b, width=4 if is_b_correct else 2)
    draw.text((1080, 460), "[B]", font=fonts["h2"], fill="#F59E0B", anchor="mm")
    draw.text((1330, 480), opt_b[1], font=fonts["huge_letter"], fill="#FFFFFF", anchor="mm")
    draw.text((1330, 590), opt_b[2], font=fonts["body"], fill="#94A3B8", anchor="mm")
    if is_b_correct:
        draw.text((1330, 400), "⭐ ĐÁP ÁN CHÍNH XÁC!", font=fonts["badge"], fill="#34D399", anchor="mm")
        
    # Status notification bar
    if state == "question":
        draw.rounded_rectangle([250, 670, 1670, 730], radius=12, fill="#1E293B", outline="#F59E0B", width=2)
        draw.text((960, 700), "⏱️ 3... 2... 1... Hãy suy nghĩ và chọn A hoặc B!", font=fonts["h3"], fill="#FDE047", anchor="mm")
        en_sub = "Listen to the sound and choose: Is it A or B?"
        vi_sub = "Hãy lắng nghe âm thanh và chọn: Đó là phương án A hay B?"
    else:
        draw.rounded_rectangle([250, 670, 1670, 730], radius=12, fill="#047857", outline="#34D399", width=2)
        draw.text((960, 700), f"🎉 BINGO! Đáp án chính xác là [{correct}]!", font=fonts["h3"], fill="#FFFFFF", anchor="mm")
        if q_num == 1:
            en_sub = "Three, two, one. Exactly, it's A: Đi! Alveolar stop /ɗ/."
            vi_sub = "Ba, hai, một. Chính xác là A: Đi! Âm tắc đầu lưỡi /ɗ/."
        else:
            en_sub = "Three, two, one. Correct! It's B: Da! Dental fricative /z/."
            vi_sub = "Ba, hai, một. Đúng rồi! Đó là B: Da! Âm xát đầu lưỡi /z/."
            
    draw_subtitle_box(draw, fonts, en_sub, vi_sub)
    im.save(os.path.join(FRAMES_DIR, f"s5_q{q_num}_{state}.png"))

# -------------------------------------------------------------
# SCENE 6: GOLDEN RULE SUMMARY
# -------------------------------------------------------------
def make_frame_s6(fonts):
    im = create_base_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_progress(draw, fonts, current_step=6)
    
    draw.text((100, 105), "TỔNG KẾT: QUY TẮC VÀNG GHI NHỚ VĨNH VIỄN", font=fonts["title"], fill="#34D399")
    draw.text((100, 160), "Master Rule: Never confuse Vietnamese D and Đ again!", font=fonts["subtitle"], fill="#94A3B8")
    
    # Table Card
    draw_card(draw, [100, 210, 1820, 750], bg="#111C35", border="#34D399", border_width=3)
    
    # Row 1: Đ
    draw.rounded_rectangle([140, 240, 1780, 465], radius=16, fill="#091024", outline="#3B82F6", width=2)
    draw.text((250, 350), "Đ", font=fonts["huge_letter"], fill="#60A5FA", anchor="mm")
    draw.text((380, 310), "CHỮ Đ (Có gạch ngang)", font=fonts["h2"], fill="#F8FAFC", anchor="lm")
    draw.text((380, 375), "➔ Phát âm giống chữ 'D' tiếng Anh trong DOOR / DAY (/ɗ/ Alveolar Stop)", font=fonts["body_bold"], fill="#93C5FD", anchor="lm")
    draw.rounded_rectangle([1450, 305, 1740, 400], radius=12, fill="#1D4ED8")
    draw.text((1595, 352), "Đi • Đỏ • Đẹp", font=fonts["h3"], fill="#FFFFFF", anchor="mm")
    
    # Row 2: D
    draw.rounded_rectangle([140, 495, 1780, 720], radius=16, fill="#091024", outline="#F59E0B", width=2)
    draw.text((250, 605), "D", font=fonts["huge_letter"], fill="#FBBF24", anchor="mm")
    draw.text((380, 565), "CHỮ D (Không gạch ngang)", font=fonts["h2"], fill="#F8FAFC", anchor="lm")
    draw.text((380, 630), "➔ Phát âm giống chữ 'Z' tiếng Anh trong ZOO / ZERO (/z/ Dental Fricative)", font=fonts["body_bold"], fill="#FDE047", anchor="lm")
    draw.rounded_rectangle([1450, 560, 1740, 655], radius=12, fill="#B45309")
    draw.text((1595, 607), "Da • Dễ • Dưa", font=fonts["h3"], fill="#FFFFFF", anchor="mm")
    
    # Congrats Bar
    draw.rounded_rectangle([100, 770, 1820, 860], radius=16, fill="#064E3B", outline="#10B981", width=2)
    draw.text((960, 815), "🌟 CHÚC MỪNG BẠN ĐÃ LÀM CHỦ PHỤ ÂM D VÀ Đ! (CONGRATULATIONS)", font=fonts["h2"], fill="#FFFFFF", anchor="mm")
    
    draw_subtitle_box(draw, fonts, 
                      "Crossbar Đ = English Door. Plain D = English Zoo. Thanks for watching! Tam biet!", 
                      "Chữ Đ có gạch = Door. Chữ D không gạch = Zoo. Cảm ơn các bạn đã theo dõi! Tạm biệt!")
    
    im.save(os.path.join(FRAMES_DIR, "s6_summary.png"))

def generate_all():
    fonts = get_fonts()
    print("Generating vibrant 2.0 slides with complete subtitles and perfect padding...")
    make_frame_s1(fonts)
    
    # Scene 2
    make_frame_s2(fonts, sub_idx=1)
    make_frame_s2(fonts, sub_idx=2)
    make_frame_s2(fonts, sub_idx=3)
    
    # Scene 3
    make_frame_s3(fonts, sub_idx=1)
    make_frame_s3(fonts, sub_idx=2)
    make_frame_s3(fonts, sub_idx=3)
    
    # Scene 4 Drills
    make_frame_s4(fonts, pair_idx=0, active_sound=None, is_repeat=False)
    make_frame_s4(fonts, pair_idx=1, active_sound="de", is_repeat=False)
    make_frame_s4(fonts, pair_idx=1, active_sound="de", is_repeat=True)
    make_frame_s4(fonts, pair_idx=1, active_sound="d", is_repeat=False)
    make_frame_s4(fonts, pair_idx=1, active_sound="d", is_repeat=True)
    
    make_frame_s4(fonts, pair_idx=2, active_sound="de", is_repeat=False)
    make_frame_s4(fonts, pair_idx=2, active_sound="de", is_repeat=True)
    make_frame_s4(fonts, pair_idx=2, active_sound="d", is_repeat=False)
    make_frame_s4(fonts, pair_idx=2, active_sound="d", is_repeat=True)
    
    make_frame_s4(fonts, pair_idx=3, active_sound="de", is_repeat=False)
    make_frame_s4(fonts, pair_idx=3, active_sound="de", is_repeat=True)
    make_frame_s4(fonts, pair_idx=3, active_sound="d", is_repeat=False)
    make_frame_s4(fonts, pair_idx=3, active_sound="d", is_repeat=True)
    
    # Scene 5 Quiz
    make_frame_s5(fonts, q_num=1, state="question")
    make_frame_s5(fonts, q_num=1, state="answer")
    make_frame_s5(fonts, q_num=2, state="question")
    make_frame_s5(fonts, q_num=2, state="answer")
    
    # Scene 6 Summary
    make_frame_s6(fonts)
    print("All slides v2 generated successfully!")

if __name__ == "__main__":
    generate_all()
