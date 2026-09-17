import os
import sys
import subprocess
import math
import glob
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = "/home/quang/video_ai"
AUDIO_DIR = os.path.join(BASE_DIR, "audio_3_chars")
SFX_DIR = os.path.join(BASE_DIR, "audio")
ASSETS_DIR = os.path.join(BASE_DIR, "cartoon_assets")
TEMP_DIR = os.path.join(BASE_DIR, "cartoon_temp_v2")
os.makedirs(TEMP_DIR, exist_ok=True)

FINAL_OUTPUT = os.path.join(BASE_DIR, "video_microlearning_O_Ô_Ơ.mp4")
W, H = 1920, 1080
FPS = 30

FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

def get_fonts():
    return {
        "title": ImageFont.truetype(FONT_BOLD, 36),
        "h2": ImageFont.truetype(FONT_BOLD, 30),
        "h3": ImageFont.truetype(FONT_BOLD, 24),
        "huge_letter": ImageFont.truetype(FONT_BOLD, 120),
        "badge": ImageFont.truetype(FONT_BOLD, 22),
        "sub_vi": ImageFont.truetype(FONT_BOLD, 28),
        "sub_en": ImageFont.truetype(FONT_REG, 22),
        "quiz_opt": ImageFont.truetype(FONT_BOLD, 26),
        "timer": ImageFont.truetype(FONT_BOLD, 72)
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
sil_03 = os.path.join(TEMP_DIR, "sil_03.wav")
sil_04 = os.path.join(TEMP_DIR, "sil_04.wav")
sil_05 = os.path.join(TEMP_DIR, "sil_05.wav")
sil_10 = os.path.join(TEMP_DIR, "sil_10.wav")
sil_15 = os.path.join(TEMP_DIR, "sil_15.wav")
make_silence(1.5, sil_15)
sil_25 = os.path.join(TEMP_DIR, "sil_25.wav")
make_silence(0.3, sil_03)
make_silence(0.4, sil_04)
make_silence(0.5, sil_05)
make_silence(1.0, sil_10)
make_silence(2.5, sil_25)

wav_tick = prep_wav(SFX_DIR, "sfx_tick.mp3")
wav_ding = prep_wav(SFX_DIR, "sfx_ding.mp3")

# Load Cartoon Asset Images
ASSETS = {
    "egg": Image.open(os.path.join(ASSETS_DIR, "item_egg.png")).convert("RGBA"),
    "cow": Image.open(os.path.join(ASSETS_DIR, "item_cow.png")).convert("RGBA"),
    "hat": Image.open(os.path.join(ASSETS_DIR, "item_hat.png")).convert("RGBA"),
    "teacher": Image.open(os.path.join(ASSETS_DIR, "item_teacher.png")).convert("RGBA"),
    "hook": Image.open(os.path.join(ASSETS_DIR, "item_hook.png")).convert("RGBA"),
    "avocado": Image.open(os.path.join(ASSETS_DIR, "item_avocado.png")).convert("RGBA"),
    "trophy": Image.open(os.path.join(ASSETS_DIR, "item_trophy.png")).convert("RGBA"),
    "confetti": Image.open(os.path.join(ASSETS_DIR, "item_confetti.png")).convert("RGBA")
}

# Define Timeline Segments
# (scene_type, speaker_name, speaker_color, visual_mode, audio_list, vi_sub, en_sub)
# scene_types: "title", "solo_o", "solo_oe", "solo_ow", "trio_meadow", "trio_room"
timeline = [
    # --- SCENE 1: Mở Màn Cổng Chào Cầu Vồng (Title Intro) ---
    ("title", "Bộ Ba O - Ô - Ơ", "#3B82F6", "title_intro",
     [sil_05, prep_wav(AUDIO_DIR, "c_trio_intro.mp3"), sil_04],
     "Chào mừng các bạn nhỏ! Chúng tớ là bộ ba bạn thân O, Ô, Ơ!",
     "Welcome friends! We are best friends O, Ô, Ơ!"),

    # --- SCENE 2: Làm Quen Riêng Từng Bạn (Solo Introductions) ---
    ("solo_o", "Bé O", "#EF4444", "intro_o",
     [prep_wav(AUDIO_DIR, "c_o_intro.mp3"), sil_04],
     "Xin chào các bạn! Tớ là Bé O tròn vo như quả trứng gà nè!",
     "Hello friends! I am round O like a chicken egg!"),

    ("solo_oe", "Bé Ô", "#10B981", "intro_oe",
     [prep_wav(AUDIO_DIR, "c_oe_intro.mp3"), sil_04],
     "Còn tớ là Bé Ô! Tớ có chiếc mũ chóp nhọn cực xinh trên đầu!",
     "And I am Ô! I have a cute pointy hat on my head!"),

    ("solo_ow", "Bé Ơ", "#F59E0B", "intro_ow",
     [prep_wav(AUDIO_DIR, "c_ow_intro.mp3"), sil_05],
     "Hihi, tớ là Bé Ơ đây! Tớ có chiếc râu móc cong cong đáng yêu nè!",
     "Hihi, I am Ơ! I have an adorable curved hook whisker!"),

    # --- SCENE 3: Khám Phá Sâu Từng Bạn (Solo Deep Dive + Pronunciation + Vocabulary) ---
    # Bé O
    ("solo_o", "Bé O", "#EF4444", "feature_o",
     [prep_wav(AUDIO_DIR, "c_o_feature.mp3"), sil_05],
     "Tớ là Bé O! Chữ chỉ có một nét cong tròn khép kín. Mở to môi nói O: O ... O ... Con bò!",
     "I am Bé O! One smooth round circle. Open lips wide and say O: O ... O ... Con bò!"),

    # Bé Ô
    ("solo_oe", "Bé Ô", "#10B981", "feature_oe",
     [prep_wav(AUDIO_DIR, "c_oe_feature.mp3"), sil_05],
     "Đến lượt tớ, Bé Ô đây! Tớ đội chiếc mũ nón chóp. Chu môi nhô ra trước và nói Ô: Ô ... Ô ... Cô giáo!",
     "My turn, Bé Ô! I wear a cute hat. Pucker lips forward and say Ô: Ô ... Ô ... Cô giáo!"),

    # Bé Ơ
    ("solo_ow", "Bé Ơ", "#F59E0B", "feature_ow",
     [prep_wav(AUDIO_DIR, "c_ow_feature.mp3"), sil_05],
     "Còn tớ là Bé Ơ! Tớ có chiếc râu móc bên phải. Mỉm cười dẹt môi ngang và nói Ơ: Ơ ... Ơ ... Quả bơ!",
     "And I am Bé Ơ! I have a hook on the right. Smile with flat lips and say Ơ: Ơ ... Ơ ... Quả bơ!"),

    # --- SCENE 4: Cỗ Máy Biến Hình Kỳ Diệu Tại Lớp Học 3D (Magic Transformation) ---
    ("trio_room", "Bé O", "#EF4444", "magic_o",
     [prep_wav(AUDIO_DIR, "c_magic_o.mp3"), sil_04],
     "Nhìn tớ nè! Tớ tròn xoe không mũ không râu!",
     "Look at me! Plain round O without a hat or hook!"),

    ("trio_room", "Bé Ô", "#10B981", "magic_oe",
     [prep_wav(AUDIO_DIR, "c_magic_oe.mp3"), sil_04],
     "Thêm chiếc mũ nhọn rơi xuống boong một cái là biến thành tớ: Ô!",
     "Add a pointy hat dropping down and it becomes me: Ô!"),

    ("trio_room", "Bé Ơ", "#F59E0B", "magic_ow",
     [prep_wav(AUDIO_DIR, "c_magic_ow.mp3"), sil_05],
     "Thêm chiếc râu móc cong cong là biến thành tớ: Ơ! Thật là kỳ diệu!",
     "Add a curved whisker hook and it becomes me: Ơ! So magical!"),

    # --- SCENE 5: Trò Chơi Nhắc Lại Tương Tác (Interactive Shadowing Game) ---
    # Round 1: BÒ (Bé O)
    ("solo_o", "Bé O", "#EF4444", "game_o_q",
     [prep_wav(AUDIO_DIR, "c_game_o_q.mp3"), sil_04],
     "Các bạn cùng chơi trò nhắc lại nhé! Hãy nói theo tớ nào: BÒ!",
     "Let's play the repeat game! Say after me: BÒ!"),

    ("solo_o", "Lượt Của Bạn", "#EF4444", "game_o_repeat",
     [sil_25, wav_ding],
     "[Đến lượt bạn nói to: BÒ!] ... Ding!",
     "[Your turn to repeat loudly: BÒ!] ... Ding!"),

    ("solo_o", "Bé O", "#EF4444", "game_o_praise",
     [prep_wav(AUDIO_DIR, "c_game_o_praise.mp3"), sil_05],
     "Hoan hô! Các bạn phát âm từ Bò chuẩn lắm!",
     "Bravo! You pronounced Bò so accurately!"),

    # Round 2: CÔ (Bé Ô)
    ("solo_oe", "Bé Ô", "#10B981", "game_oe_q",
     [prep_wav(AUDIO_DIR, "c_game_oe_q.mp3"), sil_04],
     "Đến lượt tớ nè! Hãy nói thật to theo tớ: CÔ!",
     "My turn! Say loudly after me: CÔ!"),

    ("solo_oe", "Lượt Của Bạn", "#10B981", "game_oe_repeat",
     [sil_25, wav_ding],
     "[Đến lượt bạn nói to: CÔ!] ... Ding!",
     "[Your turn to repeat loudly: CÔ!] ... Ding!"),

    ("solo_oe", "Bé Ô", "#10B981", "game_oe_praise",
     [prep_wav(AUDIO_DIR, "c_game_oe_praise.mp3"), sil_05],
     "Tuyệt vời quá! Bé Ô khen bạn nha!",
     "Wonderful! Bé Ô praises you!"),

    # Round 3: BƠ (Bé Ơ)
    ("solo_ow", "Bé Ơ", "#F59E0B", "game_ow_q",
     [prep_wav(AUDIO_DIR, "c_game_ow_q.mp3"), sil_04],
     "Còn tớ nữa nè! Hãy nói thật vang theo tớ: BƠ!",
     "And me! Say clearly after me: BƠ!"),

    ("solo_ow", "Lượt Của Bạn", "#F59E0B", "game_ow_repeat",
     [sil_25, wav_ding],
     "[Đến lượt bạn nói to: BƠ!] ... Ding!",
     "[Your turn to repeat loudly: BƠ!] ... Ding!"),

    ("solo_ow", "Bé Ơ", "#F59E0B", "game_ow_praise",
     [prep_wav(AUDIO_DIR, "c_game_ow_praise.mp3"), sil_05],
     "Xuất sắc! Các bạn nói từ Bơ rất hay!",
     "Excellent! You said Bơ wonderfully!"),

    # --- SCENE 6: Gameshow Đố Vui Trắc Nghiệm (Quiz Show) ---
    ("solo_oe", "Bé O", "#EF4444", "quiz_q",
     [prep_wav(AUDIO_DIR, "c_quiz_q.mp3"), sil_04, wav_tick, sil_05, wav_tick, sil_05, wav_tick, sil_05],
     "Đố các bạn nhanh trí nè: Ai trong ba chúng tớ đang ĐỘI CHIẾC MŨ trên đầu?",
     "Quick quiz: Which one of us is wearing a HAT on its head?"),

    ("solo_oe", "Bé Ô", "#10B981", "quiz_ans",
     [wav_ding, prep_wav(AUDIO_DIR, "c_quiz_ans.mp3"), sil_05],
     "Hê hê! Chính là tớ, Bé Ô đội chiếc mũ nhọn xinh xắn đây nè!",
     "Hehe! It's me, Bé Ô with the cute pointy hat!"),

    # --- SCENE 7: Lễ Hội Đồng Dao & Điệu Nhảy Tạm Biệt (Grand Finale) ---
    ("trio_meadow", "Bé Ơ", "#F59E0B", "rhyme_1",
     [prep_wav(AUDIO_DIR, "c_rhyme_1.mp3")],
     "Các bạn luôn nhớ câu thơ dân gian nhé: O tròn như quả trứng gà,",
     "Always remember the folk rhyme: Plain round is O like a chicken egg,"),

    ("trio_meadow", "Bé Ô", "#10B981", "rhyme_2",
     [prep_wav(AUDIO_DIR, "c_rhyme_2.mp3")],
     "Ô thì đội mũ,",
     "With a hat is Ô,"),

    ("trio_meadow", "Bé Ơ", "#F59E0B", "rhyme_3",
     [prep_wav(AUDIO_DIR, "c_rhyme_3.mp3"), sil_04],
     "Ơ thì thêm râu!",
     "With a hook is Ơ!"),

    ("trio_meadow", "Bộ Ba O - Ô - Ơ", "#EF4444", "goodbye",
     [prep_wav(AUDIO_DIR, "c_goodbye.mp3"), sil_15],
     "Chúc các bạn học tiếng Việt thật vui và tự tin! Tạm biệt các bạn nha!",
     "Have fun learning Vietnamese with confidence! Goodbye friends!")
]

# Step 2: Concatenate Audio
print("2. Concatenating audio segments...")
all_wavs = []
segment_info = []

for sc_type, spk_name, spk_col, vis_mode, wav_list, vi_sub, en_sub in timeline:
    dur = sum(get_dur(w) for w in wav_list)
    frames_count = max(1, int(round(dur * FPS)))
    segment_info.append({
        "scene_type": sc_type,
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

# Step 3: Mix Cheerful Marimba BGM
print("3. Mixing cheerful marimba BGM under speech (volume=0.12)...")
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

# Step 4: Index and Prepare Video Frame Sequences
print("4. Indexing video frame sequences...")
def get_frame_paths(pattern, start_idx, end_idx):
    paths = []
    for i in range(start_idx, end_idx + 1):
        p = pattern.format(i)
        if os.path.exists(p):
            paths.append(p)
    return paths

SEQ_MAP = {
    "title": get_frame_paths("frames_1w/f_{:04d}.png", 20, 135),
    "solo_o": get_frame_paths("frames_1w/f_{:04d}.png", 136, 330),
    "solo_oe": get_frame_paths("frames_1w/f_{:04d}.png", 340, 525),
    "solo_ow": get_frame_paths("frames_1w/f_{:04d}.png", 535, 655),
    "trio_meadow": get_frame_paths("frames_1w/f_{:04d}.png", 660, 820),
    "trio_room": get_frame_paths("snaptik_frames/frame_{:04d}.png", 1, 241),
}

for k, v in SEQ_MAP.items():
    print(f"  - {k:12s}: {len(v)} frames indexed")

fonts = get_fonts()

# Helper Draw Functions
def draw_lip_diagram(draw, fonts, cx, cy, lip_type="o", scale=1.0):
    w_box, h_box = 180, 90
    draw.rounded_rectangle([cx - w_box, cy - h_box, cx + w_box, cy + h_box], radius=18, fill="#FFFFFF", outline="#CBD5E1", width=3)
    draw.text((cx, cy - 60), "KHẨU HÌNH", font=fonts["badge"], fill="#64748B", anchor="mm")
    
    rx = int(45 * scale)
    ry = int(25 * scale)
    if lip_type == "o":
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill="#EF4444", outline="#FCA5A5", width=4)
        draw.ellipse([cx - int(rx*0.55), cy - int(ry*0.55), cx + int(rx*0.55), cy + int(ry*0.55)], fill="#FFFFFF")
        draw.text((cx, cy + 60), "Môi mở tròn to (/ɔ/)", font=fonts["h3"], fill="#DC2626", anchor="mm")
    elif lip_type == "oe":
        rx = int(36 * scale)
        ry = int(22 * scale)
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill="#10B981", outline="#6EE7B7", width=4)
        draw.ellipse([cx - int(rx*0.45), cy - int(ry*0.45), cx + int(rx*0.45), cy + int(ry*0.45)], fill="#FFFFFF")
        draw.line([cx - rx - 15, cy, cx - rx, cy], fill="#10B981", width=3)
        draw.line([cx + rx, cy, cx + rx + 15, cy], fill="#10B981", width=3)
        draw.text((cx, cy + 60), "Môi chúm nhô trước (/o/)", font=fonts["h3"], fill="#059669", anchor="mm")
    else:
        rx = int(55 * scale)
        ry = int(16 * scale)
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill="#F59E0B", outline="#FCD34D", width=4)
        draw.ellipse([cx - int(rx*0.55), cy - int(ry*0.5), cx + int(rx*0.55), cy + int(ry*0.5)], fill="#FFFFFF")
        draw.text((cx, cy + 60), "Mép dẹt ngang (/ɤ/)", font=fonts["h3"], fill="#D97706", anchor="mm")

