"""南半球のコリオリ偏向アニメーション（2球並列）/ Southern Hemisphere Coriolis Deflection (Dual Globe)
====================================================================

南半球におけるコリオリ力の偏向を2つの球を並列に表示して可視化する。
- 左球: 南半球（南緯45°）から赤道へ北上 → 左（西）に偏向
- 右球: 赤道から南半球へ南下 → 左（東）に偏向

北半球版（coriolis_earth_deflection.py）のパラメータを
緯度・初速の符号反転で再利用している。

南半球ではコリオリパラメータ f = 2Ω sin(φ) < 0 となるため、
北半球とは逆に進行方向の「左」に偏向される。

使用方法 / Usage:
  manim -pql scripts/coriolis_southern_hemisphere.py CoriolisSouthernHemisphere
"""

from manim import *
import numpy as np

# =============================================
# パラメータ / Parameters
# =============================================
GLOBE_RADIUS = 1.5            # 2球並列用の半径（Manim単位）
GLOBE_SHIFT = 2.8             # 球の中心のx方向オフセット
LON_START = 90.0             # 出発経度（度）※カメラ正面に合わせる
SIM_TIME = 5.0                # シミュレーション時間 (s)
N_STEPS = int(SIM_TIME * 100)  # 数値積分のステップ数
ANIM_FLIGHT_TIME = 6.0        # 粒子飛行アニメーション時間 (s)

# 左球: 南半球から赤道へ北上（北半球版 Southward の緯度・初速を反転）
# 北半球版: LAT=45, V0=-0.1, OMEGA=0.2
NORTH_LAT_START = -45.0       # 南緯45度から出発
NORTH_V0 = 0.1                # 北向き初速 (rad/s)
NORTH_OMEGA = 0.2             # コリオリ角速度

# 右球: 赤道から南半球へ南下（北半球版 Northward の初速を反転）
# 北半球版: LAT=0, V0=0.20, OMEGA=0.5
SOUTH_LAT_START = 0.0         # 赤道から出発
SOUTH_V0 = -0.20              # 南向き初速 (rad/s)
SOUTH_OMEGA = 0.5             # コリオリ角速度

# カメラ設定（南半球が見えるように仰角を調整）
CAM_PHI = 90 * DEGREES       # 仰角（赤道より下を見る = 南半球が正面）
CAM_THETA = -90 * DEGREES     # 方位角（y-方向 = 2球のx並列に対して正面対称）

# 色
CLR_EARTH = BLUE_E
CLR_GRID = BLUE_D
CLR_EQUATOR = YELLOW_C
CLR_STRAIGHT = GREEN_C        # 直進パス（破線風ドット列）
CLR_DEFLECTED = ORANGE         # 偏向パス（実線）
CLR_PARTICLE = RED_C           # 粒子ドット


# =============================================
# ユーティリティ / Utility Functions
# =============================================
def geo_to_xyz(lat_deg: float, lon_deg: float,
               r: float, center: np.ndarray = np.zeros(3)) -> np.ndarray:
    """緯度・経度 → 3D座標（中心オフセット対応）

    座標系: x=cos(lat)cos(lon), y=cos(lat)sin(lon), z=sin(lat)
    z軸が北極方向
    """
    lat = np.radians(lat_deg)
    lon = np.radians(lon_deg)
    return np.array([
        r * np.cos(lat) * np.cos(lon) + center[0],
        r * np.cos(lat) * np.sin(lon) + center[1],
        r * np.sin(lat) + center[2],
    ])


def compute_coriolis_trajectory(
    lat0_deg: float, lon0_deg: float,
    v0: float, omega: float,
    sim_time: float, n_steps: int,
) -> np.ndarray:
    """コリオリ力を受けた粒子の軌跡をRK4で計算

    状態ベクトル: [lat, lon, u, v]
      lat, lon: 緯度・経度 (radians)
      u: 東向き角速度 (rad/s)
      v: 北向き角速度 (rad/s)

    運動方程式（回転球面上の自由粒子、簡略化）:
      du/dt =  f × v
      dv/dt = -f × u
      f = 2Ω sin(lat)
    """
    dt = sim_time / n_steps
    lat0 = np.radians(lat0_deg)
    lon0 = np.radians(lon0_deg)
    state = np.array([lat0, lon0, 0.0, v0])
    trajectory = [state.copy()]

    def derivatives(s):
        lat, _lon, u, v = s
        f = 2 * omega * np.sin(lat)
        cos_lat = max(np.cos(lat), 1e-6)
        return np.array([v, u / cos_lat, f * v, -f * u])

    for _ in range(n_steps):
        k1 = derivatives(state)
        k2 = derivatives(state + 0.5 * dt * k1)
        k3 = derivatives(state + 0.5 * dt * k2)
        k4 = derivatives(state + dt * k3)
        state = state + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        trajectory.append(state.copy())

    return np.array(trajectory)


