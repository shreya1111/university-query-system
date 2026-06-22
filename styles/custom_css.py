import streamlit as st
from styles.theme import COLORS


def inject_css() -> None:
    """Inject global dark SaaS CSS. Call once per page after set_page_config."""
    st.markdown(f"""
<style>
/* ── Fonts ──────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, * {{ font-family: 'Inter', sans-serif; box-sizing: border-box; }}

/* ── Background ─────────────────────────────────────────────────── */
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
.main {{ background: {COLORS['bg']} !important; }}

/* ── Hide Streamlit chrome ──────────────────────────────────────── */
#MainMenu, footer, [data-testid="stDecoration"],
[data-testid="stStatusWidget"] {{ display: none !important; }}

/* ── Hide DEFAULT Streamlit page-nav in sidebar ─────────────────── */
[data-testid="stSidebarNav"] {{ display: none !important; }}

/* ── Sidebar shell ──────────────────────────────────────────────── */
[data-testid="stSidebar"] {{
    background: {COLORS['card']} !important;
    border-right: 1px solid {COLORS['border_solid']} !important;
    min-width: 260px !important;
    max-width: 260px !important;
}}
[data-testid="stSidebar"] > div:first-child {{ padding: 0 !important; }}

/* sidebar page-link text */
[data-testid="stSidebar"] [data-testid="stPageLink"] p {{
    color: {COLORS['muted']} !important;
    font-size: .875rem !important;
    font-weight: 500;
    transition: color .15s;
    padding: .1rem 0;
}}
[data-testid="stSidebar"] [data-testid="stPageLink"]:hover p {{
    color: {COLORS['text']} !important;
}}

/* ── Block container ────────────────────────────────────────────── */
.main .block-container {{
    padding: 1.8rem 2.2rem 2rem !important;
    max-width: 100% !important;
}}

/* ── Typography ─────────────────────────────────────────────────── */
h1, h2, h3, h4 {{ color: {COLORS['text']} !important; font-weight: 700; margin-bottom: .4rem; }}
p, li {{ color: {COLORS['muted']}; line-height: 1.6; }}

/* ── Inputs ─────────────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea textarea {{
    background: {COLORS['card2']} !important;
    border: 1px solid {COLORS['border_solid']} !important;
    border-radius: 10px !important;
    color: {COLORS['text']} !important;
    font-size: .9rem !important;
    transition: border-color .15s;
}}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {{
    border-color: {COLORS['primary']} !important;
    box-shadow: 0 0 0 2px {COLORS['primary']}33 !important;
}}
.stTextInput label, .stTextArea label, .stSelectbox label {{
    color: {COLORS['muted']} !important;
    font-size: .8rem !important;
    font-weight: 600;
}}

/* ── Selectbox ──────────────────────────────────────────────────── */
div[data-baseweb="select"] > div {{
    background: {COLORS['card2']} !important;
    border: 1px solid {COLORS['border_solid']} !important;
    border-radius: 10px !important;
    color: {COLORS['text']} !important;
}}

/* ── Buttons ────────────────────────────────────────────────────── */
.stButton > button {{
    background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['accent']}) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: .5rem 1.4rem !important;
    font-weight: 600 !important;
    font-size: .875rem !important;
    transition: opacity .2s, transform .15s !important;
    width: 100%;
}}
.stButton > button:hover {{
    opacity: .88 !important;
    transform: translateY(-1px) !important;
}}

/* ── Tabs ───────────────────────────────────────────────────────── */
[data-testid="stTabs"] [data-testid="stTab"] {{
    color: {COLORS['muted']} !important;
    font-weight: 600;
    font-size: .875rem;
}}
[data-testid="stTabs"] [aria-selected="true"] {{
    color: {COLORS['text']} !important;
    border-bottom: 2px solid {COLORS['primary']} !important;
}}

/* ── Expanders ──────────────────────────────────────────────────── */
[data-testid="stExpander"] {{
    background: {COLORS['card2']} !important;
    border: 1px solid {COLORS['border_solid']} !important;
    border-radius: 12px !important;
    margin-bottom: .5rem;
}}

/* ── Metrics ────────────────────────────────────────────────────── */
[data-testid="stMetricLabel"] {{ color: {COLORS['muted']} !important; font-size: .78rem !important; }}
[data-testid="stMetricValue"] {{ color: {COLORS['text']} !important; font-weight: 700 !important; }}

/* ── Dataframe ──────────────────────────────────────────────────── */
[data-testid="stDataFrame"] th {{
    background: {COLORS['card2']} !important;
    color: {COLORS['muted']} !important;
    font-size: .75rem !important;
    text-transform: uppercase;
    letter-spacing: .06em;
}}
[data-testid="stDataFrame"] td {{
    background: {COLORS['card']} !important;
    color: {COLORS['text']} !important;
    font-size: .85rem !important;
}}

/* ── Scrollbar ──────────────────────────────────────────────────── */
::-webkit-scrollbar {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {COLORS['bg']}; }}
::-webkit-scrollbar-thumb {{ background: {COLORS['border_solid']}; border-radius: 4px; }}

/* ── HR ─────────────────────────────────────────────────────────── */
hr {{ border-color: {COLORS['border_solid']} !important; margin: 1rem 0 !important; }}

/* ── Alerts ─────────────────────────────────────────────────────── */
[data-testid="stNotification"] {{ border-radius: 10px !important; }}
</style>
""", unsafe_allow_html=True)