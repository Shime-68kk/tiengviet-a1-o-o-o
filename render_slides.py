from PIL import Image, ImageDraw, ImageFont
import os

FRAMES_DIR = "/home/quang/video_ai/frames"
os.makedirs(FRAMES_DIR, exist_ok=True)

W, H = 1920, 1080

FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

def get_fonts():
    return {
        "title": ImageFont.truetype(FONT_BOLD, 64),
        "subtitle": ImageFont.truetype(FONT_REG, 34),
        "h2": ImageFont.truetype(FONT_BOLD, 48),
        "big_letter": ImageFont.truetype(FONT_BOLD, 160),
        "huge_letter": ImageFont.truetype(FONT_BOLD, 220),
        "word_vn": ImageFont.truetype(FONT_BOLD, 72),
        "word_en": ImageFont.truetype(FONT_REG, 36),
        "body": ImageFont.truetype(FONT_REG, 32),
        "body_bold": ImageFont.truetype(FONT_BOLD, 32),
        "badge": ImageFont.truetype(FONT_BOLD, 28),
        "small": ImageFont.truetype(FONT_REG, 24)
    }

def draw_header(draw, fonts, scene_tag, title_text, subtitle_text=""):
    # Header tag / breadcrumb
    draw.rounded_rectangle([80, 50, 320, 100], radius=12, fill="#0284C7")
    draw.text((100, 62), scene_tag, font=fonts["badge"], fill="#FFFFFF")
    
    # Title
    draw.text((350, 52), title_text, font=fonts["h2"], fill="#F8FAFC")
    if subtitle_text:
        draw.text((350, 115), subtitle_text, font=fonts["subtitle"], fill="#94A3B8")

def draw_card(draw, box, bg="#1E293B", border="#334155", border_width=2, radius=20):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=radius, fill=bg, outline=border, width=border_width)

def draw_articulatory_diagram(draw, fonts, x, y, sound_type="de"):
    # Box for diagram
    box = [x, y, x + 500, y + 420]
    draw_card(draw, box, bg="#0F172A", border="#38BDF8", border_width=2, radius=16)
    
    draw.text((x + 30, y + 25), "SƠ ĐỒ CẤU ÂM (ARTICULATION)", font=fonts["badge"], fill="#38BDF8")
    
    if sound_type == "de": # Đ - Alveolar Stop
        # Draw palate and teeth
        draw.arc([x + 80, y + 90, x + 380, y + 250], start=180, end=340, fill="#E2E8F0", width=8)
        # Upper teeth
        draw.rectangle([x + 140, y + 170, x + 165, y + 220], fill="#FFFFFF", outline="#94A3B8", width=2)
        draw.text((x + 80, y + 230), "Răng trên", font=fonts["small"], fill="#94A3B8")
        
        # Alveolar ridge circle
        draw.ellipse([x + 180, y + 155, x + 205, y + 180], fill="#F43F5E")
        draw.text((x + 215, y + 140), "Nướu răng (Alveolar)", font=fonts["small"], fill="#FDA4AF")
        
        # Tongue touching alveolar ridge
        draw.arc([x + 150, y + 170, x + 350, y + 340], start=160, end=300, fill="#FB7185", width=24)
        # Touch point highlight
        draw.ellipse([x + 180, y + 165, x + 210, y + 195], fill="#EF4444")
        
        # Caption
        draw.text((x + 30, y + 330), "• Đầu lưỡi CHẶM nướu răng trên", font=fonts["body_bold"], fill="#F8FAFC")
        draw.text((x + 30, y + 370), "• Chặn luồng hơi → Bật ra dứt khoát", font=fonts["body"], fill="#38BDF8")
    else: # D - Dental Fricative
        # Draw upper & lower teeth lightly closed
        draw.rectangle([x + 170, y + 130, x + 195, y + 180], fill="#FFFFFF", outline="#94A3B8", width=2)
        draw.rectangle([x + 170, y + 195, x + 195, y + 245], fill="#FFFFFF", outline="#94A3B8", width=2)
        draw.text((x + 60, y + 175), "Răng khép", font=fonts["small"], fill="#94A3B8")
        
        # Air stream arrows through teeth gap
        for offset in [-10, 0, 10]:
            draw.line([x + 210, y + 190 + offset, x + 340, y + 190 + offset], fill="#F59E0B", width=4)
            # Arrow head
            draw.polygon([(x + 340, y + 185 + offset), (x + 360, y + 190 + offset), (x + 340, y + 195 + offset)], fill="#F59E0B")
            
        # Tongue behind teeth
        draw.arc([x + 200, y + 190, x + 380, y + 350], start=160, end=300, fill="#FB7185", width=20)
        
        # Caption
        draw.text((x + 30, y + 330), "• Hai hàm răng KHÉP NHẸ", font=fonts["body_bold"], fill="#F8FAFC")
        draw.text((x + 30, y + 370), "• Luồng khí xát qua kẽ răng (/z/ buzz)", font=fonts["body"], fill="#FBBF24")

