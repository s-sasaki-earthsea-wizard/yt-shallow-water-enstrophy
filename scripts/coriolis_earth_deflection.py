"""3D地球上のコリオリ偏向アニメーション / Coriolis Deflection on 3D Earth
====================================================================

自転する3D地球の球面上で、赤道付近から北向きに出発した粒子が
コリオリ力によって右（東）に偏向される様子を可視化する。

yt_script.md L55-56:
  「地球もメリーゴーランドのように回転しています。
   私たちは地球と一緒に回転しているので...」

使用方法 / Usage:
  manim -pql scripts/coriolis_earth_deflection.py CoriolisEarthDeflection
"""

from manim import *
import numpy as np

# =============================================
# パラメータ / Parameters
# =============================================
EARTH_RADIUS = 2.0          # 球体の半径（Manim単位）
OMEGA_DEMO = 0.5            # デモ用の誇張された角速度
V0_NORTH = 0.20             # 初期の北向き角速度 (rad/s, 単位球上)
LAT_START = 0.0             # 出発緯度 (度)
LON_START = -90.0           # 出発経度 (度) ※カメラ正面に合わせる
SIM_TIME = 5.0              # シミュレーション時間 (s)
N_STEPS = int(SIM_TIME * 100)     # 数値積分のステップ数

ANIM_FLIGHT_TIME = 6.0      # 粒子飛行アニメーション時間 (s)

# カメラ設定
CAM_PHI = 65 * DEGREES      # 仰角（z軸からの角度）
CAM_THETA = -50 * DEGREES   # 方位角

# 色
CLR_EARTH = BLUE_E
CLR_GRID = BLUE_D
CLR_EQUATOR = YELLOW_C
CLR_STRAIGHT = GREEN_C      # 直進パス（破線）
CLR_DEFLECTED = ORANGE       # 偏向パス（実線）
CLR_PARTICLE = RED_C         # 粒子ドット


# =============================================
# ユーティリティ / Utility Functions
# =============================================
def geo_to_xyz(lat_deg: float, lon_deg: float,
               r: float = EARTH_RADIUS) -> np.ndarray:
    """緯度・経度 → Manim 3D座標

    座標系: x=cos(lat)cos(lon), y=cos(lat)sin(lon), z=sin(lat)
    z軸が北極方向
    """
    lat = np.radians(lat_deg)
    lon = np.radians(lon_deg)
    return np.array([
        r * np.cos(lat) * np.cos(lon),
        r * np.cos(lat) * np.sin(lon),
        r * np.sin(lat),
    ])


