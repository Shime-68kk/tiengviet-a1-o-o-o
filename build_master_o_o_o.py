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
TRANSITION_FRAMES = 15 # 0.5s smooth cosine ease crossfade

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
    
    # Máy quét
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

# Calculate durations & construct master audio
print("2. Concatenating master audio...")
all_wavs = []
segment_frames = []

for img_name, wav_list in timeline:
    dur = sum(get_dur(w) for w in wav_list)
    frames_count = max(1, int(round(dur * FPS)))
    img_path = os.path.join(FRAMES_DIR, img_name)
    segment_frames.append((img_path, frames_count))
    all_wavs.extend(wav_list)

master_audio_list = os.path.join(TEMP_DIR, "master_audio_list.txt")
with open(master_audio_list, "w") as f:
    for w in all_wavs:
        f.write(f"file '{w}'\n")

master_audio_wav = os.path.join(TEMP_DIR, "master_audio.wav")
cmd = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", master_audio_list,
    "-c:a", "pcm_s16le", master_audio_wav
]
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

total_audio_dur = get_dur(master_audio_wav)
total_target_frames = int(round(total_audio_dur * FPS))
print(f"Master Audio Duration: {total_audio_dur:.2f}s ({total_target_frames} frames @ {FPS} fps)")

# Pre-load all images as RGB numpy arrays
print("3. Pre-loading slide images...")
loaded_images = {}
for img_path, _ in segment_frames:
    if img_path not in loaded_images:
        im = Image.open(img_path).convert("RGB")
        loaded_images[img_path] = np.array(im, dtype=np.float32)

print("4. Rendering video with smooth ease-in-out landing page transitions...")
t0 = time.time()
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo", "-pix_fmt", "rgb24",
    "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
    "-i", master_audio_wav,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "19",
    "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
    "-shortest",
    FINAL_OUTPUT
]

pipe = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

num_segments = len(segment_frames)
frames_written = 0

for idx in range(num_segments):
    cur_img_path, cur_count = segment_frames[idx]
    cur_arr = loaded_images[cur_img_path]
    
    if idx < num_segments - 1:
        next_img_path, _ = segment_frames[idx + 1]
        do_transition = (cur_img_path != next_img_path)
        next_arr = loaded_images[next_img_path] if do_transition else None
    else:
        do_transition = False
        next_arr = None
        
    t_frames = TRANSITION_FRAMES if do_transition else 0
    steady_count = max(1, cur_count - t_frames)
    
    # Steady frames
    cur_bytes = cur_arr.astype(np.uint8).tobytes()
    for _ in range(steady_count):
        pipe.stdin.write(cur_bytes)
        frames_written += 1
        
    # Smooth cosine ease-in-out crossfade
    if do_transition:
        for t in range(t_frames):
            progress = (t + 1) / float(t_frames)
            alpha = 0.5 * (1.0 - math.cos(math.pi * progress))
            blend_arr = (1.0 - alpha) * cur_arr + alpha * next_arr
            pipe.stdin.write(blend_arr.astype(np.uint8).tobytes())
            frames_written += 1

pipe.stdin.close()
pipe.wait()
t1 = time.time()

print(f"Rendered {frames_written} frames in {t1 - t0:.2f}s!")
print(f"SUCCESS: Video generated at: {FINAL_OUTPUT}")
