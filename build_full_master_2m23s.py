#!/usr/bin/env python3
import os
import subprocess

BASE_DIR = "/home/quang/video_ai"
RAW_DIR = os.path.join(BASE_DIR, "raw_clips")
RENDERED_DIR = os.path.join(BASE_DIR, "rendered_clips")
FINAL_DIR = os.path.join(BASE_DIR, "final")
EXTENDED_DIR = os.path.join(RENDERED_DIR, "extended_full")
os.makedirs(EXTENDED_DIR, exist_ok=True)
os.makedirs(FINAL_DIR, exist_ok=True)

SCENE_NAMES = [
    "clip_01_000s_010s",
    "clip_02_010s_020s",
    "clip_03_020s_030s",
    "clip_04_030s_040s",
    "clip_05_040s_050s",
    "clip_06_050s_060s",
    "clip_07_060s_070s",
    "clip_08_070s_080s",
    "clip_09_080s_090s",
    "clip_10_090s_100s",
    "clip_11_100s_110s",
    "clip_12_110s_120s",
    "clip_13_120s_130s",
    "clip_14_130s_140s",
    "clip_15_140s_143s"
]

def get_dur(fpath):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", fpath
    ]
    return float(subprocess.check_output(cmd).decode().strip())

print("Step 1: Processing each clip to match full audio duration...")
full_clips = []
for idx, name in enumerate(SCENE_NAMES, 1):
    raw_ai = os.path.join(RENDERED_DIR, f"{name}_ai_raw.mp4")
    if not os.path.exists(raw_ai):
        raw_ai = os.path.join(RENDERED_DIR, f"{name}_rendered.mp4")
    
    audio_source = os.path.join(RAW_DIR, f"{name}.mp4")
    target_dur = get_dur(audio_source)
    
    out_clip = os.path.join(EXTENDED_DIR, f"{name}_full.mp4")
    print(f"[{idx}/15] {name}: Target duration = {target_dur:.3f}s")
    
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", raw_ai,
        "-i", audio_source,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "25",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "128k",
        "-t", f"{target_dur:.3f}",
        out_clip
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    full_clips.append(out_clip)

print("\nStep 2: Concatenating all 15 clips into master 2m23s video...")
concat_txt = os.path.join(FINAL_DIR, "concat_full_list.txt")
with open(concat_txt, "w") as f:
    for c in full_clips:
        f.write(f"file '{c}'\n")

final_master = os.path.join(FINAL_DIR, "master_video_o_o_o_2m23s.mp4")
cmd_concat = [
    "ffmpeg", "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", concat_txt,
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "26",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "128k",
    "-movflags", "+faststart",
    final_master
]
subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

total_dur = get_dur(final_master)
size_mb = os.path.getsize(final_master) / (1024 * 1024)
print(f"🏆 SUCCESS: Final Master Video created at {final_master}")
print(f"⏱️ Total duration: {total_dur:.2f}s ({total_dur/60:.2f} min)")
print(f"💾 File size: {size_mb:.2f} MB")

root_master = os.path.join(BASE_DIR, "video_microlearning_O_Ô_Ơ.mp4")
subprocess.run(["cp", "-f", final_master, root_master], check=True)

sym1 = os.path.join(BASE_DIR, "video_o_o_o.mp4")
sym2 = os.path.join(BASE_DIR, "assets", "hero.mp4")
for s in [sym1, sym2]:
    if os.path.islink(s) or os.path.exists(s):
        os.remove(s)
    os.symlink("video_microlearning_O_Ô_Ơ.mp4", s)

print("✅ Master video successfully synchronized with web player!")
