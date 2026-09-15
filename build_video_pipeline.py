import os
import subprocess

BASE_DIR = "/home/quang/video_ai"
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
FRAMES_DIR = os.path.join(BASE_DIR, "frames")
TEMP_DIR = os.path.join(BASE_DIR, "temp_segments")
os.makedirs(TEMP_DIR, exist_ok=True)

FINAL_OUTPUT = os.path.join(BASE_DIR, "video_microlearning_D_Đ.mp4")

def get_audio_duration(path):
    res = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path
    ], capture_output=True, text=True)
    return float(res.stdout.strip())

def make_silence(duration, out_path):
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-t", f"{duration:.3f}", "-c:a", "libmp3lame", "-q:a", "2", out_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def concat_audio_files(file_list, out_path):
    # Using ffmpeg concat filter to re-encode all segments consistently
    inputs = []
    filter_complex = []
    for idx, f in enumerate(file_list):
        inputs.extend(["-i", f])
        filter_complex.append(f"[{idx}:a]")
    
    filter_complex_str = "".join(filter_complex) + f"concat=n={len(file_list)}:v=0:a=1[aout]"
    
    cmd = [
        "ffmpeg", "-y", *inputs,
        "-filter_complex", filter_complex_str,
        "-map", "[aout]",
        "-c:a", "libmp3lame", "-q:a", "2",
        out_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def create_video_segment(image_path, audio_path, out_mp4):
    dur = get_audio_duration(audio_path)
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", image_path,
        "-i", audio_path,
        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{dur:.3f}",
        "-r", "30",
        "-shortest",
        out_mp4
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"Created segment: {os.path.basename(out_mp4)} ({dur:.2f}s)")

