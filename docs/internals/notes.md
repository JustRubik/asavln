# Notes

Written by JustRubik / DangHuyHieu

# Yêu cầu kĩ thuật

## Mô tả chung

Sử dụng thuật toán SLAM - Simultaneous Localization And Mapping - để ứng dụng trong robot hút bụi.

## Mục tiêu

Tạo được chương trình mô phỏng thể hiện được cách 1 con robot hút bụi lập được bản đồ, lập đường đi, xác định vị trí, và thực hiện nhiệm vụ.

Có cân nhắc sử dụng phần cứng. (sẽ nói rõ hơn ở phần Công cụ)

## Công cụ

- Python (để đảm nhiệm các nhệm vụ về visual)
- Matlab (nếu có, có thể cân nhắc sử dụng octave)
- C/C++ (để viết firmware cho vi điều khiển, có thể mô phỏng)
- Assembly (nếu cần thiết)
- Git/Github (quản lý phiên bản mã nguồn của dự án)
- Phần cứng (trong trường hợp cần), bao gồm: vi điều khiển esp32/stm32, động cơ giảm tốc, IMU, trong trường hợp tính toán quá nặng mà mcu không kham nổi -> sử dụng laptop và truyền với wifi.
- Thuần mô phỏng, thì có thể cân nhắc mqtt.

## Sản phẩm đầu ra

Hai hướng: 

* Chỉ mô phỏng: 1 chương trình mô phỏng được quá trình robot làm việc, đo đạc và viết báo cáo.
* Có phần cứng: 1 robot được mô tả bằng 4 bánh xe đơn giản, phải thể hiện được quá trình làm việc.

Sản phẩm nộp thầy: 1 báo cáo đầy đủ về sản phẩm (pdf, docx, v.v), 1 slide thuyết trình, sản phẩm demo.

## Yêu cầu kĩ thuật

Xem thêm ở các tài liệu trong `specs/`

### Scope

#### Core

- [ ] 2D environment
- [ ] robot model
- [ ] simulated LiDAR
- [ ] odometry
- [ ] SLAM
- [ ] occupancy grid
- [ ] localization
- [ ] path planning
- [ ] obstacle avoidance
- [ ] cleaning/coverage
- [ ] visualization

#### Extension (nếu còn time)

- [ ] IMU
- [ ] real encoder
- [ ] ESP32
- [ ] WiFi
- [ ] MQTT
- [ ] real LiDAR
- [ ] battery simulation
- [ ] docking station
- [ ] loop closure
- [ ] dynamic obstacles
- [ ] multi-room environment

## Kế hoạch công việc

### Phân công công việc

(phân công cho việc mô phỏng)

- Làm bản đồ (bản đồ 2D, con robot, vật cản, v.v)
- SLAM (LiDAR SLAM, loop closure)
- Path planning (lập đường chạy, tránh vật cản)
- Làm documents (specs, .pdf, .ppt)
- Quản lý mã nguồn
- 

### Kế hoạch tuần

(tuần 1 bắt đầu từ 28/09/2026)

|Tuần|Nội dung|Kết quả|
|----|--------|------|
|Tuần 1|Cả nhóm tập trung tìm hiểu thuật toán SLAM|Báo cáo về cách triển khai, thuật toán|

