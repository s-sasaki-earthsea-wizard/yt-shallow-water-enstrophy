"""コリオリパラメーターの定義 / Coriolis Parameter Definition
====================================================================

コリオリパラメーター f = 2Ω sin φ の定義を数式と図解で示す。
左に四分円弧（φ=0°〜90°）、右にφ-fグラフを同時描画し、
単位円と三角関数の関係を利用してfの緯度依存性を直感的に示す。

yt_script.md L121-128:
  「このコリオリ力の強さは緯度によって変わります。
   その強さを表す量を『コリオリパラメーター』と呼びます。」
  f = 2Ω sin φ
  コリオリパラメーター = 2 × 自転の角速度 × sin(緯度)

使用方法 / Usage:
  manim -pql scripts/coriolis_parameter_definition.py CoriolisParameterDefinition
"""

from manim import *
import numpy as np


# =============================================
# パラメータ / Parameters
# =============================================

# 円弧の設定
ARC_RADIUS = 2.0
ARC_CENTER = np.array([-4.0, -1.0, 0])

# グラフの設定
GRAPH_WIDTH = 4.5
GRAPH_HEIGHT = 2.8

# 色 / Colors
CLR_ARC = BLUE_C
CLR_DOT = RED_C
CLR_ANGLE = YELLOW_C
CLR_SIN_LINE = GREEN_C
CLR_GRAPH_CURVE = ORANGE
CLR_FORMULA = WHITE
CLR_DESCRIPTION = GRAY_A


