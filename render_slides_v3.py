from PIL import Image, ImageDraw, ImageFont
import os

FRAMES_DIR = "/home/quang/video_ai/frames_v3"
os.makedirs(FRAMES_DIR, exist_ok=True)

W, H = 1920, 1080

FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

def get_fonts():
    return {
        "title": ImageFont.truetype(FONT_BOLD, 46),
        "subtitle": ImageFont.truetype(FONT_REG, 26),
        "h2": ImageFont.truetype(FONT_BOLD, 36),
        "h3": ImageFont.truetype(FONT_BOLD, 28),
        "big_letter": ImageFont.truetype(FONT_BOLD, 130),
        "huge_letter": ImageFont.truetype(FONT_BOLD, 170),
        "word_vn": ImageFont.truetype(FONT_BOLD, 50),
        "word_en": ImageFont.truetype(FONT_REG, 26),
        "body": ImageFont.truetype(FONT_REG, 24),
        "body_bold": ImageFont.truetype(FONT_BOLD, 24),
        "badge": ImageFont.truetype(FONT_BOLD, 20),
        "sub_en": ImageFont.truetype(FONT_BOLD, 26),
        "sub_vi": ImageFont.truetype(FONT_REG, 24),
        "small": ImageFont.truetype(FONT_REG, 20)
    }

