# NHẬT KÝ ỨNG DỤNG TRÍ TUỆ NHÂN TẠO (AI LOG)
**Dự án**: Thiết kế video Microlearning "Nguyên âm O - Ô - Ơ trong tiếng Việt" cho người nước ngoài trình độ A1  
**Trưởng nhóm & Phụ trách hồ sơ**: Nguyễn Thị Hồng Thương  
**Quy mô**: 1 trang theo đúng yêu cầu hồ sơ nộp  

---

### 1. Nguyên tắc ứng dụng AI của nhóm
Tuân thủ chỉ đạo của giảng viên: **"Dùng AI để hỗ trợ những công đoạn thực sự cần thiết, không giao toàn bộ sản phẩm cho AI"**. Mọi sản phẩm do AI hỗ trợ đều được nhóm 5 thành viên đối chiếu chặt chẽ theo tài liệu Ngữ âm học tiếng Việt chuẩn và tinh chỉnh thủ công.

---

### 2. Nhật ký chi tiết các công đoạn ứng dụng AI

| STT | Công đoạn & Công cụ AI | Câu lệnh (Prompt) đưa vào AI | Kết quả AI phản hồi (Output) | Đánh giá & Hoạt động kiểm chứng, chỉnh sửa của con người |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Xây dựng kịch bản & Lời thoại**<br>*(Gemini / Antigravity)* | *"Xây dựng kịch bản video microlearning 2.5 phút dạy phát âm và viết 3 nguyên âm O, Ô, Ơ dựa trên câu ca dao 'O tròn như quả trứng gà, Ô thì đội mũ, Ơ thì thêm râu' và phân công 5 thành viên"* | AI đề xuất kịch bản chi tiết, nhưng đưa vào các từ vựng phức tạp như *"mơ mộng"*, *"cổ kính"*, *"thơ thẩn"*. | **Hiệu đính của nhóm (Rất quan trọng):**<br>- Nhóm lọc bỏ toàn bộ từ trừu tượng trên vì không phù hợp trình độ A1.<br>- Thống nhất chọn các từ đơn giản, trực quan, tần suất cao trong giáo trình A1: **Bò** (cow), **Cô** (teacher), **Bơ** (avocado). |
| **2** | **Tạo giọng đọc mẫu tiếng Việt & Hướng dẫn**<br>*(Edge-TTS Neural Voice Engine)* | `- Giọng dẫn tiếng Việt: vi-VN-HoaiMyNeural (tốc độ -6%, phát âm chậm, tròn vành rõ chữ)<br>- Giọng phát âm mẫu: vi-VN-NamMinhNeural` | Giọng đọc AI mượt mà nhưng ở âm "Ơ", AI phát âm hơi nhanh, làm người học khó nhận biết độ dẹt của môi. | **Hiệu đính của nhóm:**<br>- Nhóm chèn thêm khoảng nghỉ 400ms và ngắt nhịp rõ ràng giữa chữ cái và từ vựng.<br>- Thiết lập khoảng lặng 2.5 giây cho người học lặp lại (Shadowing). |
| **3** | **Đồ họa trực quan & Hoạt cảnh**<br>*(Pillow Graphic Rendering + AI Code)* | *"Lập trình Python vẽ nét bút cong tròn cho O, hoạt cảnh chiếc mũ rơi xuống tạo Ô, chiếc râu móc mọc ra tạo Ơ và máy quét 3 chữ O - Ô - Ơ"* | Ban đầu code dùng emoji màu khiến giao diện bị lỗi ô vuông `[]` trên Linux và bố cục bị đóng khung hộp chật chội. | **Hiệu đính của nhóm:**<br>- Áp dụng triết lý thiết kế Editorial từ skill `creating-oneshot-landing-pages`: loại bỏ hoàn toàn các khung viền dày và emoji lỗi font.<br>- Thiết kế sơ đồ độ tròn môi 3 cấp độ (Tròn rộng $\rightarrow$ Tròn chúm $\rightarrow$ Môi dẹt). |
| **4** | **Biên tập chuyển cảnh & Đồng bộ Video**<br>*(Python & FFmpeg Pipeline)* | *"Tự động ghép nối chuỗi hình ảnh với track âm thanh chủ, tạo chuyển cảnh mượt mà Cosine Ease-in-Out giữa các phân đoạn"* | Xuất video ban đầu bị lệch 0.4s giữa tiếng chuông Ting và đáp án câu hỏi trắc nghiệm. | **Hiệu đính của nhóm:**<br>- Căn chỉnh lại timeline chính xác từng frame (30 fps), đồng bộ phụ đề song ngữ khớp 100% với từng câu thoại. |

---

### 3. Đánh giá giá trị gia tăng & Đóng góp của con người
- **Giá trị AI mang lại**: Giúp tạo ra giọng đọc chuẩn bản ngữ, tự động hóa render hoạt cảnh và chuyển cảnh video chất lượng cao mà không tốn chi phí phòng thu.
- **Giá trị quyết định của con người**: Tính sư phạm, sự phân cấp từ vựng phù hợp A1, chuẩn xác về mặt ngữ âm học và tư duy thẩm mỹ không thể thay thế bởi AI.
