# Requirements

Hệ thống mô phỏng một robot di động 2D có khả năng khám phá môi trường và xây dựng bản đồ bằng thuật toán FastSLAM 1.0.

Môi trường được sinh ngẫu nhiên với kích thước cố định, bao gồm các vật cản có hình dạng và kích thước đa dạng. Môi trường được biểu diễn trực quan bằng bảng lưới (Grid Map).

Hệ thống được chia thành hai thành phần độc lập:

1. **Simulator:** Mô phỏng môi trường, robot, chuyển động và cảm biến. Simulator duy trì toàn bộ thông tin thực tế (Ground Truth).
2. **SLAM:** Triển khai thuật toán FastSLAM 1.0 để ước lượng vị trí robot và xây dựng bản đồ dựa trên dữ liệu đầu vào từ Simulator.

Một thành phần Visualization & Evaluation độc lập chịu trách nhiệm hiển thị và đánh giá kết quả của hai thành phần trên.

Toàn bộ hệ thống được triển khai bằng Python, không yêu cầu phần cứng robot thực tế. Webots có thể được sử dụng như một lựa chọn bổ sung cho việc trực quan hóa.

---

# 1. Phạm vi hệ thống

Hệ thống phải mô phỏng được robot di động 2D hoạt động trong môi trường ngẫu nhiên và sử dụng FastSLAM 1.0 để đồng thời định vị và xây dựng bản đồ.

Các thành phần chính:

- Simulator.
- Environment Generator.
- Robot Model.
- Sensor Simulator.
- FastSLAM 1.0.
- Feature Extraction.
- Visualization.
- Evaluation.

Các yêu cầu:

- [ ] Hệ thống tạo được môi trường ngẫu nhiên có kích thước cố định.
- [ ] Robot có thể tự khám phá môi trường.
- [ ] Robot có thể thu thập dữ liệu cảm biến.
- [ ] FastSLAM 1.0 có thể tiếp nhận dữ liệu từ Simulator.
- [ ] FastSLAM ước lượng vị trí robot.
- [ ] FastSLAM xây dựng bản đồ landmark.
- [ ] Simulator và FastSLAM hoạt động độc lập.
- [ ] Hệ thống ghi lại trajectory của robot.
- [ ] Hệ thống hiển thị Ground Truth và kết quả ước lượng.
- [ ] Hệ thống hỗ trợ đánh giá độ chính xác của SLAM.

---

# 2. Simulator

Simulator là thành phần mô phỏng môi trường và hoạt động của robot.

Simulator chịu trách nhiệm duy trì trạng thái thực tế của hệ thống, không thực hiện thuật toán SLAM.

## 2.1. Environment

Môi trường được biểu diễn dưới dạng không gian hai chiều.

Có thể sử dụng Grid Map để biểu diễn môi trường và phục vụ trực quan hóa.

Các yêu cầu:

- [ ] Môi trường có kích thước cố định.
- [ ] Môi trường có hệ tọa độ xác định.
- [ ] Môi trường có các biên giới hạn.
- [ ] Môi trường chứa các vùng trống.
- [ ] Môi trường chứa các vật cản.
- [ ] Vật cản có thể có kích thước và hình dạng đa dạng.
- [ ] Có thể xác định vị trí khởi tạo robot.
- [ ] Robot không được khởi tạo bên trong vật cản.

## 2.2. Map Generator

Hệ thống phải có khả năng sinh môi trường ngẫu nhiên.

Các yêu cầu:

- [ ] Có thể sinh bản đồ ngẫu nhiên.
- [ ] Kích thước bản đồ được giữ cố định.
- [ ] Vị trí vật cản được tạo ngẫu nhiên.
- [ ] Kích thước vật cản được tạo ngẫu nhiên.
- [ ] Có thể cấu hình mật độ vật cản.
- [ ] Vật cản không được chồng lấn không hợp lệ.
- [ ] Có thể đảm bảo tồn tại khu vực có thể di chuyển.
- [ ] Có thể sử dụng Random Seed để tái lập bản đồ.
- [ ] Cùng cấu hình và Random Seed phải tạo ra cùng một môi trường.

## 2.3. Ground Truth

Simulator duy trì toàn bộ thông tin thực tế của môi trường.

Ground Truth bao gồm:

- Ground-truth map.
- Ground-truth robot pose.
- Ground-truth trajectory.
- Vị trí thực tế của các đặc trưng trong môi trường.

