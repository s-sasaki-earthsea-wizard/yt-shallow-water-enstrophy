"""海嶺による流れの偏向（topographic steering）
====================================================================

海嶺（海底の山）を越える流れがPV保存により赤道方向に曲がる様子を
断面図（Side view）と平面図（Top view）の2視点で図解する。

yt_script.md L221-233:
  「海嶺の上では海底が盛り上がっているので、水深が小さくなります。
   PVを保存するためには、コリオリパラメーターも小さくならなければ
   なりません。つまり...赤道方向に流れが曲がることになります。」

使用方法 / Usage:
  manim -pql scripts/pv_topographic_steering.py TopographicSteering
"""

from manim import *
import numpy as np


# =============================================
# パラメータ / Parameters
# =============================================

# 色 / Colors
CLR_SEA_SURFACE = BLUE_C
CLR_SEAFLOOR = GOLD_E
CLR_RIDGE = GOLD_C
CLR_OCEAN_FILL = BLUE_E
CLR_H = YELLOW_C
CLR_F = ORANGE
CLR_FLOW = TEAL_C
CLR_DEFLECTED = RED_C
CLR_RIDGE_TOP = GOLD_C
CLR_LATITUDE = GRAY_B


# =============================================
# メインシーン / Main Scene
# =============================================
class TopographicSteering(Scene):
    """海嶺による流れの偏向を2視点で図解

    前半: 断面図で水深変化とPV保存のロジックを示す
    後半: 平面図で流れが南に曲がる様子をアニメーション
    """

    def construct(self):
        # ======== ① 断面図（Side View） ========
        view_label = Text(
            "断面図 / Cross-section view",
            font_size=18, color=GRAY_A,
        ).to_edge(UP, buff=0.4)
        self.play(FadeIn(view_label), run_time=0.5)

        # 海面（水平線）
        sea_y = 1.5
        floor_y = -1.5
        sea_surface = Line(
            start=LEFT * 6 + UP * sea_y,
            end=RIGHT * 6 + UP * sea_y,
            color=CLR_SEA_SURFACE, stroke_width=3,
        )
        lbl_surface = Text(
            "海面 / Sea surface",
            font_size=12, color=CLR_SEA_SURFACE,
        ).next_to(sea_surface, UP, buff=0.1).shift(LEFT * 3)

        # 海底（海嶺付きのカーブ）
        ridge_height = 1.8  # 海嶺の高さ
        ridge_sigma = 1.2   # 海嶺の幅パラメータ

        seafloor = ParametricFunction(
            lambda t: np.array([
                t,
                floor_y + ridge_height * np.exp(-t**2 / ridge_sigma**2),
                0,
            ]),
            t_range=[-6, 6, 0.02],
            color=CLR_SEAFLOOR,
            stroke_width=3,
        )

        # 海嶺ラベル
        ridge_peak_y = floor_y + ridge_height
        lbl_ridge = Text(
            "海嶺 / Mid-ocean ridge",
            font_size=14, color=CLR_RIDGE,
        ).move_to(np.array([0, ridge_peak_y + 0.3, 0]))

        # 海水の塗りつぶし（簡易的に矩形 + 海嶺上の部分を覆う）
        ocean_fill = Polygon(
            np.array([-6, sea_y, 0]),
            np.array([6, sea_y, 0]),
            *[np.array([t, floor_y + ridge_height
                        * np.exp(-t**2 / ridge_sigma**2), 0])
              for t in np.linspace(6, -6, 80)],
            fill_color=CLR_OCEAN_FILL,
            fill_opacity=0.2,
            stroke_width=0,
        )

        # h の矢印: 海嶺の左（深い）
        h1_x = -3.5
        h1_bottom = floor_y + ridge_height * np.exp(
            -h1_x**2 / ridge_sigma**2)
        h1_arrow = DoubleArrow(
            start=np.array([h1_x, h1_bottom, 0]),
            end=np.array([h1_x, sea_y, 0]),
            color=CLR_H, stroke_width=2,
            buff=0.05, tip_length=0.15,
        )
        h1_label = MathTex(
            r"h_1", font_size=28, color=CLR_H,
        ).next_to(h1_arrow, LEFT, buff=0.1)
        h1_note = Text(
            "深い / Deep",
            font_size=11, color=CLR_H,
        ).next_to(h1_label, DOWN, buff=0.1)

        # h の矢印: 海嶺の上（浅い）
        h2_x = 0.0
        h2_bottom = floor_y + ridge_height * np.exp(
            -h2_x**2 / ridge_sigma**2)
        h2_arrow = DoubleArrow(
            start=np.array([h2_x, h2_bottom, 0]),
            end=np.array([h2_x, sea_y, 0]),
            color=CLR_H, stroke_width=2,
            buff=0.05, tip_length=0.15,
        )
        h2_label = MathTex(
            r"h_2", font_size=28, color=CLR_H,
        ).next_to(h2_arrow, RIGHT, buff=0.1)
        h2_note = Text(
            "浅い / Shallow",
            font_size=11, color=CLR_H,
        ).next_to(h2_label, DOWN, buff=0.1)

        # 流れの矢印（東向き = 左→右）
        flow_arrow = Arrow(
            start=LEFT * 5.5 + UP * 0.5,
            end=RIGHT * 5.5 + UP * 0.5,
            color=CLR_FLOW, stroke_width=3,
            max_tip_length_to_length_ratio=0.03,
        )
        flow_label = Text(
            "海流 / Ocean current",
            font_size=12, color=CLR_FLOW,
        ).next_to(flow_arrow, UP, buff=0.1).shift(LEFT * 2)

        self.play(
            FadeIn(ocean_fill),
            Create(sea_surface), FadeIn(lbl_surface),
            Create(seafloor), FadeIn(lbl_ridge),
            run_time=1.5,
        )
        self.play(
            FadeIn(h1_arrow), FadeIn(h1_label), FadeIn(h1_note),
            FadeIn(h2_arrow), FadeIn(h2_label), FadeIn(h2_note),
            run_time=1.0,
        )
        self.play(
            GrowArrow(flow_arrow), FadeIn(flow_label),
            run_time=0.8,
        )
        self.wait(1.0)

        # PV保存のロジック（日本語はTextで分離）
        logic_math = MathTex(
            r"h", r"\downarrow",
            r"\;\Rightarrow\;",
            r"f", r"\downarrow",
            r"\;\Rightarrow\;",
            font_size=28,
        )
        logic_math[0].set_color(CLR_H)
        logic_math[1].set_color(CLR_DEFLECTED)
        logic_math[3].set_color(CLR_F)
        logic_math[4].set_color(CLR_DEFLECTED)

        logic_text = Text(
            "赤道方向へ / Toward equator",
            font_size=16, color=CLR_DEFLECTED,
        ).next_to(logic_math, RIGHT, buff=0.2)

        logic = VGroup(logic_math, logic_text).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(logic), run_time=1.0)
        self.wait(2.5)

        # 断面図を全部フェードアウト
        side_view_all = VGroup(
            view_label, sea_surface, lbl_surface,
            seafloor, lbl_ridge, ocean_fill,
            h1_arrow, h1_label, h1_note,
            h2_arrow, h2_label, h2_note,
            flow_arrow, flow_label, logic,
        )
        self.play(FadeOut(side_view_all), run_time=0.8)

        # ======== ② 平面図（Top View） ========
        top_label = Text(
            "平面図（北半球）/ Plan view (N. Hemisphere)",
            font_size=18, color=GRAY_A,
        ).to_edge(UP, buff=0.4)

        formula = MathTex(
            r"\mathrm{PV} = \frac{f}{h} = \text{const}",
            font_size=28,
        ).to_corner(UR, buff=0.4)
        formula[0:2].set_color(GREEN_C)

        self.play(FadeIn(top_label), FadeIn(formula), run_time=0.8)

        # 緯度線
        lat_lines = VGroup()
        lat_labels_grp = VGroup()
        lat_info = [
            (2.0, "高緯度 / Higher lat."),
            (0.5, ""),
            (-1.0, ""),
            (-2.5, "低緯度（赤道側）/ Lower lat."),
        ]

        for y, label_text in lat_info:
            line = DashedLine(
                start=LEFT * 6.5 + UP * y,
                end=RIGHT * 6.5 + UP * y,
                color=CLR_LATITUDE, stroke_width=1,
                dash_length=0.2,
            )
            lat_lines.add(line)
            if label_text:
                lbl = Text(
                    label_text, font_size=11, color=CLR_LATITUDE,
                ).next_to(line, RIGHT, buff=0.1)
                lat_labels_grp.add(lbl)

        self.play(
            *[Create(l) for l in lat_lines],
            *[FadeIn(l) for l in lat_labels_grp],
            run_time=1.0,
        )

        # 海嶺（円で表現）
        ridge_circle = Circle(
            radius=0.8,
            fill_color=CLR_RIDGE_TOP, fill_opacity=0.3,
            stroke_color=CLR_RIDGE_TOP, stroke_width=2,
        ).move_to(np.array([0, 0.5, 0]))
        ridge_label_top = Text(
            "海嶺\nRidge",
            font_size=14, color=CLR_RIDGE_TOP,
        ).move_to(ridge_circle.get_center())

        self.play(
            FadeIn(ridge_circle), FadeIn(ridge_label_top),
            run_time=0.8,
        )
        self.wait(0.5)

        # 方位ラベル
        north_lbl = Text(
            "N（極側）", font_size=12, color=GRAY_A,
        ).to_edge(UP, buff=1.2).shift(LEFT * 5)
        south_lbl = Text(
            "S（赤道側）", font_size=12, color=GRAY_A,
        ).to_edge(DOWN, buff=1.2).shift(LEFT * 5)
        east_lbl = Text(
            "E →", font_size=12, color=GRAY_A,
        ).to_edge(RIGHT, buff=0.3).shift(DOWN * 1.5)

        self.play(
            FadeIn(north_lbl), FadeIn(south_lbl), FadeIn(east_lbl),
            run_time=0.5,
        )

        # 流れの経路（海嶺を南に避けて通る）
        # 初期緯度 y=0.5 から、海嶺付近で南に曲がり、通過後に戻る
        initial_lat = 0.5
        deflection = 2.0   # 南への偏向量
        sigma = 2.0        # 偏向の幅

        flow_path = ParametricFunction(
            lambda t: np.array([
                t,
                initial_lat - deflection * np.exp(
                    -(t - 0.5)**2 / sigma**2),
                0,
            ]),
            t_range=[-5.5, 5.5, 0.02],
            color=CLR_FLOW,
            stroke_width=4,
        )

        # 流れの先端の矢印（方向を示すため終端付近に三角形）
        flow_tip = Triangle(
            fill_color=CLR_FLOW, fill_opacity=1,
            stroke_width=0,
        ).scale(0.12).rotate(-PI / 2).move_to(
            flow_path.point_from_proportion(1),
        )

        # 移動する粒子ドット
        particle = Dot(
            point=flow_path.point_from_proportion(0),
            color=RED_C, radius=0.1,
        )

        # 経路を描きながら粒子が移動
        self.play(
            Create(flow_path),
            MoveAlongPath(particle, flow_path),
            run_time=4.0,
            rate_func=linear,
        )
        self.add(flow_tip)
        self.wait(0.5)

        # 偏向の注釈
        deflect_arrow = Arrow(
            start=np.array([-1.5, 0.5, 0]),
            end=np.array([0.5, -1.3, 0]),
            color=CLR_DEFLECTED, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.12,
        )
        deflect_lbl = Text(
            "南に偏向\nDeflected south",
            font_size=14, color=CLR_DEFLECTED,
        ).next_to(deflect_arrow, DOWN, buff=0.1).shift(LEFT * 0.5)

        self.play(
            GrowArrow(deflect_arrow), FadeIn(deflect_lbl),
            run_time=0.8,
        )
        self.wait(1.0)

        # テロップ
        telop = Text(
            "地形による流れの偏向 / Topographic steering",
            font_size=22, color=WHITE,
        ).to_edge(DOWN, buff=0.4)

        self.play(FadeIn(telop), run_time=0.8)
        self.wait(3.0)
