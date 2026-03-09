"""地球表面速度の緯度依存性（3D版）/ Surface Velocity vs. Latitude (3D)
=======================================================================

3D地球上で、各緯度の緯度円とその上での表面速度 v = rω を
可視化する。緯度円が北極に近づくほど小さくなり、
円周に接する速度ベクトルも短くなる様子を示す。

yt_script.md L62-75:
  「地球は1日に1回自転しています。
   このとき、地球の表面の速さは場所によって全然違うんです。」
  ...
  「v = rω / 円周上の速度 = 半径 × 角速度」

使用方法 / Usage:
  manim -pql scripts/coriolis_surface_velocity.py SurfaceVelocityByLatitude
"""

from manim import *
import numpy as np

# =============================================
# パラメータ / Parameters
# =============================================
EARTH_RADIUS = 2.0          # 球体の半径（Manim単位）
ARROW_SCALE = 1.5           # 速度矢印のスケーリング係数
LON_DISPLAY = -70.0         # 矢印を配置する経度（度）※カメラ正面寄り

# カメラ設定（coriolis_earth_deflection.py と統一）
CAM_PHI = 65 * DEGREES      # 仰角（z軸からの角度）
CAM_THETA = -50 * DEGREES   # 方位角

# 表示する緯度（度）とメタデータ
LATITUDES = [
    {"deg": 0, "label_jp": "赤道 / Equator", "speed": "~1700 km/h"},
    {"deg": 35, "label_jp": "北緯35°（日本付近）/ 35°N", "speed": "~1400 km/h"},
    {"deg": 60, "label_jp": "北緯60° / 60°N", "speed": "~850 km/h"},
    {"deg": 90, "label_jp": "北極 / North Pole", "speed": "0 km/h"},
]

# 色 / Colors
CLR_EARTH = BLUE_E
CLR_GRID = BLUE_D
CLR_EQUATOR = YELLOW_C
CLR_LAT_HIGHLIGHT = GREEN_C    # ハイライトされた緯度円
CLR_RADIUS = TEAL_C            # 半径線 r（軸→表面）
CLR_VELOCITY = RED_C           # 速度矢印
CLR_DOT = ORANGE               # 緯度上のドット


# =============================================
# ユーティリティ / Utility Functions
# =============================================
def geo_to_xyz(lat_deg: float, lon_deg: float,
               r: float = EARTH_RADIUS) -> np.ndarray:
    """緯度・経度 → Manim 3D座標

    座標系: x=cos(lat)cos(lon), y=cos(lat)sin(lon), z=sin(lat)
    z軸が北極方向

    Args:
        lat_deg: 緯度（度）
        lon_deg: 経度（度）
        r: 球の半径（Manim単位）

    Returns:
        3Dベクトル [x, y, z]
    """
    lat = np.radians(lat_deg)
    lon = np.radians(lon_deg)
    return np.array([
        r * np.cos(lat) * np.cos(lon),
        r * np.cos(lat) * np.sin(lon),
        r * np.sin(lat),
    ])


