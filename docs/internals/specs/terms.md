# Terminology

> Tài liệu thuật ngữ của project SLAM robot hút bụi 2D.
>
> Tài liệu này tập hợp các thuật ngữ xuất hiện trực tiếp hoặc có liên quan chặt chẽ đến `algorithm.md` và `requirements.md`, đồng thời bổ sung các thuật ngữ nền tảng cần thiết để hiểu và triển khai hệ thống.
>
> **Ngôn ngữ chính:** Tiếng Việt
> **Thuật ngữ ưu tiên:** English
> **Tiếng Việt:** dùng để giải nghĩa hoặc chú thích khi cần.

---

# 1. Tổng quan

## 1.1 SLAM — Simultaneous Localization and Mapping

**SLAM** là bài toán trong đó robot đồng thời:

* ước lượng vị trí và hướng của chính nó (**Localization**);
* xây dựng bản đồ môi trường (**Mapping**).

Điểm khó của SLAM là hai bài toán phụ thuộc lẫn nhau:

```text
biết vị trí robot
    ↓
xây dựng map chính xác hơn

biết map
    ↓
ước lượng vị trí robot chính xác hơn
```

Trong project này, SLAM được thực hiện trong môi trường 2D bằng **FastSLAM**.

---

## 1.2 Localization

**Localization** (định vị) là quá trình ước lượng vị trí của robot trong môi trường.

Trong project, pose robot được biểu diễn bởi:

$$
\mathbf{x}_t =
\begin{bmatrix}
x_t\\
y_t\\
\theta_t
\end{bmatrix}
$$

Trong đó:

* \(x_t\): vị trí theo trục \(x\);
* \(y_t\): vị trí theo trục \(y\);
* \(\theta_t\): orientation của robot.

---

## 1.3 Mapping

**Mapping** (lập bản đồ) là quá trình xây dựng biểu diễn của môi trường dựa trên sensor observations.

Trong FastSLAM của project, map được biểu diễn dưới dạng **landmark map**.

```text
Map
├── Landmark 1
├── Landmark 2
├── Landmark 3
└── ...
```

---

## 1.4 Robot Pose

**Pose** là trạng thái vị trí và orientation của robot.

Trong không gian 2D:

$$
\mathbf{x}=(x,y,\theta)
$$

Cần phân biệt:

* **position**: chỉ \(x,y\);
* **orientation**: \(\theta\);
* **pose**: position + orientation.

---

## 1.5 Position

**Position** (vị trí) mô tả robot đang ở đâu trong không gian.

Trong 2D:

$$
\mathbf{p}=
\begin{bmatrix}
x\\
y
\end{bmatrix}
$$

---

## 1.6 Orientation

**Orientation** (hướng) mô tả robot đang quay theo hướng nào.

Trong 2D, orientation được biểu diễn bằng một góc:

$$
\theta
$$

Đơn vị nên được thống nhất là **radian** trong phần thuật toán.

---

## 1.7 Trajectory

**Trajectory** (quỹ đạo) là chuỗi pose của robot theo thời gian:

$$
\mathbf{x}_{1:t}
=
\left(
\mathbf{x}_1,
\mathbf{x}_2,
\ldots,
\mathbf{x}_t
\right)
$$

FastSLAM sử dụng các particle để biểu diễn các giả thuyết khác nhau về trajectory.

---

# 2. Environment và Simulation

## 2.1 Simulator

**Simulator** là chương trình mô phỏng môi trường, robot, sensor và chuyển động.

Simulator không phải là FastSLAM.

Có thể hình dung:

```text
Simulator
├── Environment
├── Ground Truth
├── Robot
├── Sensor Simulation
└── Motion Simulation
          │
          ▼
       FastSLAM
```

---

## 2.2 Environment

**Environment** (môi trường) là không gian mà robot hoạt động.

Trong project, environment là môi trường 2D có thể chứa:

* tường;
* vật cản;
* landmark;
* charging station;
* vùng cần làm sạch.

---

## 2.3 Ground Truth

**Ground Truth** là trạng thái thật của môi trường và robot trong simulator.

Ví dụ:

```text
Ground-truth map
Ground-truth robot pose
Ground-truth landmark positions
```

Ground Truth được dùng để:

* mô phỏng sensor;
* kiểm tra collision;
* đánh giá kết quả;
* tính localization error;
* tính mapping error.

Ground Truth **không được đưa trực tiếp vào FastSLAM** trong quá trình ước lượng.

---

## 2.4 Ground-truth Map

**Ground-truth map** là bản đồ thật của simulator.

Đây là bản đồ mà simulator biết nhưng FastSLAM không được biết trực tiếp.

Có thể dùng nó để so sánh:

```text
Ground-truth map
        vs
Estimated map
```

---

## 2.5 Estimated Map

**Estimated map** là bản đồ do SLAM tạo ra.

Trong FastSLAM, mỗi particle có một map riêng:

```text
Particle 1 → Map 1
Particle 2 → Map 2
Particle 3 → Map 3
...
```

---

## 2.6 Ground-truth Pose

**Ground-truth pose** là pose thật của robot trong simulator.

Nó được dùng để đánh giá:

$$
e_p=
\sqrt{
(x-\hat{x})^2+
(y-\hat{y})^2
}
$$

nhưng không được dùng để cập nhật FastSLAM.

---

## 2.7 Simulation Time

**Simulation time** là thời gian của môi trường mô phỏng.

Cần phân biệt với wall-clock time.

Một simulator có thể chạy:

```text
simulation time = 10 s
```

nhưng mất:

```text
wall-clock time = 2 s
```

để tính toán.

---

# 3. Robot

## 3.1 Robot

Robot là agent di chuyển trong environment và thực hiện nhiệm vụ.

Trong project, robot đóng vai trò robot hút bụi 2D.

Robot có:

* pose;
* motion model;
* sensor;
* trạng thái hoạt động;
* nhiệm vụ cleaning.

---

## 3.2 Robot State

**Robot state** là tập các thông tin mô tả trạng thái hiện tại của robot.

Có thể bao gồm:

```text
pose
velocity
battery
mode
cleaning state
charging state
```

Không phải tất cả robot state đều là trạng thái của FastSLAM.

---

## 3.3 Exploration

**Exploration** (thăm dò) là giai đoạn robot di chuyển để quan sát môi trường và xây dựng map.

