"""config.py — App configuration and global CSS."""

from dataclasses import dataclass


@dataclass
class _AppConfig:
    APP_NAME: str = "AI Fitness Planner"
    VERSION: str = "1.0.0"
    MODEL_DIR: str = "."  # Directory where .pkl files reside


@dataclass
class _StyleConfig:
    CSS: str = """
<style>
/* ── Google Fonts ─────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Design Tokens ────────────────────────────────────────────────────────── */
:root {
    --bg:          #0a0a0f;
    --surface:     #111118;
    --surface2:    #1a1a28;
    --border:      #2a2a3d;
    --accent:      #00ff88;
    --accent2:     #ff6b35;
    --accent3:     #4d9fff;
    --text:        #e8e8f0;
    --text-muted:  #6b6b8a;
    --font-head:   'Bebas Neue', cursive;
    --font-body:   'DM Sans', sans-serif;
    --font-mono:   'JetBrains Mono', monospace;
    --radius:      12px;
    --glow:        0 0 30px rgba(0,255,136,0.15);
}

/* ── Global Reset ─────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
}

/* ── Sidebar ──────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stTextArea label {
    color: var(--text-muted) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-family: var(--font-mono) !important;
}

/* ── Header ───────────────────────────────────────────────────────────────── */
.app-header {
    text-align: center;
    padding: 2rem 0 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
    position: relative;
}
.app-header::before {
    content: '';
    position: absolute;
    bottom: -1px; left: 50%;
    transform: translateX(-50%);
    width: 120px; height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent3));
}
.app-title {
    font-family: var(--font-head) !important;
    font-size: 3.5rem !important;
    letter-spacing: 0.15em !important;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent3) 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin: 0 !important;
}
.app-tagline {
    color: var(--text-muted) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.2em !important;
    margin-top: 0.5rem !important;
}

/* ── Landing ──────────────────────────────────────────────────────────────── */
.landing-hero {
    text-align: center;
    padding: 5rem 2rem;
}
.hero-title {
    font-family: var(--font-head) !important;
    font-size: 3rem !important;
    color: var(--text) !important;
    letter-spacing: 0.12em !important;
}
.hero-sub {
    color: var(--text-muted) !important;
    font-size: 1.1rem !important;
    max-width: 540px;
    margin: 1rem auto 0 !important;
}

/* ── Feature Cards ────────────────────────────────────────────────────────── */
.feature-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.8rem 1.5rem;
    text-align: center;
    transition: border-color 0.25s, box-shadow 0.25s;
    height: 100%;
}
.feature-card:hover {
    border-color: var(--accent);
    box-shadow: var(--glow);
}
.feature-icon {
    font-size: 2.5rem;
    margin-bottom: 0.8rem;
}
.feature-card h3 {
    font-family: var(--font-head) !important;
    letter-spacing: 0.08em !important;
    font-size: 1.3rem !important;
    color: var(--accent) !important;
    margin: 0 0 0.5rem !important;
}
.feature-card p {
    color: var(--text-muted) !important;
    font-size: 0.9rem !important;
}

/* ── Metric Cards ─────────────────────────────────────────────────────────── */
.metric-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
}
.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: var(--accent);
}
.metric-card.orange::after { background: var(--accent2); }
.metric-card.blue::after   { background: var(--accent3); }
.metric-label {
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
}
.metric-value {
    font-family: var(--font-head) !important;
    font-size: 2.8rem !important;
    color: var(--accent) !important;
    line-height: 1 !important;
    margin: 0.3rem 0 !important;
}
.metric-value.orange { color: var(--accent2) !important; }
.metric-value.blue   { color: var(--accent3) !important; }
.metric-unit {
    font-family: var(--font-mono) !important;
    font-size: 0.8rem !important;
    color: var(--text-muted) !important;
}

/* ── Fitness Badge ────────────────────────────────────────────────────────── */
.fitness-badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent3) 100%);
    color: var(--bg) !important;
    font-family: var(--font-head) !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.15em !important;
    padding: 0.4rem 1.2rem;
    border-radius: 50px;
}

/* ── Section Headers ──────────────────────────────────────────────────────── */
.section-header {
    font-family: var(--font-head) !important;
    font-size: 1.8rem !important;
    letter-spacing: 0.1em !important;
    color: var(--text) !important;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5rem;
    margin-bottom: 1.5rem !important;
}

/* ── Workout Day Card ─────────────────────────────────────────────────────── */
.day-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.day-card:hover { border-color: var(--accent3); }
.day-title {
    font-family: var(--font-head) !important;
    font-size: 1.1rem !important;
    color: var(--accent3) !important;
    letter-spacing: 0.1em !important;
    margin-bottom: 0.8rem !important;
}
.exercise-row {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.4rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.9rem;
}
.exercise-row:last-child { border-bottom: none; }
.ex-name { flex: 2; color: var(--text) !important; }
.ex-sets { flex: 1; color: var(--accent) !important; font-family: var(--font-mono) !important; font-size: 0.82rem !important; }
.ex-muscle { flex: 2; color: var(--text-muted) !important; font-size: 0.82rem !important; }

/* ── Meal Card ────────────────────────────────────────────────────────────── */
.meal-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}
.meal-title {
    font-family: var(--font-head) !important;
    font-size: 1rem !important;
    color: var(--accent2) !important;
    letter-spacing: 0.08em !important;
    margin-bottom: 0.6rem !important;
}
.meal-calories {
    float: right;
    font-family: var(--font-mono) !important;
    font-size: 0.82rem !important;
    color: var(--accent) !important;
    background: rgba(0,255,136,0.08);
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
}

/* ── Info Box ─────────────────────────────────────────────────────────────── */
.info-box {
    background: rgba(77,159,255,0.08);
    border: 1px solid rgba(77,159,255,0.25);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    font-size: 0.9rem;
    color: var(--accent3) !important;
}

/* ── NLP Note ─────────────────────────────────────────────────────────────── */
.nlp-note {
    background: rgba(255,107,53,0.08);
    border-left: 3px solid var(--accent2);
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    border-radius: 0 8px 8px 0;
    font-size: 0.88rem;
    color: var(--text) !important;
}

/* ── Tabs ─────────────────────────────────────────────────────────────────── */
[data-testid="stTabs"] [role="tablist"] {
    gap: 0.5rem;
    border-bottom: 1px solid var(--border) !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: var(--font-mono) !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 8px 8px 0 0 !important;
    color: var(--text-muted) !important;
    transition: all 0.2s !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: var(--accent) !important;
    border-color: var(--border) !important;
    border-bottom-color: var(--bg) !important;
    background: var(--surface2) !important;
}

/* ── Primary Button ───────────────────────────────────────────────────────── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent3) 100%) !important;
    color: var(--bg) !important;
    font-family: var(--font-head) !important;
    font-size: 1rem !important;
    letter-spacing: 0.15em !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 0.7rem 1.5rem !important;
    transition: opacity 0.2s, transform 0.2s !important;
}
.stButton > button[kind="primary"]:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

/* ── Scrollbar ────────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* ── Plotly container ─────────────────────────────────────────────────────── */
.js-plotly-plot .plotly, .plot-container { background: transparent !important; }
</style>
"""


APP_CONFIG = _AppConfig()
STYLE_CONFIG = _StyleConfig()
