"""コリオリ力のManimアニメーション / Coriolis Effect Animation
==========================================================

回転する円盤（メリーゴーランド）上でボールを投げたとき、
慣性系ではまっすぐ飛ぶのに、回転系では曲がって見える現象を可視化する。

yt_script.md L23-24:
  「メリーゴーランドに乗りながら、隣にいる友達にボールを投げることを想像してみてください。
   あなたはまっすぐ投げたつもりなのに、ボールは曲がって飛んでいきます。」

使用方法 / Usage:
  manim -pql scripts/coriolis_merry_go_round.py CoriolisSplitView
  manim -pql scripts/coriolis_merry_go_round.py CoriolisSequential
"""

from manim import *
import numpy as np

# =============================================
# パラメータ / Parameters
# =============================================
DISK_RADIUS = 1.8  # 円盤の半径
PERSON_RADIUS = 1.3  # 人物の中心からの距離
OMEGA = PI / 9  # 角速度 rad/s（反時計回り = 北半球の地球と同じ向き）
FLIGHT_TIME = 1.0  # ボールの飛行時間 s
# → 飛行中の回転角: ω × T = π/3 ≈ 60°
THROW_SPEED_SCALE = 3.0  # 投球速度の倍率（1.0 = Bにちょうど届く速度）

ANGLE_A = 0  # 投げる人の初期角度（右）
ANGLE_B = PI / 2  # 受ける人の初期角度（上）

# 色
CLR_DISK = BLUE_E
CLR_A = RED_C  # 投げる人
CLR_B = GREEN_C  # 受ける人
CLR_BALL = YELLOW
CLR_TRAIL_I = YELLOW_B  # 慣性系の軌跡
CLR_TRAIL_R = ORANGE  # 回転系の軌跡


# =============================================
# ユーティリティ / Utility Functions
# =============================================
def polar(angle: float, r: float = PERSON_RADIUS) -> np.ndarray:
    """極座標 → 3Dベクトル"""
    return np.array([r * np.cos(angle), r * np.sin(angle), 0])


def rot2d(v: np.ndarray, theta: float) -> np.ndarray:
    """2D回転（3次元ベクトルのx,y成分を回転）"""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], 0])


def compute_v_inertial(pa: np.ndarray, pb: np.ndarray) -> np.ndarray:
    """回転系でA→B方向に投げたときの、慣性系での初速度を計算

    v_inertial = v_aim_rotating + ω × r_A

    回転系でAがBに向かって投げる（初速がA→B方向）ためには、
    Aの回転速度 ω × r_A を加える必要がある。
    こうすると慣性系では直線だが、A→B方向とはずれた方向に飛ぶ。
    """
    v_aim = THROW_SPEED_SCALE * (pb - pa) / FLIGHT_TIME
    omega_cross_r = np.array([-OMEGA * pa[1], OMEGA * pa[0], 0])
    return v_aim + omega_cross_r


# 初期位置と慣性系初速度（グローバル）
POS_A = polar(ANGLE_A)
POS_B = polar(ANGLE_B)
V_INERTIAL = compute_v_inertial(POS_A, POS_B)


def ball_inertial(t: float, pa: np.ndarray = POS_A,
                  vi: np.ndarray = V_INERTIAL) -> np.ndarray:
    """慣性系でのボール位置（等速直線運動）"""
    return pa + vi * np.clip(t, 0.0, FLIGHT_TIME)


def ball_rotating(t: float, pa: np.ndarray = POS_A,
                  vi: np.ndarray = V_INERTIAL) -> np.ndarray:
    """回転系でのボール位置（慣性系の位置を角度 -ωt だけ逆回転）"""
    return rot2d(ball_inertial(t, pa, vi), -OMEGA * t)


def make_disk(center: np.ndarray, theta: float = 0,
              radius: float = DISK_RADIUS) -> VGroup:
    """円盤 + 放射状マーカーを生成"""
    circle = Circle(
        radius=radius, color=CLR_DISK,
        fill_opacity=0.08, stroke_width=2,
    ).move_to(center)

    n_marks = 8
    marks = VGroup(*[
        Line(
            center + radius * 0.78 * np.array([
                np.cos(i * TAU / n_marks + theta),
                np.sin(i * TAU / n_marks + theta), 0]),
            center + radius * 0.95 * np.array([
                np.cos(i * TAU / n_marks + theta),
                np.sin(i * TAU / n_marks + theta), 0]),
            color=BLUE_C, stroke_width=1.5,
        )
        for i in range(n_marks)
    ])

    axis_dot = Dot(center, color=WHITE, radius=0.04)
    return VGroup(circle, marks, axis_dot)


def make_rot_arrow(center: np.ndarray, theta_offset: float = 0,
                   radius: float = DISK_RADIUS) -> VMobject:
    """回転方向を示す弧矢印"""
    return Arc(
        radius=radius + 0.25,
        start_angle=PI / 3 + theta_offset,
        angle=PI / 2.5,
        color=WHITE, stroke_width=2,
        arc_center=center,
    ).add_tip(tip_length=0.15, tip_width=0.1)


