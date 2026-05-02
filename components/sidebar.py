"""Sidebar: index status, search settings, LLM config."""

import streamlit as st

from services.vector_store import VectorStore

AVAILABLE_MODELS = [
    "google/gemini-2.0-flash-001",
    "google/gemini-2.5-flash-preview",
    "anthropic/claude-sonnet-4",
    "openai/gpt-4.1-mini",
    "openai/gpt-4.1-nano",
    "meta-llama/llama-4-maverick",
    "deepseek/deepseek-chat-v3-0324",
]


def render_sidebar():
    with st.sidebar:
        # Brand header
        st.markdown("### Pengadilan Pajak")
        st.caption("RAG — Semantic Search + LLM")
        st.markdown("---")

        # ── LLM Config ──
        st.markdown("#### LLM")
        api_key = st.text_input(
            "OpenRouter API Key",
            type="password",
            value=st.session_state.get("openrouter_api_key", ""),
        )
        st.session_state.openrouter_api_key = api_key

        llm_model = st.selectbox(
            "Model",
            AVAILABLE_MODELS,
            index=AVAILABLE_MODELS.index(
                st.session_state.get("llm_model", AVAILABLE_MODELS[0])
            )
            if st.session_state.get("llm_model") in AVAILABLE_MODELS
            else 0,
        )
        st.session_state.llm_model = llm_model

        st.markdown("---")

        # ── Index status ──
        st.markdown("#### Index")
        if st.session_state.indexed:
            meta = VectorStore.get_index_metadata()
            if meta:
                n = int(meta.get("total_chunks", 0))
                st.markdown(f"**{n:,}** chunks indexed")
                model = meta.get("model_name", "-")
                st.caption(f"Embedding: {model}")
            else:
                st.markdown("**Index ready**")

            if st.button("Refresh", width='stretch'):
                st.session_state.indexed = VectorStore.is_indexed()
                st.rerun()
        else:
            st.warning("Index belum dibuat")
            st.code("uv run python scripts/build_index.py")
            if st.button("Cek ulang", width='stretch'):
                st.session_state.indexed = VectorStore.is_indexed()
                st.rerun()

        st.markdown("---")

        # ── Search settings ──
        st.markdown("#### Pencarian")
        st.session_state.top_k = st.slider(
            "Jumlah hasil", min_value=1, max_value=20, value=st.session_state.top_k
        )

        st.markdown("---")

        # ── Quick stats ──
        from services.data import load_data

        df = load_data()
        st.metric("Total Putusan", f"{len(df):,}")
        st.metric("Jenis Pajak", df["jenis_pajak"].nunique())
