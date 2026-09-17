import os
import subprocess
import math
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = "/home/quang/video_ai"
IMG_PATH = os.path.join(BASE_DIR, "assets", "scene_01_pixar.png")
AUDIO_SPEECH = os.path.join(BASE_DIR, "audio_3_chars", "c_trio_intro.mp3")
AUDIO_BGM = os.path.join(BASE_DIR, "audio", "bgm_cheerful.wav")
OUTPUT_CLIP = os.path.join(BASE_DIR, "scene_01_pixar_clip.mp4")
TEMP_AUDIO = os.path.join(BASE_DIR, "scene_01_audio.wav")

W, H = 1920, 1080
FPS = 30

dur = float(subprocess.check_output([
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", AUDIO_SPEECH
]).strip()) + 0.3
total_frames = int(dur * FPS)

# Mix audio: speech + BGM
cmd_audio = [
    "ffmpeg", "-y",
    "-i", AUDIO_SPEECH,
    "-stream_loop", "-1", "-i", AUDIO_BGM,
    "-filter_complex",
    f"[0:a]volume=1.0,aresample=44100[speech];[1:a]volume=0.12,aresample=44100[bgm];[speech][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout];[aout]afade=t=out:st={dur-0.5:.2f}:d=0.5[afinal]",
    "-map", "[afinal]",
    "-t", f"{dur:.2f}",
    "-c:a", "pcm_s16le",
    "-ar", "44100",
    "-ac", "2",
    TEMP_AUDIO
]
subprocess.run(cmd_audio, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

base_img = Image.open(IMG_PATH).convert("RGBA")
base_1080 = base_img.resize((W, H), Image.Resampling.LANCZOS)

FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
font_title = ImageFont.truetype(FONT_BOLD, 36)
font_sub_vi = ImageFont.truetype(FONT_BOLD, 32)
font_sub_en = ImageFont.truetype(FONT_REG, 24)

log_f = open(os.path.join(BASE_DIR, "ffmpeg_scene1.log"), "w")
cmd_video = [
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{W}x{H}",
    "-pix_fmt", "rgb24",
    "-r", str(FPS),
    "-i", "-",
    "-i", TEMP_AUDIO,
    "-c:v", "libx264",
    "-preset", "medium",
    "-crf", "22",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-movflags", "+faststart",
    "-shortest",
    OUTPUT_CLIP
]

proc = subprocess.Popen(cmd_video, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=log_f)

for f in range(total_frames):
    t = f / FPS
    progress = f / total_frames
    zoom = 1.0 + 0.05 * (1 - math.cos(progress * math.pi)) / 2.0
    cw = int(W / zoom)
    ch = int(H / zoom)
    bob_y = int(math.sin(t * 3.5) * 5)
    cx = (W - cw) // 2
    cy = max(0, min(H - ch, (H - ch) // 2 + bob_y))
    cropped = base_1080.crop((cx, cy, cx + cw, cy + ch))
    frame = cropped.resize((W, H), Image.Resampling.BILINEAR)
    
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Header Banner
    top_w, top_h = 760, 64
    top_x = (W - top_w) // 2
    top_y = 36
    draw.rounded_rectangle([top_x, top_y, top_x + top_w, top_y + top_h], radius=32, fill=(15, 23, 42, 210), outline=(255, 255, 255, 180), width=2)
    title_text = "✨ BỘ BA BẠN THÂN O — Ô — Ơ ✨"
    tb = draw.textbbox((0, 0), title_text, font=font_title)
    draw.text((top_x + (top_w - (tb[2] - tb[0])) // 2, top_y + 12), title_text, fill=(255, 225, 100), font=font_title)
    
    # Subtitle Bar
    sub_w, sub_h = 1560, 110
    sub_x = (W - sub_w) // 2
    sub_y = H - sub_h - 40
    draw.rounded_rectangle([sub_x, sub_y, sub_x + sub_w, sub_y + sub_h], radius=24, fill=(15, 23, 42, 225), outline=(59, 130, 246, 180), width=2)
    
    tag_text = "Bộ Ba O - Ô - Ơ"
    draw.rounded_rectangle([sub_x + 24, sub_y + 24, sub_x + 220, sub_y + 86], radius=16, fill=(59, 130, 246, 255))
    draw.text((sub_x + 36, sub_y + 36), tag_text, fill=(255, 255, 255), font=ImageFont.truetype(FONT_BOLD, 22))
    
    vi_text = "Chào mừng các bạn nhỏ! Chúng tớ là bộ ba bạn thân O, Ô, Ơ!"
    en_text = "Welcome friends! We are best friends O, Ô, Ơ!"
    draw.text((sub_x + 240, sub_y + 24), vi_text, fill=(255, 255, 255), font=font_sub_vi)
    draw.text((sub_x + 240, sub_y + 68), en_text, fill=(147, 197, 253), font=font_sub_en)
    
    final_frame = Image.alpha_composite(frame, overlay).convert("RGB")
    try:
        proc.stdin.write(final_frame.tobytes())
    except BrokenPipeError:
        break

proc.stdin.close()
proc.wait()
log_f.close()
print(f"Scene 1 rendered cleanly -> {OUTPUT_CLIP}")