Mục tiêu chính:

```text
quan sát environment
        ↓
SLAM
        ↓
xây dựng map
```

---

## 3.4 Cleaning

**Cleaning** (làm sạch) là giai đoạn robot thực hiện nhiệm vụ hút bụi dựa trên map và path planning.

FastSLAM vẫn tiếp tục chạy trong Cleaning.

```text
Cleaning
    ↓
Path Planning
    ↓
Robot Movement
    ↓
Sensor Observation
    ↓
FastSLAM
```

---

## 3.5 Charging Station

**Charging station** (trạm sạc) là vị trí robot có thể quay về sau khi hoàn thành cleaning hoặc khi cần sạc.

Charging station thuộc navigation/task layer, không phải thành phần của FastSLAM.

---

## 3.6 Coverage

**Coverage** là mức độ diện tích môi trường đã được robot đi qua hoặc làm sạch.

Coverage planning là bài toán xác định đường đi để robot phủ kín khu vực cần làm sạch.

---

## 3.7 Coverage Path Planning

**Coverage Path Planning** là quá trình lập kế hoạch đường đi nhằm bao phủ một vùng.

Ví dụ:

```text
┌─────────────────┐
│ → → → → → → → │
│ ← ← ← ← ← ← ← │
│ → → → → → → → │
│ ← ← ← ← ← ← ← │
└─────────────────┘
```

Coverage Path Planning không phải nhiệm vụ của FastSLAM.

---

# 4. Sensor

## 4.1 Sensor

**Sensor** là thiết bị hoặc mô hình tạo ra observation về môi trường.

Trong project, sensor chính là **2D LiDAR**.

---

## 4.2 2D LiDAR

**2D LiDAR — Light Detection and Ranging** là sensor đo khoảng cách đến vật thể bằng tia laser.

Một scan có thể được biểu diễn:

```text
angle → range
```

hoặc:

$$
(r_k,\phi_k)
$$

---

## 4.3 LiDAR Scan

**LiDAR scan** là tập các measurement thu được trong một lần quét.

Ví dụ:

$$
Z_t=
\left\{
(r_1,\phi_1),
(r_2,\phi_2),
\ldots,
(r_K,\phi_K)
\right\}
$$

---

## 4.4 Range

**Range** là khoảng cách từ robot đến điểm được sensor phát hiện.

Ký hiệu:

$$
r
$$

---

## 4.5 Bearing

**Bearing** là góc từ hướng của robot đến đối tượng được quan sát.

Ký hiệu:

$$
\phi
$$

Bearing khác với orientation của robot.

---

## 4.6 Field of View — FOV

**Field of View (FOV)** là vùng góc mà sensor có thể quan sát.

Ví dụ sensor có:

$$
FOV=180^\circ
$$

thì sensor chỉ quan sát được một nửa mặt phẳng xung quanh robot.

---

## 4.7 Sensor Range

**Sensor range** là khoảng cách tối đa mà sensor có thể đo.

Có thể có:

```text
minimum range
maximum range
```

Observation nằm ngoài range hợp lệ phải được xử lý phù hợp.

---

## 4.8 Sensor Noise

**Sensor noise** là sai số ngẫu nhiên trong measurement.

Ví dụ:

$$
r_{\text{measured}}
=
r_{\text{true}}
+
\epsilon_r
$$

với:

$$
\epsilon_r
\sim
\mathcal{N}(0,\sigma_r^2)
$$

---

## 4.9 Measurement

**Measurement** là giá trị trực tiếp do sensor tạo ra.

Measurement là dữ liệu đầu vào cho observation processing.

---

## 4.10 Observation

**Observation** là measurement đã được biểu diễn dưới dạng phù hợp với mô hình SLAM.

Trong FastSLAM landmark-based:

$$
\mathbf{z}
=
\begin{bmatrix}
r\\
\phi
\end{bmatrix}
$$

Có thể hiểu:

```text
raw sensor measurement
        ↓
processing
        ↓
observation
        ↓
FastSLAM
```

---

# 5. Coordinate Systems

## 5.1 Coordinate Frame

**Coordinate frame** (hệ tọa độ) là hệ quy chiếu dùng để biểu diễn vị trí và hướng.

Project sử dụng ít nhất:

```text
World Frame
Robot Frame
```

---

## 5.2 World Frame

**World frame** là hệ tọa độ cố định của môi trường.

Landmark map được biểu diễn trong world frame.

---

## 5.3 Robot Frame

**Robot frame** là hệ tọa độ gắn với robot.

Thông thường:

```text
x → phía trước
y → bên trái
```

Sensor measurement ban đầu thường được biểu diễn trong robot frame.

---

## 5.4 Coordinate Transformation

**Coordinate transformation** là phép chuyển một biểu diễn từ coordinate frame này sang coordinate frame khác.

Trong project, quan trọng nhất là:

```text
Robot Frame
    ↓
World Frame
```

---

## 5.5 Rotation Matrix

**Rotation matrix** biểu diễn phép quay.

Trong 2D:

$$
R(\theta)=
\begin{bmatrix}
\cos\theta & -\sin\theta\\
\sin\theta & \cos\theta
\end{bmatrix}
$$

---

## 5.6 SE(2)

**SE(2)** là nhóm các phép biến đổi rigid-body trong không gian 2D, bao gồm:

* translation theo \(x\);
* translation theo \(y\);
* rotation.

Pose:

$$
(x,y,\theta)
$$

có thể được xem là một phần tử của \(SE(2)\).

Project không nhất thiết phải triển khai trực tiếp toàn bộ formalism của \(SE(2)\), nhưng khái niệm này hữu ích để hiểu coordinate transformation.

---

# 6. Landmark

## 6.1 Landmark

**Landmark** là một đặc trưng có thể nhận dạng và sử dụng làm mốc trong SLAM.

Trong project, landmark được biểu diễn bằng điểm 2D:

$$
\mathbf{m}_j=
\begin{bmatrix}
m_x\\
m_y
\end{bmatrix}
$$

---

## 6.2 Landmark Map

**Landmark map** là tập các landmark mà SLAM đã ước lượng:

$$
M=
\{m_1,m_2,\ldots,m_N\}
$$

---

## 6.3 Point Landmark

