import asyncio
import os
import edge_tts

OUT_DIR = "/home/quang/video_ai/audio_3_chars"
os.makedirs(OUT_DIR, exist_ok=True)

# Voice profiles for the 3 distinct cute cartoon characters
VOICE_O = {"voice": "vi-VN-HoaiMyNeural", "rate": "+15%", "pitch": "+32Hz"}
VOICE_OE = {"voice": "vi-VN-NamMinhNeural", "rate": "+14%", "pitch": "+20Hz"}
VOICE_OW = {"voice": "vi-VN-HoaiMyNeural", "rate": "+8%", "pitch": "+14Hz"}

DIALOGUES = [
    # Scene 1: Introduction
    ("c_o_intro.mp3", VOICE_O, "Xin chào các bạn! Tớ là Bé O tròn vo như quả trứng gà nè!"),
    ("c_oe_intro.mp3", VOICE_OE, "Còn tớ là Bé Ô! Tớ có chiếc mũ chóp nhọn cực xinh trên đầu!"),
    ("c_ow_intro.mp3", VOICE_OW, "Hihi, tớ là Bé Ơ đây! Tớ có chiếc râu móc cong cong đáng yêu nè!"),
    ("c_trio_intro.mp3", VOICE_O, "Chúng tớ là bộ ba bạn thân O, Ô, Ơ! Cùng khám phá với chúng tớ nhé!"),
    
    # Scene 2: Meet Bé O
    ("c_o_feature.mp3", VOICE_O, "Tớ là Bé O! Chữ của tớ chỉ có một nét cong tròn khép kín mềm mại. Các bạn mở to tròn môi và nói O cùng tớ nào: O ... O ... Con bò!"),
    
    # Scene 3: Meet Bé Ô
    ("c_oe_feature.mp3", VOICE_OE, "Đến lượt tớ, Bé Ô đây! Nhìn xem, tớ đội thêm chiếc mũ nón chóp xinh xắn trên đầu. Các bạn chu môi nhô ra phía trước và nói Ô nhé: Ô ... Ô ... Cô giáo!"),
    
    # Scene 4: Meet Bé Ơ
    ("c_ow_feature.mp3", VOICE_OW, "Còn tớ là Bé Ơ! Tớ được gắn thêm một chiếc râu móc bên phải. Các bạn mỉm cười dẹt môi ngang và nói Ơ cùng tớ nào: Ơ ... Ơ ... Quả bơ!"),
    
    # Scene 5: Magic Transformation
    ("c_magic_o.mp3", VOICE_O, "Nhìn tớ nè! Tớ tròn xoe không mũ không râu!"),
    ("c_magic_oe.mp3", VOICE_OE, "Thêm chiếc mũ nhọn rơi xuống là biến thành tớ: Ô!"),
    ("c_magic_ow.mp3", VOICE_OW, "Thêm chiếc râu móc cong cong là biến thành tớ: Ơ! Thật là kỳ diệu!"),
    
    # Scene 6: Repeat Game
    ("c_game_o_q.mp3", VOICE_O, "Các bạn cùng chơi trò nhắc lại theo chúng tớ nhé! Hãy nói theo tớ nào: BÒ!"),
    ("c_game_o_praise.mp3", VOICE_O, "Hoan hô! Các bạn phát âm từ Bò chuẩn lắm!"),
    
    ("c_game_oe_q.mp3", VOICE_OE, "Đến lượt tớ nè! Hãy nói thật to theo tớ: CÔ!"),
    ("c_game_oe_praise.mp3", VOICE_OE, "Tuyệt vời quá! Bé Ô khen bạn nha!"),
    
    ("c_game_ow_q.mp3", VOICE_OW, "Còn tớ nữa nè! Hãy nói thật vang theo tớ: BƠ!"),
    ("c_game_ow_praise.mp3", VOICE_OW, "Xuất sắc! Các bạn nói từ Bơ rất hay!"),
    
    # Scene 7: Fun Quiz & Rhyme Goodbye
    ("c_quiz_q.mp3", VOICE_O, "Đố các bạn nhanh trí nè: Ai trong ba chúng tớ đang ĐỘI CHIẾC MŨ trên đầu? A: Bé O, B: Bé Ô, hay C: Bé Ơ?"),
    ("c_quiz_ans.mp3", VOICE_OE, "Hê hê! Chính là tớ, Bé Ô đội chiếc mũ nhọn xinh xắn đây nè!"),
    ("c_rhyme_1.mp3", VOICE_OW, "Các bạn luôn nhớ câu thơ dân gian nhé: O tròn như quả trứng gà,"),
    ("c_rhyme_2.mp3", VOICE_OE, "Ô thì đội mũ,"),
    ("c_rhyme_3.mp3", VOICE_OW, "Ơ thì thêm râu!"),
    ("c_goodbye.mp3", VOICE_O, "Chúc các bạn học tiếng Việt thật vui và tự tin! Tạm biệt các bạn nha!")
]

async def generate_all():
    print(f"Generating {len(DIALOGUES)} animated character voice clips...")
    for fname, cfg, text in DIALOGUES:
        out_path = os.path.join(OUT_DIR, fname)
        for attempt in range(4):
            try:
                comm = edge_tts.Communicate(
                    text,
                    cfg["voice"],
                    rate=cfg["rate"],
                    pitch=cfg["pitch"]
                )
                await comm.save(out_path)
                print(f"  [OK] {fname}")
                await asyncio.sleep(0.5)
                break
            except Exception as e:
                print(f"  [Retry {attempt+1}] {fname}: {e}")
                await asyncio.sleep(1.2)
    print("All 3-character voice clips generated successfully!")

if __name__ == "__main__":
    asyncio.run(generate_all())
