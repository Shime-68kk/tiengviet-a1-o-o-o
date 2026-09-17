import os
import subprocess
import time
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

BASE_DIR = "/home/quang/video_ai"
AUDIO_DIR = os.path.join(BASE_DIR, "audio_3_chars")
SFX_DIR = os.path.join(BASE_DIR, "audio")
FRAMES_DIR = os.path.join(BASE_DIR, "snaptik_frames")
TEMP_DIR = os.path.join(BASE_DIR, "cartoon_temp")
os.makedirs(TEMP_DIR, exist_ok=True)

FINAL_OUTPUT = os.path.join(BASE_DIR, "video_microlearning_O_Ô_Ơ.mp4")
W, H = 1920, 1080
FPS = 30

FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

def get_fonts():
    return {
        "title": ImageFont.truetype(FONT_BOLD, 36),
        "h2": ImageFont.truetype(FONT_BOLD, 32),
        "h3": ImageFont.truetype(FONT_BOLD, 26),
        "huge_letter": ImageFont.truetype(FONT_BOLD, 140),
        "word_vn": ImageFont.truetype(FONT_BOLD, 48),
        "body": ImageFont.truetype(FONT_REG, 22),
        "body_bold": ImageFont.truetype(FONT_BOLD, 22),
        "badge": ImageFont.truetype(FONT_BOLD, 20),
        "sub_vi": ImageFont.truetype(FONT_BOLD, 26),
        "sub_en": ImageFont.truetype(FONT_REG, 22),
        "speaker": ImageFont.truetype(FONT_BOLD, 22),
        "quiz_opt": ImageFont.truetype(FONT_BOLD, 28)
    }

def get_dur(path):
    res = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path
    ], capture_output=True, text=True)
    return float(res.stdout.strip())