def create_base_canvas():
    # Premium Modern Tech-Ed Slate Background with glowing gradients
    im = Image.new("RGB", (W, H), "#080E1E")
    draw = ImageDraw.Draw(im)
    
    # Ambient glows
    draw.ellipse([-150, -150, 500, 500], fill="#0F1D3D")
    draw.ellipse([W - 500, -150, W + 200, 500], fill="#131C38")
    draw.ellipse([W//2 - 450, H - 350, W//2 + 450, H + 350], fill="#0A1630")
    
    # Safe zone outline
    draw.rounded_rectangle([15, 15, W - 15, H - 15], radius=24, outline="#1E293B", width=2)
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
        
        bg = "#0284C7" if is_active else ("#1E293B" if is_past else "#0B1329")
        border = "#38BDF8" if is_active else ("#334155" if is_past else "#1E293B")
        txt_col = "#FFFFFF" if is_active else ("#94A3B8" if is_past else "#475569")
        
        draw.rounded_rectangle([sx, y, ex, y + 42], radius=10, fill=bg, outline=border, width=2 if is_active else 1)
        draw.text(((sx + ex) // 2, y + 21), s_name, font=fonts["badge"], fill=txt_col, anchor="mm")

def draw_subtitle_box(draw, fonts, en_text, vi_text):
    # Subtitle container anchored at bottom (safe zone, 0% overflow, NO emojis)
    box = [100, 895, 1820, 1030]
    draw.rounded_rectangle(box, radius=16, fill="#0B1329", outline="#0284C7", width=2)
    
    # Tag badge
    draw.rounded_rectangle([125, 915, 235, 950], radius=8, fill="#0369A1")
    draw.text((180, 932), "SUBTITLES", font=fonts["small"], fill="#FFFFFF", anchor="mm")
    
    # Dual-line bilingual subtitles
    draw.text((255, 932), en_text, font=fonts["sub_en"], fill="#F8FAFC", anchor="lm")
    draw.text((255, 985), f"[VI] {vi_text}", font=fonts["sub_vi"], fill="#38BDF8", anchor="lm")

def draw_card(draw, box, bg="#111B33", border="#1E3A8A", border_width=2, radius=18):
    draw.rounded_rectangle(box, radius=radius, fill=bg, outline=border, width=border_width)

def draw_articulatory_diagram(draw, fonts, x, y, w, h, sound_type="de"):
    # Outer card
    draw_card(draw, [x, y, x + w, y + h], bg="#0B1226", border="#38BDF8" if sound_type=="de" else "#F59E0B", border_width=2, radius=16)
    
    # Header tag
    draw.rounded_rectangle([x + 25, y + 20, x + 380, y + 60], radius=10, fill="#0369A1" if sound_type=="de" else "#B45309")
    draw.text((x + 202, y + 40), "SƠ ĐỒ CẤU ÂM (ARTICULATION)", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    
    cx = x + 240
    cy = y + 220
    
    if sound_type == "de": # Đ - Alveolar Stop
        # 1. Palate arch
        draw.arc([cx - 160, cy - 140, cx + 220, cy + 100], start=180, end=350, fill="#475569", width=12)
        draw.text((cx + 100, cy - 110), "Vòm miệng", font=fonts["small"], fill="#94A3B8")
        
        # 2. Upper Gum (Alveolar Ridge)
        draw.ellipse([cx - 130, cy - 60, cx - 40, cy + 10], fill="#BE123C")
        draw.ellipse([cx - 65, cy - 45, cx - 35, cy - 15], fill="#EF4444", outline="#FECDD3", width=3)
        
        # 3. Upper front tooth
        draw.polygon([(cx - 115, cy - 15), (cx - 95, cy - 15), (cx - 98, cy + 45), (cx - 112, cy + 45)], fill="#F8FAFC", outline="#94A3B8", width=2)
        draw.text((cx - 180, cy + 20), "Răng trên", font=fonts["small"], fill="#94A3B8")
        
        # 4. Lower front tooth
        draw.polygon([(cx - 115, cy + 85), (cx - 95, cy + 85), (cx - 98, cy + 135), (cx - 112, cy + 135)], fill="#F8FAFC", outline="#94A3B8", width=2)
        draw.text((cx - 180, cy + 100), "Răng dưới", font=fonts["small"], fill="#94A3B8")
        
        # 5. Tongue Muscle - Tip touching alveolar ridge firmly
        tongue_pts = [
            (cx - 48, cy - 25),
            (cx + 30, cy - 10),
            (cx + 120, cy + 40),
            (cx + 150, cy + 140),
            (cx + 60, cy + 150),
            (cx - 10, cy + 110),
            (cx - 60, cy + 40)
        ]
        draw.polygon(tongue_pts, fill="#F43F5E", outline="#E11D48", width=3)
        draw.text((cx + 50, cy + 70), "LƯỠI (Tongue)", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
        
        # 6. Stop air indicator
        draw.rounded_rectangle([cx - 110, cy - 90, cx + 20, cy - 55], radius=8, fill="#991B1B")
        draw.text((cx - 45, cy - 72), "[STOP AIR]", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
        
        # 7. Callouts on the right side
        draw.rounded_rectangle([x + 480, y + 80, x + w - 30, y + 210], radius=12, fill="#1E293B", outline="#F43F5E", width=2)
        draw.text((x + 500, y + 105), "1. VỊ TRÍ TIẾP XÚC:", font=fonts["body_bold"], fill="#FECDD3")
        draw.text((x + 500, y + 145), "Đầu lưỡi ÁP CHẶT vào", font=fonts["body"], fill="#F8FAFC")
        draw.text((x + 500, y + 175), "nướu răng trên (Alveolar)", font=fonts["body_bold"], fill="#38BDF8")
        
        draw.rounded_rectangle([x + 480, y + 230, x + w - 30, y + 360], radius=12, fill="#1E293B", outline="#38BDF8", width=2)
        draw.text((x + 500, y + 255), "2. CƠ CHẾ BẬT HƠI:", font=fonts["body_bold"], fill="#93C5FD")
        draw.text((x + 500, y + 295), "Chặn hoàn toàn luồng hơi,", font=fonts["body"], fill="#F8FAFC")
        draw.text((x + 500, y + 325), "bật ra dứt khoát như 'Door'", font=fonts["body_bold"], fill="#FDE047")
        
        # Pointer line
        draw.line([cx - 35, cy - 30, x + 480, y + 145], fill="#EF4444", width=2)
        draw.ellipse([x + 477, y + 142, x + 483, y + 148], fill="#EF4444")
        
    else: # D - Dental Fricative
        # Palate arch
        draw.arc([cx - 160, cy - 140, cx + 220, cy + 100], start=180, end=350, fill="#475569", width=12)
        draw.text((cx + 100, cy - 110), "Vòm miệng", font=fonts["small"], fill="#94A3B8")
        
        # Upper & lower incisors lightly closed
        draw.polygon([(cx - 95, cy - 40), (cx - 75, cy - 40), (cx - 78, cy + 20), (cx - 92, cy + 20)], fill="#F8FAFC", outline="#94A3B8", width=2)
        draw.polygon([(cx - 95, cy + 30), (cx - 75, cy + 30), (cx - 78, cy + 90), (cx - 92, cy + 90)], fill="#F8FAFC", outline="#94A3B8", width=2)
        draw.text((cx - 175, cy + 25), "Răng khép nhẹ", font=fonts["small"], fill="#94A3B8")
        
        # Continuous friction buzz waves (Amber)
        for offset in [-12, 0, 12]:
            yy = cy + 25 + offset
            draw.line([cx - 60, yy, cx + 90, yy], fill="#F59E0B", width=4)
            draw.polygon([(cx + 90, yy - 5), (cx + 105, yy), (cx + 90, yy + 5)], fill="#F59E0B")
            
        draw.rounded_rectangle([cx - 30, cy - 70, cx + 110, cy - 35], radius=8, fill="#78350F")
        draw.text((cx + 40, cy - 52), "[BUZZ /z/]", font=fonts["badge"], fill="#FDE047", anchor="mm")
        
        # Tongue positioned behind teeth without stopping air
        tongue_pts = [
            (cx - 50, cy + 20),
            (cx + 30, cy + 35),
            (cx + 120, cy + 70),
            (cx + 150, cy + 150),
            (cx + 60, cy + 160),
            (cx - 10, cy + 130),
            (cx - 60, cy + 70)
        ]
        draw.polygon(tongue_pts, fill="#F43F5E", outline="#E11D48", width=3)
        draw.text((cx + 40, cy + 100), "LƯỠI (Tongue)", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
        
        # Callouts
        draw.rounded_rectangle([x + 480, y + 80, x + w - 30, y + 210], radius=12, fill="#1E293B", outline="#F59E0B", width=2)
        draw.text((x + 500, y + 105), "1. KHẨU HÌNH RĂNG:", font=fonts["body_bold"], fill="#FDE047")
        draw.text((x + 500, y + 145), "Hai hàm răng KHÉP NHẸ,", font=fonts["body"], fill="#F8FAFC")
        draw.text((x + 500, y + 175), "đầu lưỡi đặt phía sau răng", font=fonts["body_bold"], fill="#F59E0B")
        
        draw.rounded_rectangle([x + 480, y + 230, x + w - 30, y + 360], radius=12, fill="#1E293B", outline="#38BDF8", width=2)
        draw.text((x + 500, y + 255), "2. CƠ CHẾ RUNG XÁT:", font=fonts["body_bold"], fill="#93C5FD")
        draw.text((x + 500, y + 295), "Luồng hơi ma sát liên tục", font=fonts["body"], fill="#F8FAFC")
        draw.text((x + 500, y + 325), "tạo âm rung /z/ như 'Zoo'", font=fonts["body_bold"], fill="#38BDF8")
        
        draw.line([cx - 60, cy + 25, x + 480, y + 145], fill="#F59E0B", width=2)
        draw.ellipse([x + 477, y + 142, x + 483, y + 148], fill="#F59E0B")

# -------------------------------------------------------------
# SCENE 1: INTRO
# -------------------------------------------------------------
def make_frame_s1(fonts):
    im = create_base_canvas()
    draw = ImageDraw.Draw(im)
    draw_top_progress(draw, fonts, current_step=1)
    
    # Title Tag & Main Title
    draw.rounded_rectangle([700, 95, 1220, 140], radius=12, fill="#0F172A", outline="#38BDF8", width=2)
    draw.text((960, 117), "NGỮ ÂM TIẾNG VIỆT • TRÌNH ĐỘ A1", font=fonts["badge"], fill="#38BDF8", anchor="mm")
    
    draw.text((960, 185), "PHÂN BIỆT HAI PHỤ ÂM: 'D' VÀ 'Đ'", font=fonts["title"], fill="#F8FAFC", anchor="mm")
    draw.text((960, 235), "Mastering Vietnamese D vs Đ in 2.5 Minutes", font=fonts["subtitle"], fill="#94A3B8", anchor="mm")
    
    # Left Hero Card: Đ
    draw_card(draw, [150, 280, 850, 720], bg="#0F1B36", border="#3B82F6", border_width=3)
    draw.text((500, 410), "Đ", font=fonts["huge_letter"], fill="#60A5FA", anchor="mm")
    draw.rounded_rectangle([220, 520, 780, 580], radius=12, fill="#1D4ED8")
    draw.text((500, 550), "CÓ GẠCH NGANG (CROSSBAR)", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    draw.text((500, 630), "= English 'D' in 'DOOR' / 'DAY'", font=fonts["h3"], fill="#93C5FD", anchor="mm")
    draw.text((500, 675), "IPA: /ɗ/ • Âm tắc đầu lưỡi", font=fonts["body"], fill="#CBD5E1", anchor="mm")
    
    # Center VS Badge
    draw.ellipse([900, 440, 1020, 560], fill="#EF4444", outline="#FCA5A5", width=3)
    draw.text((960, 500), "VS", font=fonts["h2"], fill="#FFFFFF", anchor="mm")
    
    # Right Hero Card: D
    draw_card(draw, [1070, 280, 1770, 720], bg="#1B1726", border="#F59E0B", border_width=3)
    draw.text((1420, 410), "D", font=fonts["huge_letter"], fill="#FBBF24", anchor="mm")
    draw.rounded_rectangle([1140, 520, 1700, 580], radius=12, fill="#B45309")
    draw.text((1420, 550), "KHÔNG GẠCH NGANG (PLAIN)", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    draw.text((1420, 630), "= English 'Z' in 'ZOO' / 'ZERO'", font=fonts["h3"], fill="#FDE047", anchor="mm")
    draw.text((1420, 675), "IPA: /z/ • Âm xát đầu lưỡi răng", font=fonts["body"], fill="#CBD5E1", anchor="mm")
    
    # Bottom Target Goal Banner
    draw.rounded_rectangle([300, 765, 1620, 840], radius=16, fill="#064E3B", outline="#10B981", width=2)
    draw.text((960, 802), "MỤC TIÊU: Làm chủ vị trí cấu âm - Luyện nói cặp từ - Vượt qua Mini Quiz", font=fonts["body_bold"], fill="#A7F3D0", anchor="mm")
    
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
    
    # Header area
    draw.text((100, 105), "BÀI HỌC 1: CHINH PHỤC PHỤ ÂM 'Đ'", font=fonts["title"], fill="#60A5FA")
    draw.text((100, 155), "Ngữ âm: Âm Tắc - Đầu Lưỡi Chân Răng (Alveolar Stop)  |  Ký hiệu IPA: /ɗ/ hoặc [ʔd]", font=fonts["subtitle"], fill="#94A3B8")
    
    # Left Column: Big Letter & Core Rules (Width 820px)
    draw_card(draw, [100, 210, 920, 850], bg="#0F1B36", border="#3B82F6", border_width=3)
    
    # Letter header block
    draw.text((250, 310), "Đ", font=fonts["huge_letter"], fill="#60A5FA", anchor="mm")
    
    draw.rounded_rectangle([390, 235, 870, 290], radius=10, fill="#1E3A8A")
    draw.text((630, 262), "CHỮ Đ: CÓ GẠCH NGANG", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    
    draw.rounded_rectangle([390, 310, 870, 365], radius=10, fill="#0B1329", outline="#3B82F6", width=2)
    draw.text((630, 337), "IPA: /ɗ/ (Hữu thanh)", font=fonts["body_bold"], fill="#93C5FD", anchor="mm")
    
    # Mnemonic Card
    draw.rounded_rectangle([130, 400, 890, 520], radius=14, fill="#172554", outline="#60A5FA", width=2)
    draw.text((510, 435), "QUY TẮC VÀNG GHI NHỚ:", font=fonts["badge"], fill="#FDE047", anchor="mm")
    draw.text((510, 485), "Đ = English 'D' trong DOOR / DAY", font=fonts["h3"], fill="#FFFFFF", anchor="mm")
    
    # 3-step Pronunciation Rules
    draw.rounded_rectangle([130, 545, 890, 820], radius=14, fill="#0B1329", outline="#334155", width=2)
    draw.text((160, 575), "3 BƯỚC PHÁT ÂM CHUẨN XÁC:", font=fonts["body_bold"], fill="#38BDF8")
    
    steps = [
        "1. Đặt đầu lưỡi chạm chặt vào nướu răng hàm trên.",
        "2. Chặn luồng hơi lại hoàn toàn trong miệng.",
        "3. Bật luồng hơi ra dứt khoát cùng lúc rung dây thanh."
    ]
    for idx, s in enumerate(steps):
        draw.text((160, 625 + idx * 55), s, font=fonts["body"], fill="#F8FAFC")
        
    # Right Column: Diagram + Vocab (Width 860px)
    draw_articulatory_diagram(draw, fonts, 960, 210, 860, 400, sound_type="de")
    
    # Vocab Container
    draw_card(draw, [960, 630, 1820, 850], bg="#0F1B36", border="#334155", border_width=2)
    draw.text((1390, 660), "TỪ VỰNG A1 MẪU (VOCABULARY)", font=fonts["badge"], fill="#38BDF8", anchor="mm")
    
    words = [
        ("Đi", "/ɗi/", "to go / walk"),
        ("Đỏ", "/ɗɔ̌/", "red color"),
        ("Đẹp", "/ɗɛp̚/", "beautiful")
    ]
    for idx, (vn, ipa, en) in enumerate(words):
        wx = 990 + idx * 265
        draw.rounded_rectangle([wx, 700, wx + 250, 820], radius=12, fill="#0B1329", outline="#1D4ED8", width=2)
        draw.text((wx + 125, 735), vn, font=fonts["word_vn"], fill="#FFFFFF", anchor="mm")
        draw.text((wx + 125, 775), ipa, font=fonts["body_bold"], fill="#60A5FA", anchor="mm")
        draw.text((wx + 125, 805), en, font=fonts["small"], fill="#CBD5E1", anchor="mm")
        
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
    
    # Header area
    draw.text((100, 105), "BÀI HỌC 2: CHINH PHỤC PHỤ ÂM 'D'", font=fonts["title"], fill="#FBBF24")
    draw.text((100, 155), "Ngữ âm: Âm Xát - Đầu Lưỡi Răng (Dental Fricative)  |  Ký hiệu IPA: /z/ (Bắc) hoặc /j/ (Nam)", font=fonts["subtitle"], fill="#94A3B8")
    
    # Left Column: Big Letter & Core Rules (Width 820px)
    draw_card(draw, [100, 210, 920, 850], bg="#1A1624", border="#F59E0B", border_width=3)
    
    # Letter header block
    draw.text((250, 310), "D", font=fonts["huge_letter"], fill="#FBBF24", anchor="mm")
    
    draw.rounded_rectangle([390, 235, 870, 290], radius=10, fill="#B45309")
    draw.text((630, 262), "CHỮ D: KHÔNG GẠCH NGANG", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    
    draw.rounded_rectangle([390, 310, 870, 365], radius=10, fill="#0B1329", outline="#F59E0B", width=2)
    draw.text((630, 337), "IPA: /z/ (Âm xát rung)", font=fonts["body_bold"], fill="#FDE047", anchor="mm")
    
    # Mnemonic Card
    draw.rounded_rectangle([130, 400, 890, 520], radius=14, fill="#451A03", outline="#F59E0B", width=2)
    draw.text((510, 435), "QUY TẮC VÀNG GHI NHỚ:", font=fonts["badge"], fill="#FDE047", anchor="mm")
    draw.text((510, 485), "D = English 'Z' trong ZOO / ZERO", font=fonts["h3"], fill="#FFFFFF", anchor="mm")
    
    # 3-step Pronunciation Rules
    draw.rounded_rectangle([130, 545, 890, 820], radius=14, fill="#0B1329", outline="#334155", width=2)
    draw.text((160, 575), "3 BƯỚC PHÁT ÂM CHUẨN XÁC:", font=fonts["body_bold"], fill="#FBBF24")
    
    steps = [
        "1. Khép nhẹ hai hàm răng, đầu lưỡi sát mặt sau răng.",
        "2. Thổi luồng hơi liên tục qua khe hở giữa các răng.",
        "3. Rung dây thanh tạo âm xát /z/. (Miền Nam đọc là /j/ như Yes)."
    ]
    for idx, s in enumerate(steps):
        draw.text((160, 625 + idx * 55), s, font=fonts["body"], fill="#F8FAFC")
        
    # Right Column: Diagram + Vocab (Width 860px)
    draw_articulatory_diagram(draw, fonts, 960, 210, 860, 400, sound_type="d")
    
    # Vocab Container
    draw_card(draw, [960, 630, 1820, 850], bg="#1A1624", border="#334155", border_width=2)
    draw.text((1390, 660), "TỪ VỰNG A1 MẪU (VOCABULARY)", font=fonts["badge"], fill="#F59E0B", anchor="mm")
    
    words = [
        ("Da", "/za/", "skin"),
        ("Dễ", "/ze˦ˀ˥/", "easy"),
        ("Dưa", "/zɨə/", "melon")
    ]
    for idx, (vn, ipa, en) in enumerate(words):
        wx = 990 + idx * 265
        draw.rounded_rectangle([wx, 700, wx + 250, 820], radius=12, fill="#0B1329", outline="#B45309", width=2)
        draw.text((wx + 125, 735), vn, font=fonts["word_vn"], fill="#FFFFFF", anchor="mm")
        draw.text((wx + 125, 775), ipa, font=fonts["body_bold"], fill="#FBBF24", anchor="mm")
        draw.text((wx + 125, 805), en, font=fonts["small"], fill="#CBD5E1", anchor="mm")
        
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
    
    # Header with generous line height and clear separation
    draw.rounded_rectangle([100, 95, 420, 135], radius=10, fill="#0369A1")
    draw.text((260, 115), "PHẦN 4: THỰC HÀNH", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    
    draw.text((100, 160), "LUYỆN TẬP CẶP TỪ ĐỐI LẬP (MINIMAL PAIRS)", font=fonts["title"], fill="#F8FAFC")
    draw.text((100, 205), "Quy trình: 1. Nghe người bản xứ  ->  2. Cảm nhận khẩu hình  ->  3. Lặp lại to rõ", font=fonts["subtitle"], fill="#38BDF8")
    
    # Left Card: Đ Column (Width 830px)
    draw_card(draw, [100, 245, 930, 760], bg="#0F1B36", border="#3B82F6", border_width=3)
    draw.rounded_rectangle([130, 265, 900, 325], radius=12, fill="#1D4ED8")
    draw.text((515, 295), "CỘT ÂM Đ: TẮC BẬT HƠI (/ɗ/ - NHƯ 'DOOR')", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    
    # Right Card: D Column (Width 830px)
    draw_card(draw, [990, 245, 1820, 760], bg="#1A1624", border="#F59E0B", border_width=3)
    draw.rounded_rectangle([1020, 265, 1790, 325], radius=12, fill="#B45309")
    draw.text((1405, 295), "CỘT ÂM D: XÁT RUNG RĂNG (/z/ - NHƯ 'ZOO')", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    
    pairs = [
        (1, "Đi", "(to go)", "Da", "(skin)"),
        (2, "Đỏ", "(red)", "Dở", "(not good)"),
        (3, "Đo", "(to measure)", "Do", "(because)")
    ]
    
    for idx, (p_num, w_de, m_de, w_d, m_d) in enumerate(pairs):
        py = 350 + idx * 130
        is_cur_pair = (pair_idx == p_num)
        
        # Left item (Đ)
        hl_de = is_cur_pair and (active_sound == "de")
        bg_de = "#1E3A8A" if hl_de else "#0B1329"
        bd_de = "#60A5FA" if hl_de else "#334155"
        draw.rounded_rectangle([130, py, 900, py + 110], radius=14, fill=bg_de, outline=bd_de, width=3 if hl_de else 1)
        draw.text((220, py + 55), w_de, font=fonts["word_vn"], fill="#FFFFFF" if not hl_de else "#93C5FD", anchor="lm")
        draw.text((430, py + 55), m_de, font=fonts["body"], fill="#94A3B8" if not hl_de else "#FFFFFF", anchor="lm")
        if hl_de:
            draw.rounded_rectangle([720, py + 30, 870, py + 80], radius=8, fill="#0284C7")
            draw.text((795, py + 55), "DANG NGHE", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
            
        # Right item (D)
        hl_d = is_cur_pair and (active_sound == "d")
        bg_d = "#78350F" if hl_d else "#0B1329"
        bd_d = "#FBBF24" if hl_d else "#334155"
        draw.rounded_rectangle([1020, py, 1790, py + 110], radius=14, fill=bg_d, outline=bd_d, width=3 if hl_d else 1)
        draw.text((1110, py + 55), w_d, font=fonts["word_vn"], fill="#FFFFFF" if not hl_d else "#FDE047", anchor="lm")
        draw.text((1320, py + 55), m_d, font=fonts["body"], fill="#94A3B8" if not hl_d else "#FFFFFF", anchor="lm")
        if hl_d:
            draw.rounded_rectangle([1610, py + 30, 1760, py + 80], radius=8, fill="#D97706")
            draw.text((1685, py + 55), "DANG NGHE", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
            
    # Bottom Action Bar
    if is_repeat:
        draw.rounded_rectangle([100, 785, 1820, 870], radius=16, fill="#064E3B", outline="#10B981", width=3)
        draw.text((960, 827), "[MIC ON] ĐẾN LƯỢT BẠN: BẬT MIC VÀ LẶP LẠI TO RÕ TRONG 2.5 GIÂY!", font=fonts["h2"], fill="#34D399", anchor="mm")
        en_sub = "Your turn: Repeat out loud now during the pause!"
        vi_sub = "Đến lượt bạn: Hãy mở mic và lặp lại thật to rõ trong khoảng dừng này!"
    else:
        draw.rounded_rectangle([100, 785, 1820, 870], radius=16, fill="#0F172A", outline="#0284C7", width=2)
        draw.text((960, 827), "LẮNG NGHE NGƯỜI BẢN XỨ VÀ CẢM NHẬN SỰ ĐỐI LẬP CẤU ÂM", font=fonts["h3"], fill="#38BDF8", anchor="mm")
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
    
    draw.rounded_rectangle([100, 95, 420, 135], radius=10, fill="#7C3AED")
    draw.text((260, 115), "PHẦN 5: THỬ THÁCH", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    
    draw.text((100, 160), f"MINI QUIZ THÍNH GIÁC: CÂU HỎI {q_num}/2", font=fonts["title"], fill="#38BDF8")
    draw.text((100, 205), "Quy tắc: Nghe âm thanh người bản xứ -> Chọn đáp án đúng trong 3 giây", font=fonts["subtitle"], fill="#94A3B8")
    
    # Question Card
    draw_card(draw, [150, 245, 1770, 765], bg="#0F1B36", border="#38BDF8", border_width=3)
    
    draw.rounded_rectangle([200, 275, 1720, 385], radius=16, fill="#0B1329", outline="#0284C7", width=2)
    draw.text((960, 310), f"CÂU HỎI {q_num}: BẠN VỪA NGHE THẤY TỪ NÀO DƯỚI ĐÂY?", font=fonts["h2"], fill="#F8FAFC", anchor="mm")
    draw.text((960, 355), "Which word did the native speaker just pronounce?", font=fonts["subtitle"], fill="#94A3B8", anchor="mm")
    
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
    bg_a = "#064E3B" if is_a_correct else "#0B1329"
    bd_a = "#10B981" if is_a_correct else "#3B82F6"
    draw.rounded_rectangle([250, 415, 930, 655], radius=18, fill=bg_a, outline=bd_a, width=4 if is_a_correct else 2)
    draw.text((340, 485), "[A]", font=fonts["h2"], fill="#60A5FA", anchor="mm")
    draw.text((590, 505), opt_a[1], font=fonts["huge_letter"], fill="#FFFFFF", anchor="mm")
    draw.text((590, 615), opt_a[2], font=fonts["body"], fill="#94A3B8", anchor="mm")
    if is_a_correct:
        draw.rounded_rectangle([440, 425, 740, 465], radius=8, fill="#047857")
        draw.text((590, 445), "DAP AN CHINH XAC!", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
        
    # Choice B
    is_b_correct = (correct == "B" and state == "answer")
    bg_b = "#064E3B" if is_b_correct else "#0B1329"
    bd_b = "#10B981" if is_b_correct else "#F59E0B"
    draw.rounded_rectangle([990, 415, 1670, 655], radius=18, fill=bg_b, outline=bd_b, width=4 if is_b_correct else 2)
    draw.text((1080, 485), "[B]", font=fonts["h2"], fill="#F59E0B", anchor="mm")
    draw.text((1330, 505), opt_b[1], font=fonts["huge_letter"], fill="#FFFFFF", anchor="mm")
    draw.text((1330, 615), opt_b[2], font=fonts["body"], fill="#94A3B8", anchor="mm")
    if is_b_correct:
        draw.rounded_rectangle([1180, 425, 1480, 465], radius=8, fill="#047857")
        draw.text((1330, 445), "DAP AN CHINH XAC!", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
        
    # Status bar
    if state == "question":
        draw.rounded_rectangle([250, 680, 1670, 740], radius=12, fill="#1E293B", outline="#F59E0B", width=2)
        draw.text((960, 710), "3... 2... 1... HÃY SUY NGHĨ VÀ CHỌN A HOẶC B!", font=fonts["h3"], fill="#FDE047", anchor="mm")
        en_sub = "Listen to the sound and choose: Is it A or B?"
        vi_sub = "Hãy lắng nghe âm thanh và chọn: Đó là phương án A hay B?"
    else:
        draw.rounded_rectangle([250, 680, 1670, 740], radius=12, fill="#047857", outline="#34D399", width=2)
        draw.text((960, 710), f"BINGO! ĐÁP ÁN ĐÚNG LÀ [{correct}]!", font=fonts["h3"], fill="#FFFFFF", anchor="mm")
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
    
    draw.rounded_rectangle([100, 95, 420, 135], radius=10, fill="#047857")
    draw.text((260, 115), "PHẦN 6: TỔNG KẾT", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    
    draw.text((100, 160), "TỔNG KẾT: QUY TẮC VÀNG GHI NHỚ VĨNH VIỄN", font=fonts["title"], fill="#34D399")
    draw.text((100, 205), "Master Rule: Never confuse Vietnamese D and Đ again!", font=fonts["subtitle"], fill="#94A3B8")
    
    # Table Card
    draw_card(draw, [100, 245, 1820, 765], bg="#0F1B36", border="#34D399", border_width=3)
    
    # Row 1: Đ
    draw.rounded_rectangle([140, 275, 1780, 490], radius=16, fill="#0B1329", outline="#3B82F6", width=2)
    draw.text((250, 382), "Đ", font=fonts["huge_letter"], fill="#60A5FA", anchor="mm")
    draw.text((380, 335), "CHỮ Đ (CÓ GẠCH NGANG)", font=fonts["h2"], fill="#F8FAFC", anchor="lm")
    draw.text((380, 400), "-> Phát âm giống chữ 'D' tiếng Anh trong DOOR / DAY (/ɗ/ Alveolar Stop)", font=fonts["body_bold"], fill="#93C5FD", anchor="lm")
    draw.rounded_rectangle([1450, 335, 1740, 430], radius=12, fill="#1D4ED8")
    draw.text((1595, 382), "Đi • Đỏ • Đẹp", font=fonts["h3"], fill="#FFFFFF", anchor="mm")
    
    # Row 2: D
    draw.rounded_rectangle([140, 520, 1780, 735], radius=16, fill="#0B1329", outline="#F59E0B", width=2)
    draw.text((250, 627), "D", font=fonts["huge_letter"], fill="#FBBF24", anchor="mm")
    draw.text((380, 580), "CHỮ D (KHÔNG GẠCH NGANG)", font=fonts["h2"], fill="#F8FAFC", anchor="lm")
    draw.text((380, 645), "-> Phát âm giống chữ 'Z' tiếng Anh trong ZOO / ZERO (/z/ Dental Fricative)", font=fonts["body_bold"], fill="#FDE047", anchor="lm")
    draw.rounded_rectangle([1450, 580, 1740, 675], radius=12, fill="#B45309")
    draw.text((1595, 627), "Da • Dễ • Dưa", font=fonts["h3"], fill="#FFFFFF", anchor="mm")
    
    # Congrats Bar
    draw.rounded_rectangle([100, 785, 1820, 870], radius=16, fill="#064E3B", outline="#10B981", width=2)
    draw.text((960, 827), "CHÚC MỪNG BẠN ĐÃ LÀM CHỦ PHỤ ÂM D VÀ Đ! (CONGRATULATIONS)", font=fonts["h2"], fill="#FFFFFF", anchor="mm")
    
    draw_subtitle_box(draw, fonts, 
                      "Crossbar Đ = English Door. Plain D = English Zoo. Thanks for watching! Tam biet!", 
                      "Chữ Đ có gạch = Door. Chữ D không gạch = Zoo. Cảm ơn các bạn đã theo dõi! Tạm biệt!")
    
    im.save(os.path.join(FRAMES_DIR, "s6_summary.png"))

def generate_all():
    fonts = get_fonts()
    print("Generating v3 frames with 0% tofu boxes, landing page layout, and refined anatomy...")
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
    print("All slides v3 generated successfully!")

if __name__ == "__main__":
    generate_all()
