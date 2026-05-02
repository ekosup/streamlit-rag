import sys
import csv

import pandas as pd
import streamlit as st

CSV_PATH = "data/indonesia_tax_court_verdict.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load the tax court verdict CSV."""
    csv.field_size_limit(sys.maxsize)
    df = pd.read_csv(CSV_PATH)
    return df


def get_vector_store() -> "VectorStore | None":
    """Get the initialized vector store from session state."""
    return st.session_state.get("vector_store")
