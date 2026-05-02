"""Data browser: filter & explore verdicts."""

import streamlit as st
import pandas as pd

from services.data import load_data


def render_data_browser():
    st.markdown("### Data Putusan")
    st.caption("Jelajahi dan filter seluruh putusan Pengadilan Pajak.")

    df = load_data()

    # ── Filters ──
    col1, col2, col3 = st.columns(3)
    with col1:
        jenis_pajak = st.multiselect("Jenis Pajak", sorted(df["jenis_pajak"].unique()))
    with col2:
        jenis_putusan = st.multiselect("Jenis Putusan", sorted(df["jenis_putusan"].unique()))
    with col3:
        tahun_pajak = st.multiselect("Tahun Pajak", sorted(df["tahun_pajak"].unique()))

    mask = pd.Series([True] * len(df))
    if jenis_pajak:
        mask &= df["jenis_pajak"].isin(jenis_pajak)
    if jenis_putusan:
        mask &= df["jenis_putusan"].isin(jenis_putusan)
    if tahun_pajak:
        mask &= df["tahun_pajak"].isin(tahun_pajak)

    filtered = df[mask].copy()

    # Text search
    text_search = st.text_input("Cari dalam teks putusan...", placeholder="kata kunci...")
    if text_search:
        filtered = filtered[
            filtered["text"].str.contains(text_search, case=False, na=False)
        ]

    st.caption(f"**{len(filtered):,}** putusan ditemukan")

    # ── Table ──
    display_cols = [
        "nomor_putusan", "tahun_pajak", "jenis_pajak",
        "tahun_putusan", "pokok_sengketa", "jenis_putusan",
    ]
    st.dataframe(
        filtered[display_cols].head(200),
        width='stretch',
        hide_index=True,
        column_config={
            "nomor_putusan": st.column_config.TextColumn("Nomor Putusan", width="large"),
            "pokok_sengketa": st.column_config.TextColumn("Pokok Sengketa", width="large"),
        },
    )

    # ── Detail viewer ──
    if len(filtered) > 0:
        st.markdown("---")
        st.markdown("#### Detail Putusan")
        idx = st.selectbox(
            "Pilih putusan",
            range(len(filtered)),
            format_func=lambda i: filtered.iloc[i]["nomor_putusan"],
            label_visibility="collapsed",
        )
        row = filtered.iloc[idx]

        col_meta, col_text = st.columns([1, 2])
        with col_meta:
            _detail_field("Nomor Putusan", row["nomor_putusan"])
            _detail_field("Jenis Pajak", row["jenis_pajak"])
            _detail_field("Tahun Pajak", row["tahun_pajak"])
            _detail_field("Tahun Putusan", row["tahun_putusan"])
            _detail_field("Jenis Putusan", row["jenis_putusan"])
            _detail_field("Pokok Sengketa", row["pokok_sengketa"])

        with col_text:
            with st.expander("Teks lengkap putusan"):
                st.text_area(
                    "text",
                    value=row["text"],
                    height=500,
                    disabled=True,
                    label_visibility="collapsed",
                )


def _detail_field(label: str, value: str):
    st.markdown(
        f'<div class="detail-label">{label}</div>'
        f'<div class="detail-value">{value}</div>',
        unsafe_allow_html=True,
    )
