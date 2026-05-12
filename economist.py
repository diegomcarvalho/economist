"""Economist-style charts with plotnine.

This module provides reusable helpers for line, bar, and box-and-whisker charts
that accept either wide or long data formats. Automatically reshapes data and
applies The Economist visual style: light blue background, white horizontal grids,
custom color palette, and sans-serif typography.
"""

from __future__ import annotations

import warnings
from typing import Iterable, Sequence

import pandas as pd
from plotnine import (
    aes,
    coord_flip,
    element_blank,
    element_line,
    element_rect,
    element_text,
    geom_boxplot,
    geom_col,
    geom_jitter,
    geom_line,
    geom_point,
    ggplot,
    labs,
    position_dodge,
    scale_color_manual,
    scale_fill_manual,
    scale_x_continuous,
    scale_y_continuous,
    scale_x_discrete,
    theme,
    theme_bw,
)

warnings.filterwarnings("ignore")

# ── Economist color palette ──────────────────────────────────────────────────
ECON_BLUE = "#006BA2"  # primary blue
ECON_RED = "#E3120B"  # accent red (top stripe)
ECON_BG = "#D7E9F5"  # light-blue background
ECON_GRID = "#FFFFFF"  # white grid lines
ECON_TEXT = "#121212"
ECON_MUTED = "#758D99"
ECON_PALETTE = [
    "#006BA2",
    "#E3120B",
    "#DB444B",
    "#3EBCD2",
    "#379A8B",
    "#EBB434",
    "#B4BA39",
    "#9A607F",
]


# ── Economist theme function ─────────────────────────────────────────────────
def theme_economist():
    """Returns a plotnine theme mimicking The Economist style."""
    return theme_bw() + theme(
        # Background
        plot_background=element_rect(fill=ECON_BG, color=ECON_BG),
        panel_background=element_rect(fill=ECON_BG, color=ECON_BG),
        # Grid lines: only horizontal, white
        panel_grid_major_y=element_line(color=ECON_GRID, size=0.8),
        panel_grid_major_x=element_blank(),
        panel_grid_minor=element_blank(),
        panel_border=element_blank(),
        # Axis
        axis_line_x=element_line(color=ECON_TEXT, size=0.6),
        axis_line_y=element_blank(),
        axis_ticks=element_blank(),
        axis_text=element_text(color=ECON_TEXT, size=10),
        axis_title=element_text(color=ECON_TEXT, size=10),
        # Title & subtitle
        plot_title=element_text(color=ECON_TEXT, size=14, face="bold", ha="left"),
        plot_subtitle=element_text(color=ECON_MUTED, size=10, ha="left"),
        plot_caption=element_text(color=ECON_MUTED, size=8, ha="right"),
        # Legend
        legend_background=element_rect(fill=ECON_BG, color=ECON_BG),
        legend_key=element_rect(fill=ECON_BG, color=ECON_BG),
        legend_title=element_blank(),
        legend_text=element_text(color=ECON_TEXT, size=9),
        legend_position="top",
        # Facets
        strip_background=element_rect(fill=ECON_BG, color=ECON_BG),
        strip_text=element_text(color=ECON_TEXT, size=9, face="bold"),
        # Margins
        plot_margin=0.05,
        text=element_text(family="Roboto"),
    )


def _to_long(
    df: pd.DataFrame,
    x_var_name: str,
    value_name: str = "value",
    group_name: str = "series",
    y_var_names: Sequence[str] | None = None,
) -> pd.DataFrame:
    if y_var_names is not None:
        cols = [x_var_name, *y_var_names]
        return df.loc[:, cols].melt(
            id_vars=[x_var_name], var_name=group_name, value_name=value_name
        )

    other_cols = [c for c in df.columns if c != x_var_name]
    if len(other_cols) == 1:
        return df.loc[:, [x_var_name, other_cols[0]]].rename(
            columns={other_cols[0]: value_name}
        )
    return df.melt(id_vars=[x_var_name], var_name=group_name, value_name=value_name)


