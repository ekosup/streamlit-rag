"""Vector store backed by sqlite-vec — read-only client for Streamlit."""

import sqlite3

import numpy as np
from sentence_transformers import SentenceTransformer

DB_PATH = "data/tax_court.vec.db"


MODEL_CACHE = "model"


class VectorStore:
    """Read-only vector store client for Streamlit."""

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name, cache_folder=MODEL_CACHE)
        self.dim = self.model.get_sentence_embedding_dimension()
        self.conn = self._connect()
        self._meta = self._load_metadata()

    @classmethod
    def is_indexed(cls) -> bool:
        """Check if index DB exists and has data."""
        from pathlib import Path

        if not Path(DB_PATH).exists():
            return False
        try:
            conn = sqlite3.connect(DB_PATH)
            count = conn.execute("SELECT COUNT(*) FROM verdicts_meta").fetchone()[0]
            conn.close()
            return count > 0
        except Exception:
            return False

    @classmethod
    def get_index_metadata(cls) -> dict | None:
        """Load index metadata without loading the embedding model."""
        from pathlib import Path

        if not Path(DB_PATH).exists():
            return None
        try:
            conn = sqlite3.connect(DB_PATH)
            rows = conn.execute(
                "SELECT key, value FROM index_metadata"
            ).fetchall()
            conn.close()
            if not rows:
                return None
            return dict(rows)
        except Exception:
            return None

    # ------------------------------------------------------------------
    # DB helpers
    # ------------------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        import sqlite_vec

        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)
        return conn

    def _load_metadata(self) -> dict:
        try:
            rows = self.conn.execute(
                "SELECT key, value FROM index_metadata"
            ).fetchall()
            return dict(rows)
        except Exception:
            return {}

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def total_chunks(self) -> int:
        return int(self._meta.get("total_chunks", 0))

    @property
    def index_model_name(self) -> str:
        return self._meta.get("model_name", self.model_name)

    @property
    def index_info(self) -> dict:
        return self._meta

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Semantic search returning top-k results."""
        q_emb = self.model.encode([query], show_progress_bar=False)[0]
        q_bytes = q_emb.astype(np.float32).tobytes()

        results = self.conn.execute(
            """
            SELECT
                v.id,
                m.nomor_putusan,
                m.tahun_pajak,
                m.jenis_pajak,
                m.tahun_putusan,
                m.pokok_sengketa,
                m.jenis_putusan,
                m.text_chunk,
                v.distance
            FROM verdicts_vec v
            JOIN verdicts_meta m ON v.id = m.id
            WHERE text_embedding MATCH ? AND k = ?
            ORDER BY v.distance
            """,
            (q_bytes, top_k),
        ).fetchall()

        cols = [
            "id", "nomor_putusan", "tahun_pajak", "jenis_pajak",
            "tahun_putusan", "pokok_sengketa", "jenis_putusan",
            "text_chunk", "distance",
        ]
        return [dict(zip(cols, r)) for r in results]

    def close(self):
        self.conn.close()
