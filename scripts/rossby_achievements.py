"""ロスビーの業績リスト / Rossby's Achievements
====================================================================

カール＝グスタフ・ロスビーの主要な業績を段階的にリストアップする。

yt_script.md L285-289:
  「これらのPVの保存やコリオリパラメーターを通して地球規模の流れを
   理解する理論は1930から40年代に気象学者、カール＝グスタフ・ロスビー
   を中心として築かれました。
   彼は流体力学や熱力学などの物理の様々な分野の知見を活かし、
   数理的に気象を研究し始めた気象学のパイオニアのひとりです。
   コンピューターを気象の研究に利用した最初期の人物としても知られて
   いるんですよね。」

使用方法 / Usage:
  manim -pql scripts/rossby_achievements.py RossbyAchievements
"""

from manim import *


# =============================================
# パラメータ / Parameters
# =============================================

# 色 / Colors
CLR_NAME = GOLD_C
CLR_ERA = GRAY_A
CLR_BULLET = TEAL_C
CLR_TEXT = WHITE
CLR_EN = GRAY_B
CLR_HIGHLIGHT = GREEN_C
CLR_PV = GREEN_C


# =============================================
# メインシーン / Main Scene
# =============================================
class RossbyAchievements(Scene):
    """ロスビーの業績を段階的にリストアップ

    ① 名前と時代の表示
    ② 業績を1つずつフェードイン
    ③ PV保存理論をハイライト
    """

    def construct(self):
        # ======== ① 名前と時代 ========
        name_jp = Text(
            "カール＝グスタフ・ロスビー",
            font_size=32, color=CLR_NAME,
        )
        name_en = Text(
            "Carl-Gustaf Rossby",
            font_size=22, color=CLR_NAME,
        ).next_to(name_jp, DOWN, buff=0.15)

        era = Text(
            "1898–1957",
            font_size=18, color=CLR_ERA,
        ).next_to(name_en, DOWN, buff=0.2)

        name_group = VGroup(name_jp, name_en, era).move_to(
            UP * 2.5,
        )

        # 名前の下に区切り線
        divider = Line(
            start=LEFT * 4, end=RIGHT * 4,
            color=CLR_NAME, stroke_width=1.5,
        ).next_to(name_group, DOWN, buff=0.25)

        self.play(
            FadeIn(name_jp, shift=DOWN * 0.3),
            run_time=0.8,
        )
        self.play(
            FadeIn(name_en), FadeIn(era),
            run_time=0.6,
        )
        self.play(Create(divider), run_time=0.5)
        self.wait(1.0)

        # ======== ② 業績リスト ========
        achievements = [
            {
                "jp": "物理学の知見を気象学に応用",
                "en": "Applied physics to meteorology",
                "sub_jp": "流体力学・熱力学など",
                "sub_en": "Fluid dynamics, thermodynamics, etc.",
            },
            {
                "jp": "数理的気象学のパイオニア",
                "en": "Pioneer of mathematical meteorology",
                "sub_jp": "",
                "sub_en": "",
            },
            {
                "jp": "コンピューターの気象研究への活用",
                "en": "Early use of computers in meteorology",
                "sub_jp": "",
                "sub_en": "",
            },
            {
                "jp": "PV保存理論の構築（1930–40年代）",
                "en": "Developed PV conservation theory (1930s–40s)",
                "sub_jp": "",
                "sub_en": "",
                "highlight": True,
            },
        ]

        list_start_y = 0.8
        line_spacing = 1.1
        items = []

        for i, ach in enumerate(achievements):
            y_pos = list_start_y - i * line_spacing
            is_highlight = ach.get("highlight", False)
            text_color = CLR_HIGHLIGHT if is_highlight else CLR_TEXT
            bullet_color = CLR_HIGHLIGHT if is_highlight else CLR_BULLET

            # 弾丸記号
            bullet = Text(
                "▸", font_size=22, color=bullet_color,
            ).move_to(np.array([-5.0, y_pos, 0]))

            # 日本語テキスト
            jp_text = Text(
                ach["jp"], font_size=20, color=text_color,
            ).next_to(bullet, RIGHT, buff=0.2)
            jp_text.align_to(bullet, UP)

            # 英語テキスト
            en_text = Text(
                ach["en"], font_size=14, color=CLR_EN,
            ).next_to(jp_text, DOWN, buff=0.05, aligned_edge=LEFT)

            item_group = VGroup(bullet, jp_text, en_text)

            # サブテキスト（補足情報）がある場合
            if ach["sub_jp"]:
                sub_text = Text(
                    f"  — {ach['sub_jp']} / {ach['sub_en']}",
                    font_size=12, color=GRAY_B,
                ).next_to(en_text, DOWN, buff=0.05, aligned_edge=LEFT)
                item_group.add(sub_text)

            items.append(item_group)

        # 1つずつフェードイン
        for i, item in enumerate(items):
            self.play(
                FadeIn(item, shift=RIGHT * 0.3),
                run_time=0.8,
            )
            if i < len(items) - 1:
                self.wait(1.5)
            else:
                self.wait(0.5)

        # ======== ③ PV保存理論をハイライト ========
        # 最後の項目（PV保存理論）を囲む枠
        highlight_rect = SurroundingRectangle(
            items[-1],
            color=CLR_PV, stroke_width=2,
            buff=0.15, corner_radius=0.1,
        )

        self.play(Create(highlight_rect), run_time=0.8)
        self.wait(3.0)