Các yêu cầu:

- [ ] Simulator lưu trữ đầy đủ thông tin môi trường.
- [ ] Simulator duy trì ground-truth pose.
- [ ] Simulator duy trì ground-truth trajectory.
- [ ] Ground Truth được sử dụng để mô phỏng cảm biến.
- [ ] Ground Truth được sử dụng để kiểm tra va chạm.
- [ ] Ground Truth được sử dụng để đánh giá kết quả SLAM.
- [ ] Không cung cấp Ground Truth trực tiếp cho FastSLAM.

---

# 3. Robot Model

Robot được mô hình hóa dưới dạng robot di động hai chiều.

Trạng thái thực tế:

- Position `(x, y)`.
- Orientation `θ`.
- Linear velocity.
- Angular velocity.

Các yêu cầu:

- [ ] Robot có pose ban đầu xác định.
- [ ] Robot có thể di chuyển tiến và lùi.
- [ ] Robot có thể thay đổi hướng.
- [ ] Robot cập nhật pose theo từng timestep.
- [ ] Robot không xuyên qua vật cản.
- [ ] Robot không đi ra ngoài biên môi trường.
- [ ] Chuyển động thực tế được lưu lại.
- [ ] Có thể mô phỏng sai số chuyển động.

Robot không được sử dụng ground-truth pose để tự định vị.

---

# 4. Sensor Simulator

Simulator phải mô phỏng dữ liệu cảm biến và cung cấp dữ liệu này cho FastSLAM.

## 4.1. LiDAR / Range Sensor

Sử dụng mô hình LiDAR 2D để thu thập thông tin về môi trường.

Các yêu cầu:

- [ ] Cảm biến có Field of View xác định.
- [ ] Có số lượng tia hoặc độ phân giải xác định.
- [ ] Có giới hạn khoảng cách tối đa.
- [ ] Mỗi tia trả về khoảng cách đến vật thể gần nhất.
- [ ] Dữ liệu cảm biến được cập nhật theo timestep.
- [ ] Có thể thêm noise vào dữ liệu.
- [ ] Có thể thay đổi tham số cảm biến.
- [ ] Dữ liệu cảm biến không chứa trực tiếp thông tin Ground Truth.

## 4.2. Odometry

Simulator tạo dữ liệu chuyển động quan sát được từ chuyển động thực tế của robot.

Các yêu cầu:

- [ ] Có thể tạo dữ liệu odometry.
- [ ] Odometry có thể chứa sai số.
- [ ] Có thể cấu hình noise của odometry.
- [ ] Ground-truth motion và observed motion được lưu riêng biệt.
- [ ] FastSLAM chỉ nhận observed motion.

## 4.3. Feature Extraction

FastSLAM 1.0 sử dụng mô hình bản đồ landmark. Vì vậy, dữ liệu cảm biến cần được xử lý để trích xuất các đặc trưng có thể quan sát.

Các yêu cầu:

- [ ] Có thể trích xuất landmark từ dữ liệu cảm biến.
- [ ] Landmark có thể được biểu diễn bằng tọa độ hoặc thông tin đo khoảng cách và góc.
- [ ] Có thể mô phỏng sai số đo landmark.
- [ ] Có thể thực hiện Data Association.
- [ ] Không cung cấp tọa độ landmark thực tế cho FastSLAM.
- [ ] Ground-truth landmark chỉ được sử dụng để đánh giá.

---

# 5. FastSLAM 1.0

FastSLAM 1.0 là thuật toán SLAM chính của hệ thống.

Thuật toán được triển khai thành một module độc lập với Simulator.

FastSLAM sử dụng Particle Filter để ước lượng trạng thái robot và duy trì bản đồ landmark riêng cho từng particle.

## 5.1. Input

FastSLAM chỉ nhận các dữ liệu sau:

- Odometry / Motion observation.
- Sensor measurements.
- Landmark observations sau quá trình trích xuất đặc trưng.

Các yêu cầu:

- [ ] FastSLAM không truy cập trực tiếp Simulator.
- [ ] FastSLAM không nhận ground-truth pose.
- [ ] FastSLAM không nhận ground-truth map.
- [ ] FastSLAM không nhận tọa độ landmark thực tế.
- [ ] Dữ liệu đầu vào được truyền thông qua một interface xác định.

## 5.2. Particle Filter