**Point landmark** là landmark được biểu diễn bằng một điểm trong không gian.

Đây là dạng landmark được sử dụng trong implementation FastSLAM cơ sở.

---

## 6.4 Landmark Initialization

**Landmark initialization** là quá trình tạo landmark mới khi observation không khớp với landmark hiện có.

```text
new observation
      ↓
Data Association
      ↓
no match
      ↓
new landmark
```

---

## 6.5 Landmark Covariance

**Landmark covariance** mô tả độ không chắc chắn của vị trí landmark.

$$
\Sigma_j=
\begin{bmatrix}
\sigma_x^2 & \sigma_{xy}\\
\sigma_{xy} & \sigma_y^2
\end{bmatrix}
$$

Covariance càng nhỏ thường biểu thị estimate càng chắc chắn.

---

# 7. Probabilistic Robotics

## 7.1 Probability Distribution

**Probability distribution** là phân phối xác suất mô tả uncertainty của một đại lượng.

SLAM về bản chất là một bài toán ước lượng xác suất.

---

## 7.2 Prior

**Prior** là niềm tin trước khi nhận observation mới.

Ký hiệu thường dùng:

$$
p(x)
$$

---

## 7.3 Likelihood

**Likelihood** mô tả mức độ một observation phù hợp với giả thuyết hiện tại.

Ví dụ:

$$
p(z\mid x)
$$

---

## 7.4 Posterior

**Posterior** là phân phối sau khi kết hợp prior với observation.

$$
p(x\mid z)
$$

Theo Bayes:

$$
p(x\mid z)
\propto
p(z\mid x)p(x)
$$

---

## 7.5 Conditional Probability

**Conditional probability** là xác suất có điều kiện.

Ví dụ:

$$
p(x\mid z)
$$

đọc là:

> xác suất của \(x\) khi biết \(z\).

---

## 7.6 Gaussian Distribution

**Gaussian distribution** (phân phối Gaussian / phân phối chuẩn) được sử dụng để biểu diễn uncertainty của landmark trong EKF.

Dạng nhiều chiều:

$$
p(\mathbf{x})
=
\frac{
1
}{
\sqrt{(2\pi)^n|\Sigma|}
}
\exp
\left(
-\frac12
(\mathbf{x}-\boldsymbol{\mu})^T
\Sigma^{-1}
(\mathbf{x}-\boldsymbol{\mu})
\right)
$$

---

## 7.7 Mean

**Mean** là giá trị trung bình hoặc estimate trung tâm của phân phối.

Ký hiệu:

$$
\boldsymbol{\mu}
$$

Trong landmark:

$$
\boldsymbol{\mu}_j
$$

là vị trí landmark được ước lượng.

---

## 7.8 Covariance

**Covariance** mô tả mức độ uncertainty và sự tương quan giữa các biến.

Ký hiệu:

$$
\Sigma
$$

---

## 7.9 Variance

**Variance** là phương sai của một biến.

Nếu:

$$
\sigma^2
$$

lớn, uncertainty của biến tương ứng lớn hơn.

---

## 7.10 Uncertainty

**Uncertainty** (độ không chắc chắn) mô tả mức độ không biết chính xác giá trị thật.

Trong SLAM, uncertainty xuất hiện ở:

* robot pose;
* landmark position;
* sensor measurement;
* motion;
* particle weights.

---

# 8. Bayesian Filtering

## 8.1 Bayesian Filtering

**Bayesian filtering** là nhóm phương pháp ước lượng trạng thái động dựa trên mô hình xác suất.

Chu trình cơ bản:

```text
Prediction
    ↓
Correction
```

FastSLAM có thể được xem là một phương pháp Bayesian filtering sử dụng Particle Filter và EKF.

---

## 8.2 Prediction

**Prediction** là bước dự đoán trạng thái dựa trên trạng thái trước đó và motion.

Ví dụ:

$$
p(x_t\mid x_{t-1},u_t)
$$

---

## 8.3 Correction / Update

**Correction** hoặc **Update** là bước sử dụng observation mới để điều chỉnh estimate.

```text
prediction
    ↓
measurement
    ↓
update
```

---

# 9. Particle Filter

## 9.1 Particle Filter

**Particle Filter** là phương pháp biểu diễn probability distribution bằng một tập các samples gọi là particle.

Một particle có dạng khái niệm:

$$
P^{[i]}
=
(x^{[i]},w^{[i]})
$$

---

## 9.2 Particle

**Particle** là một giả thuyết về trạng thái hiện tại.

Trong FastSLAM, particle không chỉ chứa pose mà còn chứa map riêng.

```text
Particle
├── pose
├── weight
└── landmark map
```

---

## 9.3 Particle Weight

**Particle weight** là mức độ phù hợp của particle với observations.

Ký hiệu:

$$
w_i
$$

Weight càng cao thì particle càng phù hợp với dữ liệu quan sát.

---

## 9.4 Sampling

**Sampling** là quá trình lấy mẫu trạng thái mới từ probability distribution.

Trong FastSLAM:

$$
x_t^{[i]}
\sim
p(x_t\mid x_{t-1}^{[i]},u_t)
$$

---

## 9.5 Weighting

**Weighting** là quá trình tính trọng số cho particle dựa trên observation likelihood.

$$
w_i
\propto
p(z_t\mid x_t^{[i]},m^{[i]})
$$

---

## 9.6 Normalization

**Normalization** là quá trình biến các weight thành tổng bằng 1:

$$
\bar{w}_i
=
\frac{w_i}
{\sum_j w_j}
$$

---

## 9.7 Resampling

**Resampling** là quá trình tạo particle set mới dựa trên normalized weights.

Particle có weight cao có xác suất được chọn nhiều hơn.

---

## 9.8 Systematic Resampling

**Systematic Resampling** là một phương pháp Resampling sử dụng các điểm lấy mẫu cách đều nhau trên cumulative distribution.

Đây là phương pháp được sử dụng trong implementation cơ sở.

---

## 9.9 Low-variance Resampling

**Low-variance Resampling** là tên thường dùng cho nhóm phương pháp Resampling có variance thấp, trong đó systematic resampling là một cách triển khai phổ biến.

---

## 9.10 Effective Sample Size — ESS

**Effective Sample Size** đo mức độ đa dạng hiệu dụng của particle set.

