"""ベルトコンベア比喩によるコリオリ偏向メカニズム / Belt Conveyor Analogy for Coriolis Deflection
=================================================================================================

赤道付近の空気が北上すると、地面との東向き速度差で東に逸れて見える
メカニズムを、2本の平行レーン（ベルトコンベア）で直感的に可視化する。

yt_script.md L77-84:
  「ここで、赤道付近の空気が北に向かって移動する場合を考えてみましょう。
   この空気はもともと赤道にいたので、時速約1700キロの東向きの速度を持っています。
   北に移動しても、この東向きの速度はそのまま残るんです。
   ところが、移動先の地面は赤道より遅い速さで東に動いている。
   だから空気は地面に対して『東に逸れて』見えるんです。」

使用方法 / Usage:
  manim -pql scripts/coriolis_belt_conveyor.py CoriolisBeltConveyor
"""

from manim import *
import numpy as np

# =============================================
# パラメータ / Parameters
# =============================================

# 表示用の速度 (km/h) — 脚本に合わせた丸め値
V_EQUATOR_DISPLAY = 1700
V_LAT35_DISPLAY = 1400
V_DIFF_DISPLAY = V_EQUATOR_DISPLAY - V_LAT35_DISPLAY  # 300

# 速度比
SPEED_RATIO = V_LAT35_DISPLAY / V_EQUATOR_DISPLAY  # ≈ 0.824

# 矢印スケーリング（赤道矢印の長さ = ARROW_LEN_EQ Manim単位）
ARROW_LEN_EQ = 3.5
ARROW_LEN_35 = ARROW_LEN_EQ * SPEED_RATIO  # ≈ 2.88
ARROW_LEN_DIFF = ARROW_LEN_EQ - ARROW_LEN_35  # ≈ 0.62

# レーン座標
LANE_LEFT = -5.5
LANE_RIGHT = 5.5
LANE_WIDTH = LANE_RIGHT - LANE_LEFT  # 11.0
LANE_HEIGHT = 2.0
EQUATOR_Y = -1.0       # 赤道レーン中心
LAT35_Y = 1.0          # 北緯35°レーン中心
BOUNDARY_Y = 0.0

# ストライプ（地面の動きを示す縦線）
N_STRIPES = 14
STRIPE_SPACING = LANE_WIDTH / N_STRIPES
STRIPE_SPEED_EQ = 1.8          # 赤道ストライプの速度 (Manim単位/秒)
STRIPE_SPEED_35 = STRIPE_SPEED_EQ * SPEED_RATIO  # ≈ 1.48

# 空気塊
AIR_START_X = -2.5
AIR_RADIUS = 0.15
NORTHWARD_MOVE_TIME = 2.5      # 北上アニメーション時間 (s)
DRIFT_DISTANCE = 1.8           # 東への逸れ量（誇張表示）
DRIFT_TIME = 1.5               # 逸れアニメーション時間 (s)

# 色 / Colors（プロジェクト統一パレット）
CLR_LANE_BG = BLUE_E
CLR_EQUATOR = YELLOW_C         # 赤道レーン
CLR_LAT35 = BLUE_D             # 北緯35°レーン
CLR_AIR = RED_C                # 空気塊
CLR_AIR_VEL = ORANGE           # 空気の速度矢印
CLR_DIFF = RED_C               # 差分強調
CLR_BOUNDARY = GRAY_C          # 境界線


