import os
import subprocess
import time
import math
from PIL import Image
import numpy as np

BASE_DIR = "/home/quang/video_ai"
AUDIO_DIR = os.path.join(BASE_DIR, "audio_o")
SFX_DIR = os.path.join(BASE_DIR, "audio")
FRAMES_DIR = os.path.join(BASE_DIR, "frames_o")
TEMP_DIR = os.path.join(BASE_DIR, "o_temp")
os.makedirs(TEMP_DIR, exist_ok=True)

FINAL_OUTPUT = os.path.join(BASE_DIR, "video_microlearning_O_Ô_Ơ.mp4")
W, H = 1920, 1080
FPS = 30
TRANSITION_FRAMES = 12 # 0.4s smooth cosine ease crossfade

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

print("1. Preparing audio clips for O-Ô-Ơ...")
sil_03 = os.path.join(TEMP_DIR, "sil_03.wav")
sil_05 = os.path.join(TEMP_DIR, "sil_05.wav")
sil_15 = os.path.join(TEMP_DIR, "sil_15.wav")
sil_25 = os.path.join(TEMP_DIR, "sil_25.wav")
make_silence(0.3, sil_03)
make_silence(0.5, sil_05)
make_silence(1.5, sil_15)
make_silence(2.5, sil_25)

def prep_wav(dir_path, name):
    src = os.path.join(dir_path, name)
    dst = os.path.join(TEMP_DIR, name.replace(".mp3", ".wav"))
    to_wav(src, dst)
    return dst

wav_tick = prep_wav(SFX_DIR, "sfx_tick.mp3")
wav_ding = prep_wav(SFX_DIR, "sfx_ding.mp3")

timeline = [
    # 1. Khởi động (Lim)
    ("s1_lim_intro.png", [prep_wav(AUDIO_DIR, "s1_lim_intro.mp3"), sil_05]),
    
    # 2. Phát âm & Cách viết (Nhung)
    # O
    ("s2_nhung_o_1.png", [prep_wav(AUDIO_DIR, "s2_nhung_o_desc.mp3"), sil_03]),
    ("s2_nhung_o_2.png", [prep_wav(AUDIO_DIR, "s2_nhung_o_sound.mp3"), sil_05]),
    
    # Ô
    ("s2_nhung_oe_1.png", [prep_wav(AUDIO_DIR, "s2_nhung_oe_desc.mp3"), sil_03]),
    ("s2_nhung_oe_2.png", [prep_wav(AUDIO_DIR, "s2_nhung_oe_sound.mp3"), sil_05]),
    
    # Ơ
    ("s2_nhung_ow_1.png", [prep_wav(AUDIO_DIR, "s2_nhung_ow_desc.mp3"), sil_03]),
    ("s2_nhung_ow_2.png", [prep_wav(AUDIO_DIR, "s2_nhung_ow_sound.mp3"), sil_05]),
    
    # Máy biến hình
    ("s2_nhung_scanner.png", [prep_wav(AUDIO_DIR, "s2_nhung_scanner.mp3"), sil_05]),
    
    # 3. Luyện tập Thực hành (Ý)
    ("s3_y_idle_lis.png", [prep_wav(AUDIO_DIR, "s3_y_intro.mp3"), sil_05]),
    
    # Drill O (Bò)
    ("s3_y_o_lis.png", [prep_wav(AUDIO_DIR, "s3_y_pair_o.mp3"), sil_03]),
    ("s3_y_o_rep.png", [sil_25]),
    
    # Drill Ô (Cô)
    ("s3_y_oe_lis.png", [prep_wav(AUDIO_DIR, "s3_y_pair_oe.mp3"), sil_03]),
    ("s3_y_oe_rep.png", [sil_25]),
    
    # Drill Ơ (Bơ)
    ("s3_y_ow_lis.png", [prep_wav(AUDIO_DIR, "s3_y_pair_ow.mp3"), sil_03]),
    ("s3_y_ow_rep.png", [sil_25]),
    
    ("s3_y_idle_lis.png", [prep_wav(AUDIO_DIR, "s3_y_outro.mp3"), sil_05]),
    
    # 4. Tổng kết & Củng cố (Thủy)
    ("s4_thuy_quiz_question.png", [prep_wav(AUDIO_DIR, "s4_thuy_quiz_q.mp3"), sil_03]),
    ("s4_thuy_quiz_question.png", [prep_wav(AUDIO_DIR, "s4_thuy_quiz_sound.mp3"), sil_03, wav_tick, sil_05, wav_tick, sil_05, wav_tick, sil_05]),
    ("s4_thuy_quiz_answer.png", [wav_ding, prep_wav(AUDIO_DIR, "s4_thuy_quiz_ans.mp3"), sil_05]),
    
    ("s4_thuy_summary.png", [prep_wav(AUDIO_DIR, "s4_thuy_golden_rule.mp3"), sil_15])
]

