"""水深hの導入 / Introduction of Depth h
====================================================================

§3冒頭: 「水深」という新しい概念を導入する。
海の断面図（海面↔海底）と大気の断面図（地表↔対流圏界面）で
流体の厚み h を視覚的に説明する。

yt_script.md L147-151:
  「さて、コリオリ力を理解したところで、もうひとつの主役を紹介します。
   それは『水深』です。」
  「海の流れや大気の流れには、もちろん厚みがあります。
   海なら海面から海底までの水深、大気なら対流圏の厚さですね。」

使用方法 / Usage:
  manim -pql scripts/pv_depth_introduction.py DepthIntroduction
"""

from manim import *
import numpy as np


# =============================================
# パラメータ / Parameters
# =============================================
PANEL_WIDTH = 4.5
PANEL_HEIGHT = 3.0

# 色 / Colors
CLR_SEA_SURFACE = BLUE_C
CLR_SEAFLOOR = GOLD_E
CLR_OCEAN_FILL = BLUE_E
CLR_TROPOPAUSE = GRAY_A
CLR_GROUND = GREEN_E
CLR_ATMO_FILL = BLUE_E
CLR_H_ARROW = YELLOW_C
CLR_LABEL = WHITE


# =============================================
# ユーティリティ / Utility Functions
# =============================================
def build_ocean_panel() -> VGroup:
    """海の断面図を構築

    海面（波線）と海底（凹凸線）の間にhの矢印を配置。
    """
    w, h = PANEL_WIDTH, PANEL_HEIGHT

    # 海水の矩形（半透明）
    body = Rectangle(
        width=w, height=h,
        fill_color=CLR_OCEAN_FILL,
        fill_opacity=0.25,
        stroke_width=0,
    )

    # 海面（波線）
    sea_surface = ParametricFunction(
        lambda t: np.array([
            t, h / 2 + 0.12 * np.sin(2.5 * t), 0,
        ]),
        t_range=[-w / 2, w / 2, 0.02],
        color=CLR_SEA_SURFACE,
        stroke_width=3,
    )

    # 海底（凹凸線）
    seafloor = ParametricFunction(
        lambda t: np.array([
            t,
            -h / 2 + 0.08 * np.sin(4 * t + 1)
            + 0.05 * np.sin(7 * t),
            0,
        ]),
        t_range=[-w / 2, w / 2, 0.02],
        color=CLR_SEAFLOOR,
        stroke_width=3,
    )

    # h の両端矢印
    h_arrow = DoubleArrow(
        start=DOWN * h / 2,
        end=UP * h / 2,
        color=CLR_H_ARROW,
        stroke_width=3,
        buff=0.05,
        tip_length=0.2,
    ).shift(RIGHT * (w / 2 + 0.5))

    h_label = MathTex(
        "h", font_size=36, color=CLR_H_ARROW,
    ).next_to(h_arrow, RIGHT, buff=0.15)

    # ラベル
    lbl_surface = Text(
        "海面 / Sea surface",
        font_size=14, color=CLR_SEA_SURFACE,
    ).next_to(sea_surface, UP, buff=0.2)

    lbl_floor = Text(
        "海底 / Seafloor",
        font_size=14, color=CLR_SEAFLOOR,
    ).next_to(seafloor, DOWN, buff=0.2)

    # パネルタイトル
    panel_title = Text(
        "海 / Ocean",
        font_size=22, color=CLR_LABEL,
    ).next_to(lbl_surface, UP, buff=0.25)

    return VGroup(
        body, sea_surface, seafloor,
        h_arrow, h_label,
        lbl_surface, lbl_floor,
        panel_title,
    )


def build_atmosphere_panel() -> VGroup:
    """大気の断面図を構築

    対流圏界面（破線）と地表（凹凸線）の間にhの矢印を配置。
    """
    w, h = PANEL_WIDTH, PANEL_HEIGHT

    # 大気の矩形（半透明）
    body = Rectangle(
        width=w, height=h,
        fill_color=CLR_ATMO_FILL,
        fill_opacity=0.15,
        stroke_width=0,
    )

    # 対流圏界面（破線）
    tropopause = DashedLine(
        start=LEFT * w / 2 + UP * h / 2,
        end=RIGHT * w / 2 + UP * h / 2,
        color=CLR_TROPOPAUSE,
        stroke_width=2.5,
        dash_length=0.15,
    )

    # 地表（凹凸線）
    ground = ParametricFunction(
        lambda t: np.array([
            t,
            -h / 2 + 0.06 * np.sin(3.5 * t + 2)
            + 0.04 * np.sin(6 * t),
            0,
        ]),
        t_range=[-w / 2, w / 2, 0.02],
        color=CLR_GROUND,
        stroke_width=3,
    )

    # h の両端矢印
    h_arrow = DoubleArrow(
        start=DOWN * h / 2,
        end=UP * h / 2,
        color=CLR_H_ARROW,
        stroke_width=3,
        buff=0.05,
        tip_length=0.2,
    ).shift(RIGHT * (w / 2 + 0.5))

    h_label = MathTex(
        "h", font_size=36, color=CLR_H_ARROW,
    ).next_to(h_arrow, RIGHT, buff=0.15)

    # ラベル
    lbl_tropo = Text(
        "対流圏界面 / Tropopause",
        font_size=14, color=CLR_TROPOPAUSE,
    ).next_to(tropopause, UP, buff=0.2)

    lbl_ground = Text(
        "地表 / Ground",
        font_size=14, color=CLR_GROUND,
    ).next_to(ground, DOWN, buff=0.2)

    # パネルタイトル
    panel_title = Text(
        "大気 / Atmosphere",
        font_size=22, color=CLR_LABEL,
    ).next_to(lbl_tropo, UP, buff=0.25)

    return VGroup(
        body, tropopause, ground,
        h_arrow, h_label,
        lbl_tropo, lbl_ground,
        panel_title,
    )


# =============================================
# メインシーン / Main Scene
# =============================================
class DepthIntroduction(Scene):
    """水深hの導入アニメーション

    L147-148: 「水深」のインパクト表示 → 海の断面図
    L150-151: 海と大気の2パネル構成で流体の厚み h を図解
    """

    def construct(self):
        # ======== ① 「水深」の名称表示 ========
        name_jp = Text("水深", font_size=52, color=CLR_LABEL)
        name_en = Text(
            "Depth", font_size=32, color=GRAY_B,
        ).next_to(name_jp, DOWN, buff=0.25)
        name_group = VGroup(name_jp, name_en).move_to(ORIGIN)

        self.play(FadeIn(name_group, scale=1.2), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(name_group), run_time=0.5)

        # ======== ② 海の断面図（中央に表示） ========
        ocean = build_ocean_panel()
        ocean.move_to(ORIGIN)

        telop_depth = Text(
            "水深 h / Depth h",
            font_size=22, color=CLR_LABEL,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            FadeIn(ocean, shift=UP * 0.3),
            FadeIn(telop_depth),
            run_time=1.5,
        )
        self.wait(2.0)

        # ======== ③ 海を左に移動、大気パネルを右に追加 ========
        atmo = build_atmosphere_panel()
        atmo.move_to(RIGHT * 3.5)

        telop_thickness = Text(
            "流体の厚み h / Fluid layer thickness h",
            font_size=22, color=CLR_LABEL,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            ocean.animate.move_to(LEFT * 3.5),
            FadeTransform(telop_depth, telop_thickness),
            run_time=1.0,
        )
        self.play(
            FadeIn(atmo, shift=UP * 0.3),
            run_time=1.5,
        )
        self.wait(3.0)