$$
N_{\mathrm{eff}}
=
\frac{1}
{\sum_i w_i^2}
$$

Nếu \(N_{\mathrm{eff}}\) thấp, particle set có dấu hiệu degeneracy.

---

## 9.11 Particle Degeneracy

**Particle degeneracy** xảy ra khi chỉ một số rất ít particle có weight đáng kể.

Ví dụ:

```text
P1 → 0.99
P2 → 0.003
P3 → 0.002
...
```

Điều này làm giảm diversity của particle set.

---

## 9.12 Particle Depletion

**Particle depletion** là hiện tượng particle diversity giảm mạnh sau nhiều lần Resampling.

Degeneracy và depletion có liên quan nhưng không hoàn toàn đồng nghĩa.

---

# 10. Rao-Blackwellization

## 10.1 Rao-Blackwellization

**Rao-Blackwellization** là kỹ thuật tận dụng việc một phần của phân phối xác suất có thể được tính analytically thay vì sampling.

Trong FastSLAM:

```text
Robot trajectory
      ↓
Particle Filter

Landmarks | trajectory
      ↓
EKF
```

---

## 10.2 Rao-Blackwellized Particle Filter — RBPF

**Rao-Blackwellized Particle Filter (RBPF)** là Particle Filter trong đó một phần trạng thái được marginalized / tính toán có điều kiện.

FastSLAM là một ví dụ nổi tiếng của RBPF.

---

## 10.3 Marginalization

**Marginalization** là quá trình loại bỏ một biến khỏi probability distribution bằng cách tích phân hoặc tổng hóa biến đó.

Khái niệm này là nền tảng để hiểu tại sao FastSLAM có thể phân tách bài toán.

---

# 11. EKF

## 11.1 Kalman Filter

**Kalman Filter (KF)** là bộ lọc tối ưu cho một số mô hình tuyến tính với Gaussian noise.

KF sử dụng:

```text
Prediction
+
Measurement Update
```

---

## 11.2 Extended Kalman Filter — EKF

**Extended Kalman Filter (EKF)** mở rộng Kalman Filter cho hệ thống phi tuyến bằng cách tuyến tính hóa quanh estimate hiện tại.

Nếu:

$$
z=h(x)+v
$$

thì EKF sử dụng Jacobian của \(h\).

Trong FastSLAM, mỗi landmark có một EKF riêng.

---

## 11.3 EKF Prediction

Bước dự đoán của EKF sử dụng motion model để dự đoán trạng thái và covariance.

Trong FastSLAM landmark EKF, phần quan trọng nhất là measurement update.

---

## 11.4 EKF Measurement Update

Measurement update sử dụng observation để điều chỉnh landmark estimate.

Chu trình:

```text
predicted observation
        ↓
innovation
        ↓
innovation covariance
        ↓
Kalman Gain
        ↓
state update
        ↓
covariance update
```

---

## 11.5 Kalman Gain

**Kalman Gain** xác định mức độ measurement ảnh hưởng đến estimate.

$$
K=
\Sigma H^T
(H\Sigma H^T+Q)^{-1}
$$

---

## 11.6 Innovation

**Innovation** là sai khác giữa observation thực tế và observation dự đoán.

$$
\nu=z-\hat{z}
$$

Trong bearing, innovation phải được angle-normalized.

---

## 11.7 Innovation Covariance

**Innovation covariance** mô tả uncertainty của innovation.

$$
S=
H\Sigma H^T+Q
$$

---

## 11.8 Joseph Form

**Joseph Form** là dạng ổn định hơn để cập nhật covariance:

$$
\Sigma'
=
(I-KH)\Sigma(I-KH)^T
+
KQK^T
$$

Nó giúp giảm một số vấn đề numerical stability.

---

# 12. Jacobian và Linearization

## 12.1 Jacobian

**Jacobian** là ma trận đạo hàm riêng của một vector-valued function.

$$
J=
\frac{\partial f}{\partial x}
$$

Jacobian được dùng để tuyến tính hóa mô hình phi tuyến trong EKF.

---

## 12.2 Linearization

**Linearization** là quá trình xấp xỉ một hàm phi tuyến bằng mô hình tuyến tính quanh một điểm.

$$
f(x+\Delta x)
\approx
f(x)+J\Delta x
$$

EKF dựa trên ý tưởng này.

---

# 13. Observation Model

## 13.1 Observation Model

**Observation model** mô tả cách sensor measurement phụ thuộc vào robot pose và landmark.

Trong project:

$$
z=h(x,m)+v
$$

với:

* \(x\): robot pose;
* \(m\): landmark;
* \(v\): sensor noise.

---

## 13.2 Motion Model

**Motion model** mô tả cách robot thay đổi trạng thái khi nhận control hoặc odometry.

Dạng xác suất:

$$
p(x_t\mid x_{t-1},u_t)
$$

---

## 13.3 Sensor Model

**Sensor model** mô tả xác suất sensor tạo ra observation khi robot và môi trường ở một trạng thái cụ thể.

Ví dụ:

$$
p(z_t\mid x_t,m)
$$

---

# 14. Data Association

## 14.1 Data Association

**Data Association** là quá trình xác định observation hiện tại tương ứng với landmark nào.

Đây là một trong những vấn đề quan trọng nhất của landmark-based SLAM.

---

## 14.2 Association Hypothesis

**Association hypothesis** là giả thuyết về việc observation \(z\) thuộc về landmark nào.

Ví dụ:

```text
z₁ → landmark 3
z₂ → landmark 7
z₃ → new landmark
```

---

## 14.3 Gating

**Gating** là quá trình loại bỏ các landmark ứng viên không đủ phù hợp với observation.

Trong project, gating dựa trên Mahalanobis distance.

---

## 14.4 Mahalanobis Distance

**Mahalanobis distance** đo khoảng cách giữa observation và prediction có xét đến covariance.

$$
d^2
=
\nu^T
S^{-1}
\nu
$$

Nó tốt hơn Euclidean distance trong trường hợp uncertainty theo các hướng khác nhau.

---

## 14.5 Association Threshold

**Association threshold** là ngưỡng quyết định observation có đủ gần một landmark để được xem là match hay không.

$$
d^2<\gamma
$$

Nếu không có landmark nào thỏa mãn, observation có thể được dùng để tạo landmark mới.

