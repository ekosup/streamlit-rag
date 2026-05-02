"""Chat: RAG + LLM query interface — stateless, no history."""

import streamlit as st

from services.vector_store import VectorStore
from services.llm import get_client, build_rag_messages, chat


def render_chat():
    st.markdown("### Cari Putusan Pengadilan Pajak")
    st.caption(
        "Tanyakan tentang putusan pajak — sistem menemukan dokumen relevan lalu "
        "merangkum jawaban menggunakan AI."
    )

    # Check config
    api_key = st.session_state.get("openrouter_api_key", "")
    if not api_key:
        st.warning("Masukkan OpenRouter API Key di sidebar untuk mengaktifkan chatbot.")
        return

    # Show last exchange only (current query + response)
    last = st.session_state.get("last_exchange")
    if last:
        with st.chat_message("user"):
            st.markdown(last["query"])
        with st.chat_message("assistant"):
            st.markdown(last["response"], unsafe_allow_html=True)

    # Input
    if prompt := st.chat_input("Contoh: putusan PPN kelapa sawit tahun 2011..."):
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = _generate_response(prompt)
            st.markdown(response, unsafe_allow_html=True)

        # Overwrite — no history accumulation
        st.session_state.last_exchange = {
            "query": prompt,
            "response": response,
        }
        st.rerun()


def _get_vector_store() -> VectorStore:
    if st.session_state.vector_store is None:
        model_name = st.session_state.get(
            "embedding_model_name", "paraphrase-multilingual-MiniLM-L12-v2"
        )
        with st.spinner("Memuat model embedding..."):
            st.session_state.vector_store = VectorStore(model_name=model_name)
    return st.session_state.vector_store


def _generate_response(query: str) -> str:
    vs = _get_vector_store()
    top_k = st.session_state.get("top_k", 5)

    # 1. Retrieve
    with st.spinner("Mencari putusan yang relevan..."):
        results = vs.search(query, top_k=top_k)

    if not results:
        return "Tidak ditemukan putusan yang relevan untuk pertanyaan tersebut."

    # 2. Sources
    sources = _build_sources(results)

    # 3. LLM
    api_key = st.session_state.get("openrouter_api_key", "")
    model = st.session_state.get("llm_model", "google/gemini-2.0-flash-001")
    client = get_client(api_key)
    messages = build_rag_messages(query, results)

    with st.spinner("Menyusun jawaban..."):
        try:
            answer = chat(client, model, messages)
        except Exception as e:
            return f"⚠️ Gagal menghubungi LLM: {e}\n\n{sources}"

    return f"{answer}\n\n---\n{sources}"


def _build_sources(results: list[dict]) -> str:
    parts = [f'<small>Sumber: **{len(results)}** putusan relevan</small>\n']

    for i, r in enumerate(results, 1):
        score = 1 - r["distance"]
        sengketa = r["pokok_sengketa"][:250]
        chunk = r["text_chunk"][:800].replace("\n", " ")

        parts.append(
            f"""
<div class="result-card">

**{i}. {r['nomor_putusan']}** <span class="similarity">{score:.1%} match</span>

<div class="meta-grid">
  <dt>Jenis Pajak</dt><dd>{r['jenis_pajak']}</dd>
  <dt>Tahun Pajak</dt><dd>{r['tahun_pajak']}</dd>
  <dt>Tahun Putusan</dt><dd>{r['tahun_putusan']}</dd>
  <dt>Putusan</dt><dd>{r['jenis_putusan']}</dd>
</div>

{sengketa}...

<details><summary>Cuplikan teks putusan</summary>
<p>{chunk}...</p>
</details>

</div>
"""
        )

    return "\n".join(parts)
