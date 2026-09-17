#!/usr/bin/env python3
"""
Local Automation Pipeline for 15 O-Ô-Ơ Animated Letter Clips
Using Fal.ai (Kling Video Image-to-Video Engine)
"""

import os
import sys
import time
import glob
import json
import argparse
import subprocess
import requests
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
FAL_KEY = os.getenv("FAL_KEY") or os.getenv("VIDEO_API_KEY")
if not FAL_KEY:
    print("❌ LỖI: Chưa tìm thấy FAL_KEY hoặc VIDEO_API_KEY trong file .env!")
    sys.exit(1)

import fal_client

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "raw_clips")
REF_DIR = os.path.join(BASE_DIR, "ref_frames")
RENDERED_DIR = os.path.join(BASE_DIR, "rendered_clips")
FINAL_DIR = os.path.join(BASE_DIR, "final")

for d in [RAW_DIR, REF_DIR, RENDERED_DIR, FINAL_DIR]:
    os.makedirs(d, exist_ok=True)

# 15 Detailed Storyboard Prompts tailored to letter actions and dialogue
SCENE_PROMPTS = [
    {
        "id": 1,
        "name": "clip_01_000s_010s",
        "title": "Mở đầu: Bộ ba O, Ô, Ơ chào mừng",
        "prompt": "High quality 3D Pixar style animation, three cute anthropomorphic letters O (red), Ô (green wearing conical hat), Ơ (orange with tiny hooked whisker) happily jumping and waving hands at camera in colorful kindergarten classroom, joyful welcoming expressions, 1080p, 16:9, cinematic character animation"
    },
    {
        "id": 2,
        "name": "clip_02_010s_020s",
        "title": "Chào hỏi solo: Bé O tròn xoe & quả trứng gà vàng",
        "prompt": "High quality 3D Pixar animation, cute anthropomorphic red letter O character with white cartoon gloves and red sneakers, waving friendly hands and smiling, a shiny golden egg hopping cheerfully beside him, colorful sunlit kindergarten classroom background, 4k cinematic character animation, 16:9"
    },
    {
        "id": 3,
        "name": "clip_03_020s_030s",
        "title": "Chào hỏi solo: Bé Ô chiếc mũ chóp nhọn thần kỳ",
        "prompt": "High quality 3D Pixar animation, cute anthropomorphic green letter Ô character wearing a green pointed conical hat, adjusting his conical hat with white gloved hands, smiling proudly, colorful kindergarten classroom background, warm gentle lighting, 4k cinematic animation, 16:9"
    },
    {
        "id": 4,
        "name": "clip_04_030s_040s",
        "title": "Chào hỏi solo: Bé Ơ chiếc râu móc cong cong",
        "prompt": "High quality 3D Pixar animation, cute anthropomorphic orange letter Ơ character with a playful curved whisker hook on the right, winking and giving a cheerful thumbs up gesture with white gloved hand, sunny kindergarten room background, 4k cinematic animation, 16:9"
    },
    {
        "id": 5,
        "name": "clip_05_040s_050s",
        "title": "Bài học chữ O: Khẩu hình tròn & từ CON BÒ",
        "prompt": "High quality 3D Pixar animation, close up on red letter O character opening mouth in a perfect round shape demonstrating vowel pronunciation /ɔ/, cute cartoon dairy cow standing nearby, bright cheerful preschool classroom, 4k, 16:9"
    },
    {
        "id": 6,
        "name": "clip_06_050s_060s",
        "title": "Củng cố chữ O & chuyển cảnh Bé Ô",
        "prompt": "High quality 3D Pixar animation, red letter O character joyfully dancing and turning, pointing hands enthusiastically toward green letter Ô, colorful kindergarten classroom background, warm sunlight, 4k, 16:9"
    },
    {
        "id": 7,
        "name": "clip_07_060s_070s",
        "title": "Bài học chữ Ô: Khẩu hình chu môi & từ CÔ GIÁO",
        "prompt": "High quality 3D Pixar animation, close up on green letter Ô character puckering lips forward into a small round shape pronouncing /o/, touching his conical hat proudly, cute friendly teacher figure in background, 4k, 16:9"
    },
    {
        "id": 8,
        "name": "clip_08_070s_080s",
        "title": "Bài học chữ Ơ: Khẩu hình dẹt & từ QUẢ BƠ",
        "prompt": "High quality 3D Pixar animation, close up on orange letter Ơ character smiling wide with flat lips pronouncing /ɤ/, pointing to her cute curved whisker hook, fresh sliced cartoon avocado floating, 4k, 16:9"
    },
    {
        "id": 9,
        "name": "clip_09_080s_090s",
        "title": "Cỗ máy biến hình: Mũ bay vào Ô, râu móc bay vào Ơ",
        "prompt": "Cinematic 3D animation, magical transformation in bright kindergarten classroom, a cute pointed conical hat floating down onto letter Ô with sparkling stars, a curved whisker hook swooshing onto letter Ơ, magical fairy lights, 4k, 16:9"
    },
    {
        "id": 10,
        "name": "clip_10_090s_100s",
        "title": "Shadowing tương tác: Nhại giọng chữ O (BÒ)",
        "prompt": "High quality 3D animation, red letter O character holding a colorful toy microphone, cheerfully singing and bouncing, colorful musical notes floating, classroom game stage, 4k, 16:9"
    },
    {
        "id": 11,
        "name": "clip_11_100s_110s",
        "title": "Shadowing tương tác: Nhại giọng chữ Ô (CÔ) & Cúp vàng",
        "prompt": "High quality 3D animation, green letter Ô character holding a toy microphone, bouncing happily with a shiny golden championship trophy sparkling on a podium beside him, confetti stars, 4k, 16:9"
    },
    {
        "id": 12,
        "name": "clip_12_110s_120s",
        "title": "Shadowing tương tác: Nhại giọng chữ Ơ (BƠ)",
        "prompt": "High quality 3D animation, orange letter Ơ character holding a toy microphone, winking and clapping white-gloved hands joyfully, celebration stars and victory cheering atmosphere, 4k, 16:9"
    },
    {
        "id": 13,
        "name": "clip_13_120s_130s",
        "title": "Trắc nghiệm phản xạ 3 giây: Đèn Spotlight Bé Ô",
        "prompt": "Dramatic 3D animated game show scene in preschool classroom, room lights dim softly, a bright warm golden spotlight suddenly beams down onto green letter Ô, celebratory burst of sparkles, 4k, 16:9"
    },
    {
        "id": 14,
        "name": "clip_14_130s_140s",
        "title": "Đồng dao dân gian: O tròn như trứng gà, Ô đội mũ...",
        "prompt": "High quality 3D Pixar animation, three cute anthropomorphic letters O (red), Ô (green with conical hat), Ơ (orange with whisker hook) dancing in sync, golden egg, hat, and hook floating above them, sunny classroom, 4k, 16:9"
    },
    {
        "id": 15,
        "name": "clip_15_140s_143s",
        "title": "Kết bài: Ơ thêm râu, pháo hoa giấy & vẫy tay chào",
        "prompt": "Grand finale 3D Pixar animation, colorful confetti and paper streamers raining down, three cute letters O, Ô, Ơ happily jumping and waving both hands at camera saying goodbye, big warm smiles, 4k, 16:9"
    }
]