---

# 15. Probability và Numerical Stability

## 15.1 Log Probability

**Log probability** là logarithm của probability.

Thay vì:

$$
w=\prod_i p_i
$$

có thể tính:

$$
\log w
=
\sum_i\log p_i
$$

Điều này giúp tránh underflow.

---

## 15.2 Underflow

**Underflow** xảy ra khi số thực quá nhỏ khiến máy tính lưu thành 0.

Trong Particle Filter, việc nhân nhiều likelihood nhỏ có thể gây underflow.

Giải pháp là sử dụng log-weight.

---

## 15.3 Overflow

**Overflow** xảy ra khi giá trị vượt quá giới hạn biểu diễn của kiểu số.

Cần chú ý khi tính exponential hoặc probability density.

---

## 15.4 Numerical Stability

**Numerical stability** là khả năng thuật toán duy trì kết quả hợp lệ khi thực hiện tính toán floating-point.

Các vấn đề quan trọng:

* covariance không đối xứng;
* covariance không positive semi-definite;
* ma trận gần singular;
* underflow;
* overflow;
* division by zero.

---

## 15.5 Singular Matrix

**Singular matrix** là ma trận không khả nghịch.

Trong EKF, innovation covariance:

$$
S
$$

có thể trở nên gần singular nếu mô hình hoặc dữ liệu không hợp lệ.

Implementation nên ưu tiên giải hệ tuyến tính thay vì tính trực tiếp:

$$
S^{-1}
$$

---

## 15.6 Positive Semi-definite — PSD

Một covariance hợp lệ thường phải là **positive semi-definite**.

Điều kiện:

$$
\mathbf{x}^T\Sigma\mathbf{x}\geq0
$$

với mọi \(\mathbf{x}\).

---

## 15.7 Symmetric Matrix

Covariance lý tưởng phải thỏa:

$$
\Sigma=\Sigma^T
$$

Do numerical error, implementation có thể cần symmetrize:

$$
\Sigma
\leftarrow
\frac12
(\Sigma+\Sigma^T)
$$

---

# 16. Error và Evaluation

## 16.1 Error

**Error** là độ chênh lệch giữa estimate và ground truth.

---

## 16.2 Localization Error

**Localization error** là sai số giữa estimated pose và ground-truth pose.

Position error:

$$
e_p=
\sqrt{
(x-\hat{x})^2+
(y-\hat{y})^2
}
$$

---

## 16.3 Orientation Error

**Orientation error** là sai số orientation:

$$
e_\theta
=
\operatorname{normalizeAngle}
(\theta-\hat{\theta})
$$

---

## 16.4 Mapping Error

**Mapping error** là sai số giữa estimated landmark và ground-truth landmark tương ứng.

$$
e_m=
\left\|
m-\hat{m}
\right\|
$$

---

## 16.5 RMSE — Root Mean Square Error

**RMSE** là một metric thường dùng để đánh giá sai số:

$$
RMSE=
\sqrt{
\frac{1}{N}
\sum_{i=1}^{N}
e_i^2
}
$$

---

## 16.6 Mean Error

**Mean error** là trung bình của các error:

$$
\bar{e}
=
\frac1N
\sum_{i=1}^{N}
e_i
$$

---

## 16.7 Maximum Error

**Maximum error** là error lớn nhất trong toàn bộ trajectory hoặc tập dữ liệu:

$$
e_{\max}
=
\max_i e_i
$$

---

## 16.8 Random Seed

**Random seed** là giá trị khởi tạo bộ sinh số ngẫu nhiên.

FastSLAM có thành phần stochastic nên cùng một scenario có thể cho kết quả khác nhau nếu seed khác nhau.

Dùng fixed seed giúp:

* reproducibility;
* debugging;
* regression testing.

---

## 16.9 Reproducibility

**Reproducibility** là khả năng tái tạo lại kết quả của một experiment khi sử dụng cùng điều kiện.

Một experiment nên ghi lại:

```text
random seed
number of particles
sensor noise
motion noise
association threshold
environment
```

---

# 17. Navigation và Planning

## 17.1 Navigation

**Navigation** là quá trình quyết định và thực hiện cách robot di chuyển từ vị trí hiện tại đến mục tiêu.

Navigation sử dụng:

```text
estimated pose
map
goal
planner
controller
```

---

## 17.2 Path Planning

**Path Planning** là quá trình tìm một đường đi từ start đến goal.

FastSLAM cung cấp:

```text
estimated pose
estimated map
```

cho Path Planner.

---

## 17.3 Planner

**Planner** là module thực hiện Path Planning hoặc Coverage Planning.

Planner không nên được trộn với SLAM.

---

## 17.4 Controller

**Controller** biến path hoặc target motion thành command cho robot.

Ví dụ:

```text
target pose
    ↓
controller
    ↓
velocity / motion command
```

---

## 17.5 Motion Command

**Motion command** là command điều khiển robot di chuyển.

Có thể có dạng:

$$
u_t=
\begin{bmatrix}
\Delta s\\
\Delta\theta
\end{bmatrix}
$$

hoặc velocity:

$$
u_t=
\begin{bmatrix}
v\\
\omega
\end{bmatrix}
$$

---

# 18. SLAM Architecture

## 18.1 Frontend

**Frontend** là phần xử lý sensor data và tạo ra các measurement/constraints có ý nghĩa cho backend.

Trong một SLAM system lớn, frontend có thể bao gồm:

* feature extraction;
* feature matching;
* tracking;
* scan processing;
* Data Association.

Trong project FastSLAM đơn giản, frontend chủ yếu liên quan đến:

```text
LiDAR
  ↓
feature / landmark observation
  ↓
Data Association
```

---

## 18.2 Backend

**Backend** là phần thực hiện estimation / optimization trên các measurement.

Trong Graph SLAM, backend thường là graph optimization.

Trong FastSLAM, cấu trúc backend không giống Graph SLAM; Particle Filter + landmark EKF chính là phần estimation cốt lõi.

---

## 18.3 Estimator

**Estimator** là module ước lượng trạng thái từ các observation.

FastSLAM là một estimator.

---

## 18.4 State Estimation

**State Estimation** là quá trình ước lượng trạng thái ẩn của hệ thống từ sensor và motion information.

Trong project:

