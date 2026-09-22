# Demo SLAM - chatgpt

import math
import heapq
from collections import deque

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ============================================================
# Configuration
# ============================================================
N = 31                    # odd number: 7, 15, 21, 31, ...
SEED = 7

S = (1, 1)               # start: (row, col)
D = (N - 2, N - 2)       # destination

LIDAR_BEAMS = 16
LIDAR_MAX_RANGE = 8.0
RAY_STEP = 0.10

ODOM_DISTANCE_STD = 0.010
ODOM_HEADING_STD = math.radians(0.3)
LIDAR_NOISE_STD = 0.015

LO_FREE, LO_OCC = -0.30, +0.90
LO_MIN, LO_MAX = -4.0, +4.0
FREE_THRESHOLD, OCC_THRESHOLD = -0.60, +1.50

MAX_FRAMES = 900
MOVE_EVERY = 3
FRAME_MS = 55

BEAM_ANGLES = np.linspace(0, 2*np.pi, LIDAR_BEAMS, endpoint=False)


# ============================================================
# Grid / path utilities
# ============================================================
def wrap(a):
    return (a + np.pi) % (2*np.pi) - np.pi


def center(rc):
    r, c = rc
    return np.array([c + 0.5, r + 0.5], float)


def cell(x, y):
    return int(math.floor(y)), int(math.floor(x))


def inside(r, c):
    return 0 <= r < N and 0 <= c < N


def nbr4(r, c):
    for dr, dc in ((-1,0), (1,0), (0,-1), (0,1)):
        rr, cc = r + dr, c + dc
        if inside(rr, cc):
            yield rr, cc


def bfs(maze, start, goal):
    q = deque([start])
    parent = {start: None}

    while q:
        u = q.popleft()
        if u == goal:
            break
        for v in nbr4(*u):
            if maze[v] or v in parent:
                continue
            parent[v] = u
            q.append(v)

    if goal not in parent:
        return None

    path, u = [], goal
    while u is not None:
        path.append(u)
        u = parent[u]
    return path[::-1]


def astar(maze, start, goal):
    pq = [(0, start)]
    g = {start: 0}
    parent = {start: None}

    while pq:
        _, u = heapq.heappop(pq)
        if u == goal:
            break

        for v in nbr4(*u):
            if maze[v]:
                continue

            ng = g[u] + 1
            if ng >= g.get(v, 10**9):
                continue

            g[v] = ng
            h = abs(goal[0] - v[0]) + abs(goal[1] - v[1])
            heapq.heappush(pq, (ng + h, v))
            parent[v] = u

    if goal not in parent:
        return None

    path, u = [], goal
    while u is not None:
        path.append(u)
        u = parent[u]
    return path[::-1]