# =============================================
# ユーティリティ / Utility Functions
# =============================================
def make_stripes(y_center: float, lane_height: float,
                 speed: float, t_val: float,
                 color, lane_left: float = LANE_LEFT,
                 lane_right: float = LANE_RIGHT) -> VGroup:
    """スクロールするストライプ（縦線群）を生成

    Args:
        y_center: レーン中心のy座標
        lane_height: レーンの高さ
        speed: ストライプの移動速度 (Manim単位/秒)
        t_val: 現在時刻
        color: ストライプの色
        lane_left: レーン左端
        lane_right: レーン右端

    Returns:
        VGroup of Lines
    """
    stripes = VGroup()
    offset = (speed * t_val) % STRIPE_SPACING
    y_top = y_center + lane_height / 2
    y_bot = y_center - lane_height / 2
    for i in range(N_STRIPES + 2):
        x = lane_left + i * STRIPE_SPACING + offset - STRIPE_SPACING
        if lane_left <= x <= lane_right:
            stripes.add(Line(
                start=[x, y_bot, 0],
                end=[x, y_top, 0],
                color=color,
                stroke_width=1.0,
                stroke_opacity=0.3,
            ))
    return stripes


# =============================================
# メインシーン / Main Scene
# =============================================
class CoriolisBeltConveyor(Scene):
    """ベルトコンベア比喩で地表速度差→コリオリ偏向を可視化

    赤道と北緯35°の2レーンで地面の東向き速度差を示し、
    空気塊が北上すると地面に対して東に逸れるメカニズムを描画する。
    """

    def construct(self):
        # ストライプ駆動用のグローバル時間トラッカー
        t = ValueTracker(0)

        # ==========================================
        # Phase 1: レーン構築
        # ==========================================
        # レーン枠
        equator_lane = Rectangle(
            width=LANE_WIDTH, height=LANE_HEIGHT,
            color=CLR_EQUATOR, stroke_width=2,
            fill_color=CLR_LANE_BG, fill_opacity=0.12,
        ).move_to([0, EQUATOR_Y, 0])

        lat35_lane = Rectangle(
            width=LANE_WIDTH, height=LANE_HEIGHT,
            color=CLR_LAT35, stroke_width=2,
            fill_color=CLR_LANE_BG, fill_opacity=0.08,
        ).move_to([0, LAT35_Y, 0])

        # 境界線
        boundary = DashedLine(
            start=[LANE_LEFT, BOUNDARY_Y, 0],
            end=[LANE_RIGHT, BOUNDARY_Y, 0],
            color=CLR_BOUNDARY, dash_length=0.15,
            stroke_width=1.5,
        )

        # レーンラベル（左端に配置）
        lbl_equator = VGroup(
            Text("赤道 / Equator", font_size=18, color=CLR_EQUATOR),
            Text(f"~{V_EQUATOR_DISPLAY} km/h →", font_size=14, color=CLR_EQUATOR),
        ).arrange(DOWN, buff=0.1).next_to(equator_lane, LEFT, buff=0.3)

        lbl_lat35 = VGroup(
            Text("北緯35° / 35°N", font_size=18, color=CLR_LAT35),
            Text(f"~{V_LAT35_DISPLAY} km/h →", font_size=14, color=CLR_LAT35),
        ).arrange(DOWN, buff=0.1).next_to(lat35_lane, LEFT, buff=0.3)

        # 方位コンパス（右上）
        compass_center = np.array([5.5, 2.8, 0])
        compass = VGroup(
            Arrow(
                start=compass_center,
                end=compass_center + UP * 0.5,
                color=WHITE, stroke_width=2, buff=0,
                max_tip_length_to_length_ratio=0.4,
            ),
            Text("N", font_size=14, color=WHITE).move_to(
                compass_center + UP * 0.75
            ),
            Arrow(
                start=compass_center,
                end=compass_center + RIGHT * 0.5,
                color=WHITE, stroke_width=2, buff=0,
                max_tip_length_to_length_ratio=0.4,
            ),
            Text("E", font_size=14, color=WHITE).move_to(
                compass_center + RIGHT * 0.75
            ),
        )

        # アニメーション: レーン出現
        self.play(
            FadeIn(equator_lane), FadeIn(lat35_lane),
            Create(boundary),
            run_time=1.5,
        )
        self.play(
            FadeIn(lbl_equator), FadeIn(lbl_lat35),
            FadeIn(compass),
            run_time=1.0,
        )
        self.wait(0.5)

        # ==========================================
        # Phase 2: 地面速度の可視化
        # ==========================================
        # 地面速度矢印
        ground_arrow_eq = Arrow(
            start=[LANE_LEFT + 1.0, EQUATOR_Y, 0],
            end=[LANE_LEFT + 1.0 + ARROW_LEN_EQ, EQUATOR_Y, 0],
            color=CLR_EQUATOR, stroke_width=4, buff=0,
            max_tip_length_to_length_ratio=0.08,
        )
        ground_arrow_35 = Arrow(
            start=[LANE_LEFT + 1.0, LAT35_Y, 0],
            end=[LANE_LEFT + 1.0 + ARROW_LEN_35, LAT35_Y, 0],
            color=CLR_LAT35, stroke_width=4, buff=0,
            max_tip_length_to_length_ratio=0.08,
        )

        self.play(Create(ground_arrow_eq), run_time=0.8)
        self.play(Create(ground_arrow_35), run_time=0.8)

        # ストライプ（動的）
        eq_stripes = always_redraw(
            lambda: make_stripes(
                EQUATOR_Y, LANE_HEIGHT,
                STRIPE_SPEED_EQ, t.get_value(), CLR_EQUATOR,
            )
        )
        lat35_stripes = always_redraw(
            lambda: make_stripes(
                LAT35_Y, LANE_HEIGHT,
                STRIPE_SPEED_35, t.get_value(), CLR_LAT35,
            )
        )

        self.add(eq_stripes, lat35_stripes)

        # ストライプ駆動開始
        t.add_updater(lambda mob, dt: mob.increment_value(dt))

        # テロップ管理用
        prev_telop = None

        telop_1 = Text(
            "地面は東に動いている。赤道ほど速い\n"
            "The ground moves east — faster at the equator",
            font_size=18,
        ).to_edge(DOWN, buff=0.4)

        self.play(FadeIn(telop_1), run_time=0.8)
        prev_telop = telop_1
        self.wait(2.0)

        # 地面速度矢印をフェードアウト（ストライプだけで速度差は十分伝わる）
        self.play(
            FadeOut(ground_arrow_eq), FadeOut(ground_arrow_35),
            run_time=0.5,
        )

        # ==========================================
        # Phase 3: 空気塊の登場
        # ==========================================
        # 空気塊のy座標トラッカー (0=赤道, 1=北緯35°)
        north_frac = ValueTracker(0)
        # 空気塊のx方向ドリフトトラッカー
        drift = ValueTracker(0)

        def air_pos():
            nf = north_frac.get_value()
            y = EQUATOR_Y + nf * (LAT35_Y - EQUATOR_Y)
            # drift × nf² で放物線的に東へ逸れる
            # （北上するほど速度差の累積で曲がりが大きくなる）
            x = AIR_START_X + drift.get_value() * nf ** 2
            return np.array([x, y, 0])

        air_dot = always_redraw(
            lambda: Dot(
                point=air_pos(),
                color=CLR_AIR, radius=AIR_RADIUS,
            )
        )

        # 空気塊の東向き速度矢印（常に赤道速度の長さ = 保存されている）
        air_arrow = always_redraw(
            lambda: Arrow(
                start=air_pos() + RIGHT * 0.2,
                end=air_pos() + RIGHT * (0.2 + ARROW_LEN_EQ),
                color=CLR_AIR_VEL, stroke_width=4, buff=0,
                max_tip_length_to_length_ratio=0.08,
            )
        )

        air_label = Text(
            "空気塊 / Air parcel",
            font_size=14, color=CLR_AIR,
        ).next_to(air_dot, DOWN, buff=0.2)

        vel_label = Text(
            f"~{V_EQUATOR_DISPLAY} km/h",
            font_size=14, color=CLR_AIR_VEL,
        )
        vel_label.add_updater(
            lambda m: m.next_to(air_arrow, UP, buff=0.08)
        )

        telop_2 = Text(
            f"赤道の空気は ~{V_EQUATOR_DISPLAY} km/h の東向き速度を持つ\n"
            f"Air at the equator carries ~{V_EQUATOR_DISPLAY} km/h eastward",
            font_size=18, color=CLR_AIR_VEL,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            FadeOut(prev_telop),
            FadeIn(air_dot), FadeIn(air_label),
            run_time=0.8,
        )
        self.play(
            Create(air_arrow), FadeIn(vel_label),
            FadeIn(telop_2),
            run_time=0.8,
        )
        prev_telop = telop_2
        self.wait(1.0)

        # ==========================================
        # Phase 4: 空気塊の北上
        # ==========================================
        telop_3a = Text(
            "空気が北に移動する\nThe air moves northward",
            font_size=18,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            FadeOut(prev_telop), FadeOut(air_label),
            FadeIn(telop_3a),
            run_time=0.5,
        )
        prev_telop = telop_3a

        # 北上アニメーション
        self.play(
            north_frac.animate.set_value(1),
            run_time=NORTHWARD_MOVE_TIME,
            rate_func=smooth,
        )

        telop_3b = Text(
            "東向き速度はそのまま残る\nThe eastward velocity is preserved",
            font_size=18, color=CLR_AIR_VEL,
        ).to_edge(DOWN, buff=0.4)

        self.play(FadeOut(prev_telop), FadeIn(telop_3b), run_time=0.5)
        prev_telop = telop_3b
        self.wait(1.0)

        # ==========================================
        # Phase 5: 速度差の可視化（クライマックス）
        # ==========================================
        # 空気の速度矢印と地面の速度矢印を比較表示
        compare_x = AIR_START_X + 0.3
        compare_y_air = LAT35_Y + 0.35
        compare_y_ground = LAT35_Y - 0.35

        air_compare = Arrow(
            start=[compare_x, compare_y_air, 0],
            end=[compare_x + ARROW_LEN_EQ, compare_y_air, 0],
            color=CLR_AIR_VEL, stroke_width=5, buff=0,
            max_tip_length_to_length_ratio=0.08,
        )
        air_compare_lbl = Text(
            f"空気 / Air: ~{V_EQUATOR_DISPLAY} km/h",
            font_size=14, color=CLR_AIR_VEL,
        ).next_to(air_compare, UP, buff=0.08)

        ground_compare = Arrow(
            start=[compare_x, compare_y_ground, 0],
            end=[compare_x + ARROW_LEN_35, compare_y_ground, 0],
            color=CLR_LAT35, stroke_width=5, buff=0,
            max_tip_length_to_length_ratio=0.08,
        )
        ground_compare_lbl = Text(
            f"地面 / Ground: ~{V_LAT35_DISPLAY} km/h",
            font_size=14, color=CLR_LAT35,
        ).next_to(ground_compare, DOWN, buff=0.08)

        # 差分矢印
        diff_arrow = Arrow(
            start=[compare_x + ARROW_LEN_35, compare_y_air, 0],
            end=[compare_x + ARROW_LEN_EQ, compare_y_air, 0],
            color=CLR_DIFF, stroke_width=6, buff=0,
        )
        diff_lbl = Text(
            f"+{V_DIFF_DISPLAY} km/h →",
            font_size=16, color=CLR_DIFF, weight=BOLD,
        ).next_to(diff_arrow, UP, buff=0.05)

        telop_4a = Text(
            f"地面: ~{V_LAT35_DISPLAY} km/h　空気: ~{V_EQUATOR_DISPLAY} km/h\n"
            f"Ground: ~{V_LAT35_DISPLAY} km/h　Air: ~{V_EQUATOR_DISPLAY} km/h",
            font_size=18,
        ).to_edge(DOWN, buff=0.4)

        # 空気塊の速度矢印を一旦非表示にして比較矢印に置き換え
        self.play(
            FadeOut(prev_telop),
            FadeOut(air_arrow), FadeOut(vel_label),
            run_time=0.3,
        )
        self.play(
            Create(air_compare), FadeIn(air_compare_lbl),
            Create(ground_compare), FadeIn(ground_compare_lbl),
            FadeIn(telop_4a),
            run_time=1.2,
        )
        prev_telop = telop_4a
        self.wait(0.8)

        # 差分矢印を強調表示
        telop_4b = Text(
            "空気は地面より速い → 東に逸れて見える\n"
            "Air is faster → appears to drift east",
            font_size=18, color=CLR_DIFF,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            Create(diff_arrow), FadeIn(diff_lbl),
            FadeOut(prev_telop), FadeIn(telop_4b),
            run_time=1.0,
        )
        prev_telop = telop_4b
        self.wait(0.8)

        # 比較矢印をフェードアウトし、空気塊を赤道に戻してリプレイ
        self.play(
            FadeOut(air_compare), FadeOut(air_compare_lbl),
            FadeOut(ground_compare), FadeOut(ground_compare_lbl),
            FadeOut(diff_arrow), FadeOut(diff_lbl),
            FadeOut(air_dot),
            run_time=0.5,
        )

        # 空気塊を赤道位置にリセットし、ドリフト係数をセット
        # air_pos: x = AIR_START_X + drift * nf² なので、
        # nf=0 の時点では drift の値に関わらず x = AIR_START_X
        north_frac.set_value(0)
        drift.set_value(DRIFT_DISTANCE)

        telop_4c = Text(
            "この速度差が「曲がり」として現れる\n"
            "This velocity difference causes the deflection",
            font_size=18, color=CLR_DIFF,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            FadeOut(prev_telop),
            FadeIn(air_dot), FadeIn(telop_4c),
            run_time=0.5,
        )
        prev_telop = telop_4c

        # TracedPathで曲線軌跡を描きながら、北上＋東ドリフトを同時実行
        curve_trail = TracedPath(
            lambda: air_dot.get_center(),
            stroke_color=CLR_AIR_VEL,
            stroke_width=4,
        )
        self.add(curve_trail)

        # north_fracだけを0→1にアニメート
        # drift は既にDRIFT_DISTANCEなので、nf² に比例して東に曲がる
        self.play(
            north_frac.animate.set_value(1),
            run_time=3.0,
            rate_func=linear,
        )

        # 曲線の横に差分ラベルを添えて因果を明示
        curve_diff_lbl = Text(
            f"+{V_DIFF_DISPLAY} km/h",
            font_size=16, color=CLR_DIFF, weight=BOLD,
        ).move_to([AIR_START_X + DRIFT_DISTANCE * 0.5, 0, 0]).shift(RIGHT * 0.8)
        curve_diff_arrow = Arrow(
            start=curve_diff_lbl.get_left() + LEFT * 0.1,
            end=curve_diff_lbl.get_left() + LEFT * 0.8,
            color=CLR_DIFF, stroke_width=3, buff=0,
            max_tip_length_to_length_ratio=0.3,
        )

        self.play(
            FadeIn(curve_diff_lbl), Create(curve_diff_arrow),
            run_time=0.6,
        )
        self.wait(0.8)

        # ==========================================
        # Phase 6: 結論
        # ==========================================
        conclusion = Text(
            "北半球で北向きの空気は右に曲がる\n"
            "Northward air deflects right in the N. Hemisphere",
            font_size=20, color=CLR_AIR_VEL,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            FadeOut(prev_telop),
            FadeOut(curve_diff_lbl), FadeOut(curve_diff_arrow),
            FadeIn(conclusion),
            run_time=0.8,
        )
        self.wait(2.5)

        # ストライプ駆動停止
        t.clear_updaters()
