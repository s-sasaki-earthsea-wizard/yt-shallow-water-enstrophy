"""PV保存: h一定 → 帯状流 / PV Conservation: Constant h → Zonal Flow
====================================================================

大気の厚みhが一定のとき、PV保存によりfも一定 → 緯度が変わらない
→ 流れは東西方向に制限される、という偏西風の帯状構造の説明。

yt_script.md L206-210:
  「偏西風のような大気の大きな流れでは、大気の厚みがほぼ一定…
   厚みが一定の時、PVが保存されるためには、コリオリパラメーターも
   一定でなければなりません。…流れは南北方向にはほとんど動けず、
   東西方向に制限されるんです。」

使用方法 / Usage:
  manim -pql scripts/pv_zonal_flow.py PVZonalFlow
"""

from manim import *
import numpy as np


# =============================================
# パラメータ / Parameters
# =============================================

# 色 / Colors
CLR_F = ORANGE
CLR_H = YELLOW_C
CLR_PV = GREEN_C
CLR_CONST = GREEN_C
CLR_WIND = BLUE_C           # 東西風の矢印
CLR_BLOCKED = RED_C          # ブロックされた南北方向
CLR_LATITUDE = GRAY_B        # 緯度線


# =============================================
# メインシーン / Main Scene
# =============================================
class PVZonalFlow(Scene):
    """h一定 → f一定 → 帯状流のロジックをアニメーションで図解

    前半: 数式によるロジックチェーン
    後半: 緯度線上の東西矢印 + 南北ブロックの図解
    """

    def construct(self):
        # ======== ① 前提条件: h ≈ 一定 ========
        premise = Text(
            "大気の厚みはほぼ一定\n"
            "Atmospheric thickness is nearly constant",
            font_size=22, color=CLR_H,
        ).move_to(UP * 2.5)

        # 大気層の模式図（横長の矩形、均一な厚み）
        atmo_layer = Rectangle(
            width=8, height=1.0,
            fill_color=BLUE_E, fill_opacity=0.2,
            stroke_color=CLR_H, stroke_width=2,
        ).move_to(UP * 0.5)

        h_arrow_l = DoubleArrow(
            start=atmo_layer.get_bottom() + LEFT * 3.5,
            end=atmo_layer.get_top() + LEFT * 3.5,
            color=CLR_H, stroke_width=2,
            buff=0.05, tip_length=0.15,
        )
        h_label = MathTex(
            "h", font_size=28, color=CLR_H,
        ).next_to(h_arrow_l, LEFT, buff=0.1)

        h_const = MathTex(
            r"h \approx \text{const}",
            font_size=32, color=CLR_H,
        ).next_to(atmo_layer, RIGHT, buff=0.5)

        # 地表線
        ground = Line(
            start=atmo_layer.get_corner(DL),
            end=atmo_layer.get_corner(DR),
            color=GREEN_E, stroke_width=3,
        )
        # 大気上端
        top_line = DashedLine(
            start=atmo_layer.get_corner(UL),
            end=atmo_layer.get_corner(UR),
            color=GRAY_A, stroke_width=1.5,
            dash_length=0.15,
        )

        self.play(
            FadeIn(premise),
            FadeIn(atmo_layer), FadeIn(ground), FadeIn(top_line),
            FadeIn(h_arrow_l), FadeIn(h_label),
            FadeIn(h_const),
            run_time=1.5,
        )
        self.wait(2.0)

        # 全部まとめてフェードアウト
        premise_group = VGroup(
            premise, atmo_layer, ground, top_line,
            h_arrow_l, h_label, h_const,
        )
        self.play(FadeOut(premise_group), run_time=0.5)

        # ======== ② ロジックチェーン ========
        formula = MathTex(
            r"\mathrm{PV}",
            r"=",
            r"\frac{f}{h}",
            r"=",
            r"\text{const}",
            font_size=40,
        ).to_edge(UP, buff=0.5)
        formula[0].set_color(CLR_PV)
        formula[4].set_color(CLR_CONST)

        self.play(FadeIn(formula), run_time=0.8)

        # ロジックチェーンを段階的に表示
        chain_y = 1.5
        spacing = 1.3

        step1 = MathTex(
            r"h", r"=", r"\text{const}",
            font_size=36,
        ).move_to(UP * chain_y)
        step1[0].set_color(CLR_H)
        step1[2].set_color(CLR_CONST)

        arr1 = MathTex(
            r"\Downarrow", font_size=36, color=WHITE,
        ).next_to(step1, DOWN, buff=0.25)

        step2 = MathTex(
            r"f", r"=", r"\text{const}",
            font_size=36,
        ).next_to(arr1, DOWN, buff=0.25)
        step2[0].set_color(CLR_F)
        step2[2].set_color(CLR_CONST)

        arr2 = MathTex(
            r"\Downarrow", font_size=36, color=WHITE,
        ).next_to(step2, DOWN, buff=0.25)

        step3 = Text(
            "緯度が一定 / Latitude is constant",
            font_size=22, color=CLR_F,
        ).next_to(arr2, DOWN, buff=0.25)

        arr3 = MathTex(
            r"\Downarrow", font_size=36, color=WHITE,
        ).next_to(step3, DOWN, buff=0.25)

        step4 = Text(
            "東西方向にしか動けない\nFlow restricted to east-west",
            font_size=22, color=CLR_WIND,
        ).next_to(arr3, DOWN, buff=0.25)

        self.play(FadeIn(step1), run_time=0.6)
        self.play(FadeIn(arr1), run_time=0.3)
        self.play(FadeIn(step2), run_time=0.6)
        self.play(FadeIn(arr2), run_time=0.3)
        self.play(FadeIn(step3), run_time=0.6)
        self.play(FadeIn(arr3), run_time=0.3)
        self.play(FadeIn(step4), run_time=0.6)
        self.wait(2.5)

        # チェーン全体をフェードアウト
        chain = VGroup(
            step1, arr1, step2, arr2, step3, arr3, step4,
        )
        self.play(FadeOut(chain), run_time=0.5)

        # ======== ③ 図解: 緯度線 + 東西矢印 + 南北ブロック ========
        # 緯度線（水平線で表現）
        lat_lines = VGroup()
        lat_labels = VGroup()
        lat_data = [
            (-1.8, "60°N"),
            (-0.6, "30°N"),
            (0.6, "0° (赤道 / Equator)"),
            (1.8, "30°S"),
        ]

        for y_pos, label_text in lat_data:
            line = DashedLine(
                start=LEFT * 5 + UP * (-y_pos),
                end=RIGHT * 5 + UP * (-y_pos),
                color=CLR_LATITUDE,
                stroke_width=1.5,
                dash_length=0.2,
            )
            lat_lines.add(line)

            lbl = Text(
                label_text, font_size=12, color=CLR_LATITUDE,
            ).next_to(line, RIGHT, buff=0.15)
            lat_labels.add(lbl)

        self.play(
            *[Create(l) for l in lat_lines],
            *[FadeIn(l) for l in lat_labels],
            run_time=1.0,
        )

        # 東西方向の矢印（帯状に流れる風）
        wind_arrows = VGroup()
        for y_pos, _ in lat_data[:2]:  # 60°N, 30°N のみ
            for x in np.linspace(-3.5, 2.5, 4):
                arrow = Arrow(
                    start=LEFT * 0.6, end=RIGHT * 0.6,
                    color=CLR_WIND, stroke_width=3,
                    buff=0, tip_length=0.15,
                    max_tip_length_to_length_ratio=0.15,
                ).move_to(np.array([x, -y_pos, 0]))
                wind_arrows.add(arrow)

        wind_label = Text(
            "東西方向の風（帯状流）\nZonal wind (east-west flow)",
            font_size=16, color=CLR_WIND,
        ).to_edge(DOWN, buff=1.2)

        self.play(
            *[GrowArrow(a) for a in wind_arrows],
            FadeIn(wind_label),
            run_time=1.5,
        )
        self.wait(1.0)

        # 南北方向のブロック（×印付き矢印）
        blocked_arrows = VGroup()
        blocked_crosses = VGroup()

        for x_pos in [-1.0, 2.0]:
            b_arrow = Arrow(
                start=DOWN * 0.5, end=UP * 0.5,
                color=CLR_BLOCKED, stroke_width=2,
                buff=0, tip_length=0.12,
            ).move_to(np.array([x_pos, 1.2, 0]))
            blocked_arrows.add(b_arrow)

            cross = VGroup(
                Line(
                    start=b_arrow.get_center() + UL * 0.2,
                    end=b_arrow.get_center() + DR * 0.2,
                    color=CLR_BLOCKED, stroke_width=4,
                ),
                Line(
                    start=b_arrow.get_center() + UR * 0.2,
                    end=b_arrow.get_center() + DL * 0.2,
                    color=CLR_BLOCKED, stroke_width=4,
                ),
            )
            blocked_crosses.add(cross)

        blocked_label = Text(
            "南北方向には動けない\nMeridional flow blocked",
            font_size=16, color=CLR_BLOCKED,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            *[GrowArrow(a) for a in blocked_arrows],
            run_time=0.5,
        )
        self.play(
            *[Create(c) for c in blocked_crosses],
            FadeIn(blocked_label),
            run_time=0.8,
        )
        self.wait(3.0)
