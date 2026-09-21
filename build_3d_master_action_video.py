import os
import sys
import subprocess
import math
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = "/home/quang/video_ai"
AUDIO_DIR = os.path.join(BASE_DIR, "audio_3_chars")
SFX_DIR = os.path.join(BASE_DIR, "audio")
ASSETS_DIR = os.path.join(BASE_DIR, "cartoon_assets")
FRAMES_DIR = os.path.join(BASE_DIR, "snaptik_frames")
TEMP_DIR = os.path.join(BASE_DIR, "cartoon_temp_3d")
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
        "quiz_title": ImageFont.truetype(FONT_BOLD, 28),
        "timer": ImageFont.truetype(FONT_BOLD, 72)
    }

QUIZ_DATA = {
    "quiz_q1": {
        "num": "CÂU HỎI 1/5",
        "title": "Ai đang ĐỘI CHIẾC MŨ?",
    },
    "quiz_a1": {
        "ans": "ĐÁP ÁN: [B] BÉ Ô",
        "desc": "Bé Ô đội chiếc mũ nhọn cực xinh!",
        "asset": "hat"
    },
    "quiz_q2": {
        "num": "CÂU HỎI 2/5",
        "title": "Ai có chiếc RÂU MÓC cong cong?",
    },
    "quiz_a2": {
        "ans": "ĐÁP ÁN: [C] BÉ Ơ",
        "desc": "Bé Ơ có chiếc râu móc cực xinh!",
        "asset": "hook"
    },
    "quiz_q3": {
        "num": "CÂU HỎI 3/5",
        "title": "Từ 'CON BÒ' chứa âm bạn nào?",
    },
    "quiz_a3": {
        "ans": "ĐÁP ÁN: [A] BÉ O",
        "desc": "Từ Con bò chứa nguyên âm O tròn xoe!",
        "asset": "cow"
    },
    "quiz_q4": {
        "num": "CÂU HỎI 4/5",
        "title": "Môi MỈM CƯỜI DẸT NGANG là ai?",
    },
    "quiz_a4": {
        "ans": "ĐÁP ÁN: [C] BÉ Ơ",
        "desc": "Phát âm Ơ: khóe môi kéo dẹt ngang!",
        "asset": "avocado"
    },
    "quiz_q5": {
        "num": "CÂU HỎI 5/5",
        "title": "O tròn thêm MŨ CHÓP là ai?",
    },
    "quiz_a5": {
        "ans": "ĐÁP ÁN: [B] BÉ Ô",
        "desc": "O đội mũ thành Ô — Rất xuất sắc!",
        "asset": "hat"
    }
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
sil_25 = os.path.join(TEMP_DIR, "sil_25.wav")
make_silence(0.3, sil_03)
make_silence(0.4, sil_04)
make_silence(0.5, sil_05)
make_silence(1.0, sil_10)
make_silence(1.5, sil_15)
make_silence(2.5, sil_25)

wav_tick = prep_wav(SFX_DIR, "sfx_tick.mp3")
wav_ding = prep_wav(SFX_DIR, "sfx_ding.mp3")

# Load Cartoon Action Assets
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

# Timeline Definition on top of 3D Old Clip
# (cam_mode, speaker_name, speaker_color, visual_mode, audio_list, vi_sub, en_sub)
# cam_modes: "wide", "zoom_o", "zoom_oe", "zoom_ow", "dim_quiz"
timeline = [
    # --- SCENE 1: Chào hỏi chung cả 3 bạn (Wide 3D Room) ---
    ("wide", "Bộ Ba O - Ô - Ơ", "#3B82F6", "intro_trio",
     [sil_04, prep_wav(AUDIO_DIR, "c_trio_intro.mp3"), sil_04],
     "Chào mừng các bạn nhỏ! Chúng tớ là bộ ba bạn thân O, Ô, Ơ!",
     "Welcome friends! We are best friends O, Ô, Ơ!"),

    # --- SCENE 2: Làm Quen Riêng Từng Bạn (Camera Zoom Cận Cảnh 3D) ---
    ("zoom_o", "Bé O", "#EF4444", "intro_o",
     [prep_wav(AUDIO_DIR, "c_o_intro.mp3"), sil_04],
     "Xin chào các bạn! Tớ là Bé O tròn vo như quả trứng gà nè!",
     "Hello friends! I am round O like a chicken egg!"),

    ("zoom_oe", "Bé Ô", "#10B981", "intro_oe",
     [prep_wav(AUDIO_DIR, "c_oe_intro.mp3"), sil_04],
     "Còn tớ là Bé Ô! Tớ có chiếc mũ chóp nhọn cực xinh trên đầu!",
     "And I am Ô! I have a cute pointy hat on my head!"),

    ("zoom_ow", "Bé Ơ", "#F59E0B", "intro_ow",
     [prep_wav(AUDIO_DIR, "c_ow_intro.mp3"), sil_05],
     "Hihi, tớ là Bé Ơ đây! Tớ có chiếc râu móc cong cong đáng yêu nè!",
     "Hihi, I am Ơ! I have an adorable curved hook whisker!"),

    # --- SCENE 3: Khám Phá Sâu & Khẩu Hình Sư Phạm ---
    # Bé O + BÒ
    ("zoom_o", "Bé O", "#EF4444", "feature_o",
     [prep_wav(AUDIO_DIR, "c_o_feature.mp3"), sil_05],
     "Tớ là Bé O! Chữ chỉ có một nét cong tròn khép kín. Mở to môi nói O: O ... O ... Con bò!",
     "I am Bé O! One smooth round circle. Open lips wide and say O: O ... O ... Con bò!"),

    # Bé Ô + CÔ
    ("zoom_oe", "Bé Ô", "#10B981", "feature_oe",
     [prep_wav(AUDIO_DIR, "c_oe_feature.mp3"), sil_05],
     "Đến lượt tớ, Bé Ô đây! Tớ đội chiếc mũ nón chóp. Chu môi nhô ra trước và nói Ô: Ô ... Ô ... Cô giáo!",
     "My turn, Bé Ô! I wear a cute hat. Pucker lips forward and say Ô: Ô ... Ô ... Cô giáo!"),

    # Bé Ơ + BƠ
    ("zoom_ow", "Bé Ơ", "#F59E0B", "feature_ow",
     [prep_wav(AUDIO_DIR, "c_ow_feature.mp3"), sil_05],
     "Còn tớ là Bé Ơ! Tớ có chiếc râu móc bên phải. Mỉm cười dẹt môi ngang và nói Ơ: Ơ ... Ơ ... Quả bơ!",
     "And I am Bé Ơ! I have a hook on the right. Smile with flat lips and say Ơ: Ơ ... Ơ ... Quả bơ!"),

    # --- SCENE 4: Cỗ Máy Biến Hình Kỳ Diệu (Wide 3D Room + Magic Sparkles) ---
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

    # --- SCENE 5: Trò Chơi Nhắc Lại Tương Tác (Interactive Shadowing Game) ---
    # Round 1: BÒ (Bé O)
    ("zoom_o", "Bé O", "#EF4444", "game_o_q",
     [prep_wav(AUDIO_DIR, "c_game_o_q.mp3"), sil_04],
     "Các bạn cùng chơi trò nhắc lại nhé! Hãy nói theo tớ nào: BÒ!",
     "Let's play the repeat game! Say after me: BÒ!"),

    ("zoom_o", "Lượt Của Bạn", "#EF4444", "game_o_repeat",
     [sil_25, wav_ding],
     "[Đến lượt bạn nói to: BÒ!] ... Ding!",
     "[Your turn to repeat loudly: BÒ!] ... Ding!"),

    ("zoom_o", "Bé O", "#EF4444", "game_o_praise",
     [prep_wav(AUDIO_DIR, "c_game_o_praise.mp3"), sil_05],
     "Hoan hô! Các bạn phát âm từ Bò chuẩn lắm!",
     "Bravo! You pronounced Bò so accurately!"),

    # Round 2: CÔ (Bé Ô)
    ("zoom_oe", "Bé Ô", "#10B981", "game_oe_q",
     [prep_wav(AUDIO_DIR, "c_game_oe_q.mp3"), sil_04],
     "Đến lượt tớ nè! Hãy nói thật to theo tớ: CÔ!",
     "My turn! Say loudly after me: CÔ!"),

    ("zoom_oe", "Lượt Của Bạn", "#10B981", "game_oe_repeat",
     [sil_25, wav_ding],
     "[Đến lượt bạn nói to: CÔ!] ... Ding!",
     "[Your turn to repeat loudly: CÔ!] ... Ding!"),

    ("zoom_oe", "Bé Ô", "#10B981", "game_oe_praise",
     [prep_wav(AUDIO_DIR, "c_game_oe_praise.mp3"), sil_05],
     "Tuyệt vời quá! Bé Ô khen bạn nha!",
     "Wonderful! Bé Ô praises you!"),

    # Round 3: BƠ (Bé Ơ)
    ("zoom_ow", "Bé Ơ", "#F59E0B", "game_ow_q",
     [prep_wav(AUDIO_DIR, "c_game_ow_q.mp3"), sil_04],
     "Còn tớ nữa nè! Hãy nói thật vang theo tớ: BƠ!",
     "And me! Say clearly after me: BƠ!"),

    ("zoom_ow", "Lượt Của Bạn", "#F59E0B", "game_ow_repeat",
     [sil_25, wav_ding],
     "[Đến lượt bạn nói to: BƠ!] ... Ding!",
     "[Your turn to repeat loudly: BƠ!] ... Ding!"),

    ("zoom_ow", "Bé Ơ", "#F59E0B", "game_ow_praise",
     [prep_wav(AUDIO_DIR, "c_game_ow_praise.mp3"), sil_05],
     "Xuất sắc! Các bạn nói từ Bơ rất hay!",
     "Excellent! You said Bơ wonderfully!"),

    # --- SCENE 6: Gameshow Đố Vui Trắc Nghiệm (Spotlight Quiz Arena - 5 Câu) ---
    # Q1: Đội mũ -> Ô (B)
    ("dim_quiz", "Bé O", "#EF4444", "quiz_q1",
     [prep_wav(AUDIO_DIR, "c_quiz_q1.mp3"), sil_04, wav_tick, sil_05, wav_tick, sil_05, wav_tick, sil_05],
     "Đố các bạn nhanh trí nè: Câu số một: Ai trong ba chúng tớ đang ĐỘI CHIẾC MŨ trên đầu?",
     "Quick quiz: Question 1: Which one of us is wearing a HAT on its head?"),
    ("dim_quiz", "Bé Ô", "#10B981", "quiz_a1",
     [wav_ding, prep_wav(AUDIO_DIR, "c_quiz_a1.mp3"), sil_05],
     "Hê hê! Chính là tớ, Bé Ô đội chiếc mũ nhọn xinh xắn đây nè!",
     "Hehe! It's me, Bé Ô with the cute pointy hat!"),

    # Q2: Râu móc -> Ơ (C)
    ("dim_quiz", "Bé O", "#EF4444", "quiz_q2",
     [prep_wav(AUDIO_DIR, "c_quiz_q2.mp3"), sil_04, wav_tick, sil_05, wav_tick, sil_05, wav_tick, sil_05],
     "Câu số hai: Đố các bạn, ai có chiếc RÂU MÓC cong cong ở bên phải?",
     "Question 2: Which one of us has a curved HOOK on the right side?"),
    ("dim_quiz", "Bé Ơ", "#F59E0B", "quiz_a2",
     [wav_ding, prep_wav(AUDIO_DIR, "c_quiz_a2.mp3"), sil_05],
     "Hihi, chính là tớ! Bé Ơ có chiếc râu móc cong cong bên phải nè!",
     "Hihi! It's me, Bé Ơ with the cute curved hook on the right!"),

    # Q3: Thính giác Con bò -> O (A)
    ("dim_quiz", "Bé Ô", "#10B981", "quiz_q3",
     [prep_wav(AUDIO_DIR, "c_quiz_q3.mp3"), sil_03, prep_wav(AUDIO_DIR, "c_quiz_sound3.mp3"), sil_03, wav_tick, sil_05, wav_tick, sil_05, wav_tick, sil_05],
     "Câu số ba: Lắng nghe âm thanh sau và đoán xem từ này chứa nguyên âm của bạn nào nhé: Bò... Con bò!",
     "Question 3: Listen to the audio and guess which vowel it contains: Bò... Con bò!"),
    ("dim_quiz", "Bé O", "#EF4444", "quiz_a3",
     [wav_ding, prep_wav(AUDIO_DIR, "c_quiz_a3.mp3"), sil_05],
     "Chính xác một trăm phần trăm! Từ 'Con bò' chứa nguyên âm O tròn xoe!",
     "100% correct! The word 'Con bò' contains the round vowel O!"),

    # Q4: Khẩu hình dẹt ngang -> Ơ (C)
    ("dim_quiz", "Bé Ô", "#10B981", "quiz_q4",
     [prep_wav(AUDIO_DIR, "c_quiz_q4.mp3"), sil_04, wav_tick, sil_05, wav_tick, sil_05, wav_tick, sil_05],
     "Câu số bốn: Khi phát âm, hai mép môi MỈM CƯỜI VÀ DẸT NGANG là của bạn nào?",
     "Question 4: When pronouncing, which mascot has smiling and horizontally flattened lips?"),
    ("dim_quiz", "Bé Ơ", "#F59E0B", "quiz_a4",
     [wav_ding, prep_wav(AUDIO_DIR, "c_quiz_a4.mp3"), sil_05],
     "Xuất sắc! Đúng rồi, khi phát âm Ơ, hai mép môi dẹt ngang như đang mỉm cười!",
     "Excellent! Exactly, when saying Ơ, lips flatten sideways like a smile!"),

    # Q5: Vận dụng O + Mũ = Ô -> Ô (B)
    ("dim_quiz", "Bé O", "#EF4444", "quiz_q5",
     [prep_wav(AUDIO_DIR, "c_quiz_q5.mp3"), sil_04, wav_tick, sil_05, wav_tick, sil_05, wav_tick, sil_05],
     "Câu số năm: Lấy bạn O tròn xoe, thêm một CHIẾC MŨ CHÓP, ta được bạn nào?",
     "Question 5: Take round O, add a pointy hat on top, what letter do we get?"),
    ("dim_quiz", "Bé Ô", "#10B981", "quiz_a5",
     [wav_ding, prep_wav(AUDIO_DIR, "c_quiz_a5.mp3"), sil_05],
     "Hoan hô! O tròn như quả trứng gà, Ô thì đội mũ — O thêm mũ chính là Bé Ô! Các bạn làm bài rất tuyệt vời!",
     "Hooray! Round like an egg is O, with a hat is Ô — O with a hat is Bé Ô! You did amazing!"),

    # --- SCENE 7: Lễ Hội Đồng Dao & Điệu Nhảy Tạm Biệt (Grand Finale 3D Room) ---
    ("wide", "Bé Ơ", "#F59E0B", "rhyme_1",
     [prep_wav(AUDIO_DIR, "c_rhyme_1.mp3")],
     "Các bạn luôn nhớ câu thơ dân gian nhé: O tròn như quả trứng gà,",
     "Always remember the folk rhyme: Plain round is O like a chicken egg,"),

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

# Step 2: Concatenate Audio
print("2. Concatenating audio segments...")
all_wavs = []
segment_info = []

for cam_m, spk_n, spk_c, vis_m, wav_list, vi_s, en_s in timeline:
    dur = sum(get_dur(w) for w in wav_list)
    frames_count = max(1, int(round(dur * FPS)))
    segment_info.append({
        "cam_mode": cam_m,
        "speaker": spk_n,
        "color": spk_c,
        "vis_mode": vis_m,
        "frames": frames_count,
        "dur": dur,
        "vi": vi_s,
        "en": en_s
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

# Step 4: Index 3D Room Frames (1..241)
print("4. Indexing 241 3D Room frames...")
FRAME_PATHS_3D = []
for i in range(1, 242):
    p = os.path.join(FRAMES_DIR, f"frame_{i:04d}.png")
    if os.path.exists(p):
        FRAME_PATHS_3D.append(p)
print(f"Loaded {len(FRAME_PATHS_3D)} 3D Room frames!")

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

def compose_3d_frame(base_img, seg, frame_i, total_f):
    cam = seg["cam_mode"]
    
    # 1. Camera Framing on 3D Room Clip
    if cam == "wide":
        frame = base_img.copy()
    elif cam == "zoom_o":
        # Bé O on left
        crop = base_img.crop((40, 140, 40 + 1422, 140 + 800))
        frame = crop.resize((W, H), Image.Resampling.LANCZOS)
    elif cam == "zoom_oe":
        # Bé Ô in center-right (crop 150..1572)
        crop = base_img.crop((150, 140, 150 + 1422, 140 + 800))
        frame = crop.resize((W, H), Image.Resampling.LANCZOS)
    elif cam == "zoom_ow":
        # Bé Ơ on right (crop 458..1880)
        crop = base_img.crop((458, 140, 458 + 1422, 140 + 800))
        frame = crop.resize((W, H), Image.Resampling.LANCZOS)
    elif cam == "dim_quiz":
        # Dim room for quiz show spotlight
        frame = base_img.copy()
        dim_overlay = Image.new("RGBA", (W, H), (10, 15, 30, 110))
        frame.paste(dim_overlay, (0, 0), dim_overlay)

    draw = ImageDraw.Draw(frame)
    vis = seg["vis_mode"]
    spk_col = seg["color"]
    t_ratio = frame_i / max(1, total_f)
    pulse = 1.0 + 0.08 * math.sin(frame_i * 0.4)

    # 2. Scene Specific Overlays & Actions
    if vis == "intro_trio":
        draw.rounded_rectangle([360, 50, 1560, 150], radius=25, fill=(255, 255, 255, 240), outline="#3B82F6", width=4)
        draw.text((960, 100), "BỘ BA BẠN THÂN: BÉ O — BÉ Ô — BÉ Ơ", font=fonts["title"], fill="#1D4ED8", anchor="mm")

    elif vis == "intro_o":
        # Label above 3D Bé O
        draw.rounded_rectangle([260, 80, 540, 140], radius=15, fill="#EF4444", outline="#FCA5A5", width=3)
        draw.text((400, 110), "Bé O Đang Nói", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
        # Right Card for O
        draw.rounded_rectangle([1180, 100, 1860, 870], radius=28, fill=(255, 255, 255, 245), outline="#EF4444", width=4)
        draw.text((1520, 160), "BÉ O TRÒN XOE", font=fonts["title"], fill="#DC2626", anchor="mm")
        draw.text((1520, 210), "Nguyên âm đơn /ɔ/", font=fonts["h3"], fill="#64748B", anchor="mm")
        # Bouncing Egg Action
        bounce_y = int(250 + 12 * math.sin(frame_i * 0.3))
        egg_im = ASSETS["egg"].resize((180, 180))
        frame.paste(egg_im, (1430, bounce_y), egg_im)
        draw.text((1520, 480), "Tròn vo như quả trứng gà!", font=fonts["h2"], fill="#D97706", anchor="mm")
        draw.rounded_rectangle([1220, 540, 1820, 800], radius=20, fill="#FEF2F2", outline="#EF4444", width=3)
        draw.text((1520, 600), "ĐẶC ĐIỂM", font=fonts["badge"], fill="#EF4444", anchor="mm")
        draw.text((1520, 670), "Một nét cong tròn khép kín", font=fonts["h3"], fill="#1E293B", anchor="mm")
        draw.text((1520, 725), "Không có mũ • Không có râu", font=fonts["badge"], fill="#64748B", anchor="mm")

    elif vis == "intro_oe":
        # Label above 3D Bé Ô
        draw.rounded_rectangle([1080, 80, 1360, 140], radius=15, fill="#10B981", outline="#6EE7B7", width=3)
        draw.text((1220, 110), "Bé Ô Đang Nói", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
        # Left Card for Ô
        draw.rounded_rectangle([60, 100, 740, 870], radius=28, fill=(255, 255, 255, 245), outline="#10B981", width=4)
        draw.text((400, 160), "BÉ Ô ĐỘI MŨ", font=fonts["title"], fill="#059669", anchor="mm")
        draw.text((400, 210), "Nguyên âm đơn /o/", font=fonts["h3"], fill="#64748B", anchor="mm")
        # Hat Action
        bounce_y = int(250 + 12 * math.sin(frame_i * 0.3))
        hat_im = ASSETS["hat"].resize((180, 180))
        frame.paste(hat_im, (310, bounce_y), hat_im)
        draw.text((400, 480), "Chiếc mũ chóp nhọn cực xinh!", font=fonts["h2"], fill="#059669", anchor="mm")
        draw.rounded_rectangle([100, 540, 700, 800], radius=20, fill="#ECFDF5", outline="#10B981", width=3)
        draw.text((400, 600), "ĐẶC ĐIỂM", font=fonts["badge"], fill="#10B981", anchor="mm")
        draw.text((400, 670), "Chữ O + Mũ chóp nhọn (^)", font=fonts["h3"], fill="#1E293B", anchor="mm")
        draw.text((400, 725), "Đội mũ ngay ngắn trên đầu", font=fonts["badge"], fill="#64748B", anchor="mm")

    elif vis == "intro_ow":
        # Label above 3D Bé Ơ
        draw.rounded_rectangle([1380, 80, 1660, 140], radius=15, fill="#F59E0B", outline="#FCD34D", width=3)
        draw.text((1520, 110), "Bé Ơ Đang Nói", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
        # Left Card for Ơ
        draw.rounded_rectangle([60, 100, 740, 870], radius=28, fill=(255, 255, 255, 245), outline="#F59E0B", width=4)
        draw.text((400, 160), "BÉ Ơ CÓ RÂU", font=fonts["title"], fill="#D97706", anchor="mm")
        draw.text((400, 210), "Nguyên âm đơn /ɤ/", font=fonts["h3"], fill="#64748B", anchor="mm")
        # Hook Action
        bounce_y = int(250 + 12 * math.sin(frame_i * 0.3))
        hook_im = ASSETS["hook"].resize((180, 180))
        frame.paste(hook_im, (310, bounce_y), hook_im)
        draw.text((400, 480), "Chiếc râu móc bên phải đáng yêu!", font=fonts["h2"], fill="#D97706", anchor="mm")
        draw.rounded_rectangle([100, 540, 700, 800], radius=20, fill="#FFFBEB", outline="#F59E0B", width=3)
        draw.text((400, 600), "ĐẶC ĐIỂM", font=fonts["badge"], fill="#F59E0B", anchor="mm")
        draw.text((400, 670), "Chữ O + Râu móc cong ( ' )", font=fonts["h3"], fill="#1E293B", anchor="mm")
        draw.text((400, 725), "Gắn bên tai phải tinh nghịch", font=fonts["badge"], fill="#64748B", anchor="mm")

    # 3. Deep Dive Pronunciation & Vocabulary Cards
    elif vis == "feature_o":
        draw.rounded_rectangle([260, 80, 540, 140], radius=15, fill="#EF4444", outline="#FCA5A5", width=3)
        draw.text((400, 110), "Bé O Đang Nói", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
        draw.rounded_rectangle([1180, 100, 1860, 870], radius=28, fill=(255, 255, 255, 245), outline="#EF4444", width=4)
        draw.text((1520, 160), "HỌC PHÁT ÂM: O", font=fonts["title"], fill="#DC2626", anchor="mm")
        draw_lip_diagram(draw, fonts, 1520, 290, "o", scale=pulse)
        draw.rounded_rectangle([1220, 440, 1820, 820], radius=20, fill="#FEF2F2", outline="#EF4444", width=3)
        cow_im = ASSETS["cow"].resize((180, 180))
        frame.paste(cow_im, (1240, 490), cow_im)
        draw.text((1580, 530), "TỪ VỰNG A1", font=fonts["badge"], fill="#EF4444", anchor="mm")
        draw.text((1580, 610), "CON BÒ", font=fonts["title"], fill="#1E293B", anchor="mm")
        draw.text((1580, 670), "The Cow • /bɔ˨˩/", font=fonts["h3"], fill="#64748B", anchor="mm")
        draw.text((1580, 750), "O ... O ... BÒ!", font=fonts["h2"], fill="#DC2626", anchor="mm")

    elif vis == "feature_oe":
        draw.rounded_rectangle([1080, 80, 1360, 140], radius=15, fill="#10B981", outline="#6EE7B7", width=3)
        draw.text((1220, 110), "Bé Ô Đang Nói", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
        draw.rounded_rectangle([60, 100, 740, 870], radius=28, fill=(255, 255, 255, 245), outline="#10B981", width=4)
        draw.text((400, 160), "HỌC PHÁT ÂM: Ô", font=fonts["title"], fill="#059669", anchor="mm")
        draw_lip_diagram(draw, fonts, 400, 290, "oe", scale=pulse)
        draw.rounded_rectangle([100, 440, 700, 820], radius=20, fill="#ECFDF5", outline="#10B981", width=3)
        tch_im = ASSETS["teacher"].resize((180, 180))
        frame.paste(tch_im, (120, 490), tch_im)
        draw.text((460, 530), "TỪ VỰNG A1", font=fonts["badge"], fill="#10B981", anchor="mm")
        draw.text((460, 610), "CÔ GIÁO", font=fonts["title"], fill="#1E293B", anchor="mm")
        draw.text((460, 670), "The Teacher • /ko˧˧/", font=fonts["h3"], fill="#64748B", anchor="mm")
        draw.text((460, 750), "Ô ... Ô ... CÔ!", font=fonts["h2"], fill="#059669", anchor="mm")

    elif vis == "feature_ow":
        draw.rounded_rectangle([1380, 80, 1660, 140], radius=15, fill="#F59E0B", outline="#FCD34D", width=3)
        draw.text((1520, 110), "Bé Ơ Đang Nói", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
        draw.rounded_rectangle([60, 100, 740, 870], radius=28, fill=(255, 255, 255, 245), outline="#F59E0B", width=4)
        draw.text((400, 160), "HỌC PHÁT ÂM: Ơ", font=fonts["title"], fill="#D97706", anchor="mm")
        draw_lip_diagram(draw, fonts, 400, 290, "ow", scale=pulse)
        draw.rounded_rectangle([100, 440, 700, 820], radius=20, fill="#FFFBEB", outline="#F59E0B", width=3)
        avo_im = ASSETS["avocado"].resize((180, 180))
        frame.paste(avo_im, (120, 490), avo_im)
        draw.text((460, 530), "TỪ VỰNG A1", font=fonts["badge"], fill="#F59E0B", anchor="mm")
        draw.text((460, 610), "QUẢ BƠ", font=fonts["title"], fill="#1E293B", anchor="mm")
        draw.text((460, 670), "The Avocado • /ɓɤ˧˧/", font=fonts["h3"], fill="#64748B", anchor="mm")
        draw.text((460, 750), "Ơ ... Ơ ... BƠ!", font=fonts["h2"], fill="#D97706", anchor="mm")

    # 4. Magic Transformation in 3D Classroom
    elif vis == "magic_o":
        draw.rounded_rectangle([360, 50, 1560, 150], radius=25, fill=(255, 255, 255, 240), outline="#EF4444", width=4)
        draw.text((960, 80), "CỖ MÁY BIẾN HÌNH CHỮ CÁI", font=fonts["title"], fill="#DC2626", anchor="mm")
        draw.text((960, 125), "1. Chữ gốc: Bé O tròn xoe không mũ không râu", font=fonts["h3"], fill="#1E293B", anchor="mm")

    elif vis == "magic_oe":
        draw.rounded_rectangle([360, 50, 1560, 150], radius=25, fill=(255, 255, 255, 240), outline="#10B981", width=4)
        draw.text((960, 80), "CỖ MÁY BIẾN HÌNH CHỮ CÁI", font=fonts["title"], fill="#059669", anchor="mm")
        draw.text((960, 125), "2. Thêm mũ chóp nhọn rơi xuống BOONG một cái = Bé Ô!", font=fonts["h3"], fill="#1E293B", anchor="mm")
        # Floating hat landing on Bé Ô
        hat_y = int(220 + 20 * math.sin(frame_i * 0.4))
        hat_sm = ASSETS["hat"].resize((130, 130))
        frame.paste(hat_sm, (985, hat_y), hat_sm)

    elif vis == "magic_ow":
        draw.rounded_rectangle([360, 50, 1560, 150], radius=25, fill=(255, 255, 255, 240), outline="#F59E0B", width=4)
        draw.text((960, 80), "CỖ MÁY BIẾN HÌNH CHỮ CÁI", font=fonts["title"], fill="#D97706", anchor="mm")
        draw.text((960, 125), "3. Thêm chiếc râu móc bay tới VÍU = Bé Ơ! Thật kỳ diệu!", font=fonts["h3"], fill="#1E293B", anchor="mm")
        hook_y = int(220 + 20 * math.sin(frame_i * 0.4))
        hook_sm = ASSETS["hook"].resize((130, 130))
        frame.paste(hook_sm, (1505, hook_y), hook_sm)

    # 5. Interactive Repeat Game
    elif vis in ("game_o_q", "game_o_repeat", "game_o_praise"):
        draw.rounded_rectangle([260, 80, 540, 140], radius=15, fill="#EF4444", outline="#FCA5A5", width=3)
        draw.text((400, 110), "Bé O Đang Nói", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
        draw.rounded_rectangle([1180, 100, 1860, 870], radius=28, fill=(255, 255, 255, 245), outline="#EF4444", width=4)
        draw.text((1520, 170), "TRÒ CHƠI NHẮC LẠI", font=fonts["badge"], fill="#EF4444", anchor="mm")
        draw.text((1520, 270), "BÒ", font=fonts["huge_letter"], fill="#EF4444", anchor="mm")
        cow_im = ASSETS["cow"].resize((160, 160))
        frame.paste(cow_im, (1440, 360), cow_im)
        if vis == "game_o_repeat":
            draw.rounded_rectangle([1220, 570, 1820, 780], radius=20, fill="#FEE2E2", outline="#EF4444", width=4)
            draw.text((1520, 635), "LƯỢT CỦA BẠN!", font=fonts["title"], fill="#DC2626", anchor="mm")
            draw.text((1520, 710), "Nói thật to: BÒ!", font=fonts["h2"], fill="#991B1B", anchor="mm")
        elif vis == "game_o_praise":
            draw.rounded_rectangle([1220, 570, 1820, 780], radius=20, fill="#ECFDF5", outline="#10B981", width=3)
            trophy_im = ASSETS["trophy"].resize((90, 90))
            frame.paste(trophy_im, (1250, 630), trophy_im)
            draw.text((1540, 645), "HOAN HÔ!", font=fonts["title"], fill="#059669", anchor="mm")
            draw.text((1540, 715), "Phát âm chuẩn lắm!", font=fonts["h3"], fill="#047857", anchor="mm")
        else:
            draw.text((1520, 635), "Hãy nói theo Bé O nhé!", font=fonts["h2"], fill="#334155", anchor="mm")

    elif vis in ("game_oe_q", "game_oe_repeat", "game_oe_praise"):
        draw.rounded_rectangle([1080, 80, 1360, 140], radius=15, fill="#10B981", outline="#6EE7B7", width=3)
        draw.text((1220, 110), "Bé Ô Đang Nói", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
        draw.rounded_rectangle([60, 100, 740, 870], radius=28, fill=(255, 255, 255, 245), outline="#10B981", width=4)
        draw.text((400, 170), "TRÒ CHƠI NHẮC LẠI", font=fonts["badge"], fill="#10B981", anchor="mm")
        draw.text((400, 270), "CÔ", font=fonts["huge_letter"], fill="#10B981", anchor="mm")
        tch_im = ASSETS["teacher"].resize((160, 160))
        frame.paste(tch_im, (320, 360), tch_im)
        if vis == "game_oe_repeat":
            draw.rounded_rectangle([100, 570, 700, 780], radius=20, fill="#D1FAE5", outline="#10B981", width=4)
            draw.text((400, 635), "LƯỢT CỦA BẠN!", font=fonts["title"], fill="#059669", anchor="mm")
            draw.text((400, 710), "Nói thật to: CÔ!", font=fonts["h2"], fill="#065F46", anchor="mm")
        elif vis == "game_oe_praise":
            draw.rounded_rectangle([100, 570, 700, 780], radius=20, fill="#ECFDF5", outline="#10B981", width=3)
            trophy_im = ASSETS["trophy"].resize((90, 90))
            frame.paste(trophy_im, (120, 630), trophy_im)
            draw.text((420, 645), "TUYỆT VỜI!", font=fonts["title"], fill="#059669", anchor="mm")
            draw.text((420, 715), "Bé Ô khen bạn nha!", font=fonts["h3"], fill="#047857", anchor="mm")
        else:
            draw.text((400, 635), "Hãy nói theo Bé Ô nhé!", font=fonts["h2"], fill="#334155", anchor="mm")

    elif vis in ("game_ow_q", "game_ow_repeat", "game_ow_praise"):
        draw.rounded_rectangle([1380, 80, 1660, 140], radius=15, fill="#F59E0B", outline="#FCD34D", width=3)
        draw.text((1520, 110), "Bé Ơ Đang Nói", font=fonts["badge"], fill="#FFFFFF", anchor="mm")
        draw.rounded_rectangle([60, 100, 740, 870], radius=28, fill=(255, 255, 255, 245), outline="#F59E0B", width=4)
        draw.text((400, 170), "TRÒ CHƠI NHẮC LẠI", font=fonts["badge"], fill="#F59E0B", anchor="mm")
        draw.text((400, 270), "BƠ", font=fonts["huge_letter"], fill="#F59E0B", anchor="mm")
        avo_im = ASSETS["avocado"].resize((160, 160))
        frame.paste(avo_im, (320, 360), avo_im)
        if vis == "game_ow_repeat":
            draw.rounded_rectangle([100, 570, 700, 780], radius=20, fill="#FEF3C7", outline="#F59E0B", width=4)
            draw.text((400, 635), "LƯỢT CỦA BẠN!", font=fonts["title"], fill="#D97706", anchor="mm")
            draw.text((400, 710), "Nói thật vang: BƠ!", font=fonts["h2"], fill="#92400E", anchor="mm")
        elif vis == "game_ow_praise":
            draw.rounded_rectangle([100, 570, 700, 780], radius=20, fill="#ECFDF5", outline="#10B981", width=3)
            trophy_im = ASSETS["trophy"].resize((90, 90))
            frame.paste(trophy_im, (120, 630), trophy_im)
            draw.text((420, 645), "XUẤT SẮC!", font=fonts["title"], fill="#059669", anchor="mm")
            draw.text((420, 715), "Nói từ Bơ rất hay!", font=fonts["h3"], fill="#047857", anchor="mm")
        else:
            draw.text((400, 635), "Hãy nói theo Bé Ơ nhé!", font=fonts["h2"], fill="#334155", anchor="mm")

    # 6. Gameshow Spotlight Quiz
    # 6. Gameshow Spotlight Quiz (5 Questions)
    elif vis.startswith("quiz_q"):
        q_data = QUIZ_DATA.get(vis, {"num": "CÂU HỎI", "title": "Ai đang ĐỘI CHIẾC MŨ?"})
        draw.rounded_rectangle([1180, 80, 1880, 870], radius=28, fill=(255, 255, 255, 245), outline="#3B82F6", width=4)
        draw.text((1530, 135), f"ĐỐ VUI NHANH TRÍ ({q_data['num']})", font=fonts["badge"], fill="#2563EB", anchor="mm")
        draw.text((1530, 195), q_data["title"], font=fonts["quiz_title"], fill="#1E293B", anchor="mm")
        
        draw.rounded_rectangle([1220, 260, 1840, 350], radius=16, fill="#F8FAFC", outline="#CBD5E1", width=2)
        draw.text((1530, 305), "[A] Bé O", font=fonts["quiz_opt"], fill="#334155", anchor="mm")
        
        draw.rounded_rectangle([1220, 370, 1840, 460], radius=16, fill="#F8FAFC", outline="#CBD5E1", width=2)
        draw.text((1530, 415), "[B] Bé Ô", font=fonts["quiz_opt"], fill="#334155", anchor="mm")
        
        draw.rounded_rectangle([1220, 480, 1840, 570], radius=16, fill="#F8FAFC", outline="#CBD5E1", width=2)
        draw.text((1530, 525), "[C] Bé Ơ", font=fonts["quiz_opt"], fill="#334155", anchor="mm")
        
        sec_left = max(1, 3 - int(t_ratio * 3))
        draw.ellipse([1455, 640, 1605, 790], fill="#FEF08A", outline="#EAB308", width=4)
        draw.text((1530, 715), str(sec_left), font=fonts["timer"], fill="#B45309", anchor="mm")

    elif vis.startswith("quiz_a"):
        a_data = QUIZ_DATA.get(vis, {"ans": "ĐÁP ÁN: [B] BÉ Ô", "desc": "Bé Ô đội chiếc mũ nhọn cực xinh!", "asset": "hat"})
        draw.rounded_rectangle([1180, 80, 1880, 870], radius=28, fill=(255, 255, 255, 245), outline="#10B981", width=5)
        draw.text((1530, 150), "CHÍNH XÁC!", font=fonts["title"], fill="#059669", anchor="mm")
        draw.rounded_rectangle([1220, 220, 1840, 350], radius=20, fill="#ECFDF5", outline="#10B981", width=3)
        draw.text((1530, 285), a_data["ans"], font=fonts["title"], fill="#047857", anchor="mm")
        
        item_im = ASSETS[a_data["asset"]].resize((170, 170))
        frame.paste(item_im, (1445, 390), item_im)
        draw.text((1530, 600), a_data["desc"], font=fonts["h2"], fill="#059669", anchor="mm")
        trophy_im = ASSETS["trophy"].resize((120, 120))
        frame.paste(trophy_im, (1470, 670), trophy_im)

    # 7. Rhymes & Grand Finale
    elif vis == "rhyme_1":
        draw.rounded_rectangle([360, 50, 1560, 160], radius=24, fill=(255, 255, 255, 240), outline="#EF4444", width=4)
        draw.text((960, 105), "O tròn như quả trứng gà,", font=fonts["title"], fill="#DC2626", anchor="mm")
        egg_im = ASSETS["egg"].resize((160, 160))
        frame.paste(egg_im, (470, 210), egg_im)

    elif vis == "rhyme_2":
        draw.rounded_rectangle([360, 50, 1560, 160], radius=24, fill=(255, 255, 255, 240), outline="#10B981", width=4)
        draw.text((960, 105), "Ô thì đội mũ,", font=fonts["title"], fill="#059669", anchor="mm")
        hat_im = ASSETS["hat"].resize((160, 160))
        frame.paste(hat_im, (970, 210), hat_im)

    elif vis == "rhyme_3":
        draw.rounded_rectangle([360, 50, 1560, 160], radius=24, fill=(255, 255, 255, 240), outline="#F59E0B", width=4)
        draw.text((960, 105), "Ơ thì thêm râu!", font=fonts["title"], fill="#D97706", anchor="mm")
        hook_im = ASSETS["hook"].resize((160, 160))
        frame.paste(hook_im, (1490, 210), hook_im)

    elif vis == "goodbye":
        conf_im = ASSETS["confetti"]
        frame.paste(conf_im, (100, 60), conf_im)
        frame.paste(conf_im, (1420, 60), conf_im)
        draw.rounded_rectangle([320, 60, 1600, 200], radius=28, fill=(255, 255, 255, 245), outline="#3B82F6", width=4)
        draw.text((960, 110), "TẠM BIỆT VÀ HẸN GẶP LẠI!", font=fonts["title"], fill="#1D4ED8", anchor="mm")
        draw.text((960, 160), "Chúc các bạn học tiếng Việt thật vui!", font=fonts["h2"], fill="#E11D48", anchor="mm")

    # Subtitle Bar
    draw_subtitle_bar(draw, seg["vi"], seg["en"], seg["speaker"], spk_col)
    return frame.convert("RGB")

# Step 5: Render Master Video
print("5. Starting 3D master video rendering...")
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
    "-preset", "slow",
    "-crf", "28",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "96k",
    "-movflags", "+faststart",
    "-shortest",
    FINAL_OUTPUT
]

ffmpeg_log_path = os.path.join(TEMP_DIR, "ffmpeg_render.log")
ffmpeg_log_file = open(ffmpeg_log_path, "w")
proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=ffmpeg_log_file)

total_frames_all = sum(s["frames"] for s in segment_info)
print(f"Total Video Frames to render: {total_frames_all} ({total_frames_all/FPS:.2f}s)")

# Frame Cache for 3D room frames
IMG_CACHE_3D = {}
N_3D = len(FRAME_PATHS_3D)

def get_base_3d_frame(f_idx):
    p_idx = abs(((f_idx) % (2 * N_3D)) - N_3D)
    p_idx = min(p_idx, N_3D - 1)
    target_path = FRAME_PATHS_3D[p_idx]
    if target_path not in IMG_CACHE_3D:
        IMG_CACHE_3D[target_path] = Image.open(target_path).convert("RGBA")
    return IMG_CACHE_3D[target_path]

global_f = 0
last_report = 0

for s_idx, seg in enumerate(segment_info):
    seg_frames = seg["frames"]
    for local_f in range(seg_frames):
        base_3d = get_base_3d_frame(global_f)
        composed = compose_3d_frame(base_3d, seg, local_f, seg_frames)
        proc.stdin.write(composed.tobytes())
        global_f += 1
        
        pct = int(global_f / total_frames_all * 100)
        if pct >= last_report + 5:
            last_report = pct
            print(f"  [Render Progress] {global_f}/{total_frames_all} frames ({pct}%)")

proc.stdin.close()
proc.wait()
ffmpeg_log_file.close()

if proc.returncode != 0:
    with open(ffmpeg_log_path, "r") as f:
        err = f.read()
    print(f"FFmpeg error: {err}")
    sys.exit(1)

print(f"6. 3D Master video rendered successfully -> {FINAL_OUTPUT}")
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
    (2, "c_01_intro_trio.png"),
    (8, "c_02_solo_o.png"),
    (14, "c_03_solo_oe.png"),
    (20, "c_04_solo_ow.png"),
    (32, "c_05_feature_o.png"),
    (45, "c_06_feature_oe.png"),
    (58, "c_07_feature_ow.png"),
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

# Also update poster image
subprocess.run(["cp", os.path.join(stills_dir, "c_01_intro_trio.png"), os.path.join(stills_dir, "c_01_title_intro.png")])
subprocess.run(["cp", os.path.join(stills_dir, "c_01_intro_trio.png"), os.path.join(stills_dir, "c_01_intro_o.png")])
print("Extracted all stills and synchronized poster images!")
