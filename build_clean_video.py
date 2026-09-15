import os
import subprocess

BASE_DIR = "/home/quang/video_ai"
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
FRAMES_DIR = os.path.join(BASE_DIR, "frames")
TEMP_DIR = os.path.join(BASE_DIR, "clean_temp")
os.makedirs(TEMP_DIR, exist_ok=True)

FINAL_OUTPUT = os.path.join(BASE_DIR, "video_microlearning_D_Đ.mp4")

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

# Convert all mp3/wav to uniform wav first
def to_wav(src_path, out_wav):
    cmd = [
        "ffmpeg", "-y", "-i", src_path,
        "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le", out_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

print("Preparing uniform WAV audio clips...")
# Pre-make silences
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

# Build sequence of (frame_image, list_of_wavs)
timeline = []

# 1. Scene 1: Intro
wav_s1 = prep_wav("s1_intro.mp3")
timeline.append((os.path.join(FRAMES_DIR, "s1_intro.png"), [wav_s1, sil_05]))

# 2. Scene 2: Letter Đ
wav_s2_desc = prep_wav("s2_de_desc.mp3")
wav_s2_vn = prep_wav("s2_de_vn.mp3")
wav_s2_recap = prep_wav("s2_de_recap.mp3")
timeline.append((os.path.join(FRAMES_DIR, "s2_de.png"), [wav_s2_desc, sil_03, wav_s2_vn, sil_05, wav_s2_recap, sil_05]))

# 3. Scene 3: Letter D
wav_s3_desc = prep_wav("s3_d_desc.mp3")
wav_s3_vn = prep_wav("s3_d_vn.mp3")
wav_s3_recap = prep_wav("s3_d_recap.mp3")
timeline.append((os.path.join(FRAMES_DIR, "s3_d.png"), [wav_s3_desc, sil_03, wav_s3_vn, sil_05, wav_s3_recap, sil_05]))

# 4. Scene 4: Drill minimal pairs
wav_s4_intro = prep_wav("s4_drill_intro.mp3")
timeline.append((os.path.join(FRAMES_DIR, "s4_drill_p0_listen.png"), [wav_s4_intro, sil_05]))

# Pair 1: Đi vs Da
wav_p1_de = prep_wav("s4_pair1_de.mp3")
timeline.append((os.path.join(FRAMES_DIR, "s4_drill_p1_listen.png"), [wav_p1_de, sil_03]))
timeline.append((os.path.join(FRAMES_DIR, "s4_drill_p1_rep.png"), [sil_20]))

wav_p1_d = prep_wav("s4_pair1_d.mp3")
timeline.append((os.path.join(FRAMES_DIR, "s4_drill_p1_listen.png"), [wav_p1_d, sil_03]))
timeline.append((os.path.join(FRAMES_DIR, "s4_drill_p1_rep.png"), [sil_20]))

# Pair 2: Đỏ vs Dở
wav_p2_de = prep_wav("s4_pair2_de.mp3")
timeline.append((os.path.join(FRAMES_DIR, "s4_drill_p2_listen.png"), [wav_p2_de, sil_03]))
timeline.append((os.path.join(FRAMES_DIR, "s4_drill_p2_rep.png"), [sil_20]))

wav_p2_d = prep_wav("s4_pair2_d.mp3")
timeline.append((os.path.join(FRAMES_DIR, "s4_drill_p2_listen.png"), [wav_p2_d, sil_03]))
timeline.append((os.path.join(FRAMES_DIR, "s4_drill_p2_rep.png"), [sil_20]))

# Pair 3: Đo vs Do
wav_p3_de = prep_wav("s4_pair3_de.mp3")
timeline.append((os.path.join(FRAMES_DIR, "s4_drill_p3_listen.png"), [wav_p3_de, sil_03]))
timeline.append((os.path.join(FRAMES_DIR, "s4_drill_p3_rep.png"), [sil_20]))

wav_p3_d = prep_wav("s4_pair3_d.mp3")
timeline.append((os.path.join(FRAMES_DIR, "s4_drill_p3_listen.png"), [wav_p3_d, sil_03]))
timeline.append((os.path.join(FRAMES_DIR, "s4_drill_p3_rep.png"), [sil_20]))

wav_s4_outro = prep_wav("s4_drill_outro.mp3")
timeline.append((os.path.join(FRAMES_DIR, "s4_drill_p0_listen.png"), [wav_s4_outro, sil_05]))

# 5. Scene 5: Mini Quiz
wav_s5_intro = prep_wav("s5_quiz_intro.mp3")
timeline.append((os.path.join(FRAMES_DIR, "s5_q1_question.png"), [wav_s5_intro]))

# Q1 question
wav_q1_sound = prep_wav("s5_q1_sound.mp3")
wav_tick = prep_wav("sfx_tick.wav")
timeline.append((os.path.join(FRAMES_DIR, "s5_q1_question.png"), [wav_q1_sound, sil_03, wav_tick, sil_05, wav_tick, sil_05, wav_tick, sil_05]))

# Q1 answer
wav_ding = prep_wav("sfx_ding.wav")
wav_q1_ans = prep_wav("s5_q1_ans.mp3")
timeline.append((os.path.join(FRAMES_DIR, "s5_q1_answer.png"), [wav_ding, wav_q1_ans, sil_05]))

# Q2 question
wav_q2_sound = prep_wav("s5_q2_sound.mp3")
timeline.append((os.path.join(FRAMES_DIR, "s5_q2_question.png"), [wav_q2_sound, sil_03, wav_tick, sil_05, wav_tick, sil_05, wav_tick, sil_05]))

# Q2 answer
wav_q2_ans = prep_wav("s5_q2_ans.mp3")
timeline.append((os.path.join(FRAMES_DIR, "s5_q2_answer.png"), [wav_ding, wav_q2_ans, sil_05]))

# 6. Scene 6: Summary & Outro
wav_s6 = prep_wav("s6_outro.mp3")
timeline.append((os.path.join(FRAMES_DIR, "s6_summary.png"), [wav_s6, sil_15]))

print(f"Timeline constructed with {len(timeline)} segments.")

# Now concatenate all audio into one master audio track and compute exact slide durations
all_audio_wavs = []
slide_durations = []

for frame_img, wav_list in timeline:
    seg_dur = sum(get_dur(w) for w in wav_list)
    slide_durations.append((frame_img, seg_dur))
    all_audio_wavs.extend(wav_list)

master_audio_list = os.path.join(TEMP_DIR, "master_audio.txt")
with open(master_audio_list, "w") as f:
    for w in all_audio_wavs:
        f.write(f"file '{w}'\n")

master_audio_wav = os.path.join(TEMP_DIR, "master_audio.wav")
cmd = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", master_audio_list,
    "-c:a", "pcm_s16le", master_audio_wav
]
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

total_audio_dur = get_dur(master_audio_wav)
print(f"Master Audio Track generated! Exact Duration: {total_audio_dur:.2f}s ({total_audio_dur/60:.2f} mins)")

# Write ffconcat file for video
slides_concat = os.path.join(TEMP_DIR, "slides.txt")
with open(slides_concat, "w") as f:
    f.write("ffconcat version 1.0\n")
    for img, dur in slide_durations:
        f.write(f"file '{img}'\n")
        f.write(f"duration {dur:.3f}\n")
    # Last image must be repeated per ffconcat spec
    last_img, _ = slide_durations[-1]
    f.write(f"file '{last_img}'\n")

print("Rendering master video with synchronized audio and video streams...")
cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", slides_concat,
    "-i", master_audio_wav,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
    "-shortest",
    FINAL_OUTPUT
]
subprocess.run(cmd, check=True)
print(f"SUCCESS: Generated {FINAL_OUTPUT}")