FastSLAM sử dụng tập hợp các particle để biểu diễn phân bố xác suất của robot pose.

Các yêu cầu:

- [ ] Có thể khởi tạo số lượng particle xác định.
- [ ] Mỗi particle duy trì một robot pose.
- [ ] Mỗi particle duy trì một bản đồ landmark riêng.
- [ ] Có thể cập nhật particle dựa trên motion model.
- [ ] Có thể cập nhật trọng số particle dựa trên sensor measurements.
- [ ] Có thể thực hiện resampling.
- [ ] Có thể cấu hình số lượng particle.
- [ ] Có thể theo dõi phân bố particle theo thời gian.

## 5.3. Landmark Mapping

Mỗi particle duy trì một bản đồ landmark riêng, sử dụng EKF để ước lượng vị trí và độ bất định của từng landmark.

Các yêu cầu:

- [ ] Có thể khởi tạo landmark mới.
- [ ] Có thể cập nhật landmark đã được quan sát.
- [ ] Có thể duy trì covariance của landmark.
- [ ] Có thể xử lý dữ liệu quan sát lặp lại.
- [ ] Có thể thực hiện Data Association.
- [ ] Bản đồ landmark được cập nhật trong quá trình hoạt động.

## 5.4. Localization

FastSLAM phải ước lượng vị trí và hướng của robot.

Các yêu cầu:

- [ ] Có thể ước lượng robot pose theo từng timestep.
- [ ] Có thể xác định pose đại diện từ tập particle.
- [ ] Có thể duy trì độ bất định của pose.
- [ ] Có thể lưu estimated trajectory.
- [ ] Có thể xuất particle set để phục vụ visualization.

## 5.5. Output

FastSLAM cung cấp các dữ liệu:

- Estimated pose.
- Estimated trajectory.
- Particle set.
- Estimated landmark map.
- Landmark covariance.
- Particle weights.

Các yêu cầu:

- [ ] Có interface xuất dữ liệu xác định.
- [ ] Có thể lưu kết quả sau khi simulation kết thúc.
- [ ] Có thể thay thế FastSLAM bằng thuật toán SLAM khác mà không phải sửa Simulator.

---

# 6. Exploration

Robot phải tự khám phá môi trường nhằm thu thập dữ liệu cảm biến và cung cấp dữ liệu cho FastSLAM.

Các yêu cầu:

- [ ] Robot có thể tự lựa chọn hướng di chuyển.
- [ ] Robot có thể thu thập dữ liệu cảm biến liên tục.
- [ ] Robot sử dụng thông tin định vị từ FastSLAM.
- [ ] Robot có thể ưu tiên các khu vực chưa được khám phá.
- [ ] Robot có thể tránh vật cản dựa trên thông tin quan sát.
- [ ] Robot có thể lựa chọn mục tiêu khám phá tiếp theo.
- [ ] Robot có thể tiếp tục hoạt động cho đến khi đạt điều kiện kết thúc.

Điều kiện kết thúc có thể dựa trên:

- Tỷ lệ quan sát môi trường.
- Không còn mục tiêu khám phá có thể tiếp cận.
- Đạt giới hạn số timestep.

Không sử dụng Ground-truth map để quyết định quá trình khám phá hoàn thành.

---

# 7. Visualization

Visualization là một module độc lập, có nhiệm vụ hiển thị trạng thái của Simulator và kết quả FastSLAM.

Không được can thiệp vào quá trình xử lý của thuật toán.

Ưu tiên giao diện trực quan 2D dạng top-down, có thể quan sát rõ môi trường và hoạt động của robot.

## 7.1. Environment View

- [ ] Hiển thị toàn bộ môi trường.
- [ ] Hiển thị Grid Map.
- [ ] Hiển thị các vật cản với hình dạng và kích thước tương ứng.
- [ ] Hiển thị biên môi trường.
- [ ] Hiển thị tọa độ hoặc hệ lưới.
- [ ] Có thể thay đổi tỷ lệ hiển thị.

## 7.2. Robot View

- [ ] Hiển thị robot bằng hình dạng trực quan thay vì chỉ một điểm.
- [ ] Hiển thị orientation.
- [ ] Hiển thị hướng di chuyển.
- [ ] Hiển thị vùng quan sát của cảm biến.
- [ ] Có thể hiển thị các tia LiDAR.

## 7.3. SLAM View

