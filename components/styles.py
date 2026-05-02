"""Custom CSS for a clean, professional legal research aesthetic."""

CUSTOM_CSS = """
<style>
/* ── Typography ────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=DM+Sans:wght@400;500;600&display=swap');

:root {
    --font-serif: 'Source Serif 4', 'Georgia', serif;
    --font-sans: 'DM Sans', 'Helvetica Neue', sans-serif;
    --ink: #1A1A1A;
    --slate: #4A4A4A;
    --muted: #7A7A7A;
    --rule: #D4D0C8;
    --surface: #F0EFEB;
    --surface-alt: #E8E7E3;
    --accent: #1B4332;
    --accent-light: #2D6A4F;
    --gold: #9A7B2D;
    --gold-light: #B89B3E;
}

/* Base */
.stApp {
    font-family: var(--font-sans);
    color: var(--ink);
}

h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-serif) !important;
    font-weight: 600 !important;
    color: var(--ink) !important;
    letter-spacing: -0.01em;
}

h1 { font-size: 1.75rem !important; }
h2 { font-size: 1.35rem !important; }
h3 { font-size: 1.15rem !important; }

p, .stMarkdown, .stCaption {
    font-family: var(--font-sans);
    color: var(--slate);
    line-height: 1.6;
}

/* ── Sidebar ──────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: var(--ink) !important;
}
section[data-testid="stSidebar"] * {
    color: #E0DDD6 !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
}

/* Sidebar divider */
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.1) !important;
}

/* Sidebar success box */
section[data-testid="stSidebar"] [data-testid="stSuccess"] {
    background: rgba(27,67,50,0.3) !important;
    color: #A8D5BA !important;
}

/* Sidebar caption */
section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] small {
    color: #9A9A9A !important;
    font-size: 0.8rem !important;
}

/* ── Tabs ──────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 1px solid var(--rule);
}
.stTabs [data-baseweb="tab"] {
    font-family: var(--font-sans);
    font-weight: 500;
    font-size: 0.875rem;
    padding: 0.6rem 1.2rem;
    color: var(--muted) !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
}

/* ── Chat ──────────────────────────────────────────────────── */
.stChatMessage {
    background: transparent !important;
}
[data-testid="stChatMessageAvatarAssistant"] {
    background: var(--accent) !important;
}
[data-testid="stChatMessageAvatarUser"] {
    background: var(--surface) !important;
}

/* Chat input */
.stChatInput textarea {
    font-family: var(--font-sans) !important;
    border-color: var(--rule) !important;
}
.stChatInput textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}

/* ── Tables ────────────────────────────────────────────────── */
.stDataFrame {
    font-family: var(--font-sans);
}
table th {
    font-family: var(--font-sans) !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
    color: var(--muted) !important;
}

/* ── Result cards in chat ──────────────────────────────────── */
.result-card {
    background: var(--surface);
    padding: 1rem 1.25rem;
    margin: 0.75rem 0;
    font-size: 0.9rem;
}
.result-card .meta-grid {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 0.15rem 0.75rem;
    font-size: 0.85rem;
    color: var(--slate);
}
.result-card .meta-grid dt {
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    font-size: 0.7rem;
    letter-spacing: 0.04em;
}
.result-card .meta-grid dd {
    margin: 0;
}
.result-card .similarity {
    font-family: var(--font-sans);
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--accent);
    letter-spacing: 0.02em;
}
.result-card details {
    margin-top: 0.75rem;
}
.result-card summary {
    font-size: 0.8rem;
    color: var(--muted);
    cursor: pointer;
    font-weight: 500;
}
.result-card details > p {
    font-size: 0.85rem;
    line-height: 1.65;
    color: var(--slate);
    background: white;
    padding: 0.75rem 1rem;
    border: 1px solid var(--rule);
    max-height: 200px;
    overflow-y: auto;
}

/* ── Detail viewer label ───────────────────────────────────── */
.detail-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--muted);
    margin-bottom: 0.15rem;
}
.detail-value {
    font-size: 0.95rem;
    color: var(--ink);
    margin-bottom: 0.75rem;
}

/* ── Metric cards ──────────────────────────────────────────── */
[data-testid="stMetricValue"] {
    font-family: var(--font-serif) !important;
    font-weight: 700 !important;
    font-size: 1.5rem !important;
    color: var(--ink) !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
    color: var(--muted) !important;
    font-weight: 600 !important;
}

/* ── Buttons ───────────────────────────────────────────────── */
.stButton > button {
    font-family: var(--font-sans) !important;
    font-weight: 500 !important;
    border-radius: 4px !important;
    transition: all 0.15s ease;
    color: var(--ink) !important;
}

/* ── Inputs and Dropdowns ──────────────────────────────────── */
.stTextInput input,
.stTextInput textarea,
.stSelectbox select {
    font-family: var(--font-sans) !important;
    color: var(--ink) !important;
}

/* ── Scrollbar (subtle) ────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--rule); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }

/* ── Altair charts background ──────────────────────────────── */
.vega-embed summary { display: none !important; }
</style>
"""
