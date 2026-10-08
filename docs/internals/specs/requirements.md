# Requirements

Hệ thống mô phỏng robot hút bụi bằng các công cụ mô phỏng và lập trình đơn giản, sử dụng thuật toán SLAM để lập bản đồ môi trường đồng thời định vị vị trí của robot trên bản đồ đó.

Hệ thống được thiết kế với 2 chế độ chính của robot:

* **Exploration:** Robot khám phá môi trường xung quanh và lập bản đồ.
* **Cleaning:** Robot sử dụng bản đồ đã lập để lên kế hoạch và thực hiện việc hút bụi, đồng thời vẫn sử dụng thuật toán SLAM vì:

  * Cần xác định vị trí của robot trên bản đồ.
  * Cần tiếp tục quan sát môi trường.
  * Cần cập nhật bản đồ khi môi trường có thay đổi, ví dụ xuất hiện thêm vật cản.

---

# LƯU Ý TRƯỚC KHI ĐỌC CÁI ĐỐNG NÀY

**Đây là file do chatGPT sinh ra, cần phải đọc lại, check từng dòng, vì nó cần thiết cho dự án - JustRubik**

## Mục lục

* [1. Phạm vi hệ thống](#1-phạm-vi-hệ-thống)
* [2. Yêu cầu chức năng](#2-yêu-cầu-chức-năng)

  * [2.1. Khởi tạo môi trường](#21-khởi-tạo-môi-trường)
  * [2.2. Khởi tạo robot](#22-khởi-tạo-robot)
  * [2.3. Exploration](#23-exploration)
  * [2.4. SLAM](#24-slam)
  * [2.5. Cleaning](#25-cleaning)
  * [2.6. Lập kế hoạch đường đi](#26-lập-kế-hoạch-đường-đi)
  * [2.7. Di chuyển robot](#27-di-chuyển-robot)
  * [2.8. Phát hiện hoàn thành](#28-phát-hiện-hoàn-thành)
  * [2.9. Về trạm sạc](#29-về-trạm-sạc)
* [3. Yêu cầu về cảm biến và mô phỏng](#3-yêu-cầu-về-cảm-biến-và-mô-phỏng)
* [4. Yêu cầu về bản đồ](#4-yêu-cầu-về-bản-đồ)
* [5. Yêu cầu về trạng thái robot](#5-yêu-cầu-về-trạng-thái-robot)
* [6. Yêu cầu về giao diện và trực quan hóa](#6-yêu-cầu-về-giao-diện-và-trực-quan-hóa)
* [7. Yêu cầu về đánh giá](#7-yêu-cầu-về-đánh-giá)
* [8. Yêu cầu phi chức năng](#8-yêu-cầu-phi-chức-năng)
* [9. Giới hạn và giả định](#9-giới-hạn-và-giả-định)
* [10. Tiêu chí hoàn thành](#10-tiêu-chí-hoàn-thành)

---

# 1. Phạm vi hệ thống

Hệ thống phải mô phỏng được một robot hút bụi hoạt động trong môi trường hai chiều và sử dụng SLAM để đồng thời định vị robot và xây dựng bản đồ môi trường.

Hệ thống bao gồm các thành phần chính:

* Môi trường mô phỏng.

* Robot hút bụi.

* Cảm biến của robot.

* Hệ thống SLAM.

* Bản đồ môi trường.

* Hệ thống định vị.

* Hệ thống lập kế hoạch đường đi.

* Hệ thống điều khiển chuyển động.

* Hệ thống mô phỏng hoạt động hút bụi.

* Hệ thống trực quan hóa và hiển thị kết quả.

* [ ] Hệ thống mô phỏng được môi trường hoạt động của robot.

* [ ] Hệ thống mô phỏng được robot hút bụi.

* [ ] Hệ thống mô phỏng được quá trình robot quan sát môi trường.

* [ ] Hệ thống sử dụng SLAM trong quá trình hoạt động.

* [ ] Hệ thống hỗ trợ hai chế độ Exploration và Cleaning.

* [ ] Hệ thống có thể chuyển từ Exploration sang Cleaning.

* [ ] Hệ thống có thể kết thúc quá trình Cleaning và đưa robot về trạm sạc.

---

# 2. Yêu cầu chức năng

## 2.1. Khởi tạo môi trường

Hệ thống phải tạo được một môi trường hai chiều để robot hoạt động.

Môi trường phải chứa các thông tin cần thiết để mô phỏng:

* Kích thước môi trường.

* Tường hoặc biên của môi trường.

* Các vật cản.

* Vị trí bắt đầu của robot.

* Vị trí trạm sạc.

* Vùng cần được làm sạch.

* [ ] Có thể tạo môi trường với kích thước xác định.

* [ ] Có thể xác định các vùng không thể đi qua.

* [ ] Có thể tạo tường/biên của môi trường.

* [ ] Có thể đặt vật cản trong môi trường.

* [ ] Có thể xác định vùng cần làm sạch.

* [ ] Có thể xác định vị trí trạm sạc.

* [ ] Môi trường có một **ground-truth map** dùng làm dữ liệu thực tế của simulator.

* [ ] Ground-truth map không được được sử dụng trực tiếp bởi thuật toán SLAM để xây dựng bản đồ.

## 2.2. Khởi tạo robot

Robot phải được khởi tạo trước khi bắt đầu quá trình mô phỏng.

Robot phải có trạng thái tối thiểu:

* Vị trí `x`.

* Vị trí `y`.

* Góc định hướng `θ`.

* Trạng thái chuyển động.

* Trạng thái làm sạch.

* [ ] Có thể xác định pose ban đầu của robot.

* [ ] Robot được đặt tại một vị trí hợp lệ trong môi trường.

* [ ] Robot không được khởi tạo bên trong vật cản.

* [ ] Robot có orientation ban đầu.

* [ ] Robot có trạng thái hoạt động ban đầu xác định.

* [ ] Robot có vị trí trạm sạc hoặc có thể xác định được vị trí trạm sạc.

---

## 2.3. Exploration

Trong chế độ Exploration, robot phải khám phá môi trường nhằm thu thập dữ liệu cảm biến và xây dựng bản đồ.

* [ ] Robot có thể di chuyển trong môi trường Exploration.
* [ ] Robot có thể thu thập dữ liệu cảm biến trong khi di chuyển.
* [ ] Dữ liệu cảm biến được đưa vào hệ thống SLAM.
* [ ] SLAM cập nhật bản đồ trong quá trình Exploration.
* [ ] SLAM cập nhật vị trí ước lượng của robot trong quá trình Exploration.
* [ ] Robot có thể tiếp tục khám phá các khu vực chưa được quan sát.
* [ ] Hệ thống có thể xác định khi quá trình Exploration hoàn thành.
* [ ] Sau khi Exploration hoàn thành, hệ thống có thể chuyển sang Cleaning.

### Điều kiện kết thúc Exploration

Exploration có thể được coi là hoàn thành khi môi trường đã được quan sát đủ để tạo ra bản đồ phục vụ cho quá trình Cleaning.

* [ ] Có tiêu chí xác định Exploration hoàn thành.
* [ ] Tiêu chí hoàn thành không dựa trực tiếp vào ground-truth map trong thuật toán SLAM.

---

## 2.4. SLAM

Hệ thống phải sử dụng thuật toán SLAM để đồng thời:

1. Ước lượng vị trí của robot.
2. Xây dựng hoặc cập nhật bản đồ môi trường.

* [ ] SLAM nhận dữ liệu từ cảm biến của robot.
* [ ] SLAM duy trì trạng thái ước lượng của robot.
* [ ] SLAM duy trì bản đồ được xây dựng từ dữ liệu cảm biến.
* [ ] SLAM cập nhật pose của robot theo từng bước mô phỏng.
* [ ] SLAM cập nhật bản đồ theo dữ liệu cảm biến mới.
* [ ] SLAM không sử dụng trực tiếp ground-truth pose.
* [ ] SLAM không sử dụng trực tiếp ground-truth map.
* [ ] Bản đồ do SLAM tạo ra được sử dụng cho các chức năng tiếp theo của robot.

### SLAM trong Exploration

* [ ] SLAM hoạt động liên tục trong Exploration.
* [ ] Bản đồ được xây dựng dần theo quá trình robot khám phá.
* [ ] Pose ước lượng được cập nhật theo quá trình robot di chuyển.

### SLAM trong Cleaning

SLAM không dừng hoàn toàn sau khi Exploration kết thúc.

* [ ] SLAM tiếp tục nhận dữ liệu cảm biến trong Cleaning.
* [ ] SLAM tiếp tục định vị robot trong Cleaning.
* [ ] SLAM có thể cập nhật bản đồ khi nhận được thông tin mới.
* [ ] Hệ thống có thể phản ứng với thay đổi của môi trường.
* [ ] Vật cản mới có thể được phản ánh vào bản đồ nếu được cảm biến phát hiện.

---

## 2.5. Cleaning

Trong chế độ Cleaning, robot phải sử dụng bản đồ đã xây dựng để thực hiện nhiệm vụ làm sạch môi trường.

* [ ] Robot chuyển sang Cleaning sau khi Exploration hoàn thành.
* [ ] Robot sử dụng bản đồ SLAM để xác định khu vực cần làm sạch.
* [ ] Robot xác định được các khu vực đã được làm sạch.
* [ ] Robot có thể lựa chọn khu vực tiếp theo cần làm sạch.
* [ ] Robot có thể lập kế hoạch đường đi tới khu vực cần làm sạch.
* [ ] Robot di chuyển theo đường đi được lập kế hoạch.
* [ ] Robot thực hiện hành động hút bụi trong khi di chuyển.
* [ ] Hệ thống cập nhật trạng thái các khu vực đã được làm sạch.
* [ ] Robot tiếp tục sử dụng SLAM trong quá trình Cleaning.

---

## 2.6. Lập kế hoạch đường đi

Hệ thống phải có khả năng lựa chọn đường đi cho robot dựa trên bản đồ hiện tại.

* [ ] Bộ lập kế hoạch nhận bản đồ hiện tại.
* [ ] Bộ lập kế hoạch nhận vị trí hiện tại của robot.
* [ ] Bộ lập kế hoạch xác định được mục tiêu tiếp theo.
* [ ] Bộ lập kế hoạch tạo ra một đường đi từ robot tới mục tiêu.
* [ ] Đường đi không được đi xuyên qua vùng được xác định là vật cản.
* [ ] Hệ thống có thể lập lại đường đi khi đường đi hiện tại không còn phù hợp.
* [ ] Hệ thống có thể lập lại đường đi khi phát hiện vật cản mới.
* [ ] Hệ thống có thể lựa chọn mục tiêu tiếp theo sau khi hoàn thành một khu vực.

---

## 2.7. Di chuyển robot

Robot phải có khả năng di chuyển theo lệnh điều khiển và cập nhật trạng thái của nó trong simulator.

* [ ] Robot có thể di chuyển theo hướng tiến/lùi.
* [ ] Robot có thể thay đổi hướng.
* [ ] Robot cập nhật pose sau mỗi bước mô phỏng.
* [ ] Robot không được xuyên qua vật cản.
* [ ] Robot không được đi ra ngoài biên môi trường.
* [ ] Chuyển động của robot tạo ra dữ liệu đầu vào cho SLAM.
* [ ] Chuyển động thực tế của robot được lưu dưới dạng ground-truth để phục vụ đánh giá.
* [ ] Ground-truth pose không được cung cấp trực tiếp cho SLAM.

---

## 2.8. Phát hiện hoàn thành

Hệ thống phải xác định được khi robot đã hoàn thành nhiệm vụ làm sạch.

* [ ] Hệ thống theo dõi trạng thái của vùng cần làm sạch.
* [ ] Hệ thống xác định được vùng nào đã được làm sạch.
* [ ] Hệ thống xác định được vùng nào chưa được làm sạch.
* [ ] Hệ thống xác định được khi toàn bộ vùng yêu cầu đã được làm sạch.
* [ ] Khi hoàn thành Cleaning, robot ngừng tìm kiếm khu vực mới cần làm sạch.
* [ ] Sau khi hoàn thành, robot chuyển sang trạng thái trở về trạm sạc.

---

## 2.9. Về trạm sạc

Sau khi hoàn thành nhiệm vụ Cleaning, robot phải quay về trạm sạc.

* [ ] Hệ thống xác định được vị trí trạm sạc.
* [ ] Robot có thể lập kế hoạch đường đi về trạm sạc.
* [ ] Robot có thể di chuyển về trạm sạc.
* [ ] Robot tránh vật cản trên đường về.
* [ ] Robot sử dụng pose ước lượng của SLAM trong quá trình di chuyển.
* [ ] Hệ thống xác định được khi robot đã về tới trạm sạc.
* [ ] Khi tới trạm sạc, simulation có thể kết thúc.

---

# 3. Yêu cầu về cảm biến và mô phỏng

Hệ thống phải mô phỏng dữ liệu cảm biến của robot thay vì cung cấp trực tiếp thông tin môi trường cho thuật toán SLAM.

### LiDAR / Range Sensor

* [ ] Robot có cảm biến đo khoảng cách.
* [ ] Cảm biến có trường quan sát xác định.
* [ ] Cảm biến có số lượng tia hoặc độ phân giải xác định.
* [ ] Cảm biến trả về khoảng cách tới vật thể gần nhất trong mỗi hướng quan sát.
* [ ] Cảm biến có giới hạn khoảng cách tối thiểu/tối đa.
* [ ] Dữ liệu cảm biến được cập nhật theo từng timestep.
* [ ] Dữ liệu cảm biến có thể được thêm noise để mô phỏng cảm biến thực tế.
* [ ] Cảm biến không được cung cấp ground-truth map trực tiếp cho SLAM.

### Motion / Odometry

Nếu simulator sử dụng odometry hoặc thông tin chuyển động:

* [ ] Có thể tạo dữ liệu chuyển động từ chuyển động của robot.
* [ ] Odometry có thể có sai số.
* [ ] Sai số odometry có thể được cấu hình.
* [ ] Ground-truth motion và estimated/observed motion được phân biệt rõ ràng.

---

# 4. Yêu cầu về bản đồ

Hệ thống phải phân biệt bản đồ thực tế của simulator và bản đồ được SLAM xây dựng.

## Ground-truth map

Ground-truth map biểu diễn môi trường thực tế mà simulator sử dụng.

* [ ] Ground-truth map chứa thông tin đầy đủ về môi trường.
* [ ] Ground-truth map được sử dụng để mô phỏng cảm biến.
* [ ] Ground-truth map được sử dụng để kiểm tra va chạm.
* [ ] Ground-truth map có thể được sử dụng để đánh giá độ chính xác của SLAM.
* [ ] Ground-truth map không được cung cấp trực tiếp cho SLAM.

## SLAM map

SLAM map là bản đồ do robot xây dựng từ dữ liệu cảm biến.

* [ ] SLAM map được khởi tạo khi simulation bắt đầu.
* [ ] SLAM map được cập nhật trong Exploration.
* [ ] SLAM map tiếp tục được cập nhật trong Cleaning.
* [ ] SLAM map có thể biểu diễn vùng chưa quan sát.
* [ ] SLAM map có thể biểu diễn vùng trống.
* [ ] SLAM map có thể biểu diễn vật cản.
* [ ] SLAM map được sử dụng cho localization và path planning.

---

# 5. Yêu cầu về trạng thái robot

Hệ thống phải duy trì trạng thái của robot trong suốt quá trình mô phỏng.

Trạng thái tối thiểu gồm:

* Pose thực tế.
* Pose ước lượng.
* Chế độ hoạt động.
* Trạng thái làm sạch.
* Trạng thái di chuyển.
* Trạng thái nhiệm vụ.

Các chế độ chính:

```text
EXPLORATION
    ↓
CLEANING
    ↓
RETURN_TO_CHARGER
    ↓
FINISHED
```

* [ ] Hệ thống duy trì ground-truth pose.
* [ ] Hệ thống duy trì estimated pose.
* [ ] Hai loại pose được lưu riêng biệt.
* [ ] Robot có trạng thái Exploration.
* [ ] Robot có trạng thái Cleaning.
* [ ] Robot có trạng thái Return to Charger.
* [ ] Robot có trạng thái Finished.
* [ ] Chuyển đổi giữa các trạng thái được xác định rõ ràng.

---

# 6. Yêu cầu về giao diện và trực quan hóa

Hệ thống phải cung cấp khả năng quan sát quá trình mô phỏng và kết quả của SLAM.

* [ ] Hiển thị môi trường mô phỏng.
* [ ] Hiển thị robot.
* [ ] Hiển thị vị trí hiện tại của robot.
* [ ] Hiển thị hướng của robot.
* [ ] Hiển thị dữ liệu cảm biến nếu cần thiết.
* [ ] Hiển thị bản đồ do SLAM xây dựng.
* [ ] Hiển thị đường đi của robot.
* [ ] Hiển thị vùng đã được làm sạch.
* [ ] Phân biệt được ground-truth map và SLAM map khi cần đánh giá.
* [ ] Có thể quan sát quá trình bản đồ được xây dựng theo thời gian.
* [ ] Có thể quan sát quá trình robot di chuyển.

---

# 7. Yêu cầu về đánh giá

Hệ thống phải cho phép đánh giá kết quả của thuật toán SLAM và hoạt động của robot.

## Đánh giá localization

* [ ] Có thể so sánh estimated pose với ground-truth pose.
* [ ] Có thể tính sai số vị trí.
* [ ] Có thể tính sai số orientation.
* [ ] Có thể lưu trajectory của robot.
* [ ] Có thể so sánh ground-truth trajectory và estimated trajectory.

## Đánh giá mapping

* [ ] Có thể so sánh SLAM map với ground-truth map.
* [ ] Có thể đánh giá mức độ tương đồng giữa hai bản đồ.
* [ ] Có thể xác định các vùng được SLAM xây dựng chính xác.
* [ ] Có thể xác định các vùng SLAM xây dựng sai hoặc chưa quan sát.

## Đánh giá cleaning

* [ ] Có thể xác định tỷ lệ diện tích đã được làm sạch.
* [ ] Có thể xác định thời gian hoàn thành nhiệm vụ.
* [ ] Có thể xác định quãng đường robot đã di chuyển.
* [ ] Có thể xác định robot có hoàn thành nhiệm vụ hay không.
* [ ] Có thể xác định số lần robot phải lập lại đường đi nếu cần.

---

# 8. Yêu cầu phi chức năng

## 8.1. Tính đơn giản

Hệ thống được xây dựng với mục đích mô phỏng và nghiên cứu thuật toán, do đó không yêu cầu mô phỏng vật lý ở mức độ cao.

* [ ] Hệ thống ưu tiên sự đơn giản và dễ hiểu.
* [ ] Có thể chạy trên máy tính cá nhân thông thường.
* [ ] Không yêu cầu mô phỏng vật lý phức tạp.
* [ ] Không yêu cầu mô phỏng phần cứng robot thực tế.

## 8.2. Tính cấu hình

* [ ] Có thể thay đổi kích thước môi trường.
* [ ] Có thể thay đổi số lượng vật cản.
* [ ] Có thể thay đổi vị trí vật cản.
* [ ] Có thể thay đổi vị trí robot ban đầu.
* [ ] Có thể thay đổi vị trí trạm sạc.
* [ ] Có thể thay đổi tham số cảm biến.
* [ ] Có thể thay đổi noise của cảm biến.
* [ ] Có thể thay đổi noise của motion/odometry.
* [ ] Có thể thay đổi các tham số của thuật toán SLAM.

## 8.3. Tính tái lập

* [ ] Có thể sử dụng random seed để tái lập một môi trường.
* [ ] Cùng một cấu hình và random seed phải tạo ra cùng một môi trường.
* [ ] Có thể lưu cấu hình của một lần mô phỏng.
* [ ] Có thể chạy lại một scenario để so sánh kết quả.

## 8.4. Tính mở rộng

* [ ] Có thể thay thế thuật toán SLAM mà không cần thay đổi toàn bộ simulator.
* [ ] Có thể thay thế mô hình cảm biến.
* [ ] Có thể thay thế thuật toán path planning.
* [ ] Có thể thay đổi cấu hình robot.
* [ ] Có thể thêm loại cảm biến mới trong tương lai.

---

# 9. Giới hạn và giả định

Để giữ simulator ở mức độ đơn giản, hệ thống có thể sử dụng các giả định sau:

* [ ] Môi trường được mô phỏng trong không gian 2D.
* [ ] Robot được mô hình hóa dưới dạng robot di động 2D.
* [ ] Môi trường không yêu cầu mô phỏng trọng lực hoặc động lực học vật lý phức tạp.
* [ ] Vật cản được coi là không thể đi xuyên qua.
* [ ] Robot có thể nhận dữ liệu cảm biến tại các timestep của simulation.
* [ ] Robot có thể thực hiện các lệnh chuyển động được tạo bởi simulator.
* [ ] Hoạt động hút bụi được mô phỏng ở mức trạng thái vùng đã làm sạch, không yêu cầu mô phỏng cơ cấu hút bụi thực tế.
* [ ] Trạm sạc được biểu diễn dưới dạng một vị trí hoặc vùng xác định trong môi trường.
* [ ] Các vấn đề như pin, nhiệt độ, công suất động cơ và cơ cấu cơ khí không thuộc phạm vi chính của simulator, trừ khi được bổ sung trong yêu cầu khác.

---

# 10. Tiêu chí hoàn thành

Hệ thống được coi là đáp ứng yêu cầu cơ bản khi có thể thực hiện đầy đủ chu trình:

```text
Khởi tạo môi trường
        │
        ▼
Khởi tạo robot
        ├─────────────────────┐
        ▼                     │
   Exploration                │
        │                     │
        ├── Cảm biến          │
        ├── SLAM              │
        ├── Mapping           │
        └── Localization      │
        │                     │
        ▼                     │
      Cleaning                │
        │                     │
        ├── Localization      │
        ├── Mapping update    │
        ├── Path planning     │
        ├── Movement          │
        └── Cleaning          │
        │                     │
        ▼                     │
Đã làm sạch toàn bộ?          │
       / \                    │
     Rồi Chưa─────────────────┴
      │
      ▼
Return to Charger
      │
      ▼
   Finished
```

Các tiêu chí tối thiểu:

* [ ] Simulator khởi tạo được một môi trường hợp lệ.
* [ ] Simulator khởi tạo được robot.
* [ ] Robot có thể thực hiện Exploration.
* [ ] Robot có thể thu thập dữ liệu cảm biến.
* [ ] SLAM có thể xây dựng bản đồ từ dữ liệu cảm biến.
* [ ] SLAM có thể ước lượng vị trí robot.
* [ ] Robot có thể chuyển sang Cleaning.
* [ ] Robot có thể sử dụng SLAM map để lập kế hoạch.
* [ ] Robot có thể di chuyển trong môi trường.
* [ ] Robot có thể thực hiện nhiệm vụ làm sạch.
* [ ] SLAM tiếp tục hoạt động trong Cleaning.
* [ ] Hệ thống có thể xử lý việc bản đồ thay đổi khi phát hiện vật cản mới.
* [ ] Hệ thống xác định được khi hoàn thành việc làm sạch.
* [ ] Robot có thể quay về trạm sạc.
* [ ] Hệ thống có thể hiển thị kết quả mô phỏng.
* [ ] Hệ thống có thể đánh giá trajectory/localization.
* [ ] Hệ thống có thể đánh giá kết quả mapping.
* [ ] Một scenario có thể được tái lập bằng random seed.
* [ ] Có thể thay thế thuật toán SLAM mà không phải thiết kế lại toàn bộ simulator.