def draw_subtitle_bar(draw, vi_text, en_text, speaker_name, speaker_color):
    draw.rounded_rectangle([180, 910, 1740, 1040], radius=24, fill=(15, 23, 42, 230), outline="#475569", width=2)
    draw.rounded_rectangle([210, 930, 400, 975], radius=12, fill=speaker_color)
    draw.text((305, 952), speaker_name, font=fonts["badge"], fill="#FFFFFF", anchor="mm")
    draw.text((430, 952), vi_text, font=fonts["sub_vi"], fill="#F8FAFC", anchor="lm")
    draw.text((430, 1005), en_text, font=fonts["sub_en"], fill="#94A3B8", anchor="lm")

def compose_cartoon_frame(base_img, seg, frame_i, total_f):
    im = base_img.copy()
    draw = ImageDraw.Draw(im)
    vis = seg["vis_mode"]
    spk_col = seg["color"]
    t_ratio = frame_i / max(1, total_f)
    pulse = 1.0 + 0.08 * math.sin(frame_i * 0.4)

    # 1. Title Intro Scene
    if vis == "title_intro":
        draw.rounded_rectangle([360, 60, 1560, 160], radius=25, fill=(255, 255, 255, 240), outline="#3B82F6", width=4)
        draw.text((960, 110), "BỘ BA BẠN THÂN: O — Ô — Ơ", font=fonts["title"], fill="#1E40AF", anchor="mm")

    # 2. Solo Introductions
    elif vis == "intro_o":
        # Right Card for O
        draw.rounded_rectangle([1220, 120, 1860, 860], radius=28, fill=(255, 255, 255, 245), outline="#EF4444", width=4)
        draw.text((1540, 180), "BÉ O TRÒN XOE", font=fonts["title"], fill="#DC2626", anchor="mm")
        draw.text((1540, 230), "Nguyên âm đơn /ɔ/", font=fonts["h3"], fill="#64748B", anchor="mm")
        # Bouncing egg
        bounce_y = int(270 + 12 * math.sin(frame_i * 0.3))
        egg_sz = (200, 200)
        egg_im = ASSETS["egg"].resize(egg_sz)
        im.paste(egg_im, (1440, bounce_y), egg_im)
        draw.text((1540, 520), "Tròn vo như quả trứng gà!", font=fonts["h2"], fill="#D97706", anchor="mm")
        # Sub card
        draw.rounded_rectangle([1260, 580, 1820, 810], radius=20, fill="#FEF2F2", outline="#EF4444", width=3)
        draw.text((1540, 640), "ĐẶC ĐIỂM", font=fonts["badge"], fill="#EF4444", anchor="mm")
        draw.text((1540, 710), "Một nét cong tròn khép kín", font=fonts["h3"], fill="#1E293B", anchor="mm")
        draw.text((1540, 760), "Không có mũ • Không có râu", font=fonts["badge"], fill="#64748B", anchor="mm")

    elif vis == "intro_oe":
        # Right Card for Ô
        draw.rounded_rectangle([1220, 120, 1860, 860], radius=28, fill=(255, 255, 255, 245), outline="#10B981", width=4)
        draw.text((1540, 180), "BÉ Ô ĐỘI MŨ", font=fonts["title"], fill="#059669", anchor="mm")
        draw.text((1540, 230), "Nguyên âm đơn /o/", font=fonts["h3"], fill="#64748B", anchor="mm")
        bounce_y = int(270 + 12 * math.sin(frame_i * 0.3))
        hat_im = ASSETS["hat"].resize((200, 200))
        im.paste(hat_im, (1440, bounce_y), hat_im)
        draw.text((1540, 520), "Chiếc mũ chóp nhọn cực xinh!", font=fonts["h2"], fill="#059669", anchor="mm")
        draw.rounded_rectangle([1260, 580, 1820, 810], radius=20, fill="#ECFDF5", outline="#10B981", width=3)
        draw.text((1540, 640), "ĐẶC ĐIỂM", font=fonts["badge"], fill="#10B981", anchor="mm")
        draw.text((1540, 710), "Chữ O + Mũ chóp nhọn (^)", font=fonts["h3"], fill="#1E293B", anchor="mm")
        draw.text((1540, 760), "Đội mũ ngay ngắn trên đầu", font=fonts["badge"], fill="#64748B", anchor="mm")

    elif vis == "intro_ow":
        # Left Card for Ơ (since Ơ is on right)
        draw.rounded_rectangle([60, 120, 700, 860], radius=28, fill=(255, 255, 255, 245), outline="#F59E0B", width=4)
        draw.text((380, 180), "BÉ Ơ CÓ RÂU", font=fonts["title"], fill="#D97706", anchor="mm")
        draw.text((380, 230), "Nguyên âm đơn /ɤ/", font=fonts["h3"], fill="#64748B", anchor="mm")
        bounce_y = int(270 + 12 * math.sin(frame_i * 0.3))
        hook_im = ASSETS["hook"].resize((200, 200))
        im.paste(hook_im, (280, bounce_y), hook_im)
        draw.text((380, 520), "Chiếc râu móc bên phải đáng yêu!", font=fonts["h2"], fill="#D97706", anchor="mm")
        draw.rounded_rectangle([100, 580, 660, 810], radius=20, fill="#FFFBEB", outline="#F59E0B", width=3)
        draw.text((380, 640), "ĐẶC ĐIỂM", font=fonts["badge"], fill="#F59E0B", anchor="mm")
        draw.text((380, 710), "Chữ O + Râu móc cong ( ' )", font=fonts["h3"], fill="#1E293B", anchor="mm")
        draw.text((380, 760), "Gắn bên tai phải tinh nghịch", font=fonts["badge"], fill="#64748B", anchor="mm")

    # 3. Solo Deep Dive: Pronunciation & Vocabulary
    elif vis == "feature_o":
        draw.rounded_rectangle([1200, 100, 1880, 870], radius=28, fill=(255, 255, 255, 245), outline="#EF4444", width=4)
        draw.text((1540, 160), "HỌC PHÁT ÂM: O", font=fonts["title"], fill="#DC2626", anchor="mm")
        draw_lip_diagram(draw, fonts, 1540, 290, "o", scale=pulse)
        # Cow word box
        draw.rounded_rectangle([1240, 440, 1840, 830], radius=20, fill="#FEF2F2", outline="#EF4444", width=3)
        cow_im = ASSETS["cow"].resize((180, 180))
        im.paste(cow_im, (1260, 490), cow_im)
        draw.text((1600, 530), "TỪ VỰNG TIÊU BIỂU", font=fonts["badge"], fill="#EF4444", anchor="mm")
        draw.text((1600, 610), "CON BÒ", font=fonts["title"], fill="#1E293B", anchor="mm")
        draw.text((1600, 670), "The Cow • /bɔ˨˩/", font=fonts["h3"], fill="#64748B", anchor="mm")
        draw.text((1600, 750), "O ... O ... BÒ!", font=fonts["h2"], fill="#DC2626", anchor="mm")

    elif vis == "feature_oe":
        draw.rounded_rectangle([1200, 100, 1880, 870], radius=28, fill=(255, 255, 255, 245), outline="#10B981", width=4)
        draw.text((1540, 160), "HỌC PHÁT ÂM: Ô", font=fonts["title"], fill="#059669", anchor="mm")
        draw_lip_diagram(draw, fonts, 1540, 290, "oe", scale=pulse)
        # Teacher word box
        draw.rounded_rectangle([1240, 440, 1840, 830], radius=20, fill="#ECFDF5", outline="#10B981", width=3)
        tch_im = ASSETS["teacher"].resize((180, 180))
        im.paste(tch_im, (1260, 490), tch_im)
        draw.text((1600, 530), "TỪ VỰNG TIÊU BIỂU", font=fonts["badge"], fill="#10B981", anchor="mm")
        draw.text((1600, 610), "CÔ GIÁO", font=fonts["title"], fill="#1E293B", anchor="mm")
        draw.text((1600, 670), "The Teacher • /ko˧˧/", font=fonts["h3"], fill="#64748B", anchor="mm")
        draw.text((1600, 750), "Ô ... Ô ... CÔ!", font=fonts["h2"], fill="#059669", anchor="mm")

    elif vis == "feature_ow":
        draw.rounded_rectangle([40, 100, 720, 870], radius=28, fill=(255, 255, 255, 245), outline="#F59E0B", width=4)
        draw.text((380, 160), "HỌC PHÁT ÂM: Ơ", font=fonts["title"], fill="#D97706", anchor="mm")
        draw_lip_diagram(draw, fonts, 380, 290, "ow", scale=pulse)
        # Avocado word box
        draw.rounded_rectangle([80, 440, 680, 830], radius=20, fill="#FFFBEB", outline="#F59E0B", width=3)
        avo_im = ASSETS["avocado"].resize((180, 180))
        im.paste(avo_im, (100, 490), avo_im)
        draw.text((440, 530), "TỪ VỰNG TIÊU BIỂU", font=fonts["badge"], fill="#F59E0B", anchor="mm")
        draw.text((440, 610), "QUẢ BƠ", font=fonts["title"], fill="#1E293B", anchor="mm")
        draw.text((440, 670), "The Avocado • /ɓɤ˧˧/", font=fonts["h3"], fill="#64748B", anchor="mm")
        draw.text((440, 750), "Ơ ... Ơ ... BƠ!", font=fonts["h2"], fill="#D97706", anchor="mm")

    # 4. Magic Transformation in 3D Classroom
    elif vis == "magic_o":
        draw.rounded_rectangle([460, 80, 1460, 210], radius=24, fill=(255, 255, 255, 240), outline="#EF4444", width=3)
        draw.text((960, 120), "CỖ MÁY BIẾN HÌNH CHỮ CÁI", font=fonts["title"], fill="#DC2626", anchor="mm")
        draw.text((960, 170), "1. Chữ gốc: O tròn xoe không mũ không râu", font=fonts["h3"], fill="#1E293B", anchor="mm")

    elif vis == "magic_oe":
        draw.rounded_rectangle([460, 80, 1460, 210], radius=24, fill=(255, 255, 255, 240), outline="#10B981", width=3)
        draw.text((960, 120), "CỖ MÁY BIẾN HÌNH CHỮ CÁI", font=fonts["title"], fill="#059669", anchor="mm")
        draw.text((960, 170), "2. Thêm mũ chóp nhọn (^) boong một cái = Ô!", font=fonts["h3"], fill="#1E293B", anchor="mm")
        # Floating hat dropping onto center
        hat_y = int(220 + 20 * math.sin(frame_i * 0.4))
        hat_im = ASSETS["hat"].resize((140, 140))
        im.paste(hat_im, (910, hat_y), hat_im)

    elif vis == "magic_ow":
        draw.rounded_rectangle([460, 80, 1460, 210], radius=24, fill=(255, 255, 255, 240), outline="#F59E0B", width=3)
        draw.text((960, 120), "CỖ MÁY BIẾN HÌNH CHỮ CÁI", font=fonts["title"], fill="#D97706", anchor="mm")
        draw.text((960, 170), "3. Thêm râu móc cong cong ( ' ) = Ơ! Thật kỳ diệu!", font=fonts["h3"], fill="#1E293B", anchor="mm")
        hook_y = int(220 + 20 * math.sin(frame_i * 0.4))
        hook_im = ASSETS["hook"].resize((140, 140))
        im.paste(hook_im, (910, hook_y), hook_im)

    # 5. Interactive Repeat Game
    elif vis in ("game_o_q", "game_o_repeat", "game_o_praise"):
        draw.rounded_rectangle([1220, 120, 1860, 860], radius=28, fill=(255, 255, 255, 245), outline="#EF4444", width=4)
        draw.text((1540, 180), "TRÒ CHƠI NHẮC LẠI", font=fonts["badge"], fill="#EF4444", anchor="mm")
        draw.text((1540, 280), "BÒ", font=fonts["huge_letter"], fill="#EF4444", anchor="mm")
        cow_im = ASSETS["cow"].resize((160, 160))
        im.paste(cow_im, (1460, 370), cow_im)
        if vis == "game_o_repeat":
            draw.rounded_rectangle([1260, 580, 1820, 780], radius=20, fill="#FEE2E2", outline="#EF4444", width=4)
            draw.text((1540, 640), "LƯỢT CỦA BẠN!", font=fonts["title"], fill="#DC2626", anchor="mm")
            draw.text((1540, 710), "Nói thật to: BÒ!", font=fonts["h2"], fill="#991B1B", anchor="mm")
        elif vis == "game_o_praise":
            draw.rounded_rectangle([1260, 580, 1820, 780], radius=20, fill="#ECFDF5", outline="#10B981", width=3)
            trophy_im = ASSETS["trophy"].resize((90, 90))
            im.paste(trophy_im, (1280, 630), trophy_im)
            draw.text((1560, 645), "HOAN HÔ!", font=fonts["title"], fill="#059669", anchor="mm")
            draw.text((1560, 715), "Phát âm chuẩn lắm!", font=fonts["h3"], fill="#047857", anchor="mm")
        else:
            draw.text((1540, 640), "Hãy nói theo Bé O nhé!", font=fonts["h2"], fill="#334155", anchor="mm")

    elif vis in ("game_oe_q", "game_oe_repeat", "game_oe_praise"):
        draw.rounded_rectangle([1220, 120, 1860, 860], radius=28, fill=(255, 255, 255, 245), outline="#10B981", width=4)
        draw.text((1540, 180), "TRÒ CHƠI NHẮC LẠI", font=fonts["badge"], fill="#10B981", anchor="mm")
        draw.text((1540, 280), "CÔ", font=fonts["huge_letter"], fill="#10B981", anchor="mm")
        tch_im = ASSETS["teacher"].resize((160, 160))
        im.paste(tch_im, (1460, 370), tch_im)
        if vis == "game_oe_repeat":
            draw.rounded_rectangle([1260, 580, 1820, 780], radius=20, fill="#D1FAE5", outline="#10B981", width=4)
            draw.text((1540, 640), "LƯỢT CỦA BẠN!", font=fonts["title"], fill="#059669", anchor="mm")
            draw.text((1540, 710), "Nói thật to: CÔ!", font=fonts["h2"], fill="#065F46", anchor="mm")
        elif vis == "game_oe_praise":
            draw.rounded_rectangle([1260, 580, 1820, 780], radius=20, fill="#ECFDF5", outline="#10B981", width=3)
            trophy_im = ASSETS["trophy"].resize((90, 90))
            im.paste(trophy_im, (1280, 630), trophy_im)
            draw.text((1560, 645), "TUYỆT VỜI!", font=fonts["title"], fill="#059669", anchor="mm")
            draw.text((1560, 715), "Bé Ô khen bạn nha!", font=fonts["h3"], fill="#047857", anchor="mm")
        else:
            draw.text((1540, 640), "Hãy nói theo Bé Ô nhé!", font=fonts["h2"], fill="#334155", anchor="mm")

    elif vis in ("game_ow_q", "game_ow_repeat", "game_ow_praise"):
        draw.rounded_rectangle([60, 120, 700, 860], radius=28, fill=(255, 255, 255, 245), outline="#F59E0B", width=4)
        draw.text((380, 180), "TRÒ CHƠI NHẮC LẠI", font=fonts["badge"], fill="#F59E0B", anchor="mm")
        draw.text((380, 280), "BƠ", font=fonts["huge_letter"], fill="#F59E0B", anchor="mm")
        avo_im = ASSETS["avocado"].resize((160, 160))
        im.paste(avo_im, (300, 370), avo_im)
        if vis == "game_ow_repeat":
            draw.rounded_rectangle([100, 580, 660, 780], radius=20, fill="#FEF3C7", outline="#F59E0B", width=4)
            draw.text((380, 640), "LƯỢT CỦA BẠN!", font=fonts["title"], fill="#D97706", anchor="mm")
            draw.text((380, 710), "Nói thật vang: BƠ!", font=fonts["h2"], fill="#92400E", anchor="mm")
        elif vis == "game_ow_praise":
            draw.rounded_rectangle([100, 580, 660, 780], radius=20, fill="#ECFDF5", outline="#10B981", width=3)
            trophy_im = ASSETS["trophy"].resize((90, 90))
            im.paste(trophy_im, (120, 630), trophy_im)
            draw.text((400, 645), "XUẤT SẮC!", font=fonts["title"], fill="#059669", anchor="mm")
            draw.text((400, 715), "Nói từ Bơ rất hay!", font=fonts["h3"], fill="#047857", anchor="mm")
        else:
            draw.text((380, 640), "Hãy nói theo Bé Ơ nhé!", font=fonts["h2"], fill="#334155", anchor="mm")

    # 6. Gameshow Quiz
    elif vis == "quiz_q":
        # Question card
        draw.rounded_rectangle([1180, 100, 1880, 870], radius=28, fill=(255, 255, 255, 245), outline="#3B82F6", width=4)
        draw.text((1530, 150), "ĐỐ VUI NHANH TRÍ", font=fonts["badge"], fill="#2563EB", anchor="mm")
        draw.text((1530, 220), "Ai đang ĐỘI CHIẾC MŨ?", font=fonts["title"], fill="#1E293B", anchor="mm")
        
        # 3 Options
        draw.rounded_rectangle([1220, 290, 1840, 380], radius=16, fill="#F8FAFC", outline="#CBD5E1", width=2)
        draw.text((1530, 335), "[A] Bé O (Tròn xoe)", font=fonts["quiz_opt"], fill="#334155", anchor="mm")
        
        # Option B (Pulsing highlight)
        draw.rounded_rectangle([1220, 410, 1840, 500], radius=16, fill="#EFF6FF", outline="#3B82F6", width=3)
        draw.text((1530, 455), "[B] Bé Ô (Đội mũ chóp)", font=fonts["quiz_opt"], fill="#1D4ED8", anchor="mm")
        
        draw.rounded_rectangle([1220, 530, 1840, 620], radius=16, fill="#F8FAFC", outline="#CBD5E1", width=2)
        draw.text((1530, 575), "[C] Bé Ơ (Có râu móc)", font=fonts["quiz_opt"], fill="#334155", anchor="mm")
        
        # Countdown timer
        sec_left = max(1, 3 - int(t_ratio * 3))
        draw.ellipse([1455, 680, 1605, 830], fill="#FEF08A", outline="#EAB308", width=4)
        draw.text((1530, 755), str(sec_left), font=fonts["timer"], fill="#B45309", anchor="mm")

    elif vis == "quiz_ans":
        # Winner Reveal
        draw.rounded_rectangle([1180, 100, 1880, 870], radius=28, fill=(255, 255, 255, 245), outline="#10B981", width=5)
        draw.text((1530, 170), "CHÍNH XÁC!", font=fonts["title"], fill="#059669", anchor="mm")
        draw.rounded_rectangle([1220, 240, 1840, 370], radius=20, fill="#ECFDF5", outline="#10B981", width=3)
        draw.text((1530, 305), "ĐÁP ÁN: [B] BÉ Ô", font=fonts["title"], fill="#047857", anchor="mm")
        
        hat_im = ASSETS["hat"].resize((180, 180))
        im.paste(hat_im, (1440, 410), hat_im)
        draw.text((1530, 630), "Bé Ô đội chiếc mũ nhọn cực xinh!", font=fonts["h2"], fill="#059669", anchor="mm")
        
        trophy_im = ASSETS["trophy"].resize((120, 120))
        im.paste(trophy_im, (1470, 680), trophy_im)

    # 7. Rhymes & Grand Finale
    elif vis == "rhyme_1":
        draw.rounded_rectangle([360, 60, 1560, 180], radius=24, fill=(255, 255, 255, 240), outline="#EF4444", width=4)
        draw.text((960, 120), "O tròn như quả trứng gà,", font=fonts["title"], fill="#DC2626", anchor="mm")
        egg_im = ASSETS["egg"].resize((160, 160))
        im.paste(egg_im, (420, 220), egg_im)

    elif vis == "rhyme_2":
        draw.rounded_rectangle([360, 60, 1560, 180], radius=24, fill=(255, 255, 255, 240), outline="#10B981", width=4)
        draw.text((960, 120), "Ô thì đội mũ,", font=fonts["title"], fill="#059669", anchor="mm")
        hat_im = ASSETS["hat"].resize((160, 160))
        im.paste(hat_im, (880, 220), hat_im)

    elif vis == "rhyme_3":
        draw.rounded_rectangle([360, 60, 1560, 180], radius=24, fill=(255, 255, 255, 240), outline="#F59E0B", width=4)
        draw.text((960, 120), "Ơ thì thêm râu!", font=fonts["title"], fill="#D97706", anchor="mm")
        hook_im = ASSETS["hook"].resize((160, 160))
        im.paste(hook_im, (1340, 220), hook_im)

    elif vis == "goodbye":
        # Confetti overlay
        conf_im = ASSETS["confetti"]
        im.paste(conf_im, (100, 60), conf_im)
        im.paste(conf_im, (1420, 60), conf_im)
        draw.rounded_rectangle([320, 80, 1600, 220], radius=28, fill=(255, 255, 255, 245), outline="#3B82F6", width=4)
        draw.text((960, 130), "TẠM BIỆT VÀ HẸN GẶP LẠI!", font=fonts["title"], fill="#1D4ED8", anchor="mm")
        draw.text((960, 180), "Chúc các bạn học tiếng Việt thật vui!", font=fonts["h2"], fill="#E11D48", anchor="mm")

    # Subtitle Bar
    draw_subtitle_bar(draw, seg["vi"], seg["en"], seg["speaker"], spk_col)
    return im