def make_silence(dur, out_wav):
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-t", f"{dur:.3f}", "-c:a", "pcm_s16le", out_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def to_wav(src_path, out_wav):
    cmd = [
        "ffmpeg", "-y", "-i", src_path,
        "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le", out_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def prep_wav(dir_path, name):
    src = os.path.join(dir_path, name)
    dst = os.path.join(TEMP_DIR, name.replace(".mp3", ".wav"))
    to_wav(src, dst)
    return dst

print("1. Preparing audio clips...")
sil_04 = os.path.join(TEMP_DIR, "sil_04.wav")
sil_05 = os.path.join(TEMP_DIR, "sil_05.wav")
sil_15 = os.path.join(TEMP_DIR, "sil_15.wav")
sil_25 = os.path.join(TEMP_DIR, "sil_25.wav")
make_silence(0.4, sil_04)
make_silence(0.5, sil_05)
make_silence(1.5, sil_15)
make_silence(2.5, sil_25)

wav_tick = prep_wav(SFX_DIR, "sfx_tick.mp3")
wav_ding = prep_wav(SFX_DIR, "sfx_ding.mp3")

# Define the cartoon video timeline with character actions
# Each entry: (camera_mode, speaker_name, speaker_color, visual_mode, audio_list, vi_sub, en_sub)
timeline = [
    # --- SCENE 1: Chào hỏi & Giới thiệu 3 bạn (Wide shot hoạt hình vẫy tay) ---
    ("wide", "Bé O", "#EF4444", "intro_o",
     [prep_wav(AUDIO_DIR, "c_o_intro.mp3"), sil_04],
     "Xin chào các bạn! Tớ là Bé O tròn vo như quả trứng gà nè!",
     "Hello friends! I am round O like a chicken egg!"),
     
    ("wide", "Bé Ô", "#10B981", "intro_oe",
     [prep_wav(AUDIO_DIR, "c_oe_intro.mp3"), sil_04],
     "Còn tớ là Bé Ô! Tớ có chiếc mũ chóp nhọn cực xinh trên đầu!",
     "And I am Ô! I have a cute pointy hat on my head!"),
     
    ("wide", "Bé Ơ", "#F59E0B", "intro_ow",
     [prep_wav(AUDIO_DIR, "c_ow_intro.mp3"), sil_04],
     "Hihi, tớ là Bé Ơ đây! Tớ có chiếc râu móc cong cong đáng yêu nè!",
     "Hihi, I am Ơ! I have an adorable curved hook whisker!"),
     
    ("wide", "Bộ Ba O - Ô - Ơ", "#3B82F6", "intro_trio",
     [prep_wav(AUDIO_DIR, "c_trio_intro.mp3"), sil_05],
     "Chúng tớ là bộ ba bạn thân O, Ô, Ơ! Cùng khám phá với chúng tớ nhé!",
     "We are best friends O, Ô, Ơ! Let's explore together!"),
     
    # --- SCENE 2: Gặp gỡ Bé O (Camera zoom vào Bé O đang nhún nhảy) ---
    ("zoom_o", "Bé O", "#EF4444", "learn_o",
     [prep_wav(AUDIO_DIR, "c_o_feature.mp3"), sil_05],
     "Tớ là Bé O! Chữ của tớ có một nét cong tròn. Cùng mở to môi nói O nào: O ... O ... Con bò!",
     "I am O! One smooth round circle. Open lips wide and say O with me: O ... O ... Con bò!"),
     
    # --- SCENE 3: Gặp gỡ Bé Ô (Camera zoom vào Bé Ô với mũ nhọn) ---
    ("zoom_oe", "Bé Ô", "#10B981", "learn_oe",
     [prep_wav(AUDIO_DIR, "c_oe_feature.mp3"), sil_05],
     "Đến lượt tớ, Bé Ô đây! Tớ đội chiếc mũ nón chóp xinh. Chu môi nhô ra trước và nói Ô nhé: Ô ... Ô ... Cô giáo!",
     "My turn, I am Ô! I wear a cute hat. Pucker lips forward and say Ô: Ô ... Ô ... Cô giáo!"),
     
    # --- SCENE 4: Gặp gỡ Bé Ơ (Camera zoom vào Bé Ơ với râu móc) ---
    ("zoom_ow", "Bé Ơ", "#F59E0B", "learn_ow",
     [prep_wav(AUDIO_DIR, "c_ow_feature.mp3"), sil_05],
     "Còn tớ là Bé Ơ! Tớ có chiếc râu móc bên phải. Mỉm cười dẹt môi ngang và nói Ơ nào: Ơ ... Ơ ... Quả bơ!",
     "And I am Ơ! I have a hook on the right. Smile with flat lips and say Ơ: Ơ ... Ơ ... Quả bơ!"),
     
    # --- SCENE 5: Cỗ máy biến hình kỳ diệu (Wide shot hoạt hình 3 bạn) ---
    ("wide", "Bé O", "#EF4444", "magic_o",
     [prep_wav(AUDIO_DIR, "c_magic_o.mp3"), sil_04],
     "Nhìn tớ nè! Tớ tròn xoe không mũ không râu!",
     "Look at me! Plain round O without a hat or hook!"),
     
    ("wide", "Bé Ô", "#10B981", "magic_oe",
     [prep_wav(AUDIO_DIR, "c_magic_oe.mp3"), sil_04],
     "Thêm chiếc mũ nhọn rơi xuống boong một cái là biến thành tớ: Ô!",
     "Add a pointy hat dropping down and it becomes me: Ô!"),
     
    ("wide", "Bé Ơ", "#F59E0B", "magic_ow",
     [prep_wav(AUDIO_DIR, "c_magic_ow.mp3"), sil_05],
     "Thêm chiếc râu móc cong cong là biến thành tớ: Ơ! Thật là kỳ diệu!",
     "Add a curved whisker hook and it becomes me: Ơ! So magical!"),
     
    # --- SCENE 6: Trò chơi nhại lại tương tác (Shadowing Game) ---
    # Round 1: O - Bò
    ("zoom_o", "Bé O", "#EF4444", "game_o_q",
     [prep_wav(AUDIO_DIR, "c_game_o_q.mp3"), sil_04],
     "Các bạn cùng chơi trò nhắc lại nhé! Hãy nói theo tớ nào: BÒ!",
     "Let's play the repeat game! Say after me: BÒ!"),
     
    ("zoom_o", "Lượt Của Bạn", "#EF4444", "game_o_pause",
     [sil_25, wav_ding],
     "[Đến lượt bạn nói: BÒ!] ... Ding!",
     "[Your turn to repeat: BÒ!] ... Ding!"),
     
    ("zoom_o", "Bé O", "#EF4444", "game_o_praise",
     [prep_wav(AUDIO_DIR, "c_game_o_praise.mp3"), sil_05],
     "Hoan hô! Các bạn phát âm từ Bò chuẩn lắm!",
     "Bravo! You pronounced Bò so accurately!"),
     
    # Round 2: Ô - Cô
    ("zoom_oe", "Bé Ô", "#10B981", "game_oe_q",
     [prep_wav(AUDIO_DIR, "c_game_oe_q.mp3"), sil_04],
     "Đến lượt tớ nè! Hãy nói thật to theo tớ: CÔ!",
     "My turn! Say loudly after me: CÔ!"),
     
    ("zoom_oe", "Lượt Của Bạn", "#10B981", "game_oe_pause",
     [sil_25, wav_ding],
     "[Đến lượt bạn nói: CÔ!] ... Ding!",
     "[Your turn to repeat: CÔ!] ... Ding!"),
     
    ("zoom_oe", "Bé Ô", "#10B981", "game_oe_praise",
     [prep_wav(AUDIO_DIR, "c_game_oe_praise.mp3"), sil_05],
     "Tuyệt vời quá! Bé Ô khen bạn nha!",
     "Wonderful! Bé Ô praises you!"),
     
    # Round 3: Ơ - Bơ
    ("zoom_ow", "Bé Ơ", "#F59E0B", "game_ow_q",
     [prep_wav(AUDIO_DIR, "c_game_ow_q.mp3"), sil_04],
     "Còn tớ nữa nè! Hãy nói thật vang theo tớ: BƠ!",
     "And me! Say clearly after me: BƠ!"),
     
    ("zoom_ow", "Lượt Của Bạn", "#F59E0B", "game_ow_pause",
     [sil_25, wav_ding],
     "[Đến lượt bạn nói: BƠ!] ... Ding!",
     "[Your turn to repeat: BƠ!] ... Ding!"),
     
    ("zoom_ow", "Bé Ơ", "#F59E0B", "game_ow_praise",
     [prep_wav(AUDIO_DIR, "c_game_ow_praise.mp3"), sil_05],
     "Xuất sắc! Các bạn nói từ Bơ rất hay!",
     "Excellent! You said Bơ wonderfully!"),
     
    # --- SCENE 7: Đố vui & Lời chào tạm biệt ---
    ("wide", "Bé O", "#EF4444", "quiz_q",
     [prep_wav(AUDIO_DIR, "c_quiz_q.mp3"), sil_04, wav_tick, sil_05, wav_tick, sil_05, wav_tick, sil_05],
     "Đố các bạn nhanh trí nè: Ai trong ba chúng tớ đang ĐỘI CHIẾC MŨ trên đầu?",
     "Quick quiz: Which one of us is wearing a HAT on its head?"),
     
    ("wide", "Bé Ô", "#10B981", "quiz_ans",
     [wav_ding, prep_wav(AUDIO_DIR, "c_quiz_ans.mp3"), sil_05],
     "Hê hê! Chính là tớ, Bé Ô đội chiếc mũ nhọn xinh xắn đây nè!",
     "Hehe! It's me, Bé Ô with the cute pointy hat!"),
     
    ("wide", "Bé Ơ", "#F59E0B", "rhyme_1",
     [prep_wav(AUDIO_DIR, "c_rhyme_1.mp3")],
     "Các bạn luôn nhớ câu thơ dân gian nhé: O tròn như quả trứng gà,",
     "Always remember the folk poem: Plain round is O like a chicken egg,"),
     
    ("wide", "Bé Ô", "#10B981", "rhyme_2",
     [prep_wav(AUDIO_DIR, "c_rhyme_2.mp3")],
     "Ô thì đội mũ,",
     "With a hat is Ô,"),
     
    ("wide", "Bé Ơ", "#F59E0B", "rhyme_3",
     [prep_wav(AUDIO_DIR, "c_rhyme_3.mp3"), sil_04],
     "Ơ thì thêm râu!",
     "With a hook is Ơ!"),
     
    ("wide", "Bộ Ba O - Ô - Ơ", "#EF4444", "goodbye",
     [prep_wav(AUDIO_DIR, "c_goodbye.mp3"), sil_15],
     "Chúc các bạn học tiếng Việt thật vui và tự tin! Tạm biệt các bạn nha!",
     "Have fun learning Vietnamese with confidence! Goodbye friends!")
]

# Step 2: Build Master Audio
print("2. Concatenating audio segments...")
all_wavs = []
segment_info = []

for cam_mode, spk_name, spk_col, vis_mode, wav_list, vi_sub, en_sub in timeline:
    dur = sum(get_dur(w) for w in wav_list)
    frames_count = max(1, int(round(dur * FPS)))
    segment_info.append({
        "cam_mode": cam_mode,
        "speaker": spk_name,
        "color": spk_col,
        "vis_mode": vis_mode,
        "frames": frames_count,
        "dur": dur,
        "vi": vi_sub,
        "en": en_sub
    })
    all_wavs.extend(wav_list)

master_voice_list = os.path.join(TEMP_DIR, "voice_list.txt")
with open(master_voice_list, "w") as f:
    for w in all_wavs:
        f.write(f"file '{w}'\n")

voice_raw_wav = os.path.join(TEMP_DIR, "cartoon_voice_raw.wav")
cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", master_voice_list, "-c:a", "pcm_s16le", voice_raw_wav]
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

voice_dur = get_dur(voice_raw_wav)
print(f"Total Speech Duration: {voice_dur:.2f}s")

# Mix with cheerful marimba BGM (volume=0.12)
print("3. Mixing cheerful marimba BGM under speech...")
bgm_wav = os.path.join(BASE_DIR, "audio", "bgm_cheerful.wav")
master_audio_wav = os.path.join(TEMP_DIR, "cartoon_master_audio.wav")

cmd = [
    "ffmpeg", "-y",
    "-i", voice_raw_wav,
    "-stream_loop", "-1", "-i", bgm_wav,
    "-filter_complex",
    "[1:a]volume=0.12[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[outa]",
    "-map", "[outa]",
    "-c:a", "pcm_s16le",
    "-ar", "44100",
    master_audio_wav
]
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

# Step 4: Load 3D Animation Frames
print("4. Pre-loading 241 3D animation frames...")
anim_frames = []
for i in range(1, 242):
    p = os.path.join(FRAMES_DIR, f"frame_{i:04d}.png")
    im = Image.open(p).convert("RGBA")
    anim_frames.append(im)
print(f"Loaded {len(anim_frames)} frames!")

fonts = get_fonts()

# Helper overlay drawing
def draw_lip_diagram(draw, fonts, cx, cy, lip_type="o"):
    draw.rounded_rectangle([cx - 150, cy - 75, cx + 150, cy + 75], radius=16, fill="#FFFFFF", outline="#CBD5E1", width=2)
    draw.text((cx, cy - 50), "KHẨU HÌNH", font=fonts["badge"], fill="#64748B", anchor="mm")
    if lip_type == "o":
        draw.ellipse([cx - 45, cy - 25, cx + 45, cy + 25], fill="#EF4444", outline="#FCA5A5", width=3)
        draw.ellipse([cx - 24, cy - 13, cx + 24, cy + 13], fill="#FFFFFF")
        draw.text((cx, cy + 50), "Môi mở tròn to (/ɔ/)", font=fonts["body_bold"], fill="#DC2626", anchor="mm")
    elif lip_type == "oe":
        draw.ellipse([cx - 35, cy - 22, cx + 35, cy + 22], fill="#10B981", outline="#6EE7B7", width=3)
        draw.ellipse([cx - 16, cy - 10, cx + 16, cy + 10], fill="#FFFFFF")
        draw.line([cx - 48, cy, cx - 38, cy], fill="#10B981", width=2)
        draw.line([cx + 38, cy, cx + 48, cy], fill="#10B981", width=2)
        draw.text((cx, cy + 50), "Môi chúm nhô trước (/o/)", font=fonts["body_bold"], fill="#059669", anchor="mm")
    else:
        draw.ellipse([cx - 55, cy - 15, cx + 55, cy + 15], fill="#F59E0B", outline="#FCD34D", width=3)
        draw.ellipse([cx - 30, cy - 6, cx + 30, cy + 6], fill="#FFFFFF")
        draw.text((cx, cy + 50), "Môi dẹt ngang (/ɤ/)", font=fonts["body_bold"], fill="#D97706", anchor="mm")

def compose_frame(anim_im, seg, seg_frame_idx, total_seg_f):
    cam = seg["cam_mode"]
    
    # 1. Camera Crop
    if cam == "wide":
        frame = anim_im.copy()
    elif cam == "zoom_o":
        # 16:9 crop on Bé O (left)
        crop = anim_im.crop((40, 140, 40 + 1422, 140 + 800))
        frame = crop.resize((W, H), Image.Resampling.BILINEAR)
    elif cam == "zoom_oe":
        # 16:9 crop on Bé Ô (center)
        crop = anim_im.crop((249, 140, 249 + 1422, 140 + 800))
        frame = crop.resize((W, H), Image.Resampling.BILINEAR)
    elif cam == "zoom_ow":
        # 16:9 crop on Bé Ơ (right)
        crop = anim_im.crop((458, 140, 458 + 1422, 140 + 800))
        frame = crop.resize((W, H), Image.Resampling.BILINEAR)
        
    draw = ImageDraw.Draw(frame)
    vis = seg["vis_mode"]
    spk_col = seg["color"]
    
    # 2. Specific Cartoon Visual Overlays
    if vis == "learn_o":
        # Right floating learning card
        draw.rounded_rectangle([1180, 140, 1850, 860], radius=24, fill=(255, 255, 255, 240), outline="#EF4444", width=3)
        draw.text((1515, 200), "CHỮ GỐC: O", font=fonts["title"], fill="#DC2626", anchor="mm")
        draw.text((1515, 330), "O", font=fonts["huge_letter"], fill="#EF4444", anchor="mm")
        draw.text((1515, 430), "Một nét cong tròn khép kín", font=fonts["body_bold"], fill="#334155", anchor="mm")
        draw_lip_diagram(draw, fonts, 1515, 560, "o")
        draw.rounded_rectangle([1230, 680, 1800, 810], radius=16, fill="#FEF2F2", outline="#EF4444", width=2)
        draw.text((1515, 725), "TỪ VỰNG A1: BÒ", font=fonts["badge"], fill="#DC2626", anchor="mm")
        draw.text((1515, 770), "Con bò (Cow)", font=fonts["h3"], fill="#1E293B", anchor="mm")
        
    elif vis == "learn_oe":
        # Right floating learning card
        draw.rounded_rectangle([1180, 140, 1850, 860], radius=24, fill=(255, 255, 255, 240), outline="#10B981", width=3)
        draw.text((1515, 200), "THÊM MŨ (^): Ô", font=fonts["title"], fill="#059669", anchor="mm")
        draw.text((1515, 330), "Ô", font=fonts["huge_letter"], fill="#10B981", anchor="mm")
        draw.text((1515, 430), "O + Mũ chóp nhọn = Ô", font=fonts["body_bold"], fill="#334155", anchor="mm")
        draw_lip_diagram(draw, fonts, 1515, 560, "oe")
        draw.rounded_rectangle([1230, 680, 1800, 810], radius=16, fill="#ECFDF5", outline="#10B981", width=2)
        draw.text((1515, 725), "TỪ VỰNG A1: CÔ", font=fonts["badge"], fill="#059669", anchor="mm")
        draw.text((1515, 770), "Cô giáo (Teacher)", font=fonts["h3"], fill="#1E293B", anchor="mm")
        
    elif vis == "learn_ow":
        # Left floating learning card
        draw.rounded_rectangle([70, 140, 740, 860], radius=24, fill=(255, 255, 255, 240), outline="#F59E0B", width=3)
        draw.text((405, 200), "THÊM RÂU ( ' ): Ơ", font=fonts["title"], fill="#D97706", anchor="mm")
        draw.text((405, 330), "Ơ", font=fonts["huge_letter"], fill="#F59E0B", anchor="mm")
        draw.text((405, 430), "O + Râu móc cong = Ơ", font=fonts["body_bold"], fill="#334155", anchor="mm")
        draw_lip_diagram(draw, fonts, 405, 560, "ow")
        draw.rounded_rectangle([120, 680, 690, 810], radius=16, fill="#FFFBEB", outline="#F59E0B", width=2)
        draw.text((405, 725), "TỪ VỰNG A1: BƠ", font=fonts["badge"], fill="#D97706", anchor="mm")
        draw.text((405, 770), "Quả bơ (Avocado)", font=fonts["h3"], fill="#1E293B", anchor="mm")
        
    elif vis in ("game_o_q", "game_o_pause", "game_o_praise"):
        # Game Card for O
        draw.rounded_rectangle([1180, 160, 1850, 840], radius=24, fill=(255, 255, 255, 245), outline="#EF4444", width=3)
        draw.text((1515, 220), "THỬ THÁCH NHẮC LẠI", font=fonts["badge"], fill="#DC2626", anchor="mm")
        draw.text((1515, 370), "BÒ", font=fonts["huge_letter"], fill="#EF4444", anchor="mm")
        draw.text((1515, 490), "Con bò • The cow", font=fonts["h3"], fill="#334155", anchor="mm")
        if vis == "game_o_pause":
            # Pulsing speak prompt
            draw.ellipse([1435, 560, 1595, 720], fill="#FEE2E2", outline="#EF4444", width=4)
            draw.text((1515, 640), "NÓI TO!", font=fonts["h2"], fill="#DC2626", anchor="mm")
            draw.text((1515, 770), "[Hãy phát âm từ BÒ nào!]", font=fonts["body_bold"], fill="#991B1B", anchor="mm")
        elif vis == "game_o_praise":
            draw.rounded_rectangle([1250, 580, 1780, 750], radius=16, fill="#ECFDF5", outline="#10B981", width=2)
            draw.text((1515, 640), "HOAN HÔ!", font=fonts["h2"], fill="#059669", anchor="mm")
            draw.text((1515, 700), "Phát âm rất chuẩn!", font=fonts["body_bold"], fill="#047857", anchor="mm")
            
    elif vis in ("game_oe_q", "game_oe_pause", "game_oe_praise"):
        # Game Card for Ô
        draw.rounded_rectangle([1180, 160, 1850, 840], radius=24, fill=(255, 255, 255, 245), outline="#10B981", width=3)
        draw.text((1515, 220), "THỬ THÁCH NHẮC LẠI", font=fonts["badge"], fill="#059669", anchor="mm")
        draw.text((1515, 370), "CÔ", font=fonts["huge_letter"], fill="#10B981", anchor="mm")
        draw.text((1515, 490), "Cô giáo • The teacher", font=fonts["h3"], fill="#334155", anchor="mm")
        if vis == "game_oe_pause":
            draw.ellipse([1435, 560, 1595, 720], fill="#D1FAE5", outline="#10B981", width=4)
            draw.text((1515, 640), "NÓI TO!", font=fonts["h2"], fill="#059669", anchor="mm")
            draw.text((1515, 770), "[Hãy phát âm từ CÔ nào!]", font=fonts["body_bold"], fill="#065F46", anchor="mm")
        elif vis == "game_oe_praise":
            draw.rounded_rectangle([1250, 580, 1780, 750], radius=16, fill="#ECFDF5", outline="#10B981", width=2)
            draw.text((1515, 640), "TUYỆT VỜI!", font=fonts["h2"], fill="#059669", anchor="mm")
            draw.text((1515, 700), "Bé Ô khen bạn nha!", font=fonts["body_bold"], fill="#047857", anchor="mm")
            
    elif vis in ("game_ow_q", "game_ow_pause", "game_ow_praise"):
        # Game Card for Ơ
        draw.rounded_rectangle([70, 160, 740, 840], radius=24, fill=(255, 255, 255, 245), outline="#F59E0B", width=3)
        draw.text((405, 220), "THỬ THÁCH NHẮC LẠI", font=fonts["badge"], fill="#D97706", anchor="mm")
        draw.text((405, 370), "BƠ", font=fonts["huge_letter"], fill="#F59E0B", anchor="mm")
        draw.text((405, 490), "Quả bơ • The avocado", font=fonts["h3"], fill="#334155", anchor="mm")
        if vis == "game_ow_pause":
            draw.ellipse([325, 560, 485, 720], fill="#FEF3C7", outline="#F59E0B", width=4)
            draw.text((405, 640), "NÓI TO!", font=fonts["h2"], fill="#D97706", anchor="mm")
            draw.text((405, 770), "[Hãy phát âm từ BƠ nào!]", font=fonts["body_bold"], fill="#92400E", anchor="mm")
        elif vis == "game_ow_praise":
            draw.rounded_rectangle([140, 580, 670, 750], radius=16, fill="#ECFDF5", outline="#10B981", width=2)
            draw.text((405, 640), "XUẤT SẮC!", font=fonts["h2"], fill="#059669", anchor="mm")
            draw.text((405, 700), "Các bạn phát âm rất hay!", font=fonts["body_bold"], fill="#047857", anchor="mm")
            
    elif vis in ("quiz_q", "quiz_ans"):
        # Question banner
        draw.rounded_rectangle([200, 50, 1720, 140], radius=16, fill=(255, 255, 255, 240), outline="#EF4444", width=2)
        draw.text((960, 95), "CÂU HỎI: BẠN NÀO ĐANG ĐỘI MŨ TRÊN ĐẦU?", font=fonts["title"], fill="#DC2626", anchor="mm")
        
        # 3 Options
        opts = [
            ("A. Bé O", 480, False),
            ("B. Bé Ô", 960, True),
            ("C. Bé Ơ", 1440, False)
        ]
        for opt_text, ox, is_corr in opts:
            is_hl = (vis == "quiz_ans" and is_corr)
            bg = "#ECFDF5" if is_hl else ((255, 255, 255, 240) if vis == "quiz_q" else "#F1F5F9")
            border = "#10B981" if is_hl else "#CBD5E1"
            txt_col = "#059669" if is_hl else "#1E293B"
            label = opt_text + ("  [ĐÚNG!]" if is_hl else "")
            draw.rounded_rectangle([ox - 180, 160, ox + 180, 230], radius=14, fill=bg, outline=border, width=3 if is_hl else 2)
            draw.text((ox, 195), label, font=fonts["quiz_opt"], fill=txt_col, anchor="mm")
            
    elif vis in ("rhyme_1", "rhyme_2", "rhyme_3", "goodbye"):
        # Folk rhyme celebration card
        draw.rounded_rectangle([300, 50, 1620, 190], radius=20, fill=(255, 255, 255, 245), outline="#F59E0B", width=3)
        draw.text((960, 90), "BÍ KÍP GHI NHỚ SUỐT ĐỜI", font=fonts["badge"], fill="#D97706", anchor="mm")
        draw.text((960, 140), "“O tròn như quả trứng gà • Ô thì đội mũ • Ơ thì thêm râu”", font=fonts["h2"], fill="#DC2626", anchor="mm")
    
    # 3. Top-Left Speaker Badge (identifies who is speaking!)
    spk = seg["speaker"]
    draw.rounded_rectangle([80, 50, 360, 105], radius=14, fill=spk_col)
    draw.text((220, 77), spk, font=fonts["speaker"], fill="#FFFFFF", anchor="mm")
    
    # 4. Floating Subtitle Card at Bottom (clean & zero overflow)
    draw.rounded_rectangle([80, 890, 1840, 1030], radius=18, fill=(255, 255, 255, 245), outline="#CBD5E1", width=2)
    draw.rounded_rectangle([110, 910, 240, 950], radius=10, fill=spk_col)
    draw.text((175, 930), "LỜI THOẠI", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    draw.text((265, 930), seg["vi"], font=fonts["sub_vi"], fill="#0F172A", anchor="lm")
    draw.text((265, 985), f"[EN] {seg['en']}", font=fonts["sub_en"], fill="#0284C7", anchor="lm")
    
    return frame

# Step 5: Render Video Pipe
print("5. Rendering animated cartoon video through ffmpeg pipe...")
t0 = time.time()
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo", "-pix_fmt", "rgb24",
    "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
    "-i", master_audio_wav,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "19",
    "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
    "-shortest",
    FINAL_OUTPUT
]

proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

global_frame_idx = 0
num_anim = len(anim_frames) # 241
loop_len = (num_anim - 1) * 2 # 480 (ping-pong)

for seg_idx, seg in enumerate(segment_info):
    seg_f = seg["frames"]
    for f in range(seg_f):
        # Ping-pong animation frame index
        sub_idx = global_frame_idx % loop_len
        if sub_idx >= num_anim:
            sub_idx = loop_len - sub_idx
        anim_im = anim_frames[sub_idx]
        
        composed = compose_frame(anim_im, seg, f, seg_f)
        rgb_data = composed.convert("RGB").tobytes()
        proc.stdin.write(rgb_data)
        global_frame_idx += 1

proc.stdin.close()
proc.wait()

render_time = time.time() - t0
final_dur = get_dur(FINAL_OUTPUT)
print(f"=== Video Render Completed in {render_time:.2f}s! ===")
print(f"Final Path: {FINAL_OUTPUT}")
print(f"Total Duration: {final_dur:.2f}s ({global_frame_idx} frames @ 30fps)")

# Link / copy to video_o_o_o.mp4 and assets/hero.mp4
for dest in ["video_o_o_o.mp4", os.path.join("assets", "hero.mp4")]:
    p = os.path.join(BASE_DIR, dest)
    if os.path.exists(p) or os.path.islink(p):
        if os.path.realpath(p) != os.path.realpath(FINAL_OUTPUT):
            os.remove(p)
            os.symlink(FINAL_OUTPUT, p)
    else:
        os.symlink(FINAL_OUTPUT, p)
print("Successfully symlinked output files!")
