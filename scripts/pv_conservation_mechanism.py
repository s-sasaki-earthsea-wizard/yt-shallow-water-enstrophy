"""PV保存のメカニズム: 水深変化が緯度方向の移動を強制する
====================================================================

PV = f/h = const から、水深hの変化がコリオリパラメーターfの変化を
要求し、結果として流れの緯度方向の移動を決めることを図解する。

h↓ → f↓ → 赤道方向へ / h↑ → f↑ → 極方向へ

yt_script.md L179-184:
  「もし水深が変わったら、コリオリパラメーターもそれに見合うように
   変わらなければならない。コリオリパラメーターが変わるということは、
   緯度が変わるということ。」

使用方法 / Usage:
  manim -pql scripts/pv_conservation_mechanism.py PVConservationMechanism
"""

from manim import *
import numpy as np


# =============================================
# パラメータ / Parameters
# =============================================

# バーのサイズ
BAR_WIDTH = 0.8
BAR_MAX_HEIGHT = 2.5
INITIAL_HEIGHT = 1.8       # f, h の初期高さ

# レイアウト
BARS_CENTER_X = -2.5        # バー群のx中心
LOGIC_CENTER_X = 3.0        # ロジック説明のx中心

# 色 / Colors
CLR_F = ORANGE
CLR_H = YELLOW_C
CLR_PV = GREEN_C
CLR_DECREASE = RED_C
CLR_INCREASE = BLUE_C
CLR_EQUATOR = RED_C
CLR_POLE = BLUE_C


# =============================================
# ユーティリティ / Utility Functions
# =============================================
def make_bar(height: float, color, label_tex: str,
             x_offset: float = 0) -> VGroup:
    """ラベル付きバーを生成

    Args:
        height: バーの高さ
        color: バーの色
        label_tex: ラベル（LaTeX）
        x_offset: x方向のオフセット
    """
    rect = Rectangle(
        width=BAR_WIDTH, height=height,
        fill_color=color, fill_opacity=0.6,
        stroke_color=color, stroke_width=2,
    )
    rect.move_to(
        np.array([BARS_CENTER_X + x_offset, 0, 0]),
        aligned_edge=DOWN,
    ).shift(DOWN * 1.2)

    label = MathTex(label_tex, font_size=28, color=color)
    label.next_to(rect, UP, buff=0.15)

    return VGroup(rect, label)