def render_clip(scene_idx, model="fal-ai/kling-video/v1/standard/image-to-video", duration="5", max_retries=3):
    """Render a single clip using Fal.ai Image-to-Video API with retry mechanism."""
    scene = SCENE_PROMPTS[scene_idx - 1]
    name = scene["name"]
    title = scene["title"]
    prompt = scene["prompt"]
    
    final_out = os.path.join(RENDERED_DIR, f"{name}_rendered.mp4")
    if os.path.exists(final_out) and os.path.getsize(final_out) > 500000:
        print(f"⏩ [Scene {scene_idx}/15] {name}_rendered.mp4 đã tồn tại sẵn ({os.path.getsize(final_out)/(1024*1024):.2f} MB). Bỏ qua để tiết kiệm API credits!")
        return final_out
    
    ref_img_path = os.path.join(REF_DIR, f"{name}_ref1.png")
    if not os.path.exists(ref_img_path):
        ref_img_path = os.path.join(BASE_DIR, "assets", "scene_01_pixar.png")
    
    print(f"\n=======================================================")
    print(f"🚀 [Scene {scene_idx}/15] Bắt đầu render AI: {name}")
    print(f"📌 Tiêu đề: {title}")
    print(f"🖼️ Ảnh tham chiếu: {os.path.basename(ref_img_path)}")
    print(f"📝 Prompt: {prompt[:80]}...")
    print(f"🤖 Model: {model}")
    print(f"=======================================================")

    # 1. Upload reference image to Fal CDN
    print("📤 Đang tải ảnh tham chiếu lên Fal CDN...")
    image_url = fal_client.upload_file(ref_img_path)
    print(f"✅ URL ảnh: {image_url}")

    # 2. Call API with retry
    video_url = None
    for attempt in range(1, max_retries + 1):
        try:
            print(f"⏳ Gửi yêu cầu sinh video tới Fal.ai (Lần thử {attempt}/{max_retries})...")
            handler = fal_client.submit(
                model,
                arguments={
                    "prompt": prompt,
                    "image_url": image_url,
                    "duration": duration,
                    "aspect_ratio": "16:9"
                }
            )
            print(f"📨 Job ID: {handler.request_id}. Đang chờ AI sinh chuyển động video...")
            
            # Polling status
            while True:
                st = fal_client.status(model, handler.request_id, with_logs=False)
                st_name = type(st).__name__
                if st_name == "Completed":
                    break
                elif st_name in ["Failed", "Error"]:
                    raise RuntimeError(f"Fal job thất bại: {st}")
                time.sleep(6)
                print(".", end="", flush=True)
            print(" ✅ Xong!")

            res = fal_client.result(model, handler.request_id)
            video_url = res.get("video", {}).get("url")
            if video_url:
                break
        except Exception as err:
            print(f"\n⚠️ Lỗi ở lần thử {attempt}: {err}")
            if attempt < max_retries:
                print("Đang nghỉ 10 giây trước khi thử lại...")
                time.sleep(10)
            else:
                raise err

    # 3. Download rendered video
    raw_out = os.path.join(RENDERED_DIR, f"{name}_ai_raw.mp4")
    print(f"📥 Đang tải video AI từ {video_url} về {raw_out}...")
    resp = requests.get(video_url)
    with open(raw_out, "wb") as f:
        f.write(resp.content)
    print(f"✅ Đã lưu video thô: {os.path.getsize(raw_out)/(1024*1024):.2f} MB")

    # 4. Merge original speech/audio from raw clip
    audio_source = os.path.join(RAW_DIR, f"{name}.mp4")
    
    if os.path.exists(audio_source):
        print("🔊 Đang ghép âm thanh gốc đồng bộ vào clip...")
        cmd_merge = [
            "ffmpeg", "-y",
            "-i", raw_out,
            "-i", audio_source,
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            final_out
        ]
        subprocess.run(cmd_merge, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"🎉 Hoàn thành Clip {scene_idx}: {final_out} (Đã ghép âm thanh chuẩn)")
    else:
        final_out = raw_out
        print(f"🎉 Hoàn thành Clip {scene_idx}: {final_out}")

    # Chụp ảnh tĩnh kiểm định chất lượng (Inspect Still)
    inspect_img = os.path.join(RENDERED_DIR, f"{name}_inspect.png")
    try:
        subprocess.run(["ffmpeg", "-y", "-ss", "00:00:02", "-i", final_out, "-vframes", "1", "-q:v", "2", inspect_img], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"📸 Đã trích xuất ảnh kiểm định: {inspect_img}")
    except Exception as e:
        print(f"⚠️ Không thể trích xuất ảnh kiểm định: {e}")

    return final_out