def compute_coriolis_trajectory(
    lat0_deg: float, lon0_deg: float,
    v0: float, omega: float,
    sim_time: float, n_steps: int,
) -> np.ndarray:
    """コリオリ力を受けた粒子の軌跡をRK4で計算

    状態ベクトル: [lat, lon, u, v]
      lat, lon: 緯度・経度 (radians)
      u: 東向き角速度 (rad/s, 単位球上)
      v: 北向き角速度 (rad/s, 単位球上)

    運動方程式（回転球面上の自由粒子、簡略化）:
      du/dt =  f × v    （コリオリ力の東西成分）
      dv/dt = -f × u    （コリオリ力の南北成分）
      f = 2Ω sin(lat)

    位置更新:
      dlat/dt = v
      dlon/dt = u / cos(lat)
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


def traj_to_xyz(traj: np.ndarray,
                r: float = EARTH_RADIUS) -> list[np.ndarray]:
    """軌跡データ [lat, lon, ...] → 3D座標点列"""
    return [
        geo_to_xyz(np.degrees(s[0]), np.degrees(s[1]), r)
        for s in traj
    ]


def make_lat_line(lat_deg: float, r: float = EARTH_RADIUS,
                  color=CLR_GRID, stroke_width: float = 1.0) -> VMobject:
    """緯度線を生成"""
    return ParametricFunction(
        lambda t: geo_to_xyz(lat_deg, t, r + 0.005),
        t_range=[0, 360],
        color=color,
        stroke_width=stroke_width,
    )


def make_lon_line(lon_deg: float, r: float = EARTH_RADIUS,
                  color=CLR_GRID, stroke_width: float = 1.0) -> VMobject:
    """経度線を生成（南極〜北極）"""
    return ParametricFunction(
        lambda t: geo_to_xyz(t, lon_deg, r + 0.005),
        t_range=[-90, 90],
        color=color,
        stroke_width=stroke_width,
    )


# =============================================
# メインシーン / Main Scene
# =============================================
class CoriolisEarthDeflection(ThreeDScene):
    """自転する3D地球上でのコリオリ偏向を可視化

    赤道付近から北向きに発射した粒子が、コリオリ力によって
    右（東方向）に偏向される様子を3D球面上に描画する。
    """

    def construct(self):
        # ---- カメラ設定 ----
        self.set_camera_orientation(phi=CAM_PHI, theta=CAM_THETA)

        # ---- タイトル（カメラ固定）----
        # title = Text(
        #     "地球上のコリオリ力 / Coriolis on Earth",
        #     font_size=28,
        # ).to_corner(UL, buff=0.3)
        # self.add_fixed_in_frame_mobjects(title)
        # self.remove(title)  # add_fixed_in_frame_mobjects が自動追加するので一旦除去

        # ---- 地球（半透明球体）----
        earth = Sphere(radius=EARTH_RADIUS, resolution=(48, 24))
        earth.set_color(CLR_EARTH)
        earth.set_opacity(1.0)

        # ---- グリッド（緯度線・経度線）----
        equator = make_lat_line(0, color=CLR_EQUATOR, stroke_width=2.0)
        lat_lines = VGroup(*[
            make_lat_line(lat) for lat in [-60, -30, 30, 60]
        ])
        lon_lines = VGroup(*[
            make_lon_line(lon) for lon in range(0, 360, 30)
        ])
        grid = VGroup(equator, lat_lines, lon_lines)

        # ---- 自転軸 ----
        axis = Line3D(
            start=[0, 0, -EARTH_RADIUS * 1.3],
            end=[0, 0, EARTH_RADIUS * 1.3],
            thickness=0.01,
            color=WHITE,
        )

        # ---- 軌跡の計算 ----
        traj = compute_coriolis_trajectory(
            LAT_START, LON_START, V0_NORTH, OMEGA_DEMO,
            SIM_TIME, N_STEPS,
        )

        # 球面からわずかに浮かせて描画
        r_path = EARTH_RADIUS + 0.03

        # 偏向パスの3D座標 → numpy補間でParametricFunction化
        # （VMobjectはCairo専用なのでOpenGLレンダラーと非互換）
        deflected_pts = traj_to_xyz(traj, r_path)
        step = max(1, len(deflected_pts) // 200)
        sampled = np.array(deflected_pts[::step])
        t_param = np.linspace(0, 1, len(sampled))

        deflected_curve = ParametricFunction(
            lambda t: np.array([
                np.interp(t, t_param, sampled[:, 0]),
                np.interp(t, t_param, sampled[:, 1]),
                np.interp(t, t_param, sampled[:, 2]),
            ]),
            t_range=[0, 1, 0.005],
            color=CLR_DEFLECTED,
            stroke_width=20.0,
        )

        # 直進パス（同一経度を真北方向 = コリオリ力がなければこう進む）
        # ドット列で破線風に表現（OpenGLレンダラー互換）
        final_lat_deg = np.degrees(traj[-1, 0])
        straight_dots = VGroup(*[
            Dot3D(
                point=geo_to_xyz(lat, LON_START, r_path),
                color=CLR_STRAIGHT, radius=0.025,
            )
            for lat in np.linspace(LAT_START, final_lat_deg, 40)
        ])
        straight_dots.set_opacity(0.7)

        # ---- 粒子ドット ----
        particle = Dot3D(
            point=np.array(deflected_pts[0]),
            color=CLR_PARTICLE,
            radius=0.07,
        )

        # ======== アニメーション ========

        # ① 地球出現
        self.play(FadeIn(earth), run_time=1.5)
        self.play(
            Create(grid), FadeIn(axis),
            run_time=1.5,
        )

        # ② カメラをゆっくり回転（自転している感覚を演出）
        self.begin_ambient_camera_rotation(rate=0.06)
        self.wait(1.5)

        # ③ 出発点表示
        start_lbl = Text(
            "出発点（赤道付近）/ Start (near equator)",
            font_size=18, color=CLR_PARTICLE,
        ).to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(start_lbl)
        self.remove(start_lbl)

        self.play(FadeIn(particle), FadeIn(start_lbl), run_time=0.8)
        self.wait(0.5)

        # ④ 直進パス（コリオリ力がない場合の想定軌道）
        north_lbl = Text(
            "まっすぐ北へ / Straight North",
            font_size=18, color=CLR_STRAIGHT,
        ).next_to(start_lbl, UP, buff=0.2)
        self.add_fixed_in_frame_mobjects(north_lbl)
        self.remove(north_lbl)

        self.play(
            FadeIn(straight_dots), FadeIn(north_lbl),
            run_time=1.5,
        )
        self.wait(0.5)

        # ⑤ 粒子飛行: コリオリ偏向を描画
        deflect_lbl = Text(
            "コリオリ力で右に曲がる\nDeflected right by Coriolis",
            font_size=18, color=CLR_DEFLECTED,
        ).to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(deflect_lbl)
        self.remove(deflect_lbl)

        self.play(
            Create(deflected_curve),
            MoveAlongPath(particle, deflected_curve),
            FadeOut(start_lbl),
            FadeOut(north_lbl),
            FadeIn(deflect_lbl, run_time=1),
            run_time=ANIM_FLIGHT_TIME,
            rate_func=linear,
        )
        self.wait(1)

        # ⑥ 結びテキスト
        self.stop_ambient_camera_rotation()

        conclusion = Text(
            "地球は超巨大なメリーゴーランド\n"
            "Earth: a giant merry-go-round",
            font_size=22,
        ).to_edge(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.remove(conclusion)

        self.play(
            FadeOut(deflect_lbl),
            FadeIn(conclusion),
            run_time=1,
        )
        self.wait(2)


# =============================================
# 南下バージョン / Southward Version
# =============================================
# 北半球から赤道に向かって南下する粒子が右（西）に偏向
SOUTH_LAT_START = 45.0      # 出発緯度 (度)
SOUTH_LON_START = -90.0     # 出発経度 (度)
SOUTH_V0 = -0.10            # 南向き初速 (負 = 南)
SOUTH_SIM_TIME = 5.0
SOUTH_N_STEPS = int(SOUTH_SIM_TIME * 100)


class CoriolisEarthSouthward(ThreeDScene):
    """北半球から南下する粒子がコリオリ力で右（西）に偏向"""

    def construct(self):
        self.set_camera_orientation(phi=CAM_PHI, theta=CAM_THETA)

        # ---- 地球 ----
        earth = Sphere(radius=EARTH_RADIUS, resolution=(48, 24))
        earth.set_color(CLR_EARTH)
        earth.set_opacity(1.0)

        # ---- グリッド ----
        equator = make_lat_line(0, color=CLR_EQUATOR, stroke_width=2.0)
        lat_lines = VGroup(*[
            make_lat_line(lat) for lat in [-60, -30, 30, 60]
        ])
        lon_lines = VGroup(*[
            make_lon_line(lon) for lon in range(0, 360, 30)
        ])
        grid = VGroup(equator, lat_lines, lon_lines)

        # ---- 自転軸 ----
        axis = Line3D(
            start=[0, 0, -EARTH_RADIUS * 1.3],
            end=[0, 0, EARTH_RADIUS * 1.3],
            thickness=0.01, color=WHITE,
        )

        # ---- 軌跡の計算 ----
        traj = compute_coriolis_trajectory(
            SOUTH_LAT_START, SOUTH_LON_START, SOUTH_V0, OMEGA_DEMO,
            SOUTH_SIM_TIME, SOUTH_N_STEPS,
        )

        r_path = EARTH_RADIUS + 0.03

        # 偏向パス
        deflected_pts = traj_to_xyz(traj, r_path)
        step = max(1, len(deflected_pts) // 200)
        sampled = np.array(deflected_pts[::step])
        t_param = np.linspace(0, 1, len(sampled))

        deflected_curve = ParametricFunction(
            lambda t: np.array([
                np.interp(t, t_param, sampled[:, 0]),
                np.interp(t, t_param, sampled[:, 1]),
                np.interp(t, t_param, sampled[:, 2]),
            ]),
            t_range=[0, 1, 0.005],
            color=CLR_DEFLECTED,
            stroke_width=8.0,
        )

        # 直進パス（同一経度を真南方向）
        final_lat_deg = np.degrees(traj[-1, 0])
        straight_dots = VGroup(*[
            Dot3D(
                point=geo_to_xyz(lat, SOUTH_LON_START, r_path),
                color=CLR_STRAIGHT, radius=0.025,
            )
            for lat in np.linspace(SOUTH_LAT_START, final_lat_deg, 40)
        ])
        straight_dots.set_opacity(0.7)

        # 粒子
        particle = Dot3D(
            point=np.array(deflected_pts[0]),
            color=CLR_PARTICLE, radius=0.07,
        )

        # ======== アニメーション ========

        self.play(FadeIn(earth), run_time=1.5)
        self.play(Create(grid), FadeIn(axis), run_time=1.5)

        self.begin_ambient_camera_rotation(rate=0.06)
        self.wait(1.5)

        # 出発点
        start_lbl = Text(
            "出発点（北緯55°）/ Start (55°N)",
            font_size=18, color=CLR_PARTICLE,
        ).to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(start_lbl)
        self.remove(start_lbl)

        self.play(FadeIn(particle), FadeIn(start_lbl), run_time=0.8)
        self.wait(0.5)

        # 直進パス
        south_lbl = Text(
            "まっすぐ南へ / Straight South",
            font_size=18, color=CLR_STRAIGHT,
        ).next_to(start_lbl, UP, buff=0.2)
        self.add_fixed_in_frame_mobjects(south_lbl)
        self.remove(south_lbl)

        self.play(FadeIn(straight_dots), FadeIn(south_lbl), run_time=1.5)
        self.wait(0.5)

        # 偏向パス
        deflect_lbl = Text(
            "コリオリ力で右（西）に曲がる\nDeflected right (west) by Coriolis",
            font_size=18, color=CLR_DEFLECTED,
        ).to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(deflect_lbl)
        self.remove(deflect_lbl)

        self.play(
            Create(deflected_curve),
            MoveAlongPath(particle, deflected_curve),
            FadeOut(start_lbl),
            FadeOut(south_lbl),
            FadeIn(deflect_lbl, run_time=1),
            run_time=ANIM_FLIGHT_TIME,
            rate_func=linear,
        )
        self.wait(1)

        self.stop_ambient_camera_rotation()

        conclusion = Text(
            "北半球では常に進行方向の右に曲がる\n"
            "Always deflected right in the N. Hemisphere",
            font_size=22,
        ).to_edge(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.remove(conclusion)

        self.play(FadeOut(deflect_lbl), FadeIn(conclusion), run_time=1)
        self.wait(2)