- [ ] Hiển thị estimated pose.
- [ ] Hiển thị estimated trajectory.
- [ ] Hiển thị particle cloud.
- [ ] Hiển thị estimated landmarks.
- [ ] Có thể hiển thị covariance của landmark.
- [ ] Có thể so sánh vị trí thực tế và vị trí ước lượng.

## 7.4. Trajectory View

- [ ] Hiển thị ground-truth trajectory.
- [ ] Hiển thị estimated trajectory.
- [ ] Có thể phân biệt hai trajectory bằng màu sắc hoặc kiểu đường.
- [ ] Có thể quan sát sự khác biệt giữa hai trajectory theo thời gian.

## 7.5. Interface

- [ ] Có thể bắt đầu simulation.
- [ ] Có thể tạm dừng simulation.
- [ ] Có thể tiếp tục simulation.
- [ ] Có thể reset simulation.
- [ ] Có thể điều chỉnh tốc độ mô phỏng.
- [ ] Có thể lựa chọn các lớp dữ liệu muốn hiển thị.
- [ ] Có thể quan sát kết quả cuối cùng.

Visualization có thể sử dụng Python với thư viện đồ họa phù hợp. Webots là lựa chọn bổ sung, không bắt buộc.

---

# 8. Evaluation

Evaluation là module độc lập dùng để đánh giá kết quả FastSLAM dựa trên Ground Truth do Simulator cung cấp.

## 8.1. Localization Evaluation

- [ ] So sánh estimated pose và ground-truth pose.
- [ ] Tính sai số vị trí.
- [ ] Tính sai số orientation.
- [ ] Tính sai số trung bình.
- [ ] Tính RMSE.
- [ ] So sánh estimated trajectory và ground-truth trajectory.

## 8.2. Mapping Evaluation

- [ ] So sánh estimated landmarks với ground-truth landmarks.
- [ ] Đánh giá sai số vị trí landmark.
- [ ] Đánh giá độ bất định của landmark.
- [ ] Xác định landmark được phát hiện chính xác.
- [ ] Xác định landmark bị bỏ sót hoặc nhận dạng sai.

## 8.3. Exploration Evaluation

- [ ] Tính tỷ lệ diện tích đã được quan sát.
- [ ] Tính tổng quãng đường robot di chuyển.
- [ ] Tính tổng số timestep.
- [ ] Đánh giá mức độ bao phủ môi trường.
- [ ] Xác định robot có hoàn thành quá trình khám phá hay không.

---

# 9. Kiến trúc phần mềm

Toàn bộ hệ thống được triển khai bằng Python.

Các module phải độc lập và giao tiếp thông qua những interface xác định.

Cấu trúc đề xuất:

```text
project/
│
├── simulator/
│   ├── environment.py
│   ├── map_generator.py
│   ├── robot.py
│   ├── sensors.py
│   └── simulator.py
│
├── slam/
│   ├── fastslam.py
│   ├── particle.py
│   ├── motion_model.py
│   ├── measurement_model.py
│   ├── landmark.py
│   ├── ekf.py
│   └── data_association.py
│
├── exploration/
│   ├── explorer.py
│   └── path_planning.py
│
├── visualization/
│   ├── renderer.py
│   ├── environment_view.py
│   ├── robot_view.py
│   └── slam_view.py
│
├── evaluation/
│   ├── localization.py
│   ├── mapping.py
│   └── metrics.py
│
├── config/
│   └── config.py
│
└── main.py
```

Các yêu cầu:

- [ ] Simulator không phụ thuộc vào FastSLAM.
- [ ] FastSLAM không phụ thuộc vào Simulator.
- [ ] Hai module giao tiếp thông qua dữ liệu đầu vào và đầu ra.
- [ ] Visualization có thể đọc dữ liệu từ cả hai module.
- [ ] Evaluation có thể truy cập Ground Truth và SLAM output.
- [ ] Có thể thay thế FastSLAM bằng thuật toán khác.
- [ ] Có thể thay thế thuật toán exploration.
- [ ] Có thể thay thế công cụ visualization.
- [ ] Có thể chạy simulation mà không cần Webots.

---

# 10. Yêu cầu phi chức năng

## 10.1. Tính đơn giản

- [ ] Hệ thống được triển khai hoàn toàn bằng Python.
- [ ] Không yêu cầu phần cứng robot.
- [ ] Không yêu cầu mô phỏng vật lý phức tạp.
- [ ] Có thể chạy trên máy tính cá nhân thông thường.