def build_globe(center: np.ndarray, radius: float):
    """地球の球体・グリッド・自転軸を生成

    Returns:
        sphere, grid, axis
    """
    sphere = Sphere(radius=radius, resolution=(36, 18))
    sphere.set_color(CLR_EARTH)
    sphere.set_opacity(1.0)
    sphere.move_to(center)

    # 赤道（太め）
    equator = ParametricFunction(
        lambda t, c=center, r=radius: geo_to_xyz(0, t, r + 0.005, c),
        t_range=[0, 360],
        color=CLR_EQUATOR,
        stroke_width=2.0,
    )
    # 緯度線
    lat_lines = VGroup(*[
        ParametricFunction(
            lambda t, lat=lat, c=center, r=radius: geo_to_xyz(
                lat, t, r + 0.005, c),
            t_range=[0, 360],
            color=CLR_GRID,
            stroke_width=1.0,
        )
        for lat in [-60, -30, 30, 60]
    ])
    # 経度線
    lon_lines = VGroup(*[
        ParametricFunction(
            lambda t, lon=lon, c=center, r=radius: geo_to_xyz(
                t, lon, r + 0.005, c),
            t_range=[-90, 90],
            color=CLR_GRID,
            stroke_width=1.0,
        )
        for lon in range(0, 360, 30)
    ])
    # 自転軸
    axis = Line3D(
        start=[center[0], center[1], center[2] - radius * 1.3],
        end=[center[0], center[1], center[2] + radius * 1.3],
        thickness=0.01, color=WHITE,
    )

    grid = VGroup(equator, lat_lines, lon_lines)
    return sphere, grid, axis


