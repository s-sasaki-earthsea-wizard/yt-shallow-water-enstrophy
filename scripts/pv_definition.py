"""ポテンシャル渦度の定義（簡略版）/ Potential Vorticity Definition (Simplified)
====================================================================

渦度ζを省略した簡略版 PV = f / h の定義を表示する。
名称 → 記号式＋アノテーション → 文章式 の流れで、
コリオリパラメーターfと水深hの比が保存量であることを示す。

yt_script.md L153-155:
  「実は、摩擦のない流体では『コリオリパラメーターと水深の比』が
   保存されるんです。
   この比のことを『ポテンシャル渦度』と呼びます。
   英語ではPotential Vorticity、略してPVですね。」

使用方法 / Usage:
  manim -pql scripts/pv_definition.py PVDefinition
"""

from manim import *


# =============================================
# パラメータ / Parameters
# =============================================

# 色 / Colors（coriolis_parameter_definition.py と統一）
CLR_F = ORANGE             # コリオリパラメーター f
CLR_H = YELLOW_C           # 水深 h
CLR_PV = GREEN_C           # ポテンシャル渦度 PV
CLR_FORMULA = WHITE
CLR_DESCRIPTION = GRAY_A
CLR_CONSERVED = RED_C      # 「保存される」の強調


# =============================================
# メインシーン / Main Scene
# =============================================
class PVDefinition(Scene):
    """ポテンシャル渦度 PV = f / h の定義アニメーション

    L153: 「コリオリパラメーターと水深の比」が保存される
    L154: この比を「ポテンシャル渦度」と呼ぶ
    L155: 英語で Potential Vorticity、略して PV
    """

    def construct(self):
        # ======== ① 保存則のキーメッセージ ========
        msg_jp = Text(
            "コリオリパラメーターと水深の比は保存される",
            font_size=28, color=CLR_FORMULA,
        )
        msg_en = Text(
            "The ratio of Coriolis parameter to depth is conserved",
            font_size=18, color=GRAY_B,
        ).next_to(msg_jp, DOWN, buff=0.2)
        msg_group = VGroup(msg_jp, msg_en).move_to(ORIGIN)

        self.play(FadeIn(msg_group), run_time=1.2)
        self.wait(2.0)
        self.play(FadeOut(msg_group), run_time=0.5)

        # ======== ② 名称表示 ========
        name_jp = Text(
            "ポテンシャル渦度",
            font_size=40, color=CLR_PV,
        )
        name_en = Text(
            "Potential Vorticity (PV)",
            font_size=26, color=GRAY_B,
        ).next_to(name_jp, DOWN, buff=0.2)
        name_group = VGroup(name_jp, name_en).move_to(ORIGIN)

        self.play(FadeIn(name_group, scale=1.1), run_time=1.0)
        self.wait(1.5)
        self.play(
            name_group.animate.scale(0.65).to_edge(UP, buff=0.35),
            run_time=0.8,
        )

        # ======== ③ 数式表示 PV = f / h ========
        formula = MathTex(
            r"\mathrm{PV}",  # [0]
            r"=",            # [1]
            r"\frac{",       # [2]
            r"f",            # [3]
            r"}{",           # [4]
            r"h",            # [5]
            r"}",            # [6]
            font_size=64,
        )
        formula.next_to(name_group, DOWN, buff=0.8)

        # 色分け
        formula[0].set_color(CLR_PV)   # PV
        formula[3].set_color(CLR_F)    # f
        formula[5].set_color(CLR_H)    # h

        self.play(Write(formula), run_time=1.5)
        self.wait(0.5)

        # ======== ④ 記号のアノテーション ========
        # PV のアノテーション（左側）
        annot_pv = Text(
            "ポテンシャル渦度\nPotential Vorticity",
            font_size=14, color=CLR_PV,
        )
        annot_pv.next_to(formula[0], LEFT, buff=1.2)
        annot_pv.shift(DOWN * 0.5)
        arrow_pv = Arrow(
            annot_pv.get_right(), formula[0].get_left(),
            buff=0.1, color=CLR_PV, stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )

        # f のアノテーション（右上）
        annot_f = Text(
            "コリオリパラメーター\nCoriolis parameter",
            font_size=14, color=CLR_F,
        )
        annot_f.next_to(formula[3], RIGHT, buff=1.5)
        annot_f.shift(UP * 0.5)
        arrow_f = Arrow(
            annot_f.get_left(), formula[3].get_right(),
            buff=0.1, color=CLR_F, stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )

        # h のアノテーション（右下）
        annot_h = Text(
            "水深（流体の厚み）\nDepth (fluid layer thickness)",
            font_size=14, color=CLR_H,
        )
        annot_h.next_to(formula[5], RIGHT, buff=1.5)
        annot_h.shift(DOWN * 0.5)
        arrow_h = Arrow(
            annot_h.get_left(), formula[5].get_right(),
            buff=0.1, color=CLR_H, stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )

        annotations = VGroup(
            annot_pv, arrow_pv,
            annot_f, arrow_f,
            annot_h, arrow_h,
        )

        self.play(
            FadeIn(annot_pv), Create(arrow_pv),
            run_time=0.8,
        )
        self.play(
            FadeIn(annot_f), Create(arrow_f),
            run_time=0.8,
        )
        self.play(
            FadeIn(annot_h), Create(arrow_h),
            run_time=0.8,
        )
        self.wait(2.0)

        # ======== ⑤ 文章による説明式 ========
        desc_formula = Text(
            "ポテンシャル渦度 = コリオリパラメーター / 水深",
            font_size=20, color=CLR_DESCRIPTION,
        )
        desc_en = Text(
            "Potential Vorticity = Coriolis parameter / depth",
            font_size=15, color=GRAY_C,
        ).next_to(desc_formula, DOWN, buff=0.15)
        desc_group = VGroup(desc_formula, desc_en)
        desc_group.next_to(formula, DOWN, buff=1.2)

        self.play(FadeOut(annotations), run_time=0.5)
        self.play(FadeIn(desc_group), run_time=1.0)
        self.wait(2.0)

        # ======== ⑥ 「保存される」の強調 ========
        conserved_box = SurroundingRectangle(
            formula, color=CLR_CONSERVED,
            buff=0.25, stroke_width=2.5,
            corner_radius=0.1,
        )
        conserved_label = Text(
            "保存量 / Conserved quantity",
            font_size=18, color=CLR_CONSERVED,
        ).next_to(conserved_box, DOWN, buff=0.3)

        self.play(
            FadeOut(desc_group),
            Create(conserved_box),
            FadeIn(conserved_label),
            run_time=1.0,
        )
        self.wait(2.5)