# ============================================================
# Random maze
# ============================================================
def make_maze():
    if N < 7 or N % 2 == 0:
        raise ValueError("N must be odd and >= 7.")

    rng = np.random.default_rng(SEED)
    maze = np.ones((N, N), dtype=bool)
    maze[S] = False

    stack = [S]
    while stack:
        r, c = stack[-1]
        cand = []

        for dr, dc in ((-2,0), (2,0), (0,-2), (0,2)):
            rr, cc = r + dr, c + dc
            if 1 <= rr < N-1 and 1 <= cc < N-1 and maze[rr, cc]:
                cand.append((rr, cc, dr//2, dc//2))

        if not cand:
            stack.pop()
            continue

        rr, cc, wr, wc = cand[rng.integers(len(cand))]
        maze[r+wr, c+wc] = False
        maze[rr, cc] = False
        stack.append((rr, cc))

    maze[S] = maze[D] = False
    return maze


# ============================================================
# LiDAR simulation
# ============================================================
def ray_cast(maze, pose, rel_angle):
    x, y, th = pose
    a = th + rel_angle

    d = 0.05
    while d <= LIDAR_MAX_RANGE:
        rr, cc = cell(
            x + d * math.cos(a),
            y + d * math.sin(a),
        )

        if not inside(rr, cc) or maze[rr, cc]:
            return d, True

        d += RAY_STEP

    return LIDAR_MAX_RANGE, False


def scan(maze, true_pose, rng):
    out, hits = [], []

    for a in BEAM_ANGLES:
        d, hit = ray_cast(maze, true_pose, a)
        d = np.clip(d + rng.normal(0, LIDAR_NOISE_STD),
                    0.05, LIDAR_MAX_RANGE)
        out.append(float(d))
        hits.append(hit)

    return np.asarray(out), np.asarray(hits, bool)


# ============================================================
# Occupancy grid mapping
# ============================================================
def ray_cells(pose, rel_angle, distance):
    x, y, th = pose
    a = th + rel_angle

    for i in range(1, max(1, int(distance / RAY_STEP)) + 1):
        d = min(i * RAY_STEP, distance)
        yield cell(
            x + d * math.cos(a),
            y + d * math.sin(a),
        )


def update_map(logodds, pose, ranges, hits):
    for a, d, hit in zip(BEAM_ANGLES, ranges, hits):
        cells = list(ray_cells(pose, a, d))
        if not cells:
            continue

        free = cells[:-1] if hit else cells

        prev = None
        for r, c in free:
            if (r, c) == prev:
                continue
            prev = (r, c)
            if inside(r, c):
                logodds[r, c] = np.clip(
                    logodds[r, c] + LO_FREE, LO_MIN, LO_MAX
                )

        if hit:
            r, c = cells[-1]
            if inside(r, c):
                logodds[r, c] = np.clip(
                    logodds[r, c] + LO_OCC, LO_MIN, LO_MAX
                )


# ============================================================
# Simplified scan matching
# ============================================================
def endpoint(pose, rel_angle, distance):
    a = pose[2] + rel_angle
    return np.array([
        pose[0] + distance * math.cos(a),
        pose[1] + distance * math.sin(a),
    ])


def scan_score(logodds, pose, ranges, hits):
    if not (
        0.5 <= pose[0] < N - 0.5 and
        0.5 <= pose[1] < N - 0.5
    ):
        return -1e9

    r0, c0 = cell(pose[0], pose[1])
    score = 1.0 if logodds[r0, c0] <= FREE_THRESHOLD else 0.0

    if logodds[r0, c0] >= OCC_THRESHOLD:
        score -= 10.0

    for a, d, hit in zip(BEAM_ANGLES, ranges, hits):
        r, c = cell(*endpoint(pose, a, d))
        if not inside(r, c):
            continue

        v = logodds[r, c]
        if hit:
            score += 2.5 * max(v, 0.0)
            score -= 1.5 * max(-v, 0.0)
        else:
            score += 1.0 * max(-v, 0.0)
            score -= 0.5 * max(v, 0.0)

        rr, cc = cell(*endpoint(pose, a, 0.6*d))
        if inside(rr, cc):
            fv = logodds[rr, cc]
            score += 0.8 * max(-fv, 0.0)
            score -= 0.9 * max(fv, 0.0)

    return score


def scan_match(logodds, predicted, ranges, hits):
    if np.count_nonzero(np.abs(logodds) > 0.30) < 25:
        return predicted.copy()

    best = predicted.copy()
    best_score = scan_score(logodds, best, ranges, hits)

    for dx in (-0.35, 0.0, 0.35):
        for dy in (-0.35, 0.0, 0.35):
            for da in (
                math.radians(-6),
                0.0,
                math.radians(6),
            ):
                cand = np.array([
                    predicted[0] + dx,
                    predicted[1] + dy,
                    wrap(predicted[2] + da),
                ])

                s = scan_score(logodds, cand, ranges, hits)

                # Odometry prior: prevent scan matching from teleporting
                # between visually similar maze corridors.
                s -= 3.5 * math.hypot(dx, dy)
                s -= 0.5 * abs(da)

                if s > best_score:
                    best_score = s
                    best = cand

    return best


# ============================================================
# Demo
# ============================================================
class Demo:
    def __init__(self):
        self.rng = np.random.default_rng(SEED)

        self.maze = make_maze()

        # Explicit validity check requested in the spec.
        self.bfs_path = bfs(self.maze, S, D)
        if self.bfs_path is None:
            raise RuntimeError("Maze validation failed: no S -> D path.")

        self.global_path = astar(self.maze, S, D)
        if self.global_path is None:
            raise RuntimeError("A* failed although BFS found a path.")

        # Robot's hidden true state.
        p = center(S)
        self.true = np.array([p[0], p[1], 0.0])

        # Robot's estimated state.
        self.est = self.true.copy()

        # 0 = unknown, negative = free, positive = occupied.
        self.logodds = np.zeros((N, N), float)
        self.logodds[S] = LO_MIN
        self.logodds[D] = LO_MIN

        self.ranges, self.hits = scan(
            self.maze, self.true, self.rng
        )
        update_map(
            self.logodds, self.est,
            self.ranges, self.hits
        )

        self.true_trace = [self.true.copy()]
        self.est_trace = [self.est.copy()]

        self.route_i = 1
        self.frame = 0
        self.moves = 0
        self.reached = False

    def route_heading(self):
        if self.route_i >= len(self.global_path):
            return self.est[2]

        a = self.global_path[self.route_i - 1]
        b = self.global_path[self.route_i]
        dr = b[0] - a[0]
        dc = b[1] - a[1]
        return math.atan2(dr, dc)

    def move_one_cell(self):
        if self.route_i >= len(self.global_path):
            return 0.0, self.true[2]

        prev = self.global_path[self.route_i - 1]
        nxt = self.global_path[self.route_i]

        if self.maze[nxt]:
            raise RuntimeError(f"Route enters a wall: {nxt}")

        heading = math.atan2(
            nxt[0] - prev[0],
            nxt[1] - prev[1],
        )

        self.true[:2] = center(nxt)
        self.true[2] = heading
        self.route_i += 1
        self.moves += 1

        return 1.0, heading

    def slam_cycle(self, distance, motion_heading):
        # 1) Odometry prediction
        h = (
            self.est[2]
            if motion_heading is None
            else motion_heading
        )

        predicted = np.array([
            self.est[0]
            + (
                distance
                + self.rng.normal(0, ODOM_DISTANCE_STD)
            ) * math.cos(h),

            self.est[1]
            + (
                distance
                + self.rng.normal(0, ODOM_DISTANCE_STD)
            ) * math.sin(h),

            wrap(h + self.rng.normal(0, ODOM_HEADING_STD)),
        ])

        # 2) Sensor
        self.ranges, self.hits = scan(
            self.maze,
            self.true,
            self.rng,
        )

        # 3) Correlative scan matching
        matched = scan_match(
            self.logodds,
            predicted,
            self.ranges,
            self.hits,
        )

        # Conservative fusion:
        # odometry remains dominant; scan matching removes some drift.
        alpha = 0.02
        dh = wrap(matched[2] - predicted[2])

        self.est = np.array([
            predicted[0] + alpha * (matched[0] - predicted[0]),
            predicted[1] + alpha * (matched[1] - predicted[1]),
            wrap(predicted[2] + alpha * dh),
        ])

        self.est[0] = np.clip(self.est[0], 0.5, N - 0.5)
        self.est[1] = np.clip(self.est[1], 0.5, N - 0.5)

        # 4) Mapping: use ESTIMATED pose, never the true pose.
        update_map(
            self.logodds,
            self.est,
            self.ranges,
            self.hits,
        )

        self.logodds[S] = LO_MIN
        self.logodds[D] = LO_MIN

    def step(self):
        if self.reached:
            return

        distance = 0.0
        motion_heading = None

        if (
            self.frame % MOVE_EVERY == 0
            and self.route_i < len(self.global_path)
        ):
            distance, motion_heading = self.move_one_cell()

        self.slam_cycle(
            distance,
            motion_heading,
        )

        self.true_trace.append(self.true.copy())
        self.est_trace.append(self.est.copy())
        self.frame += 1

        if self.route_i >= len(self.global_path):
            self.reached = True

    def map_image(self):
        # black = occupied, white = free, gray = unknown
        img = np.full((N, N), 0.5)
        img[self.logodds <= FREE_THRESHOLD] = 1.0
        img[self.logodds >= OCC_THRESHOLD] = 0.0
        return img

    def setup(self):
        self.fig, (self.ax0, self.ax1) = plt.subplots(
            1, 2, figsize=(12, 6)
        )

        self.fig.suptitle(
            "Simplified LiDAR SLAM — Automotive Localization & Navigation",
            fontsize=13,
        )

        self.ax0.imshow(
            self.maze,
            cmap="gray_r",
            origin="upper",
            interpolation="nearest",
        )
        self.ax0.set_title("Ground truth maze")

        self.map_im = self.ax1.imshow(
            self.map_image(),
            cmap="gray",
            origin="upper",
            interpolation="nearest",
            vmin=0, vmax=1,
        )
        self.ax1.set_title("Robot's SLAM occupancy map")

        for ax in (self.ax0, self.ax1):
            ax.set_xlim(-0.5, N - 0.5)
            ax.set_ylim(N - 0.5, -0.5)
            ax.set_xticks([])
            ax.set_yticks([])

            sr, sc = S
            dr, dc = D
            ax.text(
                sc, sr, "S",
                ha="center", va="center",
                fontsize=11, fontweight="bold",
            )
            ax.text(
                dc, dr, "D",
                ha="center", va="center",
                fontsize=11, fontweight="bold",
            )

        self.tline, = self.ax0.plot([], [], lw=1.3)
        self.eline, = self.ax1.plot([], [], lw=1.3)

        self.tcar = self.ax0.text(
            self.true[0] - 0.2,
            self.true[1],
            "O",
            fontsize=11,
            fontweight="bold",
        )
        self.ecar = self.ax1.text(
            self.est[0] - 0.2,
            self.est[1],
            "O",
            fontsize=11,
            fontweight="bold",
        )

        self.ray_lines = []
        for _ in BEAM_ANGLES:
            line, = self.ax0.plot([], [], lw=0.6, alpha=0.35)
            self.ray_lines.append(line)

        self.info = self.fig.text(
            0.02, 0.015, "", fontsize=9
        )

    def update(self, _):
        self.step()

        t = np.asarray(self.true_trace)
        e = np.asarray(self.est_trace)

        self.tline.set_data(t[:, 0], t[:, 1])
        self.eline.set_data(e[:, 0], e[:, 1])

        self.tcar.set_position(
            (self.true[0] - 0.2, self.true[1])
        )
        self.ecar.set_position(
            (self.est[0] - 0.2, self.est[1])
        )

        self.map_im.set_data(self.map_image())

        for line, a, d in zip(
            self.ray_lines,
            BEAM_ANGLES,
            self.ranges,
        ):
            x0, y0 = self.true[:2]
            x1 = x0 + d * math.cos(self.true[2] + a)
            y1 = y0 + d * math.sin(self.true[2] + a)
            line.set_data([x0, x1], [y0, y1])

        error = np.linalg.norm(
            self.true[:2] - self.est[:2]
        )

        known = np.count_nonzero(
            (self.logodds <= FREE_THRESHOLD)
            | (self.logodds >= OCC_THRESHOLD)
        )

        coverage = 100.0 * known / (N * N)

        self.info.set_text(
            f"frame={self.frame:3d} | moves={self.moves:3d} | "
            f"pose error={error:5.2f} cell | "
            f"map known={coverage:5.1f}% | "
            f"{'GOAL REACHED' if self.reached else 'RUNNING'}"
        )

        if self.reached:
            self.ani.event_source.stop()

        return (
            self.map_im,
            self.tline,
            self.eline,
            self.tcar,
            self.ecar,
            self.info,
            *self.ray_lines,
        )

    def run(self):
        print("======================================")
        print(" Simplified Automotive LiDAR SLAM")
        print("======================================")
        print(f"map size       : {N} x {N}")
        print(f"S              : {S}")
        print(f"D              : {D}")

        max_d = math.sqrt(2) * (N - 1)
        sd_d = np.linalg.norm(center(D) - center(S))

        print(f"S-D distance   : {sd_d:.3f} cells")
        print(f"max possible   : {max_d:.3f} cells")
        print(f"BFS valid      : {self.bfs_path is not None}")
        print(f"BFS path       : {len(self.bfs_path)} cells")
        print(f"A* path        : {len(self.global_path)} cells")
        print()

        self.setup()
        self.ani = FuncAnimation(
            self.fig,
            self.update,
            frames=MAX_FRAMES,
            interval=FRAME_MS,
            repeat=False,
            blit=False,
        )
        plt.tight_layout(rect=(0, 0.04, 1, 0.96))
        plt.show()

        final_error = np.linalg.norm(
            self.true[:2] - self.est[:2]
        )

        print("=== RESULT ===")
        print(f"reached        : {self.reached}")
        print(f"moves          : {self.moves}")
        print(f"pose error     : {final_error:.3f} cell")


def main():
    # Note: sqrt(2*N^2) is impossible inside an N x N grid.
    # The maximum distance between cell coordinates is sqrt(2)*(N-1).
    distance = np.linalg.norm(center(D) - center(S))
    if distance > math.sqrt(2) * (N - 1) + 1e-9:
        raise RuntimeError("Invalid S/D placement.")

    Demo().run()


if __name__ == "__main__":
    main()

