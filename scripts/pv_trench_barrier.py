"""海溝を越えられない流れ（topographic barrier）
====================================================================

水深の変化が大きすぎると緯度の変化だけではPVを保存しきれず、
流れは海溝を越えることができなくなる。結果として海溝に沿った流れとなる。

yt_script.md L267-270:
  「海嶺が高かったり、海溝が深くて、水深の変化が大きすぎる場合です。
   緯度の変化だけではPVを保存しきれず、流れは海嶺や海溝を越えることが
   できなくなるんですね。結果として流れは海嶺や海溝に沿った動きをします。
   このとき、海嶺や海溝はまるで壁のような役割になるんですね。」

使用方法 / Usage:
  manim -pql scripts/pv_trench_barrier.py TrenchBarrier
"""

from manim import *
import numpy as np


# =============================================
# パラメータ / Parameters
# =============================================

# 色 / Colors
CLR_TRENCH = BLUE_D
CLR_TRENCH_FILL = BLUE_E
CLR_FLOW = TEAL_C
CLR_BLOCKED = RED_C
CLR_ALONG = YELLOW_C
CLR_H = YELLOW_C
CLR_F = ORANGE
CLR_PV = GREEN_C
CLR_LATITUDE = GRAY_B
CLR_WALL = RED_C


# =============================================
# メインシーン / Main Scene
# =============================================
class TrenchBarrier(Scene):
    """水深変化が大きすぎて海溝を越えられない流れを図解

    ① 平面図: 海溝 + 流れが越えようとしてブロック
    ② PV保存の破綻ロジック
    ③ 流れが海溝に沿って偏向
    """

    def construct(self):
        # ======== ① 平面図セットアップ ========
        top_label = Text(
            "平面図（北半球）/ Plan view (N. Hemisphere)",
            font_size=18, color=GRAY_A,
        ).to_edge(UP, buff=0.4)

        formula = MathTex(
            r"\mathrm{PV} = \frac{f}{h} = \text{const}",
            font_size=28,
        ).to_corner(UR, buff=0.4)
        formula[0:2].set_color(CLR_PV)

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

        # 方位ラベル
        north_lbl = Text(
            "N（極側）", font_size=12, color=GRAY_A,
        ).to_edge(UP, buff=1.2).shift(LEFT * 5)
        south_lbl = Text(
            "S（赤道側）", font_size=12, color=GRAY_A,
        ).to_edge(DOWN, buff=1.2).shift(LEFT * 5)

        self.play(
            FadeIn(north_lbl), FadeIn(south_lbl),
            run_time=0.5,
        )

        # 海溝（縦長の帯 = 壁として機能）
        trench_rect = RoundedRectangle(
            width=1.0, height=5.0,
            corner_radius=0.3,
            fill_color=CLR_TRENCH_FILL, fill_opacity=0.3,
            stroke_color=CLR_TRENCH, stroke_width=2.5,
        ).move_to(np.array([0.5, -0.25, 0]))

        trench_label = Text(
            "深い海溝\nDeep trench",
            font_size=14, color=CLR_TRENCH,
        ).move_to(trench_rect.get_center())

        # Δh が大きいことを示すラベル（海溝の右側に配置）
        delta_h_label = MathTex(
            r"\Delta h", font_size=24, color=CLR_H,
        ).next_to(trench_rect, RIGHT, buff=0.3)
        delta_h_note = Text(
            "大きすぎる / Too large",
            font_size=12, color=CLR_H,
        ).next_to(delta_h_label, DOWN, buff=0.1)

        self.play(
            FadeIn(trench_rect), FadeIn(trench_label),
            run_time=0.8,
        )
        self.play(
            FadeIn(delta_h_label), FadeIn(delta_h_note),
            run_time=0.6,
        )
        self.wait(0.5)

        # ======== ② 流れが越えようとしてブロック ========
        # 流れの矢印（左から右へ）
        flow_start = np.array([-5.0, -0.25, 0])
        flow_mid = np.array([-0.3, -0.25, 0])  # 海溝の手前

        flow_arrow = Arrow(
            start=flow_start,
            end=flow_mid,
            color=CLR_FLOW, stroke_width=4,
            buff=0,
            max_tip_length_to_length_ratio=0.06,
        )
        flow_label = Text(
            "海流 / Ocean current",
            font_size=12, color=CLR_FLOW,
        ).next_to(flow_arrow, UP, buff=0.15).shift(LEFT * 1.0)

        self.play(
            GrowArrow(flow_arrow), FadeIn(flow_label),
            run_time=1.5,
        )
        self.wait(0.5)

        # ブロック演出: × マークと赤フラッシュ
        block_pos = np.array([0.0, -0.25, 0])
        cross_size = 0.3
        block_cross = VGroup(
            Line(
                start=block_pos + UP * cross_size + LEFT * cross_size,
                end=block_pos + DOWN * cross_size + RIGHT * cross_size,
                color=CLR_BLOCKED, stroke_width=6,
            ),
            Line(
                start=block_pos + UP * cross_size + RIGHT * cross_size,
                end=block_pos + DOWN * cross_size + LEFT * cross_size,
                color=CLR_BLOCKED, stroke_width=6,
            ),
        )

        # 赤い閃光エフェクト
        flash_circle = Circle(
            radius=0.5, color=CLR_BLOCKED,
            fill_color=CLR_BLOCKED, fill_opacity=0.3,
            stroke_width=3,
        ).move_to(block_pos)

        self.play(
            FadeIn(flash_circle, scale=0.3),
            Create(block_cross),
            run_time=0.5,
        )
        self.play(
            FadeOut(flash_circle),
            run_time=0.4,
        )
        self.wait(0.5)

        # ======== ③ PV保存の破綻ロジック ========
        logic_math = MathTex(
            r"\Delta h",
            r"\;\gg\;",
            r"\Delta f_{\max}",
            font_size=32,
        )
        logic_math[0].set_color(CLR_H)
        logic_math[2].set_color(CLR_F)

        logic_text = Text(
            "PVを保存できない / Can't conserve PV",
            font_size=16, color=CLR_BLOCKED,
        ).next_to(logic_math, DOWN, buff=0.2)

        logic = VGroup(logic_math, logic_text).to_edge(DOWN, buff=0.4)

        self.play(FadeIn(logic), run_time=1.0)
        self.wait(2.0)

        # ======== ④ 流れが海溝に沿って偏向 ========
        # ロジックをフェードアウト
        self.play(FadeOut(logic), run_time=0.5)

        # 既存の流れ矢印と×をフェードアウト
        self.play(
            FadeOut(flow_arrow), FadeOut(flow_label),
            FadeOut(block_cross),
            FadeOut(delta_h_label), FadeOut(delta_h_note),
            run_time=0.5,
        )

        # 海溝に沿った流れの経路（滑らかなカーブ）
        # 左から水平に来て、海溝手前で滑らかに北に曲がり、
        # 海溝に沿って北上する
        def along_func(t):
            """t: 0→1 のパラメータ"""
            # x: 指数減衰で海溝手前(x≈0)に収束
            x = -5.0 + 5.1 * (1 - np.exp(-5.0 * t))
            # y: 前半は水平、後半で滑らかに北上
            rise = max(0, (t - 0.4) / 0.6) ** 1.5
            y = -0.25 + 2.75 * rise
            return np.array([x, min(y, 2.5), 0])

        along_path = ParametricFunction(
            along_func,
            t_range=[0, 1, 0.005],
            color=CLR_ALONG,
            stroke_width=4,
        )

        # 移動する粒子
        particle = Dot(
            point=along_path.point_from_proportion(0),
            color=RED_C, radius=0.1,
        )

        # 矢印の先端（北向き = 上向き）
        along_tip = Triangle(
            fill_color=CLR_ALONG, fill_opacity=1,
            stroke_width=0,
        ).scale(0.12).rotate(0).move_to(
            along_path.point_from_proportion(1),
        )

        self.play(
            Create(along_path),
            MoveAlongPath(particle, along_path),
            run_time=4.0,
            rate_func=linear,
        )
        self.add(along_tip)
        self.wait(0.5)

        # 海溝沿いの注釈
        along_arrow = Arrow(
            start=np.array([-2.5, 0.0, 0]),
            end=np.array([-0.8, 1.5, 0]),
            color=CLR_ALONG, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.12,
        )
        along_lbl = Text(
            "海溝に沿って流れる\nFlow along the trench",
            font_size=14, color=CLR_ALONG,
        ).next_to(along_arrow, LEFT, buff=0.15)

        self.play(
            GrowArrow(along_arrow), FadeIn(along_lbl),
            run_time=0.8,
        )
        self.wait(1.0)

        # 壁アイコン（海溝の両側に薄い赤線で壁を示す）
        wall_left = Line(
            start=trench_rect.get_corner(UL),
            end=trench_rect.get_corner(DL),
            color=CLR_WALL, stroke_width=4,
        )
        wall_right = Line(
            start=trench_rect.get_corner(UR),
            end=trench_rect.get_corner(DR),
            color=CLR_WALL, stroke_width=4,
        )
        wall_label = Text(
            "壁 / Wall",
            font_size=16, color=CLR_WALL,
        ).next_to(trench_rect, RIGHT, buff=0.3)

        self.play(
            Create(wall_left), Create(wall_right),
            FadeIn(wall_label),
            run_time=0.8,
        )
        self.wait(1.0)

        # ======== ⑤ テロップ ========
        telop = Text(
            "水深変化が大きすぎると海溝は壁になる\n"
            "Extreme depth change turns a trench into a barrier",
            font_size=22, color=WHITE,
        ).to_edge(DOWN, buff=0.4)

        self.play(FadeIn(telop), run_time=0.8)
        self.wait(3.0)