# =============================================
# メインシーン / Main Scene
# =============================================
class PVConservationMechanism(Scene):
    """PV保存による水深変化 → 緯度方向移動の図解

    fとhの比がPV=constを保つ仕組みをバーチャートで視覚化し、
    h↓→f↓→赤道方向、h↑→f↑→極方向 のロジックを示す。
    """

    def construct(self):
        # ======== ① PV = f/h = const の式を表示 ========
        formula = MathTex(
            r"\mathrm{PV}",   # [0]
            r"=",             # [1]
            r"\frac{f}{h}",   # [2]
            r"=",             # [3]
            r"\text{const}",  # [4]
            font_size=44,
        )
        formula[0].set_color(CLR_PV)
        formula[4].set_color(CLR_PV)
        formula.to_edge(UP, buff=0.5)

        self.play(FadeIn(formula), run_time=1.0)
        self.wait(1.0)

        # ======== ② 初期状態のバー表示 ========
        f_bar = make_bar(INITIAL_HEIGHT, CLR_F, "f", x_offset=-0.6)
        h_bar = make_bar(INITIAL_HEIGHT, CLR_H, "h", x_offset=0.6)

        # 分数線
        divider = Line(
            start=np.array([BARS_CENTER_X - 1.2, -1.2, 0]),
            end=np.array([BARS_CENTER_X + 1.2, -1.2, 0]),
            color=WHITE, stroke_width=2,
        )
        div_label = MathTex(
            r"\mathrm{PV} = \frac{f}{h}",
            font_size=20, color=GRAY_A,
        ).next_to(divider, DOWN, buff=0.15)

        # バーの間にイコール的な記号
        eq_sign = MathTex(
            r":", font_size=36, color=WHITE,
        ).move_to(np.array([BARS_CENTER_X, 0, 0]))

        init_label = Text(
            "初期状態 / Initial state",
            font_size=16, color=GRAY_A,
        ).next_to(h_bar, RIGHT, buff=0.8)

        self.play(
            FadeIn(f_bar), FadeIn(h_bar),
            FadeIn(eq_sign),
            FadeIn(init_label),
            run_time=1.2,
        )
        self.wait(1.5)

        # ======== ③ Case 1: h↓ → f↓ → 赤道方向へ ========
        case1_title = Text(
            "水深が浅くなったら？\nWhat if depth decreases?",
            font_size=18, color=CLR_DECREASE,
        ).move_to(np.array([LOGIC_CENTER_X, 2.0, 0]))

        self.play(
            FadeOut(init_label),
            FadeIn(case1_title),
            run_time=0.8,
        )

        # h バーを縮める
        h_rect_1 = h_bar[0]
        h_label_1 = h_bar[1]
        new_h_height_1 = INITIAL_HEIGHT * 0.55
        new_h_rect_1 = Rectangle(
            width=BAR_WIDTH, height=new_h_height_1,
            fill_color=CLR_H, fill_opacity=0.6,
            stroke_color=CLR_H, stroke_width=2,
        )
        new_h_rect_1.move_to(h_rect_1.get_bottom(), aligned_edge=DOWN)

        h_down_arrow = MathTex(
            r"\downarrow", font_size=36, color=CLR_DECREASE,
        ).next_to(new_h_rect_1, RIGHT, buff=0.3)

        self.play(
            Transform(h_rect_1, new_h_rect_1),
            h_label_1.animate.next_to(new_h_rect_1, UP, buff=0.15),
            FadeIn(h_down_arrow),
            run_time=1.0,
        )
        self.wait(0.5)

        # ロジック: PV一定のためにfも下がる
        logic_1 = VGroup()
        step1 = MathTex(
            r"h", r"\downarrow",
            font_size=32,
        ).move_to(np.array([LOGIC_CENTER_X, 0.8, 0]))
        step1[0].set_color(CLR_H)
        step1[1].set_color(CLR_DECREASE)

        arrow1 = MathTex(
            r"\Rightarrow", font_size=32, color=WHITE,
        ).next_to(step1, DOWN, buff=0.3)

        step2 = MathTex(
            r"f", r"\downarrow",
            font_size=32,
        ).next_to(arrow1, DOWN, buff=0.3)
        step2[0].set_color(CLR_F)
        step2[1].set_color(CLR_DECREASE)

        step2_reason = Text(
            "PVを一定に保つため\nto keep PV constant",
            font_size=12, color=GRAY_B,
        ).next_to(step2, RIGHT, buff=0.3)

        arrow2 = MathTex(
            r"\Rightarrow", font_size=32, color=WHITE,
        ).next_to(step2, DOWN, buff=0.3)

        step3 = Text(
            "赤道方向へ\nToward equator",
            font_size=20, color=CLR_EQUATOR,
        ).next_to(arrow2, DOWN, buff=0.3)

        step3_reason = Text(
            "fが小さい = 低緯度\nsmaller f = lower latitude",
            font_size=12, color=GRAY_B,
        ).next_to(step3, RIGHT, buff=0.3)

        self.play(FadeIn(step1), run_time=0.6)
        self.play(FadeIn(arrow1), run_time=0.3)

        # f バーも縮める
        f_rect_1 = f_bar[0]
        f_label_1 = f_bar[1]
        new_f_height_1 = INITIAL_HEIGHT * 0.55
        new_f_rect_1 = Rectangle(
            width=BAR_WIDTH, height=new_f_height_1,
            fill_color=CLR_F, fill_opacity=0.6,
            stroke_color=CLR_F, stroke_width=2,
        )
        new_f_rect_1.move_to(f_rect_1.get_bottom(), aligned_edge=DOWN)

        f_down_arrow = MathTex(
            r"\downarrow", font_size=36, color=CLR_DECREASE,
        ).next_to(new_f_rect_1, LEFT, buff=0.3)

        self.play(
            FadeIn(step2), FadeIn(step2_reason),
            Transform(f_rect_1, new_f_rect_1),
            f_label_1.animate.next_to(new_f_rect_1, UP, buff=0.15),
            FadeIn(f_down_arrow),
            run_time=1.0,
        )
        self.play(FadeIn(arrow2), run_time=0.3)
        self.play(FadeIn(step3), FadeIn(step3_reason), run_time=0.8)
        self.wait(2.5)

        # ======== Case 1 クリーンアップ ========
        case1_elements = VGroup(
            case1_title,
            h_down_arrow, f_down_arrow,
            step1, arrow1, step2, step2_reason,
            arrow2, step3, step3_reason,
        )
        self.play(FadeOut(case1_elements), run_time=0.5)

        # バーを初期状態に戻す
        reset_f = Rectangle(
            width=BAR_WIDTH, height=INITIAL_HEIGHT,
            fill_color=CLR_F, fill_opacity=0.6,
            stroke_color=CLR_F, stroke_width=2,
        )
        reset_f.move_to(f_rect_1.get_bottom(), aligned_edge=DOWN)

        reset_h = Rectangle(
            width=BAR_WIDTH, height=INITIAL_HEIGHT,
            fill_color=CLR_H, fill_opacity=0.6,
            stroke_color=CLR_H, stroke_width=2,
        )
        reset_h.move_to(h_rect_1.get_bottom(), aligned_edge=DOWN)

        self.play(
            Transform(f_rect_1, reset_f),
            f_label_1.animate.next_to(reset_f, UP, buff=0.15),
            Transform(h_rect_1, reset_h),
            h_label_1.animate.next_to(reset_h, UP, buff=0.15),
            run_time=0.8,
        )

        # ======== ④ Case 2: h↑ → f↑ → 極方向へ ========
        case2_title = Text(
            "水深が深くなったら？\nWhat if depth increases?",
            font_size=18, color=CLR_INCREASE,
        ).move_to(np.array([LOGIC_CENTER_X, 2.0, 0]))

        self.play(FadeIn(case2_title), run_time=0.8)

        # h バーを伸ばす
        new_h_height_2 = INITIAL_HEIGHT * 1.4
        new_h_rect_2 = Rectangle(
            width=BAR_WIDTH, height=new_h_height_2,
            fill_color=CLR_H, fill_opacity=0.6,
            stroke_color=CLR_H, stroke_width=2,
        )
        new_h_rect_2.move_to(h_rect_1.get_bottom(), aligned_edge=DOWN)

        h_up_arrow = MathTex(
            r"\uparrow", font_size=36, color=CLR_INCREASE,
        ).next_to(new_h_rect_2, RIGHT, buff=0.3)

        self.play(
            Transform(h_rect_1, new_h_rect_2),
            h_label_1.animate.next_to(new_h_rect_2, UP, buff=0.15),
            FadeIn(h_up_arrow),
            run_time=1.0,
        )
        self.wait(0.5)

        # ロジック
        step1b = MathTex(
            r"h", r"\uparrow",
            font_size=32,
        ).move_to(np.array([LOGIC_CENTER_X, 0.8, 0]))
        step1b[0].set_color(CLR_H)
        step1b[1].set_color(CLR_INCREASE)

        arrow1b = MathTex(
            r"\Rightarrow", font_size=32, color=WHITE,
        ).next_to(step1b, DOWN, buff=0.3)

        step2b = MathTex(
            r"f", r"\uparrow",
            font_size=32,
        ).next_to(arrow1b, DOWN, buff=0.3)
        step2b[0].set_color(CLR_F)
        step2b[1].set_color(CLR_INCREASE)

        step2b_reason = Text(
            "PVを一定に保つため\nto keep PV constant",
            font_size=12, color=GRAY_B,
        ).next_to(step2b, RIGHT, buff=0.3)

        arrow2b = MathTex(
            r"\Rightarrow", font_size=32, color=WHITE,
        ).next_to(step2b, DOWN, buff=0.3)

        step3b = Text(
            "極方向へ\nToward poles",
            font_size=20, color=CLR_POLE,
        ).next_to(arrow2b, DOWN, buff=0.3)

        step3b_reason = Text(
            "fが大きい = 高緯度\nlarger f = higher latitude",
            font_size=12, color=GRAY_B,
        ).next_to(step3b, RIGHT, buff=0.3)

        self.play(FadeIn(step1b), run_time=0.6)
        self.play(FadeIn(arrow1b), run_time=0.3)

        # f バーも伸ばす
        new_f_height_2 = INITIAL_HEIGHT * 1.4
        new_f_rect_2 = Rectangle(
            width=BAR_WIDTH, height=new_f_height_2,
            fill_color=CLR_F, fill_opacity=0.6,
            stroke_color=CLR_F, stroke_width=2,
        )
        new_f_rect_2.move_to(f_rect_1.get_bottom(), aligned_edge=DOWN)

        f_up_arrow = MathTex(
            r"\uparrow", font_size=36, color=CLR_INCREASE,
        ).next_to(new_f_rect_2, LEFT, buff=0.3)

        self.play(
            FadeIn(step2b), FadeIn(step2b_reason),
            Transform(f_rect_1, new_f_rect_2),
            f_label_1.animate.next_to(new_f_rect_2, UP, buff=0.15),
            FadeIn(f_up_arrow),
            run_time=1.0,
        )
        self.play(FadeIn(arrow2b), run_time=0.3)
        self.play(FadeIn(step3b), FadeIn(step3b_reason), run_time=0.8)
        self.wait(2.5)

        # ======== ⑤ 結びのテロップ ========
        case2_elements = VGroup(
            case2_title,
            h_up_arrow, f_up_arrow,
            step1b, arrow1b, step2b, step2b_reason,
            arrow2b, step3b, step3b_reason,
        )
        self.play(FadeOut(case2_elements), run_time=0.5)

        # バーをリセット
        reset_f2 = Rectangle(
            width=BAR_WIDTH, height=INITIAL_HEIGHT,
            fill_color=CLR_F, fill_opacity=0.6,
            stroke_color=CLR_F, stroke_width=2,
        )
        reset_f2.move_to(f_rect_1.get_bottom(), aligned_edge=DOWN)
        reset_h2 = Rectangle(
            width=BAR_WIDTH, height=INITIAL_HEIGHT,
            fill_color=CLR_H, fill_opacity=0.6,
            stroke_color=CLR_H, stroke_width=2,
        )
        reset_h2.move_to(h_rect_1.get_bottom(), aligned_edge=DOWN)

        self.play(
            Transform(f_rect_1, reset_f2),
            f_label_1.animate.next_to(reset_f2, UP, buff=0.15),
            Transform(h_rect_1, reset_h2),
            h_label_1.animate.next_to(reset_h2, UP, buff=0.15),
            run_time=0.5,
        )

        conclusion = Text(
            "水深の変化が流れの南北方向の動きを強制する\n"
            "Changes in depth force meridional movement",
            font_size=22, color=WHITE,
        ).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(conclusion), run_time=1.0)
        self.wait(3.0)