# =============================================
# メインシーン / Main Scene
# =============================================
class CoriolisParameterDefinition(Scene):
    """コリオリパラメーター f = 2Ω sin φ の定義と緯度依存性を可視化

    前半: 数式の記号・文章による定義を表示
    後半: 左に四分円弧、右にφ-fグラフを同期アニメーションで描画し、
    sinφ（赤道で0、極で最大）の性質を直感的に示す。
    """

    def construct(self):
        # ======== ① 名称表示 ========
        name_jp = Text(
            "コリオリパラメーター",
            font_size=36, color=CLR_FORMULA,
        )
        name_en = Text(
            "Coriolis Parameter",
            font_size=24, color=GRAY_B,
        ).next_to(name_jp, DOWN, buff=0.2)
        name_group = VGroup(name_jp, name_en).move_to(ORIGIN)

        self.play(FadeIn(name_group), run_time=1.0)
        self.wait(1.0)
        self.play(
            name_group.animate.scale(0.7).to_edge(UP, buff=0.3),
            run_time=0.8,
        )

        # ======== ② 数式表示（記号） ========
        formula = MathTex(
            r"f", r"=", r"2", r"\Omega", r"\sin", r"\varphi",
            font_size=48,
        )
        formula.next_to(name_group, DOWN, buff=0.5)

        # 色分け
        formula[0].set_color(CLR_GRAPH_CURVE)  # f
        formula[3].set_color(TEAL_C)           # Ω
        formula[5].set_color(CLR_ANGLE)        # φ

        self.play(Write(formula), run_time=1.5)
        self.wait(0.5)

        # ======== ③ 記号のアノテーション ========
        # f のアノテーション（左寄り）
        annot_f = Text(
            "コリオリパラメーター / Coriolis parameter",
            font_size=14, color=CLR_GRAPH_CURVE,
        )
        annot_f.next_to(formula[0], DOWN, buff=0.7)
        annot_f.shift(LEFT * 0.5)
        arrow_f = Arrow(
            annot_f.get_top(), formula[0].get_bottom(),
            buff=0.05, color=CLR_GRAPH_CURVE, stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )

        # Ω のアノテーション（中央）
        annot_omega = Text(
            "自転の角速度 / Angular velocity of rotation",
            font_size=14, color=TEAL_C,
        )
        annot_omega.next_to(formula[3], DOWN, buff=1.6)
        arrow_omega = Arrow(
            annot_omega.get_top(), formula[3].get_bottom(),
            buff=0.05, color=TEAL_C, stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )

        # φ のアノテーション（右寄り）
        annot_phi = Text(
            "緯度 / Latitude",
            font_size=14, color=CLR_ANGLE,
        )
        annot_phi.next_to(formula[5], DOWN, buff=0.7)
        annot_phi.shift(RIGHT * 0.5)
        arrow_phi = Arrow(
            annot_phi.get_top(), formula[5].get_bottom(),
            buff=0.05, color=CLR_ANGLE, stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )

        annotations = VGroup(
            annot_f, arrow_f, annot_omega, arrow_omega, annot_phi, arrow_phi,
        )

        self.play(
            FadeIn(annot_f), Create(arrow_f),
            run_time=0.8,
        )
        self.play(
            FadeIn(annot_omega), Create(arrow_omega),
            run_time=0.8,
        )
        self.play(
            FadeIn(annot_phi), Create(arrow_phi),
            run_time=0.8,
        )
        self.wait(2.0)

        # ======== ④ 文章による説明式 ========
        desc_formula = Text(
            "コリオリパラメーター = 2 × 自転の角速度 × sin(緯度)",
            font_size=20, color=CLR_DESCRIPTION,
        )
        desc_en = Text(
            "Coriolis parameter = 2 × angular velocity of rotation × sin(latitude)",
            font_size=15, color=GRAY_C,
        ).next_to(desc_formula, DOWN, buff=0.15)
        desc_group = VGroup(desc_formula, desc_en).move_to(ORIGIN + DOWN * 0.3)

        self.play(FadeOut(annotations), run_time=0.5)
        self.play(FadeIn(desc_group), run_time=1.0)
        self.wait(2.5)

        # ======== ⑤ 円弧＋グラフの図解へ遷移 ========
        self.play(
            FadeOut(desc_group),
            FadeOut(name_group),
            formula.animate.scale(0.65).to_corner(UR, buff=0.4),
            run_time=0.8,
        )

        # ---- 左側: 四分円弧 ----
        arc_axes_x = Arrow(
            ARC_CENTER + LEFT * 0.3, ARC_CENTER + RIGHT * (ARC_RADIUS + 0.6),
            buff=0, color=WHITE, stroke_width=2,
        )
        arc_axes_y = Arrow(
            ARC_CENTER + DOWN * 0.3, ARC_CENTER + UP * (ARC_RADIUS + 0.6),
            buff=0, color=WHITE, stroke_width=2,
        )

        arc = Arc(
            radius=ARC_RADIUS,
            start_angle=0, angle=PI / 2,
            arc_center=ARC_CENTER,
            color=CLR_ARC, stroke_width=3,
        )

        lbl_equator = Text(
            "赤道 φ=0°\nEquator",
            font_size=13, color=GRAY_A,
        ).next_to(ARC_CENTER + RIGHT * ARC_RADIUS, DOWN, buff=0.25)
        lbl_pole = Text(
            "北極 φ=90°\nNorth Pole",
            font_size=13, color=GRAY_A,
        ).next_to(ARC_CENTER + UP * ARC_RADIUS, LEFT, buff=0.25)

        # ---- 右側: φ-f グラフ ----
        ax = Axes(
            x_range=[0, 90, 30],
            y_range=[0, 1.15, 0.5],
            x_length=GRAPH_WIDTH,
            y_length=GRAPH_HEIGHT,
            axis_config={"color": WHITE, "stroke_width": 2},
            tips=True,
        ).move_to(np.array([2.8, -0.2, 0]))

        x_label = MathTex(
            r"\varphi", font_size=24, color=CLR_ANGLE,
        ).next_to(ax.x_axis.get_end(), DOWN, buff=0.2)
        y_label = MathTex(
            r"f", font_size=24, color=CLR_GRAPH_CURVE,
        ).next_to(ax.y_axis.get_end(), LEFT, buff=0.2)

        # x軸の目盛りラベル
        x_ticks = VGroup()
        for deg in [0, 30, 60, 90]:
            lbl = MathTex(f"{deg}" + r"°", font_size=14, color=GRAY_A)
            lbl.next_to(ax.c2p(deg, 0), DOWN, buff=0.15)
            x_ticks.add(lbl)

        # y軸: 正規化表記
        y_note = MathTex(
            r"f \,/\, 2\Omega", font_size=14, color=GRAY_A,
        ).next_to(ax.y_axis, LEFT, buff=0.35).shift(UP * 0.3)

        y_tick_1 = MathTex(
            r"1", font_size=14, color=GRAY_A,
        ).next_to(ax.c2p(0, 1.0), LEFT, buff=0.15)

        # 左右の図を一括表示
        self.play(
            Create(arc_axes_x), Create(arc_axes_y), Create(arc),
            FadeIn(lbl_equator), FadeIn(lbl_pole),
            Create(ax), FadeIn(x_label), FadeIn(y_label),
            FadeIn(x_ticks), FadeIn(y_note), FadeIn(y_tick_1),
            run_time=2.0,
        )
        self.wait(0.5)

        # ======== ⑥ 同期アニメーション ========
        phi_tracker = ValueTracker(0)  # φ（度）

        # 円弧上の移動点
        dot_arc = always_redraw(
            lambda: Dot(
                point=ARC_CENTER + ARC_RADIUS * np.array([
                    np.cos(np.radians(phi_tracker.get_value())),
                    np.sin(np.radians(phi_tracker.get_value())),
                    0,
                ]),
                color=CLR_DOT, radius=0.08,
            )
        )

        # 角度の扇形
        angle_indicator = always_redraw(
            lambda: Arc(
                radius=0.5,
                start_angle=0,
                angle=np.radians(max(phi_tracker.get_value(), 0.5)),
                arc_center=ARC_CENTER,
                color=CLR_ANGLE,
                stroke_width=2.5,
            )
        )

        # φ ラベル（扇形の中間角度に配置）
        phi_label = always_redraw(
            lambda: MathTex(
                r"\varphi", font_size=22, color=CLR_ANGLE,
            ).move_to(
                ARC_CENTER + 0.85 * np.array([
                    np.cos(np.radians(phi_tracker.get_value() / 2)),
                    np.sin(np.radians(phi_tracker.get_value() / 2)),
                    0,
                ])
            )
        )

        # sin φ の高さを示す縦線（φが小さいときは非表示）
        def _make_sin_line():
            phi = phi_tracker.get_value()
            if phi < 2:
                return VGroup()  # φ≈0 では始点=終点になるので非表示
            cos_phi = np.cos(np.radians(phi))
            sin_phi = np.sin(np.radians(phi))
            return DashedLine(
                ARC_CENTER + np.array([
                    ARC_RADIUS * cos_phi, 0, 0,
                ]),
                ARC_CENTER + ARC_RADIUS * np.array([
                    cos_phi, sin_phi, 0,
                ]),
                color=CLR_SIN_LINE,
                stroke_width=2.5,
                dash_length=0.08,
            )

        sin_line = always_redraw(_make_sin_line)

        # sin φ ラベル（φが小さいときは非表示）
        def _make_sin_label():
            phi = phi_tracker.get_value()
            if phi < 5:
                return VGroup()
            cos_phi = np.cos(np.radians(phi))
            sin_phi = np.sin(np.radians(phi))
            return MathTex(
                r"\sin\varphi", font_size=16, color=CLR_SIN_LINE,
            ).next_to(
                ARC_CENTER + np.array([
                    ARC_RADIUS * cos_phi,
                    ARC_RADIUS * sin_phi / 2,
                    0,
                ]),
                LEFT, buff=0.15,
            )

        sin_label = always_redraw(_make_sin_label)

        # グラフ上の移動点（add_updaterで位置更新、TracedPath用）
        dot_graph = Dot(
            point=ax.c2p(0, 0), color=CLR_DOT, radius=0.08,
        )
        dot_graph.add_updater(
            lambda m: m.move_to(ax.c2p(
                phi_tracker.get_value(),
                np.sin(np.radians(phi_tracker.get_value())),
            ))
        )

        # グラフ上の曲線（TracedPathでドットの軌跡を描画）
        traced_curve = TracedPath(
            dot_graph.get_center,
            stroke_color=CLR_GRAPH_CURVE,
            stroke_width=3,
        )

        # 左右を結ぶ水平破線（sinφの高さ ↔ グラフのf値の対応を示す）
        def _make_connecting_line():
            phi = phi_tracker.get_value()
            if phi < 2:
                return VGroup()
            cos_phi = np.cos(np.radians(phi))
            sin_phi = np.sin(np.radians(phi))
            return DashedLine(
                ARC_CENTER + ARC_RADIUS * np.array([
                    cos_phi, sin_phi, 0,
                ]),
                ax.c2p(phi, sin_phi),
                color=GRAY_B,
                stroke_width=1.5,
                dash_length=0.1,
            )

        connecting_line = always_redraw(_make_connecting_line)

        # 全要素追加
        self.add(
            dot_arc, angle_indicator, phi_label,
            sin_line, sin_label,
            dot_graph, traced_curve,
            connecting_line,
        )

        # φ = 0° → 90° 同期アニメーション
        self.play(
            phi_tracker.animate.set_value(90),
            run_time=6.0,
            rate_func=smooth,
        )
        self.wait(1.0)

        # ======== ⑦ 結びのテロップ ========
        conclusion = Text(
            "赤道で0、極で最大\n"
            "Zero at equator, maximum at poles",
            font_size=22,
            color=WHITE,
        ).to_edge(DOWN, buff=0.3)

        self.play(FadeIn(conclusion), run_time=1.0)
        self.wait(2.5)
