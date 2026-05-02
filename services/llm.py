"""LLM client via OpenRouter API (OpenAI-compatible)."""

from openai import OpenAI

OPENROUTER_BASE = "https://openrouter.ai/api/v1"

DEFAULT_MODEL = "google/gemini-2.0-flash-001"
SYSTEM_PROMPT = """Kamu adalah asisten hukum pajak Indonesia yang ahli dalam putusan Pengadilan Pajak.
Jawab pertanyaan pengguna berdasarkan konteks putusan yang diberikan.
Jika konteks tidak cukup untuk menjawab, katakan dengan jelas.
Gunakan Bahasa Indonesia. Selalu cantumkan nomor putusan sebagai referensi.
Jawab dengan ringkas, terstruktur, dan mudah dipahami."""


def get_client(api_key: str) -> OpenAI:
    return OpenAI(base_url=OPENROUTER_BASE, api_key=api_key)


def chat(
    client: OpenAI,
    model: str,
    messages: list[dict],
) -> str:
    """Send chat completion and return the assistant message."""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,
        max_tokens=2048,
    )
    return response.choices[0].message.content


def build_rag_messages(query: str, context_chunks: list[dict]) -> list[dict]:
    """Build message payload with system prompt + RAG context + user query."""
    # Build context block
    ctx_parts = []
    for i, r in enumerate(context_chunks, 1):
        ctx_parts.append(
            f"[Putusan {i}]\n"
            f"Nomor: {r['nomor_putusan']}\n"
            f"Jenis Pajak: {r['jenis_pajak']}\n"
            f"Tahun Pajak: {r['tahun_pajak']}\n"
            f"Tahun Putusan: {r['tahun_putusan']}\n"
            f"Jenis Putusan: {r['jenis_putusan']}\n"
            f"Pokok Sengketa: {r['pokok_sengketa']}\n"
            f"Teks: {r['text_chunk'][:1500]}\n"
        )

    context = "\n---\n".join(ctx_parts)

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Berikut adalah putusan-putusan pengadilan pajak yang relevan:\n\n"
                f"{context}\n\n"
                f"---\n\n"
                f"Pertanyaan: {query}"
            ),
        },
    ]
