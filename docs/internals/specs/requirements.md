# Requirements

Hệ thống mô phỏng robot hút bụi bằng các công cụ mô phỏng và lập trình đơn giản, sử dụng thuật toán SLAM để lập bản đồ môi trường đồng thời định vị chính xác vị trí của robot trên bản đồ đó.

Hệ thống được thiết kế với 2 chế độ chính của robot: 
* Exploration: Robot khám phá môi trường xung quanh và lập bản đồ.
* Cleaning: Robot sử dụng bản đồ đã lập và lên kế hoạch thực hiện việc hút bụi, đồng thời vẫn sử dụng thuật toán SLAM vì:
    - Cần xác định vị trí của nó trên bản đồ. 
    - Cần cập nhật bản đồ mỗi khi có thay đổi trên môi trường (thêm vật cản, v.v)

## Yêu cầu chức năng

- 
