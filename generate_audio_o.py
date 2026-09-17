import asyncio
import edge_tts
import os

AUDIO_DIR = "/home/quang/video_ai/audio_o"
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICE_VN = "vi-VN-HoaiMyNeural"
RATE = "+14%"
PITCH = "+28Hz"

SEGMENTS = [
    ("s1_lim_intro", 
     "Xin chào các bạn! Chúng tớ là bộ ba bạn thân O, Ô, Ơ đây! "
     "O tròn như quả trứng gà, Ô thì đội mũ, Ơ thì thêm râu! "
     "Cùng chúng tớ khám phá bí mật phát âm siêu dễ thương nhé!"),
     
    ("s2_nhung_o_desc", 
     "Tớ là O! Tròn xoe như quả trứng gà nè! Khi phát âm tớ, các bạn hãy mở rộng miệng thật to và tròn môi nhé!"),
     
    ("s2_nhung_o_sound", 
     "Chữ O. O. Môi mở to tròn nào. O!"),
     
    ("s2_nhung_oe_desc", 
     "Bất ngờ chưa! Một chiếc mũ xinh xắn rơi xuống đầu tớ này! Tớ biến thành Ô rồi! Khẩu hình chúm tròn nhô ra phía trước nhé!"),
     
    ("s2_nhung_oe_sound", 
     "Chữ Ô. Ô. Chúm môi nhô ra nào. Ô!"),
     
    ("s2_nhung_ow_desc", 
     "Còn tớ nè! Tớ được tặng một chiếc râu móc cong cong cực ngầu! Tớ là Ơ! Cười tươi, dẹt môi sang hai bên nhé!"),
     
    ("s2_nhung_ow_sound", 
     "Chữ Ơ. Ơ. Dẹt môi thư thái. Ơ!"),
     
    ("s2_nhung_scanner", 
     "Đố các bạn nhớ được bí kíp này nha! Không có dấu là O! Đội chiếc mũ là Ô! Thêm chiếc râu là Ơ! Đừng để bị nhầm lẫn nhé!"),
     
    ("s3_y_intro", 
     "Bây giờ, chúng mình cùng nhún nhảy và luyện đọc thật to theo nhịp đếm nào! Sẵn sàng chưa? Một, hai, ba, bắt đầu!"),
     
    ("s3_y_pair_o", 
     "O! Bò! Con bò!"),
     
    ("s3_y_pair_oe", 
     "Ô! Cô! Cô giáo!"),
     
    ("s3_y_pair_ow", 
     "Ơ! Bơ! Quả bơ!"),
     
    ("s3_y_outro", 
     "Hoan hô! Các bạn phát âm siêu quá! Nhớ cảm nhận đôi môi: tròn to, chúm nhô, rồi dẹt ngang nhé!"),
     
    ("s4_thuy_quiz_q", 
     "Thử thách tai tinh mắt sáng nào! Bạn vừa nghe thấy từ bí mật nào dưới đây?"),
     
    ("s4_thuy_quiz_sound", 
     "Cô!"),
     
    ("s4_thuy_quiz_ans", 
     "Ba, hai, một! Hoan hô! Chính xác một trăm phần trăm! Đó là đáp án A: CÔ! Bạn giỏi quá!"),
     
    ("s4_thuy_golden_rule", 
     "Quy tắc vàng siêu dễ nhớ: O trứng gà, Ô đội mũ, Ơ thêm râu! Chúc các bạn học thật vui và hẹn gặp lại nhé! Bye bye!")
]

async def main():
    print(f"Generating {len(SEGMENTS)} upbeat playful character voice clips...")
    for name, text in SEGMENTS:
        out_path = os.path.join(AUDIO_DIR, f"{name}.mp3")
        for attempt in range(4):
            try:
                comm = edge_tts.Communicate(text, VOICE_VN, pitch=PITCH, rate=RATE)
                await comm.save(out_path)
                print(f"  [OK] {name}.mp3")
                await asyncio.sleep(0.8)
                break
            except Exception as e:
                print(f"  [Retry {attempt+1}] {name}: {e}")
                await asyncio.sleep(2.0)
    print("All 17 cheerful character voice clips generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
