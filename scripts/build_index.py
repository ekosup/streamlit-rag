"""
Build the sqlite-vec index from CSV data.

Usage:
    uv run python scripts/build_index.py
    uv run python scripts/build_index.py --model paraphrase-multilingual-mpnet-base-v2
    uv run python scripts/build_index.py --chunk-size 3000 --overlap 300
    uv run python scripts/build_index.py --reset
"""

import argparse
import csv
import sys
import time

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


DB_PATH = "data/tax_court.vec.db"
CSV_PATH = "data/indonesia_tax_court_verdict.csv"
DEFAULT_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"


def chunk_text(text: str, max_chars: int = 2000, overlap: int = 200) -> list[str]:
    """Character-level chunking with overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunks.append(text[start:end])
        start += max_chars - overlap
    return chunks


def build_index(
    model_name: str = DEFAULT_MODEL,
    chunk_size: int = 2000,
    overlap: int = 200,
    reset: bool = False,
):
    import sqlite3
    import sqlite_vec

    print(f"🔄 Loading model: {model_name}")
    model = SentenceTransformer(model_name, cache_folder="model")
    dim = model.get_sentence_embedding_dimension()
    print(f"   Embedding dimension: {dim}")

    # Connect
    conn = sqlite3.connect(DB_PATH)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)
    conn.enable_load_extension(False)

    # Drop existing if reset
    if reset:
        print("🗑️  Dropping existing tables...")
        conn.execute("DROP TABLE IF EXISTS verdicts_vec")
        conn.execute("DROP TABLE IF EXISTS verdicts_meta")
        conn.commit()

    # Create tables
    conn.execute(
        f"""
        CREATE VIRTUAL TABLE IF NOT EXISTS verdicts_vec
        USING vec0(
            id INTEGER PRIMARY KEY,
            text_embedding float[{dim}]
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS verdicts_meta (
            id INTEGER PRIMARY KEY,
            nomor_putusan TEXT,
            tahun_pajak TEXT,
            jenis_pajak TEXT,
            tahun_putusan TEXT,
            pokok_sengketa TEXT,
            jenis_putusan TEXT,
            text_chunk TEXT
        )
        """
    )
    conn.commit()

    # Check existing
    existing = conn.execute("SELECT COUNT(*) FROM verdicts_meta").fetchone()[0]
    if existing > 0 and not reset:
        print(f"⚠️  Index already has {existing:,} chunks. Use --reset to rebuild.")
        conn.close()
        return

    # Load CSV
    print(f"📂 Loading CSV: {CSV_PATH}")
    csv.field_size_limit(sys.maxsize)
    df = pd.read_csv(CSV_PATH)
    print(f"   {len(df):,} rows loaded")

    # Chunk & embed
    print(f"✂️  Chunking (size={chunk_size}, overlap={overlap})...")
    t0 = time.time()

    total_chunks = 0
    batch_meta = []
    batch_vec = []
    BATCH_SIZE = 5000  # commit every N chunks

    for idx, row in df.iterrows():
        text = str(row.get("text", ""))
        chunks = chunk_text(text, max_chars=chunk_size, overlap=overlap)

        if chunks:
            embeddings = model.encode(chunks, show_progress_bar=False)

            for chunk, emb in zip(chunks, embeddings):
                total_chunks += 1
                batch_meta.append(
                    (
                        total_chunks,
                        row.get("nomor_putusan", ""),
                        row.get("tahun_pajak", ""),
                        row.get("jenis_pajak", ""),
                        row.get("tahun_putusan", ""),
                        row.get("pokok_sengketa", ""),
                        row.get("jenis_putusan", ""),
                        chunk,
                    )
                )
                batch_vec.append((total_chunks, emb.astype(np.float32).tobytes()))

        # Flush batch
        if len(batch_meta) >= BATCH_SIZE:
            conn.executemany(
                "INSERT INTO verdicts_meta (id, nomor_putusan, tahun_pajak, jenis_pajak, tahun_putusan, pokok_sengketa, jenis_putusan, text_chunk) VALUES (?,?,?,?,?,?,?,?)",
                batch_meta,
            )
            conn.executemany(
                "INSERT INTO verdicts_vec (id, text_embedding) VALUES (?, ?)",
                batch_vec,
            )
            conn.commit()
            elapsed = time.time() - t0
            pct = (idx + 1) / len(df) * 100
            print(
                f"   [{pct:5.1f}%] {total_chunks:,} chunks | {idx+1:,}/{len(df):,} rows | {elapsed:.0f}s"
            )
            batch_meta.clear()
            batch_vec.clear()

    # Final flush
    if batch_meta:
        conn.executemany(
            "INSERT INTO verdicts_meta (id, nomor_putusan, tahun_pajak, jenis_pajak, tahun_putusan, pokok_sengketa, jenis_putusan, text_chunk) VALUES (?,?,?,?,?,?,?,?)",
            batch_meta,
        )
        conn.executemany(
            "INSERT INTO verdicts_vec (id, text_embedding) VALUES (?, ?)",
            batch_vec,
        )
        conn.commit()

    elapsed = time.time() - t0
    print(f"\n✅ Done! {total_chunks:,} chunks indexed in {elapsed:.1f}s")
    print(f"   DB: {DB_PATH}")

    # Save metadata
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS index_metadata (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """
    )
    conn.execute("DELETE FROM index_metadata")
    meta = [
        ("model_name", model_name),
        ("dim", str(dim)),
        ("total_chunks", str(total_chunks)),
        ("chunk_size", str(chunk_size)),
        ("overlap", str(overlap)),
        ("total_rows", str(len(df))),
        ("build_time_s", f"{elapsed:.1f}"),
    ]
    conn.executemany(
        "INSERT INTO index_metadata (key, value) VALUES (?, ?)", meta
    )
    conn.commit()
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Build sqlite-vec index for tax court verdicts")
    parser.add_argument(
        "--model", default=DEFAULT_MODEL, help="Sentence transformer model name"
    )
    parser.add_argument(
        "--chunk-size", type=int, default=2000, help="Max chars per chunk"
    )
    parser.add_argument(
        "--overlap", type=int, default=200, help="Overlap chars between chunks"
    )
    parser.add_argument(
        "--reset", action="store_true", help="Drop existing index and rebuild"
    )
    args = parser.parse_args()

    build_index(
        model_name=args.model,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        reset=args.reset,
    )


if __name__ == "__main__":
    main()