# Concatenate slide audio
print("2. Concatenating slide voiceover audio...")
all_wavs = []
segment_frames = []

for img_name, wav_list in timeline:
    dur = sum(get_dur(w) for w in wav_list)
    frames_count = max(1, int(round(dur * FPS)))
    img_path = os.path.join(FRAMES_DIR, img_name)
    segment_frames.append((img_path, frames_count))
    all_wavs.extend(wav_list)

slide_audio_list = os.path.join(TEMP_DIR, "slide_audio_list.txt")
with open(slide_audio_list, "w") as f:
    for w in all_wavs:
        f.write(f"file '{w}'\n")

slide_audio_raw = os.path.join(TEMP_DIR, "slide_voice_raw.wav")
cmd = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", slide_audio_list,
    "-c:a", "pcm_s16le", slide_audio_raw
]
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

slide_voice_dur = get_dur(slide_audio_raw)
print(f"Slide Voice Duration: {slide_voice_dur:.2f}s")

# Mix with cheerful marimba BGM (volume=0.10)
print("3. Mixing cheerful marimba BGM under speech...")
bgm_wav = os.path.join(BASE_DIR, "audio", "bgm_cheerful.wav")
slide_mixed_audio = os.path.join(TEMP_DIR, "slide_mixed_audio.wav")

cmd = [
    "ffmpeg", "-y",
    "-i", slide_audio_raw,
    "-stream_loop", "-1", "-i", bgm_wav,
    "-filter_complex",
    "[1:a]volume=0.10[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[outa]",
    "-map", "[outa]",
    "-c:a", "pcm_s16le",
    "-ar", "44100",
    slide_mixed_audio
]
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

# Pre-load all slide images
print("4. Pre-loading slide images...")
loaded_images = {}
for img_path, _ in segment_frames:
    if img_path not in loaded_images:
        im = Image.open(img_path).convert("RGB")
        loaded_images[img_path] = np.array(im, dtype=np.float32)

slides_raw_video = os.path.join(TEMP_DIR, "slides_raw.mp4")
print("5. Rendering slide video with smooth crossfades...")
t0 = time.time()
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo", "-pix_fmt", "rgb24",
    "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
    "-i", slide_mixed_audio,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "19",
    "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
    "-shortest",
    slides_raw_video
]

proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

def cosine_ease(t):
    return (1.0 - math.cos(t * math.pi)) / 2.0

num_segments = len(segment_frames)
for seg_idx, (cur_img_path, total_seg_f) in enumerate(segment_frames):
    cur_arr = loaded_images[cur_img_path]
    next_arr = None
    if seg_idx + 1 < num_segments:
        next_img_path = segment_frames[seg_idx + 1][0]
        if next_img_path != cur_img_path:
            next_arr = loaded_images[next_img_path]
            
    tf_count = TRANSITION_FRAMES if next_arr is not None else 0
    hold_f = max(0, total_seg_f - tf_count)
    
    cur_bytes = cur_arr.astype(np.uint8).tobytes()
    for _ in range(hold_f):
        proc.stdin.write(cur_bytes)
        
    for f in range(tf_count):
        alpha = cosine_ease((f + 1) / float(tf_count))
        blended = (1.0 - alpha) * cur_arr + alpha * next_arr
        proc.stdin.write(blended.astype(np.uint8).tobytes())

proc.stdin.close()
proc.wait()
print(f"Slide video rendered in {time.time() - t0:.2f}s!")

# Step 6: Concatenate Hook Clip + Slide Video
print("6. Concatenating 3D Hook Clip + Slide Video...")
hook_clip = os.path.join(TEMP_DIR, "hook_1080p.mp4")

concat_file = os.path.join(TEMP_DIR, "master_concat_list.txt")
with open(concat_file, "w") as f:
    f.write(f"file '{hook_clip}'\n")
    f.write(f"file '{slides_raw_video}'\n")

cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", concat_file,
    "-c", "copy",
    FINAL_OUTPUT
]
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

# Also link or copy to video_o_o_o.mp4 and assets/hero.mp4
for dest_name in ["video_o_o_o.mp4", os.path.join("assets", "hero.mp4")]:
    target_path = os.path.join(BASE_DIR, dest_name)
    if os.path.exists(target_path) or os.path.islink(target_path):
        if os.path.realpath(target_path) != os.path.realpath(FINAL_OUTPUT):
            os.remove(target_path)
            os.symlink(FINAL_OUTPUT, target_path)
    else:
        os.symlink(FINAL_OUTPUT, target_path)

final_dur = get_dur(FINAL_OUTPUT)
print(f"=== Master Video Exported Successfully! ===")
print(f"Path: {FINAL_OUTPUT}")
print(f"Total Duration: {final_dur:.2f}s (~{int(final_dur//60)}m {int(final_dur%60)}s)")
