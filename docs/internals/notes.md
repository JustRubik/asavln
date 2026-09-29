# Notes

Written by JustRubik / DangHuyHieu

# Yêu cầu kĩ thuật

## Mô tả chung

Sử dụng thuật toán SLAM - Simultaneous Localization And Mapping - để ứng dụng trong robot hút bụi.

## Mục tiêu

Tạo được chương trình mô phỏng thể hiện được cách 1 con robot hút bụi lập được bản đồ, lập đường đi, xác định vị trí, và thực hiện nhiệm vụ.

Có cân nhắc sử dụng phần cứng. (sẽ nói rõ hơn ở phần Công cụ)

## Công cụ

- Matlab (nếu có, có thể cân nhắc sử dụng octave)
- C/C++ (để viết firmware cho vi điều khiển, có thể mô phỏng)
- Assembly (nếu cần thiết)
- Git/Github (quản lý phiên bản mã nguồn của dự án)
- Phần cứng (trong trường hợp cần), bao gồm: vi điều khiển esp32/stm32, động cơ giảm tốc, IMU, trong trường hợp tính toán quá nặng mà mcu  không kham nổi -> sử dụng laptop và truyền với wifi.
- Thuần mô phỏng, thì có thể cân nhắc mqtt.

## Sản phẩm đầu ra

Hai hướng: 

* Chỉ mô phỏng: 1 chương trình mô phỏng được quá trình robot làm việc, đo đạc và viết báo cáo.
* Có phần cứng: 1 robot được mô tả bằng 4 bánh xe đơn giản, phải thể hiện được quá trình làm việc.

Sản phẩm nộp thầy: 1 báo cáo đầy đủ về sản phẩm (pdf, docx, v.v), 1 slide thuyết trình, sản phẩm demo.

## Yêu cầu kĩ thuật

On going...

## Kế hoạch công việc

On going...