def _is_long_format(
    df: pd.DataFrame, x_var_name: str, y_col: str, group_col: str
) -> bool:
    return x_var_name in df.columns and y_col in df.columns and group_col in df.columns


def te_line(
    df: pd.DataFrame,
    x_var_name: str,
    x_axis_title: str,
    y_axis_title: str,
    chart_title: str,
    chart_subtitle: str,
    cap: str,
    flip: bool = False,
    breaks: Iterable | None = None,
    y_var_names: Sequence[str] | None = None,
    group_col: str = "series",
    value_col: str = "value",
):
    if _is_long_format(df, x_var_name, value_col, group_col):
        df_ts = df[[x_var_name, group_col, value_col]].copy()
    else:
        df_ts = _to_long(
            df,
            x_var_name,
            value_name=value_col,
            group_name=group_col,
            y_var_names=y_var_names,
        )

    n_series = df_ts[group_col].nunique()
    values = [ECON_PALETTE[i % len(ECON_PALETTE)] for i in range(0, max(0, n_series))]

    p = (
        ggplot(df_ts, aes(x=x_var_name, y=value_col, color=group_col))
        + geom_line(size=1.0)
        + geom_point(size=1.5)
        + scale_color_manual(values=values[:n_series])
    )
    if breaks is not None:
        p = p + scale_x_continuous(breaks=list(breaks))
        p = p + scale_y_continuous(limits=(0,None))
    else:
        p = p + scale_x_discrete()

    if flip:
        p = p + coord_flip()

    return (
        p
        + labs(
            title=chart_title,
            subtitle=chart_subtitle,
            caption=cap,
            x=x_axis_title,
            y=y_axis_title,
        )
        + theme_economist()
    )


def te_bar(
    df: pd.DataFrame,
    x_var_name: str,
    x_axis_title: str,
    y_axis_title: str,
    chart_title: str,
    chart_subtitle: str,
    cap: str,
    flip: bool = False,
    y_var_names: Sequence[str] | None = None,
    group_col: str = "series",
    value_col: str = "value",
):
    if _is_long_format(df, x_var_name, value_col, group_col):
        df_ts = df[[x_var_name, group_col, value_col]].copy()
    else:
        df_ts = _to_long(
            df,
            x_var_name,
            value_name=value_col,
            group_name=group_col,
            y_var_names=y_var_names,
        )

    n_series = df_ts[group_col].nunique()
    values = [ECON_PALETTE[i % len(ECON_PALETTE)] for i in range(0, max(0, n_series))]

    ret = (
        ggplot(df_ts, aes(x=x_var_name, y=value_col, fill=group_col))
        + geom_col(position=position_dodge(width=0.8), width=0.7)
        + scale_fill_manual(values=values[:n_series])
        + labs(
            title=chart_title,
            subtitle=chart_subtitle,
            caption=cap,
            x=x_axis_title,
            y=y_axis_title,
            fill="",
        )
        + theme_economist()
    )

    if flip:
        ret = ret + coord_flip()

    return ret


def te_boxplot(
    df: pd.DataFrame,
    x_var_name: str,
    y_var_name: str,
    x_axis_title: str,
    y_axis_title: str,
    chart_title: str,
    chart_subtitle: str,
    cap: str,
    flip: bool = False,
):
    ret = (
        ggplot(df, aes(x=x_var_name, y=y_var_name, fill=x_var_name))
        + geom_boxplot(width=0.65, outlier_alpha=0.5)
        + geom_jitter()
        + scale_fill_manual(values=ECON_PALETTE[: max(0, df[x_var_name].nunique())])
        + labs(
            title=chart_title,
            subtitle=chart_subtitle,
            caption=cap,
            x=x_axis_title,
            y=y_axis_title,
            fill="",
        )
        + theme_economist()
    )

    if flip:
        ret = ret + coord_flip()

    return ret


__all__ = ["theme_economist", "te_line", "te_bar", "te_boxplot"]