# =============================================
# シーン1: 左右分割表示
# Inertial vs Rotating — side by side
# =============================================
class CoriolisSplitView(Scene):
    """慣性系と回転系を左右に並べて同時表示"""

    def construct(self):
        # パネル中心
        scale = 0.78  # 分割用に縮小
        r_disk = DISK_RADIUS * scale
        r_person = PERSON_RADIUS * scale
        pA = polar(ANGLE_A, r_person)
        pB = polar(ANGLE_B, r_person)

        LC = LEFT * 3.5  # 左パネル中心
        RC = RIGHT * 3.5  # 右パネル中心
        t = ValueTracker(0)

        # ---- UI要素 ----
        title = Text(
            "コリオリ力 / Coriolis Effect", font_size=32,
        ).to_edge(UP, buff=0.3)

        lbl_L = Text(
            "慣性系 / Inertial Frame", font_size=20,
        ).move_to(LC + UP * (r_disk + 0.7))
        lbl_R = Text(
            "回転系 / Rotating Frame", font_size=20,
        ).move_to(RC + UP * (r_disk + 0.7))

        divider = DashedLine(
            UP * 3.8, DOWN * 3.8,
            color=GRAY_C, dash_length=0.15,
        )

        # ---- 円盤 ----
        disk_L = always_redraw(
            lambda: make_disk(LC, OMEGA * t.get_value(), r_disk))
        disk_R = always_redraw(
            lambda: make_disk(RC, 0, r_disk))

        rot_arr = always_redraw(
            lambda: make_rot_arrow(LC, OMEGA * t.get_value(), r_disk))

        # ---- 人物ドット ----
        # 慣性系: 円盤と一緒に回転
        dot_A_L = always_redraw(lambda: Dot(
            LC + rot2d(pA, OMEGA * t.get_value()),
            color=CLR_A, radius=0.09))
        dot_B_L = always_redraw(lambda: Dot(
            LC + rot2d(pB, OMEGA * t.get_value()),
            color=CLR_B, radius=0.09))

        # 回転系: 位置固定
        dot_A_R = Dot(RC + pA, color=CLR_A, radius=0.09)
        dot_B_R = Dot(RC + pB, color=CLR_B, radius=0.09)

        lbl_a = Text("A", font_size=15, color=CLR_A).next_to(dot_A_R, DR, buff=0.08)
        lbl_b = Text("B", font_size=15, color=CLR_B).next_to(dot_B_R, UL, buff=0.08)

        # ---- 狙い線（回転系: AからBへの破線）----
        aim = DashedLine(
            RC + pA, RC + pB,
            color=GRAY_B, stroke_width=1.5, dash_length=0.08,
        )

        # ---- ボール ----
        vi_scaled = compute_v_inertial(pA, pB)

        def bi(tt):
            return pA + vi_scaled * np.clip(tt, 0, FLIGHT_TIME)

        def br(tt):
            return rot2d(bi(tt), -OMEGA * tt)

        ball_L = Dot(LC + pA, color=CLR_BALL, radius=0.065)
        ball_R = Dot(RC + pA, color=CLR_BALL, radius=0.065)
        ball_L.add_updater(lambda m: m.move_to(LC + bi(t.get_value())))
        ball_R.add_updater(lambda m: m.move_to(RC + br(t.get_value())))

        trail_L = TracedPath(
            ball_L.get_center,
            stroke_color=CLR_TRAIL_I, stroke_width=2.5,
        )
        trail_R = TracedPath(
            ball_R.get_center,
            stroke_color=CLR_TRAIL_R, stroke_width=2.5,
        )

        # ======== アニメーション ========
        # 1. レイアウト
        self.play(
            FadeIn(title), FadeIn(lbl_L), FadeIn(lbl_R),
            Create(divider), run_time=1,
        )

        # 2. 円盤
        self.play(FadeIn(disk_L), FadeIn(disk_R), FadeIn(rot_arr), run_time=0.8)

        # 3. 人物
        self.play(
            FadeIn(dot_A_L), FadeIn(dot_B_L),
            FadeIn(dot_A_R), FadeIn(dot_B_R),
            FadeIn(lbl_a), FadeIn(lbl_b),
            run_time=0.6,
        )

        # 4. 狙い線
        self.play(Create(aim), run_time=0.5)

        # 5. 投球テキスト
        throw_txt = Text(
            "投げる！ / Throw!", font_size=20, color=CLR_BALL,
        ).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(throw_txt), run_time=0.4)
        self.wait(0.3)

        # 6. ボール飛行
        self.add(ball_L, ball_R, trail_L, trail_R)
        self.play(
            FadeOut(throw_txt),
            t.animate.set_value(FLIGHT_TIME),
            run_time=FLIGHT_TIME, rate_func=linear,
        )

        # 7. 結果テキスト
        res_L = Text(
            "まっすぐ！ / Straight!", font_size=20, color=CLR_TRAIL_I,
        ).move_to(LC + DOWN * (r_disk + 0.7))
        res_R = Text(
            "曲がった！ / Curved!", font_size=20, color=CLR_TRAIL_R,
        ).move_to(RC + DOWN * (r_disk + 0.7))

        self.play(FadeIn(res_L), FadeIn(res_R), run_time=0.8)
        self.wait(2)


