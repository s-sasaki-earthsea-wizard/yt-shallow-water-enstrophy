"""PVの簡略化: ζを無視する根拠 / PV Simplification: Ignoring ζ
====================================================================

厳密な PV = (ζ + f) / h から、地球スケールでは ζ << f なので
ζを無視して PV ≈ f / h とする過程をアニメーションで示す。

yt_script.md L169-171:
  「厳密には渦度と呼ばれる流体自身がその場で持っている回転の
   強さとコリオリパラメーターを足した値が分子になります。
   ただし地球スケールの流れでは、渦度は地球の自転の効果に比べて
   とても小さいんです。
   だから今回はこの渦度を無視して...」

使用方法 / Usage:
  manim -pql scripts/pv_simplification.py PVSimplification
"""

from manim import *


# =============================================
# パラメータ / Parameters
# =============================================

# 色 / Colors（pv_definition.py と統一）
CLR_F = ORANGE
CLR_H = YELLOW_C
CLR_PV = GREEN_C
CLR_ZETA = TEAL_C          # 渦度 ζ
CLR_SLASH = RED_C           # 取り消し線
CLR_FORMULA = WHITE
CLR_DESCRIPTION = GRAY_A


# =============================================
# メインシーン / Main Scene
# =============================================
class PVSimplification(Scene):
    """PV = (ζ + f) / h → PV ≈ f / h の簡略化アニメーション

    L169: 厳密な式を提示し ζ を説明
    L170: ζ << f を示す
    L171: ζ にスラッシュを入れて PV ≈ f / h に変形
    """

    def construct(self):
        # ======== ① 厳密な式の提示 ========
        full_formula = MathTex(
            r"\mathrm{PV}",       # [0]
            r"=",                 # [1]
            r"\frac{",            # [2]
            r"\zeta",             # [3]
            r"+",                 # [4]
            r"f",                 # [5]
            r"}{",               # [6]
            r"h",                 # [7]
            r"}",                 # [8]
            font_size=64,
        )
        full_formula.move_to(UP * 0.5)

        # 色分け
        full_formula[0].set_color(CLR_PV)
        full_formula[3].set_color(CLR_ZETA)
        full_formula[5].set_color(CLR_F)
        full_formula[7].set_color(CLR_H)

        intro_text = Text(
            "厳密な定義 / Full definition",
            font_size=18, color=CLR_DESCRIPTION,
        ).to_edge(UP, buff=0.4)

        self.play(FadeIn(intro_text), run_time=0.5)
        self.play(Write(full_formula), run_time=1.5)
        self.wait(0.5)

        # ======== ② ζ と f のアノテーション ========
        annot_zeta = Text(
            "渦度（流体自身の回転）\nVorticity (fluid's own rotation)",
            font_size=14, color=CLR_ZETA,
        )
        annot_zeta.next_to(full_formula[3], LEFT, buff=1.5)
        annot_zeta.shift(DOWN * 0.8)
        arrow_zeta = Arrow(
            annot_zeta.get_right(), full_formula[3].get_left(),
            buff=0.1, color=CLR_ZETA, stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )

        annot_f = Text(
            "コリオリパラメーター\nCoriolis parameter",
            font_size=14, color=CLR_F,
        )
        annot_f.next_to(full_formula[5], RIGHT, buff=1.5)
        annot_f.shift(DOWN * 0.8)
        arrow_f = Arrow(
            annot_f.get_left(), full_formula[5].get_right(),
            buff=0.1, color=CLR_F, stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )

        self.play(
            FadeIn(annot_zeta), Create(arrow_zeta),
            FadeIn(annot_f), Create(arrow_f),
            run_time=1.2,
        )
        self.wait(2.0)

        # アノテーションをフェードアウト
        self.play(
            FadeOut(annot_zeta), FadeOut(arrow_zeta),
            FadeOut(annot_f), FadeOut(arrow_f),
            run_time=0.5,
        )

        # ======== ③ ζ << f の表示 ========
        comparison = MathTex(
            r"\zeta", r"\ll", r"f",
            font_size=48,
        )
        comparison[0].set_color(CLR_ZETA)
        comparison[2].set_color(CLR_F)
        comparison.next_to(full_formula, DOWN, buff=1.0)

        comp_text = Text(
            "地球スケールでは渦度はとても小さい\n"
            "At planetary scale, vorticity is negligible",
            font_size=16, color=CLR_DESCRIPTION,
        ).next_to(comparison, DOWN, buff=0.4)

        self.play(
            FadeIn(comparison, scale=1.2),
            run_time=0.8,
        )
        self.play(FadeIn(comp_text), run_time=0.8)
        self.wait(2.0)

        # ======== ④ ζ にスラッシュ（取り消し線） ========
        # ζ の位置に斜め線を描く
        zeta_mob = full_formula[3]
        slash = Line(
            start=zeta_mob.get_corner(DL) + LEFT * 0.05 + DOWN * 0.05,
            end=zeta_mob.get_corner(UR) + RIGHT * 0.05 + UP * 0.05,
            color=CLR_SLASH,
            stroke_width=4,
        )
        # + 記号にもスラッシュ
        plus_mob = full_formula[4]
        slash_plus = Line(
            start=plus_mob.get_corner(DL) + LEFT * 0.05 + DOWN * 0.05,
            end=plus_mob.get_corner(UR) + RIGHT * 0.05 + UP * 0.05,
            color=CLR_SLASH,
            stroke_width=4,
        )

        self.play(
            Create(slash),
            Create(slash_plus),
            zeta_mob.animate.set_opacity(0.3),
            plus_mob.animate.set_opacity(0.3),
            run_time=0.8,
        )
        self.wait(1.0)

        # ======== ⑤ 簡略式に変形 ========
        # 比較テキストと取り消し済み式をフェードアウト
        self.play(
            FadeOut(comparison),
            FadeOut(comp_text),
            FadeOut(intro_text),
            run_time=0.5,
        )

        # 消された式全体をフェードアウトし、新しい簡略式を表示
        simplified = MathTex(
            r"\mathrm{PV}",    # [0]
            r"\approx",        # [1]
            r"\frac{",         # [2]
            r"f",              # [3]
            r"}{",             # [4]
            r"h",              # [5]
            r"}",              # [6]
            font_size=64,
        )
        simplified.move_to(UP * 0.5)
        simplified[0].set_color(CLR_PV)
        simplified[3].set_color(CLR_F)
        simplified[5].set_color(CLR_H)

        self.play(
            FadeOut(full_formula),
            FadeOut(slash),
            FadeOut(slash_plus),
            FadeIn(simplified),
            run_time=1.0,
        )
        self.wait(0.5)

        # ======== ⑥ 結びのテロップ ========
        telop = Text(
            "今回はこの近似で考える\n"
            "We use this approximation throughout",
            font_size=20, color=CLR_FORMULA,
        ).next_to(simplified, DOWN, buff=1.0)

        self.play(FadeIn(telop), run_time=0.8)
        self.wait(2.5)
