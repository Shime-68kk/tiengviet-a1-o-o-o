import os
import subprocess

AUDIO_DIR = "/home/quang/video_ai/audio"
total_sec = 0.0

for f in sorted(os.listdir(AUDIO_DIR)):
    if f.endswith(".mp3"):
        path = os.path.join(AUDIO_DIR, f)
        res = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", path
        ], capture_output=True, text=True)
        dur = float(res.stdout.strip())
        total_sec += dur
        print(f"{f:20s}: {dur:5.2f}s")

print("-" * 30)
print(f"Total pure speech duration: {total_sec:.2f} seconds ({total_sec/60:.2f} mins)")