# Step 5: Render Video by Piping directly to FFmpeg
print("5. Starting master video rendering and piping to ffmpeg...")
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{W}x{H}",
    "-pix_fmt", "rgb24",
    "-r", str(FPS),
    "-i", "-",
    "-i", master_audio_wav,
    "-c:v", "libx264",
    "-preset", "medium",
    "-b:v", "2800k",
    "-maxrate", "3600k",
    "-bufsize", "5000k",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    FINAL_OUTPUT
]

proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

total_frames_all = sum(s["frames"] for s in segment_info)
print(f"Total Video Frames to render: {total_frames_all} ({total_frames_all/FPS:.2f}s)")

# Frame Cache to avoid re-reading disk repeatedly
IMG_CACHE = {}

def get_base_frame(sc_type, f_idx):
    paths = SEQ_MAP[sc_type]
    N = len(paths)
    # Ping pong index
    p_idx = abs(((f_idx) % (2 * N)) - N)
    p_idx = min(p_idx, N - 1)
    target_path = paths[p_idx]
    if target_path not in IMG_CACHE:
        raw_im = Image.open(target_path)
        if raw_im.size != (W, H):
            raw_im = raw_im.resize((W, H), Image.Resampling.BILINEAR)
        IMG_CACHE[target_path] = raw_im
    return IMG_CACHE[target_path]

