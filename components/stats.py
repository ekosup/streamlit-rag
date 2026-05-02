"""Statistics dashboard."""

import pandas as pd
import streamlit as st
import altair as alt

from services.data import load_data

# Altair theme — used across all charts
ACCENT = "#1B4332"
ACCENT_LIGHT = "#2D6A4F"
GOLD = "#9A7B2D"
MUTED = "#8A8A7A"
RULE = "#D4D0C8"

THEME_CONFIG = {
    "view": {"stroke": None},
    "axis": {
        "labelFont": "DM Sans",
        "titleFont": "DM Sans",
        "labelColor": "#5A5A5A",
        "titleColor": "#5A5A5A",
        "gridColor": "#ECEAE5",
        "domainColor": RULE,
        "tickColor": RULE,
        "labelFontSize": 11,
        "titleFontSize": 12,
    },
    "legend": {
        "labelFont": "DM Sans",
        "titleFont": "DM Sans",
    },
    "title": {
        "font": "Source Serif 4",
        "fontSize": 14,
        "fontWeight": 600,
        "color": "#1A1A1A",
    },
}


def _categorical_palette(n: int) -> list[str]:
    """Perceptually distinct palette for categorical data."""
    colors = [
        "#1B4332", "#2D6A4F", "#40916C", "#52B788", "#74C69D",
        "#9A7B2D", "#B89B3E", "#D4B35A", "#8B7355", "#6B5B4F",
    ]
    return colors[:n]


def render_stats():
    st.markdown("### Statistik")
    st.caption("Distribusi data putusan Pengadilan Pajak Indonesia.")

    df = load_data()

    # ── Overview metrics ──
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Putusan", f"{len(df):,}")
    col2.metric("Jenis Pajak", df["jenis_pajak"].nunique())
    col3.metric("Rentang Tahun Pajak", f"{df['tahun_pajak'].min()}–{df['tahun_pajak'].max()}")
    col4.metric("Rentang Tahun Putusan", f"{df['tahun_putusan'].min()}–{df['tahun_putusan'].max()}")

    st.markdown("---")

    # ── Jenis Pajak ──
    col_left, col_right = st.columns(2)

    with col_left:
        pajak_counts = df["jenis_pajak"].value_counts().reset_index()
        pajak_counts.columns = ["jenis", "count"]
        palette = _categorical_palette(len(pajak_counts))
        chart = (
            alt.Chart(pajak_counts, title="Distribusi Jenis Pajak")
            .mark_bar(height=22, cornerRadiusTopRight=3, cornerRadiusBottomRight=3)
            .encode(
                x=alt.X("count:Q", title=None, axis=alt.Axis(grid=True)),
                y=alt.Y("jenis:N", sort="-x", title=None),
                color=alt.Color("jenis:N", scale=alt.Scale(range=palette), legend=None),
                tooltip=["jenis", alt.Tooltip("count", format=",")],
            )
            .configure(**THEME_CONFIG)
            .properties(height=280)
        )
        st.altair_chart(chart, width='stretch')

    with col_right:
        putusan_counts = df["jenis_putusan"].value_counts().reset_index()
        putusan_counts.columns = ["jenis", "count"]
        palette2 = _categorical_palette(len(putusan_counts))
        chart = (
            alt.Chart(putusan_counts, title="Distribusi Jenis Putusan")
            .mark_bar(height=22, cornerRadiusTopRight=3, cornerRadiusBottomRight=3)
            .encode(
                x=alt.X("count:Q", title=None, axis=alt.Axis(grid=True)),
                y=alt.Y("jenis:N", sort="-x", title=None),
                color=alt.Color("jenis:N", scale=alt.Scale(range=palette2), legend=None),
                tooltip=["jenis", alt.Tooltip("count", format=",")],
            )
            .configure(**THEME_CONFIG)
            .properties(height=280)
        )
        st.altair_chart(chart, width='stretch')

    st.markdown("---")

    # ── Time series ──
    col_l, col_r = st.columns(2)

    with col_l:
        tp = df["tahun_pajak"].value_counts().sort_index().reset_index()
        tp.columns = ["tahun", "count"]
        chart = (
            alt.Chart(tp, title="Putusan per Tahun Pajak")
            .mark_line(color=ACCENT, strokeWidth=2.5)
            .encode(
                x=alt.X("tahun:O", title=None),
                y=alt.Y("count:Q", title=None, axis=alt.Axis(grid=True)),
            )
            + alt.Chart(tp).mark_circle(color=ACCENT, size=40).encode(
                x="tahun:O", y="count:Q",
                tooltip=[alt.Tooltip("tahun:O", title="Tahun"), alt.Tooltip("count:Q", title="Jumlah", format=",")],
            )
        ).configure(**THEME_CONFIG).properties(height=280)
        st.altair_chart(chart, width='stretch')

    with col_r:
        tp2 = df["tahun_putusan"].value_counts().sort_index().reset_index()
        tp2.columns = ["tahun", "count"]
        chart = (
            alt.Chart(tp2, title="Putusan per Tahun Putusan")
            .mark_line(color=GOLD, strokeWidth=2.5)
            .encode(
                x=alt.X("tahun:O", title=None),
                y=alt.Y("count:Q", title=None, axis=alt.Axis(grid=True)),
            )
            + alt.Chart(tp2).mark_circle(color=GOLD, size=40).encode(
                x="tahun:O", y="count:Q",
                tooltip=[alt.Tooltip("tahun:O", title="Tahun"), alt.Tooltip("count:Q", title="Jumlah", format=",")],
            )
        ).configure(**THEME_CONFIG).properties(height=280)
        st.altair_chart(chart, width='stretch')

    # ── Cross-tab ──
    st.markdown("---")
    st.markdown("#### Jenis Pajak × Jenis Putusan")
    cross = pd.crosstab(df["jenis_pajak"], df["jenis_putusan"])
    st.dataframe(cross, width='stretch')
