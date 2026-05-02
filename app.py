import streamlit as st
from components.sidebar import render_sidebar
from components.chat import render_chat
from components.data_browser import render_data_browser
from components.stats import render_stats
from components.styles import CUSTOM_CSS
from services.vector_store import VectorStore


def init_session_state():
    if "top_k" not in st.session_state:
        st.session_state.top_k = 5
    if "last_exchange" not in st.session_state:
        st.session_state.last_exchange = None
    if "openrouter_api_key" not in st.session_state:
        st.session_state.openrouter_api_key = ""
    if "llm_model" not in st.session_state:
        st.session_state.llm_model = "google/gemini-2.0-flash-001"
    if "indexed" not in st.session_state:
        st.session_state.indexed = VectorStore.is_indexed()
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None


def main():
    st.set_page_config(
        page_title="Pengadilan Pajak — RAG",
        page_icon="⚖",
        layout="wide",
    )

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    init_session_state()
    render_sidebar()

    st.markdown("# Pencarian Putusan Pengadilan Pajak Indonesia")

    tab_chat, tab_browse, tab_stats = st.tabs(
        ["Pencarian", "Data", "Statistik"]
    )

    with tab_chat:
        if not st.session_state.indexed:
            st.markdown("### Belum ada index")
            st.markdown(
                "Jalankan perintah berikut untuk membangun index, lalu refresh halaman."
            )
            st.code("uv run python scripts/build_index.py", language="bash")
        else:
            render_chat()

    with tab_browse:
        render_data_browser()

    with tab_stats:
        render_stats()


if __name__ == "__main__":
    main()