```text
odometry
+
LiDAR observations
        ↓
FastSLAM
        ↓
estimated pose + map
```

---

# 19. SLAM Representation

## 19.1 Landmark-based SLAM

**Landmark-based SLAM** biểu diễn môi trường bằng một tập landmark.

FastSLAM cơ sở thuộc nhóm này.

---

## 19.2 Occupancy Grid

**Occupancy grid** biểu diễn môi trường bằng một lưới trong đó mỗi cell có trạng thái hoặc xác suất bị chiếm.

Ví dụ:

```text
┌───┬───┬───┐
│ ? │ 0 │ 1 │
├───┼───┼───┤
│ 0 │ 0 │ 1 │
├───┼───┼───┤
│ 0 │ 0 │ 0 │
└───┴───┴───┘
```

Occupancy grid không phải representation chính của FastSLAM trong project.

---

## 19.3 Map Representation

**Map representation** là cách biểu diễn môi trường trong hệ thống.

Các dạng phổ biến:

* landmark map;
* occupancy grid;
* point cloud;
* topological map;
* pose graph.

Project sử dụng landmark map cho FastSLAM.

---

# 20. Các thuật ngữ SLAM liên quan

## 20.1 EKF-SLAM

**EKF-SLAM** sử dụng một EKF duy nhất để ước lượng robot pose và toàn bộ landmark map.

Khác với FastSLAM:

```text
EKF-SLAM
    ↓
một covariance lớn

FastSLAM
    ↓
Particle Filter
+
nhiều landmark EKF
```

---

## 20.2 Graph SLAM

**Graph SLAM** biểu diễn SLAM dưới dạng graph gồm:

* nodes;
* edges;
* constraints.

Sau đó giải một bài toán optimization.

Graph SLAM không phải thuật toán được sử dụng trong project hiện tại.

---

## 20.3 Visual SLAM

**Visual SLAM** sử dụng camera làm sensor chính.

Project hiện tại sử dụng 2D LiDAR nên không phải Visual SLAM.

---

## 20.4 RGB-D SLAM

**RGB-D SLAM** sử dụng camera RGB-D để đồng thời thu được màu và depth.

Không phải sensor model của project hiện tại.

---

## 20.5 Scan Matching

**Scan Matching** là quá trình tìm phép biến đổi giữa hai sensor scans sao cho chúng khớp nhau.

Scan Matching có thể được sử dụng trong các hệ thống LiDAR SLAM nhưng không phải core method của FastSLAM project.

---

## 20.6 ICP — Iterative Closest Point

**ICP** là thuật toán tìm phép biến đổi giữa hai point clouds dựa trên các correspondence giữa các điểm.

ICP không phải thuật toán FastSLAM.

---

## 20.7 Odometry

**Odometry** là thông tin về chuyển động tương đối của robot.

Ví dụ:

$$
\Delta x,\Delta y,\Delta\theta
$$

Odometry thường có drift theo thời gian.

FastSLAM sử dụng motion information nhưng dùng sensor observation để hiệu chỉnh estimate.

---

## 20.8 Drift

**Drift** là sai số tích lũy theo thời gian của odometry hoặc state estimate.

Nếu chỉ tích phân odometry:

```text
odometry
    ↓
pose
    ↓
pose
    ↓
pose
```

sai số có thể ngày càng lớn.

SLAM giúp giảm drift bằng cách sử dụng thông tin từ môi trường.

---

# 21. Software và Implementation

## 21.1 Module

**Module** là một thành phần phần mềm có trách nhiệm tương đối độc lập.

Ví dụ:

```text
sensor
motion
fastslam
planner
controller
visualization
evaluation
```

---

## 21.2 Interface

**Interface** là cách hai module trao đổi dữ liệu hoặc gọi chức năng của nhau.

Ví dụ:

```text
Sensor
    ↓
Observation
    ↓
FastSLAM
```

---

## 21.3 API

**API — Application Programming Interface** là tập các interface mà module hoặc software component cung cấp.

Trong project, API nội bộ có thể được dùng giữa:

```text
Simulator
FastSLAM
Planner
Controller
Evaluator
```

---

## 21.4 Configuration

**Configuration** là tập tham số điều khiển behavior của simulator và algorithm.

Ví dụ:

```text
particle_count
sensor_range
sensor_noise
motion_noise
association_threshold
```

Configuration không nên được hard-code vào logic thuật toán nếu có thể tránh.

---

## 21.5 Visualization

**Visualization** là phần hiển thị trạng thái simulator và kết quả SLAM.

Có thể hiển thị:

```text
Ground-truth map
Estimated map
Ground-truth pose
Estimated pose
LiDAR scan
Particle cloud
Trajectory
```

Visualization không được làm thay đổi kết quả của FastSLAM.

---

# 22. Requirements-related Terminology

## 22.1 Functional Requirement

**Functional Requirement** là yêu cầu mô tả hệ thống phải làm gì.

Ví dụ:

> Simulator phải tạo được environment 2D.

---

## 22.2 Non-functional Requirement

**Non-functional Requirement** mô tả hệ thống phải có đặc tính như thế nào.

Ví dụ:

* reproducible;
* configurable;
* extensible;
* sufficiently fast.

---

## 22.3 Requirement

**Requirement** là điều kiện hoặc capability mà hệ thống phải đáp ứng.

Requirements trả lời câu hỏi:

> **What must the system do?**

Không phải:

> How should the algorithm be implemented?

---

## 22.4 Constraint

**Constraint** là giới hạn mà implementation phải tuân thủ.

Ví dụ:

```text
FastSLAM phải được tự cài đặt.
Ground Truth không được cung cấp trực tiếp cho SLAM.
```

---

## 22.5 Assumption

**Assumption** là giả định được đưa ra để giới hạn phạm vi của bài toán.

Ví dụ:

```text
environment là 2D
landmark là static
sensor noise có thể mô hình hóa bằng Gaussian
```

---

## 22.6 Acceptance Criteria

**Acceptance Criteria** là điều kiện dùng để xác định một requirement đã được đáp ứng hay chưa.

Ví dụ:

```text
FastSLAM chạy được trên scenario cơ bản
estimated trajectory có thể được so sánh với ground truth
```

---

# 23. Testing Terminology

## 23.1 Unit Test

**Unit Test** kiểm thử một thành phần nhỏ độc lập.

