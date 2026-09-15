import os
import subprocess
import time
import math
from PIL import Image
import numpy as np

BASE_DIR = "/home/quang/video_ai"
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
FRAMES_DIR = os.path.join(BASE_DIR, "frames_v3")
TEMP_DIR = os.path.join(BASE_DIR, "v3_temp")
os.makedirs(TEMP_DIR, exist_ok=True)

FINAL_OUTPUT = os.path.join(BASE_DIR, "video_microlearning_D_Đ.mp4")
W, H = 1920, 1080
FPS = 30
TRANSITION_FRAMES = 15 # 0.5s smooth cosine crossfade

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

print("1. Preparing audio clips...")
sil_03 = os.path.join(TEMP_DIR, "sil_03.wav")
sil_05 = os.path.join(TEMP_DIR, "sil_05.wav")
sil_15 = os.path.join(TEMP_DIR, "sil_15.wav")
sil_20 = os.path.join(TEMP_DIR, "sil_20.wav")
make_silence(0.3, sil_03)
make_silence(0.5, sil_05)
make_silence(1.5, sil_15)
make_silence(2.0, sil_20)

def prep_wav(name):
    src = os.path.join(AUDIO_DIR, name)
    dst = os.path.join(TEMP_DIR, name.replace(".mp3", ".wav"))
    to_wav(src, dst)
    return dst

timeline = [
    # Scene 1: Intro
    ("s1_intro.png", [prep_wav("s1_intro.mp3"), sil_05]),
    
    # Scene 2: Letter Đ
    ("s2_de_sub1.png", [prep_wav("s2_de_desc.mp3"), sil_03]),
    ("s2_de_sub2.png", [prep_wav("s2_de_vn.mp3"), sil_05]),
    ("s2_de_sub3.png", [prep_wav("s2_de_recap.mp3"), sil_05]),
    
    # Scene 3: Letter D
    ("s3_d_sub1.png", [prep_wav("s3_d_desc.mp3"), sil_03]),
    ("s3_d_sub2.png", [prep_wav("s3_d_vn.mp3"), sil_05]),
    ("s3_d_sub3.png", [prep_wav("s3_d_recap.mp3"), sil_05]),
    
    # Scene 4: Drill minimal pairs
    ("s4_p0_idle_lis.png", [prep_wav("s4_drill_intro.mp3"), sil_05]),
    
    # Pair 1 (Đi vs Da)
    ("s4_p1_de_lis.png", [prep_wav("s4_pair1_de.mp3"), sil_03]),
    ("s4_p1_de_rep.png", [sil_20]),
    ("s4_p1_d_lis.png", [prep_wav("s4_pair1_d.mp3"), sil_03]),
    ("s4_p1_d_rep.png", [sil_20]),
    
    # Pair 2 (Đỏ vs Dở)
    ("s4_p2_de_lis.png", [prep_wav("s4_pair2_de.mp3"), sil_03]),
    ("s4_p2_de_rep.png", [sil_20]),
    ("s4_p2_d_lis.png", [prep_wav("s4_pair2_d.mp3"), sil_03]),
    ("s4_p2_d_rep.png", [sil_20]),
    
    # Pair 3 (Đo vs Do)
    ("s4_p3_de_lis.png", [prep_wav("s4_pair3_de.mp3"), sil_03]),
    ("s4_p3_de_rep.png", [sil_20]),
    ("s4_p3_d_lis.png", [prep_wav("s4_pair3_d.mp3"), sil_03]),
    ("s4_p3_d_rep.png", [sil_20]),
    
    ("s4_p0_idle_lis.png", [prep_wav("s4_drill_outro.mp3"), sil_05]),
    
    # Scene 5: Quiz
    ("s5_q1_question.png", [prep_wav("s5_quiz_intro.mp3")]),
    ("s5_q1_question.png", [prep_wav("s5_q1_sound.mp3"), sil_03, prep_wav("sfx_tick.wav"), sil_05, prep_wav("sfx_tick.wav"), sil_05, prep_wav("sfx_tick.wav"), sil_05]),
    ("s5_q1_answer.png", [prep_wav("sfx_ding.wav"), prep_wav("s5_q1_ans.mp3"), sil_05]),
    
    ("s5_q2_question.png", [prep_wav("s5_q2_sound.mp3"), sil_03, prep_wav("sfx_tick.wav"), sil_05, prep_wav("sfx_tick.wav"), sil_05, prep_wav("sfx_tick.wav"), sil_05]),
    ("s5_q2_answer.png", [prep_wav("sfx_ding.wav"), prep_wav("s5_q2_ans.mp3"), sil_05]),
    
    # Scene 6: Summary & Outro
    ("s6_summary.png", [prep_wav("s6_outro.mp3"), sil_15])
]

# Calculate durations and construct master audio
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
            # Cosine ease curve (0.0 to 1.0)
            progress = (t + 1) / float(t_frames)
            alpha = 0.5 * (1.0 - math.cos(math.pi * progress))
            blend_arr = (1.0 - alpha) * cur_arr + alpha * next_arr
            pipe.stdin.write(blend_arr.astype(np.uint8).tobytes())
            frames_written += 1

pipe.stdin.close()
pipe.wait()
t1 = time.time()

print(f"Rendered {frames_written} frames in {t1 - t0:.2f}s!")
print(f"VERSION 3.0 MASTERPIECE CREATED: {FINAL_OUTPUT}")