def build_trajectory(
    center: np.ndarray, radius: float,
    lat_start: float, lon_start: float,
    v0: float, omega: float,
    sim_time: float, n_steps: int,
):
    """軌跡の計算と描画要素を生成

    Returns:
        deflected_curve, straight_dots, particle
    """
    traj = compute_coriolis_trajectory(
        lat_start, lon_start, v0, omega, sim_time, n_steps,
    )

    r_path = radius + 0.03

    # 偏向パスの3D座標
    deflected_pts = [
        geo_to_xyz(np.degrees(s[0]), np.degrees(s[1]), r_path, center)
        for s in traj
    ]
    step = max(1, len(deflected_pts) // 200)
    sampled = np.array(deflected_pts[::step])
    t_par = np.linspace(0, 1, len(sampled))

    # 偏向パス曲線（ParametricFunction + 補間）
    deflected_curve = ParametricFunction(
        lambda t, tp=t_par, sp=sampled: np.array([
            np.interp(t, tp, sp[:, 0]),
            np.interp(t, tp, sp[:, 1]),
            np.interp(t, tp, sp[:, 2]),
        ]),
        t_range=[0, 1, 0.005],
        color=CLR_DEFLECTED,
        stroke_width=6.0,
    )

    # 直進パス（コリオリ力なしの想定軌道、ドット列で破線風）
    final_lat_deg = np.degrees(traj[-1, 0])
    straight_dots = VGroup(*[
        Dot3D(
            point=geo_to_xyz(lat, lon_start, r_path, center),
            color=CLR_STRAIGHT, radius=0.02,
        )
        for lat in np.linspace(lat_start, final_lat_deg, 30)
    ])
    straight_dots.set_opacity(0.7)

    # 粒子ドット
    particle = Dot3D(
        point=np.array(deflected_pts[0]),
        color=CLR_PARTICLE, radius=0.06,
    )

    return deflected_curve, straight_dots, particle


# =============================================
# メインシーン / Main Scene
# =============================================
class CoriolisSouthernHemisphere(ThreeDScene):
    """南半球のコリオリ偏向を2球並列で可視化

    左球: 南半球（南緯45°）から赤道へ北上 → 左（西）に偏向
    右球: 赤道から南半球へ南下 → 左（東）に偏向

    南半球では f < 0 なので、北半球とは逆に
    進行方向の「左」に偏向される。
    """

    def construct(self):
        # ---- カメラ設定（南半球が見える角度）----
        self.set_camera_orientation(phi=CAM_PHI, theta=CAM_THETA)

        left_center = np.array([-GLOBE_SHIFT, 0.0, 0.0])
        right_center = np.array([GLOBE_SHIFT, 0.0, 0.0])

        # ---- 2つの地球を構築 ----
        l_earth, l_grid, l_axis = build_globe(left_center, GLOBE_RADIUS)
        r_earth, r_grid, r_axis = build_globe(right_center, GLOBE_RADIUS)

        # ---- 軌跡を構築 ----
        l_curve, l_dots, l_particle = build_trajectory(
            left_center, GLOBE_RADIUS,
            NORTH_LAT_START, LON_START, NORTH_V0, NORTH_OMEGA,
            SIM_TIME, N_STEPS,
        )
        r_curve, r_dots, r_particle = build_trajectory(
            right_center, GLOBE_RADIUS,
            SOUTH_LAT_START, LON_START, SOUTH_V0, SOUTH_OMEGA,
            SIM_TIME, N_STEPS,
        )

        # ======== アニメーション ========

        # ① 2つの地球を同時に出現
        self.play(
            FadeIn(l_earth), FadeIn(r_earth),
            run_time=1.5,
        )
        self.play(
            Create(l_grid), FadeIn(l_axis),
            Create(r_grid), FadeIn(r_axis),
            run_time=1.5,
        )

        self.wait(1.0)

        # ② 各球のタイトルラベル
        left_title = Text(
            "南半球から北上\nNorthward from SH",
            font_size=16, color=WHITE,
        ).to_corner(UL, buff=0.3)
        right_title = Text(
            "赤道から南下\nSouthward from Eq.",
            font_size=16, color=WHITE,
        ).to_corner(UR, buff=0.3)
        self.add_fixed_in_frame_mobjects(left_title, right_title)
        self.remove(left_title, right_title)

        # 粒子を出発点に表示
        self.play(
            FadeIn(left_title), FadeIn(right_title),
            FadeIn(l_particle), FadeIn(r_particle),
            run_time=0.8,
        )
        self.wait(0.5)

        # ③ 直進パス（コリオリ力がない場合の想定軌道）
        straight_lbl = Text(
            "緑 = コリオリ力なしの経路\n"
            "Green = path without Coriolis",
            font_size=14, color=CLR_STRAIGHT,
        ).to_edge(DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(straight_lbl)
        self.remove(straight_lbl)

        self.play(
            FadeIn(l_dots), FadeIn(r_dots),
            FadeIn(straight_lbl),
            run_time=1.5,
        )
        self.wait(0.5)

        # ④ 粒子飛行: コリオリ偏向を2球同時に描画
        deflect_lbl = Text(
            "南半球ではコリオリ力で左に曲がる\n"
            "Deflected LEFT in the S. Hemisphere",
            font_size=16, color=CLR_DEFLECTED,
        ).to_edge(DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(deflect_lbl)
        self.remove(deflect_lbl)

        self.play(
            Create(l_curve), MoveAlongPath(l_particle, l_curve),
            Create(r_curve), MoveAlongPath(r_particle, r_curve),
            FadeOut(straight_lbl),
            FadeIn(deflect_lbl, run_time=1),
            run_time=ANIM_FLIGHT_TIME,
            rate_func=linear,
        )
        self.wait(1)

        # ⑤ 結びテキスト
        conclusion = Text(
            "南半球: 進行方向の左に偏向\n"
            "S. Hemisphere: always deflected LEFT",
            font_size=20,
        ).to_edge(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.remove(conclusion)

        self.play(
            FadeOut(deflect_lbl), FadeIn(conclusion),
            run_time=1,
        )
        self.wait(2)