global_f = 0
last_report = 0

for s_idx, seg in enumerate(segment_info):
    sc_type = seg["scene_type"]
    seg_frames = seg["frames"]
    for local_f in range(seg_frames):
        base_im = get_base_frame(sc_type, local_f)
        composed = compose_cartoon_frame(base_im, seg, local_f, seg_frames).convert("RGB")
        raw_bytes = composed.tobytes()
        proc.stdin.write(raw_bytes)
        global_f += 1
        
        pct = int(global_f / total_frames_all * 100)
        if pct >= last_report + 5:
            last_report = pct
            print(f"  [Render Progress] {global_f}/{total_frames_all} frames ({pct}%)")

proc.stdin.close()
err = proc.stderr.read().decode('utf-8', errors='ignore')
proc.wait()

if proc.returncode != 0:
    print(f"FFmpeg error: {err}")
    sys.exit(1)

print(f"6. Master video rendered successfully -> {FINAL_OUTPUT}")
final_dur = get_dur(FINAL_OUTPUT)
size_mb = os.path.getsize(FINAL_OUTPUT) / (1024 * 1024)
print(f"Master Video Stats: Duration = {final_dur:.2f}s, Size = {size_mb:.2f} MB")

# Re-link symlinks
sym1 = os.path.join(BASE_DIR, "video_o_o_o.mp4")
sym2 = os.path.join(BASE_DIR, "assets", "hero.mp4")
for s in [sym1, sym2]:
    if os.path.islink(s) or os.path.exists(s):
        os.remove(s)
    os.symlink(FINAL_OUTPUT, s)
print("Symlinks updated successfully!")

# Extract fresh still thumbnails for Web UI
stills_dir = os.path.join(BASE_DIR, "assets", "cartoon_stills")
os.makedirs(stills_dir, exist_ok=True)
for sec_mark, out_name in [
    (2, "c_01_title_intro.png"),
    (8, "c_02_solo_o.png"),
    (14, "c_03_solo_oe.png"),
    (20, "c_04_solo_ow.png"),
    (32, "c_05_deep_o.png"),
    (45, "c_06_deep_oe.png"),
    (58, "c_07_deep_ow.png"),
    (70, "c_08_magic_room.png"),
    (90, "c_09_repeat_game.png"),
    (110, "c_10_quiz_arena.png"),
    (135, "c_11_rhyme_finale.png")
]:
    out_p = os.path.join(stills_dir, out_name)
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(sec_mark), "-i", FINAL_OUTPUT,
        "-vframes", "1", "-q:v", "2", out_p
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Extracted 11 rich still thumbnails for UI!")