## 10.2. Tính cấu hình

- [ ] Có thể thay đổi kích thước môi trường.
- [ ] Có thể thay đổi mật độ vật cản.
- [ ] Có thể thay đổi vị trí và kích thước vật cản.
- [ ] Có thể thay đổi vị trí robot ban đầu.
- [ ] Có thể thay đổi tham số cảm biến.
- [ ] Có thể thay đổi noise của cảm biến và odometry.
- [ ] Có thể thay đổi số lượng particle.
- [ ] Có thể thay đổi các tham số FastSLAM.

## 10.3. Tính tái lập

- [ ] Có thể sử dụng Random Seed.
- [ ] Cùng cấu hình và seed phải tạo ra cùng môi trường.
- [ ] Có thể lưu cấu hình simulation.
- [ ] Có thể chạy lại một scenario.
- [ ] Có thể lưu dữ liệu kết quả.

## 10.4. Tính mở rộng

- [ ] Có thể thay thế thuật toán SLAM.
- [ ] Có thể bổ sung loại cảm biến mới.
- [ ] Có thể thay thế thuật toán exploration.
- [ ] Có thể bổ sung phương pháp đánh giá mới.
- [ ] Có thể thay thế công cụ visualization.

---

# 11. Giới hạn và giả định

- [ ] Môi trường được mô phỏng trong không gian 2D.
- [ ] Môi trường có kích thước cố định trong mỗi lần simulation.
- [ ] Grid Map thuộc về Simulator và Visualization.
- [ ] FastSLAM không sử dụng Grid Map làm cấu trúc bản đồ nội bộ.
- [ ] FastSLAM sử dụng landmark-based representation.
- [ ] Robot được mô hình hóa dưới dạng robot di động 2D.
- [ ] Chuyển động không yêu cầu mô phỏng động lực học phức tạp.
- [ ] Cảm biến được mô phỏng bằng phần mềm.
- [ ] Không yêu cầu phần cứng thực tế.
- [ ] Không yêu cầu Webots.
- [ ] Ground Truth chỉ phục vụ mô phỏng và đánh giá.
- [ ] FastSLAM không được truy cập trực tiếp Ground Truth.

---

# 12. Tiêu chí hoàn thành

Hệ thống được coi là hoàn thành khi có thể thực hiện đầy đủ chu trình:

```text
         Khởi tạo
             |
             v
      Sinh môi trường
             |
             v
       Khởi tạo robot
             |
             v
        SIMULATOR
             |
             v
       Robot di chuyển
             |
             v
       Thu thập sensor
             |
             v
      Odometry + Features
             |
             v
        FASTSLAM 1.0
             |
       +-----+-----+
       |           |
       v           v
 Localization   Mapping
       |           |
       +-----+-----+
             |
             v
     Xuất kết quả SLAM
             |
             v
       Visualization
             |
             v
         Evaluation
             |
             v
      Tiếp tục khám phá
             |
             v
      Đạt điều kiện dừng?
          /       \
        Chưa       Rồi
         |          |
         +----------+
                    |
                    v
             Dừng simulation
                    |
                    v
              Đánh giá kết quả
```

Các tiêu chí tối thiểu:

- [ ] Simulator tạo được môi trường ngẫu nhiên.
- [ ] Simulator mô phỏng được robot và cảm biến.
- [ ] Simulator duy trì Ground Truth.
- [ ] FastSLAM hoạt động độc lập với Simulator.
- [ ] FastSLAM nhận được dữ liệu odometry và sensor observations.
- [ ] FastSLAM duy trì được tập particle.
- [ ] Mỗi particle có bản đồ landmark riêng.
- [ ] FastSLAM ước lượng được robot pose.
- [ ] FastSLAM xây dựng được bản đồ landmark.
- [ ] Robot có thể tự khám phá môi trường.
- [ ] Hệ thống ghi lại được ground-truth trajectory.
- [ ] Hệ thống ghi lại được estimated trajectory.
- [ ] Visualization hiển thị được môi trường và hoạt động của robot.
- [ ] Visualization hiển thị được kết quả FastSLAM.
- [ ] Evaluation đánh giá được localization.
- [ ] Evaluation đánh giá được mapping.
- [ ] Có thể tái lập một scenario bằng Random Seed.
- [ ] Có thể thay thế thuật toán SLAM mà không phải thiết kế lại Simulator.