Ví dụ:

```text
normalizeAngle()
```

---

## 23.2 Integration Test

**Integration Test** kiểm tra sự tương tác giữa nhiều module.

Ví dụ:

```text
Sensor
  ↓
Observation
  ↓
FastSLAM
```

---

## 23.3 System Test

**System Test** kiểm thử toàn bộ simulator.

Ví dụ:

```text
Environment
+
Robot
+
Sensor
+
FastSLAM
+
Planner
+
Controller
```

---

## 23.4 Regression Test

**Regression Test** kiểm tra rằng thay đổi mới không làm hỏng behavior đã hoạt động trước đó.

---

## 23.5 Scenario

**Scenario** là một cấu hình cụ thể của environment, robot và experiment.

Ví dụ:

```text
Scenario:
    10 landmarks
    100 particles
    sensor noise = ...
    robot trajectory = ...
```

---

## 23.6 Benchmark

**Benchmark** là scenario hoặc tập scenario được chuẩn hóa để so sánh performance.

---

# 24. Complexity và Performance

## 24.1 Computational Complexity

**Computational Complexity** mô tả mức độ tăng của lượng tính toán theo kích thước input.

FastSLAM implementation đơn giản của project có thể có:

$$
O(NKM)
$$

với:

* \(N\): số particle;
* \(K\): số observation;
* \(M\): số landmark.

---

## 24.2 Runtime

**Runtime** là thời gian chương trình cần để thực hiện một task.

Có thể đo:

```text
time per timestep
time per scan
total simulation time
```

---

## 24.3 Real-time

**Real-time** nghĩa là hệ thống phải xử lý dữ liệu đủ nhanh để đáp ứng tốc độ hoạt động của hệ thống vật lý hoặc simulator.

Project mô phỏng không nhất thiết phải real-time, trừ khi requirement quy định.

---

## 24.4 Scalability

**Scalability** là khả năng hệ thống tiếp tục hoạt động khi quy mô bài toán tăng.

Các yếu tố ảnh hưởng:

```text
number of particles
number of landmarks
number of observations
map size
```

---

# 25. Các thuật ngữ quan trọng cần phân biệt

## 25.1 Measurement vs Observation

**Measurement** là dữ liệu trực tiếp từ sensor.

**Observation** là representation của measurement phù hợp với estimator.

```text
Sensor
 ↓
Measurement
 ↓
Processing
 ↓
Observation
```

Trong implementation đơn giản, hai khái niệm này có thể gần như trùng nhau, nhưng về mặt kiến trúc nên phân biệt.

---

## 25.2 Ground Truth vs Estimate

**Ground Truth** là giá trị thật trong simulator.

**Estimate** là giá trị do thuật toán suy ra.

```text
Ground Truth
    ≠
Estimate
```

Đây là một trong những phân biệt quan trọng nhất của project.

---

## 25.3 Map vs Ground-truth Map

**Map** trong ngữ cảnh SLAM thường là estimated map.

**Ground-truth map** là map thật được simulator biết.

---

## 25.4 Pose vs Position

```text
Position = (x, y)

Pose = (x, y, theta)
```

Pose chứa orientation, position thì không.

---

## 25.5 Motion vs Control

**Motion** là sự thay đổi trạng thái thực tế của robot.

**Control** là command được gửi cho robot.

Ví dụ:

```text
control
  ↓
robot motion
  ↓
odometry
```

Trong simulator, control và motion có thể được mô hình hóa khác nhau.

---

## 25.6 Sensor Model vs Observation Model

**Sensor Model** là khái niệm rộng về cách sensor tạo measurement.

**Observation Model** trong SLAM thường mô tả trực tiếp quan hệ:

$$
z=h(x,m)+v
$$

Observation model là một phần cụ thể hơn của sensor model trong ngữ cảnh estimator.

---

## 25.7 Landmark vs Feature

**Feature** là đặc trưng được trích xuất từ sensor data.

**Landmark** là feature được chọn và biểu diễn như một mốc có thể được theo dõi trong map.

Trong implementation đơn giản, hai khái niệm có thể gần như tương đương.

---

## 25.8 Localization vs Navigation

**Localization** trả lời:

> Robot đang ở đâu?

**Navigation** trả lời:

> Robot nên đi đâu và đi như thế nào?

FastSLAM thuộc Localization/Mapping, không phải Navigation.

---

## 25.9 Mapping vs Path Planning

**Mapping** xây dựng representation của environment.

**Path Planning** tìm đường đi trên representation đó.

```text
Mapping
   ↓
Map
   ↓
Path Planning
   ↓
Path
```

---

# 26. Thuật ngữ cốt lõi của project

Nếu chỉ cần nhớ những thuật ngữ quan trọng nhất để làm project, cần nắm:

```text
SLAM
Localization
Mapping
Pose
Trajectory
Ground Truth
Estimate

2D LiDAR
Scan
Range
Bearing
Observation
Sensor Noise

Landmark
Landmark Map
Data Association
Mahalanobis Distance
Gating

Probability
Prior
Likelihood
Posterior
Gaussian
Mean
Covariance
Uncertainty

Particle Filter
Particle
Weight
Sampling
Normalization
Resampling
Systematic Resampling
Effective Sample Size
Particle Degeneracy

Rao-Blackwellization
Rao-Blackwellized Particle Filter

Kalman Filter
EKF
Innovation
Innovation Covariance
Kalman Gain
Jacobian
Linearization

Motion Model
Observation Model
Sensor Model

Coordinate Frame
World Frame
Robot Frame
Coordinate Transformation
SE(2)

Odometry
Drift

Path Planning
Coverage
Navigation
Controller

Simulation
Scenario
Ground Truth
Evaluation
RMSE
Random Seed
Reproducibility
```

---

# 27. Quan hệ giữa các thuật ngữ

Toàn bộ project có thể được nhìn dưới dạng:

```text
                         SLAM
                          │
              ┌───────────┴───────────┐
              │                       │
        Localization               Mapping
              │                       │
              └───────────┬───────────┘
                          │
                     FastSLAM
                          │
             ┌────────────┴────────────┐
             │                         │
       Particle Filter                EKF
             │                         │
       Robot trajectory            Landmark
             │                         │
             └────────────┬────────────┘
                          │
                    Data Association
                          │
                    LiDAR Observation
                          │
                    Sensor Simulation
                          │
                       Simulator
```