def concat_all():
    """Stitch all 15 clips into the final 2m23s master video."""
    print("\n🎞️ Bắt đầu ghép nối 15 clip thành Master Video hoàn chỉnh...")
    
    # Check all clips
    clip_files = []
    for s in SCENE_PROMPTS:
        c_path = os.path.join(RENDERED_DIR, f"{s['name']}_rendered.mp4")
        if not os.path.exists(c_path):
            # Fallback to raw clip if rendered clip is missing
            c_path = os.path.join(RAW_DIR, f"{s['name']}.mp4")
        clip_files.append(c_path)

    concat_list_file = os.path.join(FINAL_DIR, "concat_list.txt")
    with open(concat_list_file, "w") as f:
        for c in clip_files:
            f.write(f"file '{c}'\n")

    output_master = os.path.join(FINAL_DIR, "master_video_o_o_o_2m23s.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_file,
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "24",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        output_master
    ]
    subprocess.run(cmd, check=True)
    
    dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", output_master
    ]).decode().strip())
    size_mb = os.path.getsize(output_master) / (1024 * 1024)
    print(f"\n🏆 XUẤT MASTER VIDEO THÀNH CÔNG -> {output_master}")
    print(f"📊 Thời lượng: {dur:.2f}s | Dung lượng: {size_mb:.2f} MB")
    
    # Update root master video symlinks
    root_master = os.path.join(BASE_DIR, "video_microlearning_O_Ô_Ơ.mp4")
    subprocess.run(["cp", "-f", output_master, root_master], check=True)
    sym1 = os.path.join(BASE_DIR, "video_o_o_o.mp4")
    sym2 = os.path.join(BASE_DIR, "assets", "hero.mp4")
    for s in [sym1, sym2]:
        if os.path.islink(s) or os.path.exists(s):
            os.remove(s)
        os.symlink("video_microlearning_O_Ô_Ơ.mp4", s)
    print("✅ Đã đồng bộ Master Video vào Web Player!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline Video AI O-Ô-Ơ")
    parser.add_argument("--test-clip", type=int, default=0, help="Chỉ render 1 clip thử nghiệm")
    parser.add_argument("--all", action="store_true", help="Chạy render tuần tự toàn bộ 15 clip")
    parser.add_argument("--concat", action="store_true", help="Ghép nối các clip đã render thành master video")
    parser.add_argument("--model", type=str, default="fal-ai/kling-video/v1/standard/image-to-video", help="Model Fal.ai")
    parser.add_argument("--duration", type=str, default="5", help="Thời lượng (5 hoặc 10)")
    args = parser.parse_args()

    if args.test_clip > 0:
        render_clip(args.test_clip, model=args.model, duration=args.duration)
    elif args.concat:
        concat_all()
    elif args.all:
        for idx in range(1, 16):
            render_clip(idx, model=args.model, duration=args.duration)
        concat_all()
    else:
        parser.print_help()
