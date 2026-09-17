import os
import subprocess
import math

BASE_DIR = "/home/quang/video_ai"
INPUT_VIDEO = os.path.join(BASE_DIR, "video_microlearning_O_Ô_Ơ.mp4")
OUTPUT_DIR = os.path.join(BASE_DIR, "clips_10s")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Get total duration
probe_out = subprocess.check_output([
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", INPUT_VIDEO
]).decode().strip()
total_dur = float(probe_out)
print(f"Input video duration: {total_dur:.2f}s ({total_dur/60:.2f} mins)")

CLIP_LEN = 10.0
num_clips = math.ceil(total_dur / CLIP_LEN)
print(f"Total 10s clips to create: {num_clips}\n")

# Storyboard scene references for quick user identification
SCENE_HINTS = [
    "00:00 - 00:10 | Mở đầu: Bộ ba O, Ô, Ơ nhún nhảy vẫy tay chào mừng",
    "00:10 - 00:20 | Chào hỏi solo: Bé O tròn xoe & quả trứng gà vàng",
    "00:20 - 00:30 | Chào hỏi solo: Bé Ô chiếc mũ chóp nhọn thần kỳ",
    "00:30 - 00:40 | Chào hỏi solo: Bé Ơ chiếc râu móc cong cong",
    "00:40 - 00:50 | Bài học chữ O: Phát âm /ɔ/, khẩu hình tròn & từ CON BÒ",
    "00:50 - 01:00 | Bài học chữ O tiếp theo & chuyển cảnh Bé Ô",
    "01:00 - 01:10 | Bài học chữ Ô: Phát âm /o/, chu môi nhọn & từ CÔ GIÁO",
    "01:10 - 01:20 | Bài học chữ Ơ: Phát âm /ɤ/, mép dẹt & từ QUẢ BƠ",
    "01:20 - 01:30 | Cỗ máy biến hình: Mũ chóp bay xuống Ô, râu móc bay vào Ơ",
    "01:30 - 01:40 | Luyện tập tương tác (Shadowing): Nhại giọng bé O (BÒ)",
    "01:40 - 01:50 | Luyện tập tương tác (Shadowing): Nhại giọng bé Ô (CÔ) & cúp vàng",
    "01:50 - 02:00 | Luyện tập tương tác (Shadowing): Nhại giọng bé Ơ (BƠ)",
    "02:00 - 02:10 | Trắc nghiệm phản xạ 3 giây: Đèn rọi Spotlight Bé Ô",
    "02:10 - 02:20 | Đồng dao kinh điển: O tròn như quả trứng gà, Ô đội mũ...",
    "02:20 - 02:23.5 | Kết bài: Ơ thêm râu, pháo hoa giấy chúc mừng & vẫy tay chào"
]

clips_meta = []

for i in range(num_clips):
    start = i * CLIP_LEN
    end = min((i + 1) * CLIP_LEN, total_dur)
    clip_dur = end - start
    
    out_filename = f"clip_{i+1:02d}_{int(start):03d}s_{int(end):03d}s.mp4"
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    
    # Accurate fast cutting
    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{start:.3f}",
        "-t", f"{clip_dur:.3f}",
        "-i", INPUT_VIDEO,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        out_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    hint = SCENE_HINTS[i] if i < len(SCENE_HINTS) else "Đoạn video"
    clips_meta.append((out_filename, start, end, clip_dur, size_mb, hint))
    print(f"[{i+1:02d}/{num_clips}] {out_filename} ({clip_dur:.2f}s, {size_mb:.2f} MB) -> {hint}")

# Write a README summary in clips_10s
with open(os.path.join(OUTPUT_DIR, "README_CLIPS.txt"), "w", encoding="utf-8") as f:
    f.write("=== DANH SÁCH CÁC CLIP 10 GIÂY CẮT TỪ VIDEO 2P23S GỐC ===\n\n")
    for name, s, e, d, sz, hint in clips_meta:
        f.write(f"- {name}: {s:.1f}s -> {e:.1f}s ({d:.1f}s, {sz:.2f} MB)\n  Nội dung: {hint}\n\n")

print("\nHoàn tất cắt toàn bộ video thành các clip 10 giây!")
