import asyncio
import edge_tts
import os

AUDIO_DIR = "/home/quang/video_ai/audio_o"
VOICE_VN = "vi-VN-HoaiMyNeural" # Clear, warm, natural Vietnamese teacher voice

SEGMENTS = [
    # 1. Lim (Khởi động)
    ("s1_lim_intro", VOICE_VN, "-5%",
     "Xin chào các em! Trước khi vào bài học hôm nay, chúng ta cùng nhớ lại câu thơ dân gian quen thuộc nhé: "
     "O tròn như quả trứng gà, Ô thì đội mũ, Ơ thì thêm râu. "
     "Hôm nay chúng ta sẽ cùng học 3 nguyên âm rất thú vị trong tiếng Việt, đó là: O, Ô, Ơ. "
     "Chúng có mặt chữ khá giống nhau nhưng âm thanh và khẩu hình miệng lại hoàn toàn khác nhau!"),
     
    # 2. Nhung (Phát âm & Cách viết)
    # Cảnh 1: O nhân vật ban đầu
    ("s2_nhung_o_desc", VOICE_VN, "-5%",
     "Đây là O. Một chữ cái rất quen thuộc. Nhưng trong tiếng Việt, chỉ cần thêm một dấu hiệu nhỏ, O có thể thay đổi. Hãy xem điều gì xảy ra!"),
    ("s2_nhung_o_sound", VOICE_VN, "-10%",
     "O. O. Môi mở rộng, tròn môi: O."),
     
    # Cảnh 2: O biến thành Ô
    ("s2_nhung_oe_desc", VOICE_VN, "-5%",
     "Một chiếc mũ nhỏ xuất hiện. O đã trở thành Ô!"),
    ("s2_nhung_oe_sound", VOICE_VN, "-10%",
     "Ô. Ô. Môi chúm tròn nhô ra phía trước: Ô."),
     
    # Cảnh 3: O biến thành Ơ
    ("s2_nhung_ow_desc", VOICE_VN, "-5%",
     "Nhưng nếu dấu hiệu thay đổi thì sao? Một chiếc râu nhỏ xuất hiện: O đã trở thành Ơ!"),
    ("s2_nhung_ow_sound", VOICE_VN, "-10%",
     "Ơ. Ơ. Khẩu hình như Ô nhưng môi không tròn, mở dẹt ngang: Ơ."),
     
    # Cảnh 4: Máy quét
    ("s2_nhung_scanner", VOICE_VN, "-5%",
     "Đừng để dấu đánh lừa bạn! Hãy nhớ: Không có dấu phụ, là O. Có dấu mũ, là Ô. Có dấu móc râu, là Ơ!"),
     
    # 3. Ý (Luyện tập)
    ("s3_y_intro", VOICE_VN, "-5%",
     "Bây giờ, chúng ta cùng luyện tập nhé! Hãy lắng nghe và lặp lại thật to theo cô trong nhịp đếm:"),
    ("s3_y_pair_o", VOICE_VN, "-8%",
     "O. Bò. Con bò."),
    ("s3_y_pair_oe", VOICE_VN, "-8%",
     "Ô. Cô. Cô giáo."),
    ("s3_y_pair_ow", VOICE_VN, "-8%",
     "Ơ. Bơ. Quả bơ."),
    ("s3_y_outro", VOICE_VN, "-5%",
     "Rất tốt! Các em hãy cảm nhận đôi môi chuyển động từ tròn rộng, tròn chúm đến môi dẹt nhé!"),
     
    # 4. Thủy (Tổng kết & Củng cố)
    ("s4_thuy_quiz_q", VOICE_VN, "-5%",
     "Thử thách thính giác nào! Bạn vừa nghe thấy từ nào dưới đây?"),
    ("s4_thuy_quiz_sound", VOICE_VN, "-10%",
     "Cô."),
    ("s4_thuy_quiz_ans", VOICE_VN, "-5%",
     "Ba, hai, một. Chính xác! Đó là đáp án A: CÔ!"),
    ("s4_thuy_golden_rule", VOICE_VN, "-5%",
     "Hãy luôn nhớ quy tắc vàng: O tròn như quả trứng, Ô thì đội mũ, Ơ thì thêm râu. Cảm ơn các em và hẹn gặp lại trong bài học tiếp theo! Tạm biệt!")
]

async def main():
    for name, voice, rate, text in SEGMENTS:
        out_path = os.path.join(AUDIO_DIR, f"{name}.mp3")
        print(f"Generating {out_path}...")
        comm = edge_tts.Communicate(text, voice, rate=rate)
        await comm.save(out_path)
    print("All O-Ô-Ơ audio clips generated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