Ở tầng hệ thống:

```text
                 Simulator
                     │
        ┌────────────┴────────────┐
        │                         │
   Ground Truth                Robot
        │                         │
        │                    LiDAR / Motion
        │                         │
        │                         ▼
        │                    Observations
        │                         │
        │                         ▼
        │                     FastSLAM
        │                         │
        │              ┌──────────┴──────────┐
        │              │                     │
        │          Estimated Pose       Estimated Map
        │              │                     │
        │              └──────────┬──────────┘
        │                         │
        │                    Path Planning
        │                         │
        │                     Controller
        │                         │
        └─────────────────────────┘
                    Evaluation
```

---

# 28. Phân loại thuật ngữ theo tài liệu

## `requirements.md`

Các thuật ngữ liên quan nhiều nhất:

```text
Simulator
Environment
Robot
Exploration
Cleaning
Sensor
LiDAR
Ground Truth
Map
Pose
Path Planning
Coverage
Charging Station
Visualization
Evaluation
Functional Requirement
Non-functional Requirement
```

## `algorithm.md`

Các thuật ngữ liên quan trực tiếp:

```text
FastSLAM
Particle Filter
Rao-Blackwellized Particle Filter
Particle
Landmark
Motion Model
Observation Model
Sensor Model
Data Association
Mahalanobis Distance
EKF
Jacobian
Innovation
Covariance
Kalman Gain
Likelihood
Weight
Resampling
Effective Sample Size
```

## Kiến thức bổ trợ

```text
Bayes
Probability Distribution
Gaussian
Mean
Variance
Covariance
Uncertainty
Bayesian Filtering
Kalman Filter
Linearization
SE(2)
Coordinate Transformation
Numerical Stability
RMSE
Reproducibility
```

---

# 29. Tài liệu tham khảo thuật ngữ

Các thuật ngữ trong tài liệu này được sử dụng theo cách phổ biến trong các lĩnh vực:

* Probabilistic Robotics;
* SLAM;
* State Estimation;
* Robotics;
* Bayesian Filtering;
* Computer Vision / LiDAR processing;
* Robot Navigation.

Nguồn kiến thức nền tảng chính:

1. Sebastian Thrun, Wolfram Burgard, Dieter Fox — *Probabilistic Robotics*.
2. Michael Montemerlo et al. — *FastSLAM: A Factored Solution to the Simultaneous Localization and Mapping Problem*.
3. Michael Montemerlo et al. — *FastSLAM 2.0: An Improved Particle Filtering Algorithm for Simultaneous Localization and Mapping that Probably Works*.
4. Arnaud Doucet et al. — *Rao-Blackwellised Particle Filtering for Dynamic Bayesian Networks*.

---

# 30. Quy ước sử dụng thuật ngữ trong project

Để tránh việc mỗi thành viên sử dụng một cách gọi khác nhau, project nên ưu tiên các thuật ngữ sau:

| Khái niệm                | Thuật ngữ nên dùng               |
| ------------------------ | -------------------------------- |
| Định vị                  | **Localization**                 |
| Lập bản đồ               | **Mapping**                      |
| Tư thế robot             | **Pose**                         |
| Vị trí                   | **Position**                     |
| Hướng                    | **Orientation**                  |
| Mốc                      | **Landmark**                     |
| Bản đồ landmark          | **Landmark Map**                 |
| Hệ tọa độ thế giới       | **World Frame**                  |
| Hệ tọa độ robot          | **Robot Frame**                  |
| Cảm biến                 | **Sensor**                       |
| Quét LiDAR               | **LiDAR Scan**                   |
| Khoảng cách              | **Range**                        |
| Góc quan sát             | **Bearing**                      |
| Nhiễu                    | **Noise**                        |
| Độ không chắc chắn       | **Uncertainty**                  |
| Hiệp phương sai          | **Covariance**                   |
| Trung bình               | **Mean**                         |
| Sai số quan sát          | **Innovation**                   |
| Ghép quan sát            | **Data Association**             |
| Khoảng cách Mahalanobis  | **Mahalanobis Distance**         |
| Bộ lọc Kalman mở rộng    | **Extended Kalman Filter (EKF)** |
| Bộ lọc hạt               | **Particle Filter**              |
| Hạt                      | **Particle**                     |
| Trọng số                 | **Weight**                       |
| Lấy mẫu                  | **Sampling**                     |
| Tái lấy mẫu              | **Resampling**                   |
| Kích thước mẫu hiệu dụng | **Effective Sample Size (ESS)**  |
| Mô hình chuyển động      | **Motion Model**                 |
| Mô hình quan sát         | **Observation Model**            |
| Mô hình cảm biến         | **Sensor Model**                 |
| Sự thật chuẩn            | **Ground Truth**                 |
| Ước lượng                | **Estimate**                     |
| Định tuyến/lập đường     | **Path Planning**                |
| Phủ kín khu vực          | **Coverage**                     |
| Điều khiển               | **Control / Controller**         |
| Mô phỏng                 | **Simulation**                   |
| Kiểm thử                 | **Testing**                      |
| Đánh giá                 | **Evaluation**                   |
| Tính tái lập             | **Reproducibility**              |

---

# 31. Kết luận

`terms.md` là tài liệu tham chiếu thuật ngữ chung của project.

Mục tiêu của tài liệu không phải thay thế `algorithm.md` hoặc `requirements.md`, mà tạo một vocabulary thống nhất giữa các thành viên.

Ba tài liệu có vai trò:

```text
requirements.md
        │
        │ WHAT?
        ▼
Hệ thống phải làm gì?


architecture.md
        │
        │ HOW?
        ▼
Hệ thống được tổ chức như thế nào?


algorithm.md
        │
        │ HOW?
        ▼
FastSLAM hoạt động như thế nào?


terms.md
        │
        │ WHAT DOES EACH TERM MEAN?
        ▼
Các thuật ngữ trong toàn bộ project có nghĩa gì?
```

Trong đó:

> **`terms.md` là glossary dùng chung cho toàn bộ project; thuật ngữ ưu tiên English để giữ tính nhất quán với tài liệu kỹ thuật, còn phần giải thích được viết bằng tiếng Việt.**

