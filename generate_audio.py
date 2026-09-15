import asyncio
import edge_tts
import os

AUDIO_DIR = "/home/quang/video_ai/audio"

# Voice configurations
VOICE_EN = "en-US-AvaMultilingualNeural" # Natural, clear English narrator
VOICE_VN = "vi-VN-HoaiMyNeural"          # Native clear Northern Vietnamese

# Script lines
AUDIO_SEGMENTS = [
    # Scene 1: Intro & Objective (0:00 - 0:25)
    ("s1_intro", VOICE_EN, "-4%", 
     "Xin chao! Have you ever felt confused when seeing the Vietnamese letters D and D with crossbar? "
     "Many English speakers pronounce Vietnamese D with crossbar like English D, but get totally stuck on Vietnamese D! "
     "In just two and a half minutes, you will master both sounds effortlessly. Let's start!"),
     
    # Scene 2: The letter Đ (0:25 - 0:55)
    ("s2_de_desc", VOICE_EN, "-4%",
     "First, meet the letter D with a horizontal crossbar. In phonetic science, this is an alveolar stop. "
     "Good news: It sounds almost identical to the English D in 'Door' or 'Day'! "
     "Place the tip of your tongue against your upper gum, stop the air, and release it voiced. "
     "Listen to our native speaker:"),
    ("s2_de_vn", VOICE_VN, "-8%",
     "Đờ. Đ. Đi. Đỏ. Đẹp."),
    ("s2_de_recap", VOICE_EN, "-4%",
     "Awesome! Just remember: Crossbar D equals English Door."),

    # Scene 3: The letter D (0:55 - 1:30)
    ("s3_d_desc", VOICE_EN, "-4%",
     "Now, look closely at this letter: D without any crossbar. This is completely different! "
     "In standard Northern Vietnamese, it is pronounced like the English Z in 'Zoo' or 'Zero'. "
     "The air continuously hisses through your lightly closed teeth. Listen carefully:"),
    ("s3_d_vn", VOICE_VN, "-8%",
     "Dờ. D. Da. Dễ. Dưa."),
    ("s3_d_recap", VOICE_EN, "-4%",
     "Notice that? It's a gentle buzzing Z sound! Note that in Southern Vietnam, people often pronounce it like Y in Yes."),

    # Scene 4: Practice & Shadowing (1:30 - 2:05)
    ("s4_drill_intro", VOICE_EN, "-4%",
     "Now, let's practice minimal pairs! Listen to the native speaker, then repeat out loud during the countdown!"),
    ("s4_pair1_de", VOICE_VN, "-8%", "Đi"),
    ("s4_pair1_d", VOICE_VN, "-8%", "Da"),
    ("s4_pair2_de", VOICE_VN, "-8%", "Đỏ"),
    ("s4_pair2_d", VOICE_VN, "-8%", "Dở"),
    ("s4_pair3_de", VOICE_VN, "-8%", "Đo"),
    ("s4_pair3_d", VOICE_VN, "-8%", "Do"),
    ("s4_drill_outro", VOICE_EN, "-4%",
     "Great job! Feel the difference between the stop and the buzz!"),

    # Scene 5: Mini Quiz (2:05 - 2:35)
    ("s5_quiz_intro", VOICE_EN, "-4%",
     "Quiz time! Listen to the sound and choose: Is it A or B? Question 1: Which word do you hear?"),
    ("s5_q1_sound", VOICE_VN, "-8%", "Đi"),
    ("s5_q1_ans", VOICE_EN, "-4%",
     "Three, two, one. Exactly, it's A: Đi! Question 2: Which word do you hear?"),
    ("s5_q2_sound", VOICE_VN, "-8%", "Da"),
    ("s5_q2_ans", VOICE_EN, "-4%",
     "Three, two, one. Correct! It's B: Da! You nailed it!"),

    # Scene 6: Golden Rule & Outro (2:35 - 2:48)
    ("s6_outro", VOICE_EN, "-4%",
     "Here is your golden rule to remember forever: "
     "Crossbar D equals English D like Door. Plain D equals English Z like Zoo. "
     "Cảm ơn các bạn! See you in the next Vietnamese microlearning lesson. Tạm biệt!")
]

async def generate_all():
    for name, voice, rate, text in AUDIO_SEGMENTS:
        output_file = os.path.join(AUDIO_DIR, f"{name}.mp3")
        print(f"Generating {output_file}...")
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(output_file)
    print("All audio files generated successfully!")

if __name__ == "__main__":
    asyncio.run(generate_all())