def build_all():
    print("Preparing audio & video segments...")
    silence_05 = os.path.join(TEMP_DIR, "silence_05.mp3")
    silence_03 = os.path.join(TEMP_DIR, "silence_03.mp3")
    silence_15 = os.path.join(TEMP_DIR, "silence_15.mp3")
    silence_20 = os.path.join(TEMP_DIR, "silence_20.mp3")
    make_silence(0.5, silence_05)
    make_silence(0.3, silence_03)
    make_silence(1.5, silence_15)
    make_silence(2.0, silence_20)
    
    segments = []
    
    # 1. Scene 1: Intro
    a_s1 = os.path.join(TEMP_DIR, "a_s1.mp3")
    concat_audio_files([os.path.join(AUDIO_DIR, "s1_intro.mp3"), silence_05], a_s1)
    v_s1 = os.path.join(TEMP_DIR, "v_01_intro.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s1_intro.png"), a_s1, v_s1)
    segments.append(v_s1)
    
    # 2. Scene 2: Letter Đ
    a_s2 = os.path.join(TEMP_DIR, "a_s2.mp3")
    concat_audio_files([
        os.path.join(AUDIO_DIR, "s2_de_desc.mp3"),
        silence_03,
        os.path.join(AUDIO_DIR, "s2_de_vn.mp3"),
        silence_05,
        os.path.join(AUDIO_DIR, "s2_de_recap.mp3"),
        silence_05
    ], a_s2)
    v_s2 = os.path.join(TEMP_DIR, "v_02_de.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s2_de.png"), a_s2, v_s2)
    segments.append(v_s2)
    
    # 3. Scene 3: Letter D
    a_s3 = os.path.join(TEMP_DIR, "a_s3.mp3")
    concat_audio_files([
        os.path.join(AUDIO_DIR, "s3_d_desc.mp3"),
        silence_03,
        os.path.join(AUDIO_DIR, "s3_d_vn.mp3"),
        silence_05,
        os.path.join(AUDIO_DIR, "s3_d_recap.mp3"),
        silence_05
    ], a_s3)
    v_s3 = os.path.join(TEMP_DIR, "v_03_d.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s3_d.png"), a_s3, v_s3)
    segments.append(v_s3)
    
    # 4. Scene 4: Drill minimal pairs
    # 4.0: Drill intro
    a_s4_intro = os.path.join(TEMP_DIR, "a_s4_intro.mp3")
    concat_audio_files([os.path.join(AUDIO_DIR, "s4_drill_intro.mp3"), silence_05], a_s4_intro)
    v_s4_intro = os.path.join(TEMP_DIR, "v_04_drill_intro.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s4_drill_p0_listen.png"), a_s4_intro, v_s4_intro)
    segments.append(v_s4_intro)
    
    # 4.1: Pair 1: Đi vs Da
    a_p1_1 = os.path.join(TEMP_DIR, "a_p1_1.mp3")
    concat_audio_files([os.path.join(AUDIO_DIR, "s4_pair1_de.mp3"), silence_03], a_p1_1)
    v_p1_1 = os.path.join(TEMP_DIR, "v_04_p1_listen_de.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s4_drill_p1_listen.png"), a_p1_1, v_p1_1)
    segments.append(v_p1_1)
    
    v_p1_1_rep = os.path.join(TEMP_DIR, "v_04_p1_rep_de.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s4_drill_p1_rep.png"), silence_20, v_p1_1_rep)
    segments.append(v_p1_1_rep)
    
    a_p1_2 = os.path.join(TEMP_DIR, "a_p1_2.mp3")
    concat_audio_files([os.path.join(AUDIO_DIR, "s4_pair1_d.mp3"), silence_03], a_p1_2)
    v_p1_2 = os.path.join(TEMP_DIR, "v_04_p1_listen_d.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s4_drill_p1_listen.png"), a_p1_2, v_p1_2)
    segments.append(v_p1_2)
    
    v_p1_2_rep = os.path.join(TEMP_DIR, "v_04_p1_rep_d.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s4_drill_p1_rep.png"), silence_20, v_p1_2_rep)
    segments.append(v_p1_2_rep)
    
    # 4.2: Pair 2: Đỏ vs Dở
    a_p2_1 = os.path.join(TEMP_DIR, "a_p2_1.mp3")
    concat_audio_files([os.path.join(AUDIO_DIR, "s4_pair2_de.mp3"), silence_03], a_p2_1)
    v_p2_1 = os.path.join(TEMP_DIR, "v_04_p2_listen_de.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s4_drill_p2_listen.png"), a_p2_1, v_p2_1)
    segments.append(v_p2_1)
    
    v_p2_1_rep = os.path.join(TEMP_DIR, "v_04_p2_rep_de.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s4_drill_p2_rep.png"), silence_20, v_p2_1_rep)
    segments.append(v_p2_1_rep)
    
    a_p2_2 = os.path.join(TEMP_DIR, "a_p2_2.mp3")
    concat_audio_files([os.path.join(AUDIO_DIR, "s4_pair2_d.mp3"), silence_03], a_p2_2)
    v_p2_2 = os.path.join(TEMP_DIR, "v_04_p2_listen_d.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s4_drill_p2_listen.png"), a_p2_2, v_p2_2)
    segments.append(v_p2_2)
    
    v_p2_2_rep = os.path.join(TEMP_DIR, "v_04_p2_rep_d.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s4_drill_p2_rep.png"), silence_20, v_p2_2_rep)
    segments.append(v_p2_2_rep)
    
    # 4.3: Pair 3: Đo vs Do
    a_p3_1 = os.path.join(TEMP_DIR, "a_p3_1.mp3")
    concat_audio_files([os.path.join(AUDIO_DIR, "s4_pair3_de.mp3"), silence_03], a_p3_1)
    v_p3_1 = os.path.join(TEMP_DIR, "v_04_p3_listen_de.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s4_drill_p3_listen.png"), a_p3_1, v_p3_1)
    segments.append(v_p3_1)
    
    v_p3_1_rep = os.path.join(TEMP_DIR, "v_04_p3_rep_de.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s4_drill_p3_rep.png"), silence_20, v_p3_1_rep)
    segments.append(v_p3_1_rep)
    
    a_p3_2 = os.path.join(TEMP_DIR, "a_p3_2.mp3")
    concat_audio_files([os.path.join(AUDIO_DIR, "s4_pair3_d.mp3"), silence_03], a_p3_2)
    v_p3_2 = os.path.join(TEMP_DIR, "v_04_p3_listen_d.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s4_drill_p3_listen.png"), a_p3_2, v_p3_2)
    segments.append(v_p3_2)
    
    v_p3_2_rep = os.path.join(TEMP_DIR, "v_04_p3_rep_d.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s4_drill_p3_rep.png"), silence_20, v_p3_2_rep)
    segments.append(v_p3_2_rep)
    
    # Drill Outro
    a_s4_outro = os.path.join(TEMP_DIR, "a_s4_outro.mp3")
    concat_audio_files([os.path.join(AUDIO_DIR, "s4_drill_outro.mp3"), silence_05], a_s4_outro)
    v_s4_outro = os.path.join(TEMP_DIR, "v_04_drill_outro.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s4_drill_p0_listen.png"), a_s4_outro, v_s4_outro)
    segments.append(v_s4_outro)
    
    # 5. Scene 5: Mini Quiz
    # Quiz intro
    v_s5_intro = os.path.join(TEMP_DIR, "v_05_quiz_intro.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s5_q1_question.png"), os.path.join(AUDIO_DIR, "s5_quiz_intro.mp3"), v_s5_intro)
    segments.append(v_s5_intro)
    
    # Q1 Question sound + 3s thinking
    a_q1_think = os.path.join(TEMP_DIR, "a_q1_think.mp3")
    concat_audio_files([
        os.path.join(AUDIO_DIR, "s5_q1_sound.mp3"),
        silence_03,
        os.path.join(AUDIO_DIR, "sfx_tick.mp3"),
        silence_05,
        os.path.join(AUDIO_DIR, "sfx_tick.mp3"),
        silence_05,
        os.path.join(AUDIO_DIR, "sfx_tick.mp3"),
        silence_05
    ], a_q1_think)
    v_q1_q = os.path.join(TEMP_DIR, "v_05_q1_question.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s5_q1_question.png"), a_q1_think, v_q1_q)
    segments.append(v_q1_q)
    
    # Q1 Answer reveal
    a_q1_ans = os.path.join(TEMP_DIR, "a_q1_ans.mp3")
    concat_audio_files([
        os.path.join(AUDIO_DIR, "sfx_ding.mp3"),
        os.path.join(AUDIO_DIR, "s5_q1_ans.mp3"),
        silence_05
    ], a_q1_ans)
    v_q1_a = os.path.join(TEMP_DIR, "v_05_q1_answer.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s5_q1_answer.png"), a_q1_ans, v_q1_a)
    segments.append(v_q1_a)
    
    # Q2 Question sound + 3s thinking
    a_q2_think = os.path.join(TEMP_DIR, "a_q2_think.mp3")
    concat_audio_files([
        os.path.join(AUDIO_DIR, "s5_q2_sound.mp3"),
        silence_03,
        os.path.join(AUDIO_DIR, "sfx_tick.mp3"),
        silence_05,
        os.path.join(AUDIO_DIR, "sfx_tick.mp3"),
        silence_05,
        os.path.join(AUDIO_DIR, "sfx_tick.mp3"),
        silence_05
    ], a_q2_think)
    v_q2_q = os.path.join(TEMP_DIR, "v_05_q2_question.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s5_q2_question.png"), a_q2_think, v_q2_q)
    segments.append(v_q2_q)
    
    # Q2 Answer reveal
    a_q2_ans = os.path.join(TEMP_DIR, "a_q2_ans.mp3")
    concat_audio_files([
        os.path.join(AUDIO_DIR, "sfx_ding.mp3"),
        os.path.join(AUDIO_DIR, "s5_q2_ans.mp3"),
        silence_05
    ], a_q2_ans)
    v_q2_a = os.path.join(TEMP_DIR, "v_05_q2_answer.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s5_q2_answer.png"), a_q2_ans, v_q2_a)
    segments.append(v_q2_a)
    
    # 6. Scene 6: Outro
    a_s6 = os.path.join(TEMP_DIR, "a_s6.mp3")
    concat_audio_files([
        os.path.join(AUDIO_DIR, "s6_outro.mp3"),
        silence_15
    ], a_s6)
    v_s6 = os.path.join(TEMP_DIR, "v_06_summary.mp4")
    create_video_segment(os.path.join(FRAMES_DIR, "s6_summary.png"), a_s6, v_s6)
    segments.append(v_s6)
    
    print(f"Concatenating {len(segments)} segments into {FINAL_OUTPUT}...")
    concat_list = os.path.join(TEMP_DIR, "concat_list.txt")
    with open(concat_list, "w") as f:
        for seg in segments:
            f.write(f"file '{seg}'\n")
            
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        FINAL_OUTPUT
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"FINAL VIDEO GENERATED SUCCESSFULLY: {FINAL_OUTPUT}")

if __name__ == "__main__":
    build_all()
