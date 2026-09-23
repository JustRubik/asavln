# Notes

By JustRubik / DangHuyHieu

## About

### Visual SLAM Algorithm

Visual SLAM (VSLAM) trên xe tự hành là thuật toán để phân tích ảnh mà các cảm biến quét được khi xe di chuyển, đồng thời lập bản đồ. Sau đó xe có thể tự định vị trong không gian và thực hiện các tác vụ.

SLAM trở thành giải pháp thay thế GPS, ví dụ như trong một vùng không gian giới hạn.

### Phân loại VSLAM

Visual Only SLAM (Monocular SLAM)

Visual Inertial (Stereo)

RGB-D SLAM

### 3 tiến trình chính của Visual-based SLAM 

Có 3 nhiệm vụ chính để tạo lập 1 bản đồ 3D từ những bức ảnh 2D mà cảm biến quét được:

- Khởi hành (initialization)

- Theo dõi (tracking)

- Lập bản đồ (mapping)

## Về kĩ thuật SLAM

### Chuẩn bị về hệ thống và thu thập dữ liệu

Camera, cảm biến, thu thập dữ liệu để vi điều khiển xử lý thông tin và quyết định các bước tiếp theo của xe tự hành.

Cần thiết kế hệ thống để giảm thiểu lỗi lan truyền (error propagation) và phải lưu ý về thiết kế dữ liệu để tối ưu hóa hiệu năng bởi việc xử lý lượng lớn thông tin động (dynamic and varied environments) trong suốt quá trình xe hoạt động.

### Định vị

Xác định vị trí của xe trong không gian. Không gian được sinh ra từ việc tính toán ở bước trên.

Sử dụng các phương pháp như là ORB (Oriented FAST and Rotated BRIEF) hay SIFT (Scale-Invarient Feature Transform).

Thành phần quan trọng: feature tracking (theo dõi đặc điểm nhận dạng của đối tượng), feature matching (sử dụng đặc điểm nhận dạng của đối tượng để đối chiếu), relocalization (tái định vị), và pose estimation (ước lượng tư thế).

### Lập bản đồ

Hệ thống lập bản đồ dựa trên: occupancy grids (lưới chiếm dụ), relocalization (tái định vị), và pose estimation (ước lượng tư thế).

### Lập bản đồ

Hệ thống lập bản đồ dựa trên: occupancy grids (lưới chiếm dụng), point clouds (mây điểm, lưới điểm).

### Tinh chỉnh chương trình và Vòng lặp đóng

Process tuning:

- Tìm điểm cân bằng giữa độ chính xác, hiệu suất tính toán và khả năng thích ứng.
- Đảm bảo tính real-time thông qua kiểm thử nghiêm ngặt

## Mô hình của VSLAM

Ứng dụng học máy, học sâu và cảm biến cắt biên (cutting edge sensors???) để xe thích ứng được với những tình huống không quen

3 mô hình V-SLAM (như trình bày bên trên)

### Visual-Only SLAM (monocular VSLAM)

Tóm tắt thì, xử lý ảnh 2D quét được, sau đó ánh xạ sang mô hình 3D bằng các tính toán.

Điểm mạnh: giá thành rẻ, tiết kiệm điện, nhanh chóng triển khai 

Điểm yếu: độ chính xác không tốt

### Visual-Inertial SLAM 

Đoạn sau này tài liệu viết lan man quá :D Bỏ qua đi



# Conclusion

Chốt lại, Visual SLAM là ứng dụng cảm biến camera để thực hiện bài toán định vị và định hướng, đồng thời hướng nghiên cứu có thể bẻ thành ứng dụng trí tuệ nhân tạo để vận hành xe.

Còn mảng ekf-SLAM và fastSLAM là đang tập trung vào các bộ lọc thống kê -> mô hình ước lượng vị trí và pose của xe trong không gian, từ các quan sát không chắc chắn. 