# Scene 1: Intro
def make_frame_s1(fonts):
    im = Image.new("RGB", (W, H), "#0B1329")
    draw = ImageDraw.Draw(im)
    
    # Top banner
    draw.rounded_rectangle([680, 50, 1240, 105], radius=28, fill="#1E293B", outline="#38BDF8", width=2)
    draw.text((710, 62), "VIETNAMESE PHONETICS • LEVEL A1", font=fonts["badge"], fill="#38BDF8")
    
    # Main title
    draw.text((960, 170), "Phân Biệt Phụ Âm 'D' và 'Đ'", font=fonts["title"], fill="#F8FAFC", anchor="mt")
    draw.text((960, 250), "How to Master Vietnamese D vs Đ in 2.5 Minutes", font=fonts["subtitle"], fill="#94A3B8", anchor="mt")
    
    # Card 1: Letter Đ
    draw_card(draw, [250, 330, 850, 780], bg="#1E293B", border="#3B82F6", border_width=4)
    draw.text((550, 470), "Đ", font=fonts["huge_letter"], fill="#60A5FA", anchor="mm")
    draw.rounded_rectangle([350, 600, 750, 660], radius=12, fill="#1D4ED8")
    draw.text((550, 630), "CÓ GẠCH NGANG", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    draw.text((550, 710), "Sounds like English 'D' in 'Door'", font=fonts["body"], fill="#CBD5E1", anchor="mm")
    
    # VS circle
    draw.ellipse([900, 500, 1020, 620], fill="#EF4444")
    draw.text((960, 560), "VS", font=fonts["h2"], fill="#FFFFFF", anchor="mm")
    
    # Card 2: Letter D
    draw_card(draw, [1070, 330, 1670, 780], bg="#1E293B", border="#F59E0B", border_width=4)
    draw.text((1370, 470), "D", font=fonts["huge_letter"], fill="#FBBF24", anchor="mm")
    draw.rounded_rectangle([1170, 600, 1570, 660], radius=12, fill="#B45309")
    draw.text((1370, 630), "KHÔNG GẠCH NGANG", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    draw.text((1370, 710), "Sounds like English 'Z' in 'Zoo'", font=fonts["body"], fill="#CBD5E1", anchor="mm")
    
    # Bottom Microlearning Goal Bar
    draw_card(draw, [250, 830, 1670, 970], bg="#0F172A", border="#10B981", border_width=2)
    draw.text((960, 875), "🎯 MỤC TIÊU MICROLEARNING:", font=fonts["body_bold"], fill="#10B981", anchor="mm")
    draw.text((960, 925), "Phân biệt cấu âm chuẩn xác • Luyện phát âm từ A1 • Làm đúng 100% Mini Quiz", font=fonts["body"], fill="#F8FAFC", anchor="mm")
    
    im.save(os.path.join(FRAMES_DIR, "s1_intro.png"))

# Scene 2: Letter Đ (/ɗ/)
def make_frame_s2(fonts):
    im = Image.new("RGB", (W, H), "#0B1329")
    draw = ImageDraw.Draw(im)
    draw_header(draw, fonts, "BÀI HỌC 1", "CHINH PHỤC PHỤ ÂM: 'Đ' (/ɗ/)", "Âm Tắc - Đầu Lưỡi Chân Răng (Alveolar Stop)")
    
    # Left: Big letter card + Mnemonic
    draw_card(draw, [80, 200, 600, 700], bg="#1E293B", border="#3B82F6", border_width=3)
    draw.text((340, 350), "Đ", font=fonts["huge_letter"], fill="#60A5FA", anchor="mm")
    draw.text((340, 490), "IPA: /ɗ/ hoặc [ʔd]", font=fonts["body_bold"], fill="#93C5FD", anchor="mm")
    
    # Mnemonic box
    draw.rounded_rectangle([120, 550, 560, 660], radius=14, fill="#1E3A8A", outline="#60A5FA", width=2)
    draw.text((340, 580), "🔑 MẸO GHI NHỚ:", font=fonts["badge"], fill="#FDE047", anchor="mm")
    draw.text((340, 625), "Đ = English 'D' in DOOR / DAY", font=fonts["body_bold"], fill="#FFFFFF", anchor="mm")
    
    # Middle: Articulation diagram
    draw_articulatory_diagram(draw, fonts, 640, 200, sound_type="de")
    
    # Right: Vocabulary Cards
    draw_card(draw, [1180, 200, 1840, 700], bg="#1E293B", border="#334155", border_width=2)
    draw.text((1510, 245), "VÍ DỤ TỪ VỰNG A1 CHUẨN", font=fonts["badge"], fill="#38BDF8", anchor="mm")
    
    # Vocab items
    words = [
        ("Đi", "/ɗi/", "to go / walk", "🚶"),
        ("Đỏ", "/ɗɔ̌/", "red color", "🔴"),
        ("Đẹp", "/ɗɛp̚/", "beautiful", "✨")
    ]
    for idx, (vn, ipa, en, icon) in enumerate(words):
        wy = 310 + idx * 125
        draw.rounded_rectangle([1220, wy, 1800, wy + 105], radius=12, fill="#0F172A", outline="#3B82F6", width=2)
        draw.text((1250, wy + 52), f"{icon} {vn}", font=fonts["word_vn"], fill="#FFFFFF", anchor="lm")
        draw.text((1480, wy + 52), ipa, font=fonts["body"], fill="#60A5FA", anchor="lm")
        draw.text((1630, wy + 52), en, font=fonts["word_en"], fill="#CBD5E1", anchor="lm")
        
    # Bottom Practice banner
    draw_card(draw, [80, 740, 1840, 980], bg="#0F172A", border="#10B981", border_width=2)
    draw.text((960, 810), "🔊 LẮNG NGHE NGƯỜI BẢN XỨ PHÁT ÂM:", font=fonts["h2"], fill="#F8FAFC", anchor="mm")
    draw.text((960, 890), "ĐỜ   •   Đ   •   ĐI   •   ĐỎ   •   ĐẸP", font=fonts["word_vn"], fill="#34D399", anchor="mm")
    draw.text((960, 950), "(Tongue touches upper gum, stop air, release!)", font=fonts["body"], fill="#94A3B8", anchor="mm")

    im.save(os.path.join(FRAMES_DIR, "s2_de.png"))

# Scene 3: Letter D (/z/)
def make_frame_s3(fonts):
    im = Image.new("RGB", (W, H), "#0B1329")
    draw = ImageDraw.Draw(im)
    draw_header(draw, fonts, "BÀI HỌC 2", "CHINH PHỤC PHỤ ÂM: 'D' (/z/)", "Âm Xát - Đầu Lưỡi Răng (Dental Fricative)")
    
    # Left: Big letter card + Mnemonic
    draw_card(draw, [80, 200, 600, 700], bg="#1E293B", border="#F59E0B", border_width=3)
    draw.text((340, 350), "D", font=fonts["huge_letter"], fill="#FBBF24", anchor="mm")
    draw.text((340, 490), "IPA: /z/ (Bắc) • /j/ (Nam)", font=fonts["body_bold"], fill="#FCD34D", anchor="mm")
    
    # Mnemonic box
    draw.rounded_rectangle([120, 550, 560, 660], radius=14, fill="#78350F", outline="#FBBF24", width=2)
    draw.text((340, 580), "🔑 MẸO GHI NHỚ:", font=fonts["badge"], fill="#FDE047", anchor="mm")
    draw.text((340, 625), "D = English 'Z' in ZOO / ZERO", font=fonts["body_bold"], fill="#FFFFFF", anchor="mm")
    
    # Middle: Articulation diagram
    draw_articulatory_diagram(draw, fonts, 640, 200, sound_type="d")
    
    # Right: Vocabulary Cards
    draw_card(draw, [1180, 200, 1840, 700], bg="#1E293B", border="#334155", border_width=2)
    draw.text((1510, 245), "VÍ DỤ TỪ VỰNG A1 CHUẨN", font=fonts["badge"], fill="#F59E0B", anchor="mm")
    
    words = [
        ("Da", "/za/", "skin", "✋"),
        ("Dễ", "/ze˦ˀ˥/", "easy", "👌"),
        ("Dưa", "/zɨə/", "melon", "🍉")
    ]
    for idx, (vn, ipa, en, icon) in enumerate(words):
        wy = 310 + idx * 125
        draw.rounded_rectangle([1220, wy, 1800, wy + 105], radius=12, fill="#0F172A", outline="#F59E0B", width=2)
        draw.text((1250, wy + 52), f"{icon} {vn}", font=fonts["word_vn"], fill="#FFFFFF", anchor="lm")
        draw.text((1480, wy + 52), ipa, font=fonts["body"], fill="#FBBF24", anchor="lm")
        draw.text((1630, wy + 52), en, font=fonts["word_en"], fill="#CBD5E1", anchor="lm")
        
    # Bottom Practice banner
    draw_card(draw, [80, 740, 1840, 980], bg="#0F172A", border="#F59E0B", border_width=2)
    draw.text((960, 810), "🔊 LẮNG NGHE NGƯỜI BẢN XỨ PHÁT ÂM:", font=fonts["h2"], fill="#F8FAFC", anchor="mm")
    draw.text((960, 890), "DỜ   •   D   •   DA   •   DỄ   •   DƯA", font=fonts["word_vn"], fill="#FBBF24", anchor="mm")
    draw.text((960, 950), "(Teeth lightly closed, continuous hissing buzz /z/!)", font=fonts["body"], fill="#94A3B8", anchor="mm")

    im.save(os.path.join(FRAMES_DIR, "s3_d.png"))

# Scene 4: Drill minimal pairs
def make_frame_s4(fonts, active_pair=None, repeat_prompt=False):
    im = Image.new("RGB", (W, H), "#0B1329")
    draw = ImageDraw.Draw(im)
    draw_header(draw, fonts, "THỰC HÀNH", "LUYỆN TẬP CẶP TỪ ĐỐI LẬP (MINIMAL PAIRS)", "Nghe Người Bản Xứ → Nhìn Tín Hiệu → Bắt Chước To Rõ")
    
    # Left Header: Đ column
    draw_card(draw, [120, 200, 920, 820], bg="#1E293B", border="#3B82F6", border_width=3)
    draw.rounded_rectangle([150, 230, 890, 310], radius=12, fill="#1D4ED8")
    draw.text((520, 270), "PHỤ ÂM Đ (/ɗ/ - Stop like Door)", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    
    # Right Header: D column
    draw_card(draw, [1000, 200, 1800, 820], bg="#1E293B", border="#F59E0B", border_width=3)
    draw.rounded_rectangle([1030, 230, 1770, 310], radius=12, fill="#B45309")
    draw.text((1400, 270), "PHỤ ÂM D (/z/ - Buzz like Zoo)", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    
    pairs = [
        (1, "ĐI", "(to go)", "DA", "(skin)"),
        (2, "ĐỎ", "(red)", "DỞ", "(bad/not good)"),
        (3, "ĐO", "(to measure)", "DO", "(because of)")
    ]
    
    for idx, (num, w_de, m_de, w_d, m_d) in enumerate(pairs):
        py = 340 + idx * 150
        is_active = (active_pair == num)
        
        # Left card
        border_de = "#60A5FA" if is_active else "#334155"
        fill_de = "#172554" if is_active else "#0F172A"
        draw.rounded_rectangle([160, py, 880, py + 120], radius=14, fill=fill_de, outline=border_de, width=3 if is_active else 1)
        draw.text((250, py + 60), w_de, font=fonts["word_vn"], fill="#FFFFFF", anchor="lm")
        draw.text((500, py + 60), m_de, font=fonts["body"], fill="#93C5FD", anchor="lm")
        
        # Right card
        border_d = "#FBBF24" if is_active else "#334155"
        fill_d = "#451A03" if is_active else "#0F172A"
        draw.rounded_rectangle([1040, py, 1760, py + 120], radius=14, fill=fill_d, outline=border_d, width=3 if is_active else 1)
        draw.text((1130, py + 60), w_d, font=fonts["word_vn"], fill="#FFFFFF", anchor="lm")
        draw.text((1380, py + 60), m_d, font=fonts["body"], fill="#FCD34D", anchor="lm")
        
    # Bottom Action Bar
    draw_card(draw, [120, 860, 1800, 990], bg="#0F172A", border="#10B981" if repeat_prompt else "#38BDF8", border_width=2)
    if repeat_prompt:
        draw.text((960, 925), "🎙️ ĐẾN LƯỢT BẠN: BẬT MIC VÀ LẶP LẠI TO RÕ! (REPEAT NOW)", font=fonts["h2"], fill="#10B981", anchor="mm")
    else:
        draw.text((960, 925), "🎧 LẮNG NGHE VÀ CẢM NHẬN SỰ KHÁC BIỆT CẤU ÂM", font=fonts["h2"], fill="#38BDF8", anchor="mm")

    filename = f"s4_drill_p{active_pair if active_pair else 0}_{'rep' if repeat_prompt else 'listen'}.png"
    im.save(os.path.join(FRAMES_DIR, filename))

# Scene 5: Mini Quiz
def make_frame_s5(fonts, q_num=1, state="question"): # state: question, answer
    im = Image.new("RGB", (W, H), "#0B1329")
    draw = ImageDraw.Draw(im)
    draw_header(draw, fonts, "THỬ THÁCH", f"MINI QUIZ - CÂU HỎI {q_num}/2", "Nghe Âm Thanh → Chọn Từ Bạn Nghe Được Trong 3 Giây")
    
    # Quiz container
    draw_card(draw, [250, 200, 1670, 980], bg="#1E293B", border="#38BDF8", border_width=3)
    
    # Sound prompt card
    draw.rounded_rectangle([320, 250, 1600, 420], radius=16, fill="#0F172A", outline="#0284C7", width=2)
    draw.text((960, 310), f"🔊 CÂU HỎI {q_num}: Bạn vừa nghe thấy từ nào dưới đây?", font=fonts["h2"], fill="#F8FAFC", anchor="mm")
    draw.text((960, 375), "Which word did the native speaker just say?", font=fonts["subtitle"], fill="#94A3B8", anchor="mm")
    
    if q_num == 1:
        opt_a = ("A", "Đi", "/ɗi/ (to go)")
        opt_b = ("B", "Di", "/zi/ (fricative)")
        correct = "A"
    else:
        opt_a = ("A", "Đa", "/ɗa/ (banyan)")
        opt_b = ("B", "Da", "/za/ (skin)")
        correct = "B"
        
    # Choice A
    box_a = [320, 470, 930, 770]
    is_a_correct = (correct == "A" and state == "answer")
    border_a = "#10B981" if is_a_correct else "#334155"
    fill_a = "#064E3B" if is_a_correct else "#0F172A"
    draw.rounded_rectangle(box_a, radius=18, fill=fill_a, outline=border_a, width=4 if is_a_correct else 2)
    draw.text((400, 550), "[A]", font=fonts["h2"], fill="#60A5FA", anchor="mm")
    draw.text((620, 580), opt_a[1], font=fonts["huge_letter"], fill="#FFFFFF", anchor="mm")
    draw.text((620, 710), opt_a[2], font=fonts["body"], fill="#94A3B8", anchor="mm")
    
    # Choice B
    box_b = [990, 470, 1600, 770]
    is_b_correct = (correct == "B" and state == "answer")
    border_b = "#10B981" if is_b_correct else "#334155"
    fill_b = "#064E3B" if is_b_correct else "#0F172A"
    draw.rounded_rectangle(box_b, radius=18, fill=fill_b, outline=border_b, width=4 if is_b_correct else 2)
    draw.text((1070, 550), "[B]", font=fonts["h2"], fill="#F59E0B", anchor="mm")
    draw.text((1290, 580), opt_b[1], font=fonts["huge_letter"], fill="#FFFFFF", anchor="mm")
    draw.text((1290, 710), opt_b[2], font=fonts["body"], fill="#94A3B8", anchor="mm")
    
    # Status bar
    if state == "question":
        draw.rounded_rectangle([320, 820, 1600, 930], radius=14, fill="#1E293B", outline="#F59E0B", width=2)
        draw.text((960, 875), "⏱️ 3... 2... 1... Bạn chọn A hay B?", font=fonts["h2"], fill="#FBBF24", anchor="mm")
    else:
        draw.rounded_rectangle([320, 820, 1600, 930], radius=14, fill="#065F46", outline="#34D399", width=2)
        draw.text((960, 875), f"🎉 CHÍNH XÁC! ĐÁP ÁN ĐÚNG LÀ [{correct}]!", font=fonts["h2"], fill="#FFFFFF", anchor="mm")

    im.save(os.path.join(FRAMES_DIR, f"s5_q{q_num}_{state}.png"))

# Scene 6: Golden Rule Summary
def make_frame_s6(fonts):
    im = Image.new("RGB", (W, H), "#0B1329")
    draw = ImageDraw.Draw(im)
    draw_header(draw, fonts, "TỔNG KẾT", "QUY TẮC VÀNG GHI NHỚ SUỐT ĐỜI", "Golden Rules to Never Confuse D and Đ Again")
    
    # Table Card
    draw_card(draw, [150, 200, 1770, 780], bg="#1E293B", border="#38BDF8", border_width=3)
    
    # Row 1: Đ
    draw.rounded_rectangle([200, 240, 1720, 470], radius=16, fill="#0F172A", outline="#3B82F6", width=2)
    draw.text((320, 355), "Đ", font=fonts["huge_letter"], fill="#60A5FA", anchor="mm")
    draw.text((470, 320), "CHỮ Đ (Có gạch ngang)", font=fonts["h2"], fill="#F8FAFC", anchor="lm")
    draw.text((470, 390), "= English 'D' in DOOR / DAY (/ɗ/ Alveolar Stop)", font=fonts["subtitle"], fill="#93C5FD", anchor="lm")
    draw.text((1480, 355), "Ví dụ: Đi, Đỏ, Đẹp", font=fonts["word_en"], fill="#34D399", anchor="mm")
    
    # Row 2: D
    draw.rounded_rectangle([200, 510, 1720, 740], radius=16, fill="#0F172A", outline="#F59E0B", width=2)
    draw.text((320, 625), "D", font=fonts["huge_letter"], fill="#FBBF24", anchor="mm")
    draw.text((470, 590), "CHỮ D (Không gạch ngang)", font=fonts["h2"], fill="#F8FAFC", anchor="lm")
    draw.text((470, 660), "= English 'Z' in ZOO / ZERO (/z/ Dental Fricative)", font=fonts["subtitle"], fill="#FCD34D", anchor="lm")
    draw.text((1480, 625), "Ví dụ: Da, Dễ, Dưa", font=fonts["word_en"], fill="#34D399", anchor="mm")
    
    # Bottom congrats bar
    draw_card(draw, [150, 830, 1770, 980], bg="#047857", border="#34D399", border_width=2)
    draw.text((960, 880), "🌟 CHÚC MỪNG BẠN ĐÃ LÀM CHỦ PHỤ ÂM D VÀ Đ!", font=fonts["h2"], fill="#FFFFFF", anchor="mm")
    draw.text((960, 935), "Cảm ơn các bạn • Like & Subscribe để học thêm tiếng Việt A1 • Tạm biệt!", font=fonts["body"], fill="#D1FAE5", anchor="mm")

    im.save(os.path.join(FRAMES_DIR, "s6_summary.png"))

def generate_all_slides():
    fonts = get_fonts()
    print("Rendering slides...")
    make_frame_s1(fonts)
    make_frame_s2(fonts)
    make_frame_s3(fonts)
    
    # Drill frames
    make_frame_s4(fonts, active_pair=0, repeat_prompt=False)
    make_frame_s4(fonts, active_pair=1, repeat_prompt=False)
    make_frame_s4(fonts, active_pair=1, repeat_prompt=True)
    make_frame_s4(fonts, active_pair=2, repeat_prompt=False)
    make_frame_s4(fonts, active_pair=2, repeat_prompt=True)
    make_frame_s4(fonts, active_pair=3, repeat_prompt=False)
    make_frame_s4(fonts, active_pair=3, repeat_prompt=True)
    
    # Quiz frames
    make_frame_s5(fonts, q_num=1, state="question")
    make_frame_s5(fonts, q_num=1, state="answer")
    make_frame_s5(fonts, q_num=2, state="question")
    make_frame_s5(fonts, q_num=2, state="answer")
    
    # Summary frame
    make_frame_s6(fonts)
    print("All slides rendered successfully!")

if __name__ == "__main__":
    generate_all_slides()