# =============================================
# シーン2: 順次表示（慣性系 → 回転系）
# Full-screen: Inertial, then Rotating
# =============================================
class CoriolisSequential(Scene):
    """慣性系 → 回転系の順番で全画面表示"""

    def _show_inertial(self):
        """パート1: 慣性系（外からの視点）"""
        C = ORIGIN
        t = ValueTracker(0)

        title = Text(
            "慣性系（外からの視点）/ Inertial Frame",
            font_size=28,
        ).to_edge(UP, buff=0.4)

        disk = always_redraw(
            lambda: make_disk(C, OMEGA * t.get_value()))
        arr = always_redraw(
            lambda: make_rot_arrow(C, OMEGA * t.get_value()))

        # 人物: 円盤と一緒に回転
        dA = always_redraw(lambda: Dot(
            C + rot2d(POS_A, OMEGA * t.get_value()),
            color=CLR_A, radius=0.12))
        dB = always_redraw(lambda: Dot(
            C + rot2d(POS_B, OMEGA * t.get_value()),
            color=CLR_B, radius=0.12))

        # ラベル（人物に追従）
        lA = Text("A", font_size=18, color=CLR_A)
        lA.add_updater(lambda m: m.next_to(
            C + rot2d(POS_A, OMEGA * t.get_value()), DR, buff=0.12))
        lB = Text("B", font_size=18, color=CLR_B)
        lB.add_updater(lambda m: m.next_to(
            C + rot2d(POS_B, OMEGA * t.get_value()), UL, buff=0.12))

        # ボール
        ball = Dot(C + POS_A, color=CLR_BALL, radius=0.09)
        ball.add_updater(
            lambda m: m.move_to(C + ball_inertial(t.get_value())))
        trail = TracedPath(
            ball.get_center,
            stroke_color=CLR_TRAIL_I, stroke_width=3,
        )

        # アニメーション
        self.play(FadeIn(title), FadeIn(disk), FadeIn(arr), run_time=1)
        self.play(FadeIn(dA), FadeIn(dB), FadeIn(lA), FadeIn(lB), run_time=0.5)

        throw_txt = Text(
            "投げる！ / Throw!", font_size=22, color=CLR_BALL,
        ).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(throw_txt), run_time=0.4)
        self.wait(0.3)

        self.add(ball, trail)
        self.play(
            FadeOut(throw_txt),
            t.animate.set_value(FLIGHT_TIME),
            run_time=FLIGHT_TIME, rate_func=linear,
        )

        note = Text(
            "ボールはまっすぐ飛んでいる\nThe ball travels in a straight line",
            font_size=22, color=CLR_TRAIL_I,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)

    def _show_rotating(self):
        """パート2: 回転系（一緒に回る視点）"""
        C = ORIGIN
        t = ValueTracker(0)

        title = Text(
            "回転系（一緒に回る視点）/ Rotating Frame",
            font_size=28,
        ).to_edge(UP, buff=0.4)

        disk = make_disk(C, 0)  # 静止

        # 人物: 位置固定
        dA = Dot(C + POS_A, color=CLR_A, radius=0.12)
        dB = Dot(C + POS_B, color=CLR_B, radius=0.12)
        lA = Text("A", font_size=18, color=CLR_A).next_to(dA, DR, buff=0.12)
        lB = Text("B", font_size=18, color=CLR_B).next_to(dB, UL, buff=0.12)

        # AからBへの狙い線（まっすぐ飛ぶはずの方向）
        aim = DashedLine(
            C + POS_A, C + POS_B,
            color=GRAY_B, stroke_width=1.5, dash_length=0.1,
        )

        # ボール
        ball = Dot(C + POS_A, color=CLR_BALL, radius=0.09)
        ball.add_updater(
            lambda m: m.move_to(C + ball_rotating(t.get_value())))
        trail = TracedPath(
            ball.get_center,
            stroke_color=CLR_TRAIL_R, stroke_width=3,
        )

        # アニメーション
        self.play(FadeIn(title), FadeIn(disk), run_time=1)
        self.play(
            FadeIn(dA), FadeIn(dB),
            FadeIn(lA), FadeIn(lB),
            run_time=0.5,
        )
        self.play(Create(aim), run_time=0.5)

        throw_txt = Text(
            "投げる！ / Throw!", font_size=22, color=CLR_BALL,
        ).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(throw_txt), run_time=0.4)
        self.wait(0.3)

        self.add(ball, trail)
        self.play(
            FadeOut(throw_txt),
            t.animate.set_value(FLIGHT_TIME),
            run_time=FLIGHT_TIME, rate_func=linear,
        )

        note = Text(
            "同じボールなのに曲がって見える！\nThe same ball appears to curve!",
            font_size=22, color=CLR_TRAIL_R,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(1.5)

        # 結びテキスト
        conclusion = Text(
            "この見かけの力 = コリオリ力\nThis apparent force = Coriolis effect",
            font_size=26,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeOut(note), FadeIn(conclusion), run_time=1)
        self.wait(2)

    def construct(self):
        self._show_inertial()
        self._show_rotating()