def east_direction(lon_deg: float) -> np.ndarray:
    """指定経度での東向き単位ベクトル

    東向きは緯度円の接線方向で、経度のみに依存する。

    Args:
        lon_deg: 経度（度）

    Returns:
        3D単位ベクトル [-sin(lon), cos(lon), 0]
    """
    lon = np.radians(lon_deg)
    return np.array([-np.sin(lon), np.cos(lon), 0])


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
class SurfaceVelocityByLatitude(ThreeDScene):
    """3D地球上で表面速度 v = rω の緯度依存性を可視化

    各緯度の緯度円を描き、円周に接する速度ベクトルの長さが
    赤道から北極に向かって減少する様子を示す。
    """

    def construct(self):
        # ---- カメラ設定 ----
        self.set_camera_orientation(phi=CAM_PHI, theta=CAM_THETA)

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
            thickness=0.01, color=WHITE,
        )

        # ======== アニメーション ========

        # ① 地球出現
        self.play(FadeIn(earth), run_time=1.5)
        self.play(Create(grid), FadeIn(axis), run_time=1.5)

        # ② カメラ回転（自転の演出）
        self.begin_ambient_camera_rotation(rate=0.05)
        self.wait(1.5)
        self.stop_ambient_camera_rotation()

        # ③ 各緯度を順に表示
        r_path = EARTH_RADIUS + 0.03  # 球面からわずかに浮かせる
        prev_telop = None

        for lat_info in LATITUDES:
            lat_deg = lat_info["deg"]
            cos_lat = np.cos(np.radians(lat_deg))

            # ---- テロップ（画面下部、カメラ固定）----
            telop = Text(
                f"{lat_info['label_jp']}: {lat_info['speed']}",
                font_size=20, color=CLR_DOT,
            ).to_edge(DOWN, buff=0.5)
            self.add_fixed_in_frame_mobjects(telop)
            self.remove(telop)

            telop_anims = []
            if prev_telop is not None:
                telop_anims.append(FadeOut(prev_telop))
            telop_anims.append(FadeIn(telop))

            if lat_deg < 90:
                # ---- 緯度円のハイライト ----
                lat_circle = make_lat_line(
                    lat_deg, r=EARTH_RADIUS,
                    color=CLR_LAT_HIGHLIGHT, stroke_width=3.5,
                )

                # ---- 表面上のドット ----
                surface_pt = geo_to_xyz(lat_deg, LON_DISPLAY, r_path)
                dot = Dot3D(point=surface_pt, color=CLR_DOT, radius=0.06)

                # ---- 半径線 r: z軸 → 表面点（水平距離）----
                axis_pt = np.array([
                    0, 0, r_path * np.sin(np.radians(lat_deg)),
                ])
                radius_line = Line3D(
                    start=axis_pt, end=surface_pt,
                    thickness=0.015, color=CLR_RADIUS,
                )

                # ---- 速度矢印（緯度円の接線方向 = 東向き）----
                e_dir = east_direction(LON_DISPLAY)
                arrow_len = ARROW_SCALE * cos_lat
                arrow_end = surface_pt + e_dir * arrow_len
                velocity_arrow = Arrow3D(
                    start=surface_pt, end=arrow_end,
                    color=CLR_VELOCITY,
                )

                # ---- アニメーション ----
                self.play(Create(lat_circle), *telop_anims, run_time=1.0)
                self.play(FadeIn(dot), FadeIn(radius_line), run_time=0.8)
                self.play(Create(velocity_arrow), run_time=0.8)

            else:
                # ---- 北極: 緯度円なし、速度 = 0 ----
                pole_pt = geo_to_xyz(90, 0, r_path)
                dot = Dot3D(point=pole_pt, color=CLR_DOT, radius=0.08)

                self.play(FadeIn(dot), *telop_anims, run_time=1.0)

            self.wait(1.0)
            prev_telop = telop

        # ④ 数式表示（カメラ固定）
        formula_v = MathTex(
            r"v = r\omega", font_size=36, color=WHITE,
        ).to_corner(UL, buff=0.4)
        self.add_fixed_in_frame_mobjects(formula_v)
        self.remove(formula_v)

        formula_jp = Text(
            "円周上の速度 = 半径 × 角速度",
            font_size=16, color=GRAY_A,
        ).next_to(formula_v, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(formula_jp)
        self.remove(formula_jp)

        formula_r = MathTex(
            r"r = R\cos\varphi", font_size=28, color=CLR_RADIUS,
        ).next_to(formula_jp, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(formula_r)
        self.remove(formula_r)

        if prev_telop is not None:
            self.play(FadeOut(prev_telop), run_time=0.5)

        self.play(FadeIn(formula_v), run_time=0.8)
        self.play(FadeIn(formula_jp), FadeIn(formula_r), run_time=0.8)
        self.wait(1.0)

        # ⑤ 締め
        conclusion = Text(
            "緯度が上がるほど表面速度は小さくなる\n"
            "Surface speed decreases toward the poles",
            font_size=22,
        ).to_edge(DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.remove(conclusion)

        self.play(FadeIn(conclusion), run_time=1.0)
        self.wait(2.5)
