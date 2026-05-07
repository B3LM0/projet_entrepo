import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

API_BASE = "https://projet-entrepo.onrender.com/"

# ─── CONFIG PAGE ──────────────────────────────────────────────
st.set_page_config(
    page_title="BioMed Explorer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS GLOBAL ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f0f7f4;
    color: #1a3a2e;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #c8e6d8 !important;
}
[data-testid="stSidebar"] * {
    color: #1a3a2e !important;
}

/* Selectbox sidebar */
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stSelectbox > div > div > div {
    background-color: #f0f7f4 !important;
    color: #1a3a2e !important;
    border: 1px solid #a8d5bc !important;
    border-radius: 8px !important;
}

/* Text input sidebar */
[data-testid="stSidebar"] .stTextInput input {
    background-color: #f0f7f4 !important;
    color: #1a3a2e !important;
    border: 1px solid #a8d5bc !important;
    border-radius: 8px !important;
}

/* Number input field */
[data-testid="stSidebar"] .stNumberInput input {
    background-color: #f0f7f4 !important;
    color: #1a3a2e !important;
    border: 1px solid #a8d5bc !important;
    border-radius: 8px !important;
}

/* Boutons + et - du number input */
[data-testid="stSidebar"] .stNumberInput button,
[data-testid="stSidebar"] .stNumberInput button:hover,
[data-testid="stSidebar"] .stNumberInput button:focus,
[data-testid="stSidebar"] .stNumberInput button:active {
    background-color: #1a6b4a !important;
    background: #1a6b4a !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    box-shadow: none !important;
}

/* Dropdown options */
[data-testid="stSidebar"] [role="option"] {
    background-color: #ffffff !important;
    color: #1a3a2e !important;
}
[data-testid="stSidebar"] [role="option"]:hover {
    background-color: #e8f5ee !important;
}

/* ── TOUS LES BOUTONS ── */
button,
button:hover,
button:focus,
button:active,
.stButton > button,
.stButton > button:hover,
.stButton > button:focus,
.stButton > button:active,
.stDownloadButton > button,
.stDownloadButton > button:hover,
.stDownloadButton > button:focus,
.stDownloadButton > button:active,
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] .stButton > button:hover,
[data-testid="stSidebar"] .stButton > button:focus,
[data-testid="stSidebar"] .stButton > button:active,
button[kind="primary"],
button[kind="secondary"],
button[kind="tertiary"] {
    background-color: #1a6b4a !important;
    background: #1a6b4a !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    box-shadow: none !important;
}

button:hover,
.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #155a3c !important;
    background: #155a3c !important;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] > div,
[data-testid="stFileUploader"] section,
[data-testid="stFileUploaderDropzone"] {
    background-color: #e8f5ee !important;
    background: #e8f5ee !important;
    border-color: #a8d5bc !important;
    color: #1a3a2e !important;
}
[data-testid="stFileUploader"] * {
    color: #1a3a2e !important;
    background-color: transparent !important;
}
[data-testid="stFileUploaderDropzone"] {
    background-color: #e8f5ee !important;
    border: 1px dashed #a8d5bc !important;
    border-radius: 8px !important;
}
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploaderDropzone"] button:hover {
    background-color: #1a6b4a !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
}
.uploadedFile, [data-testid="stFileUploaderFile"] {
    background: #e8f5ee !important;
    border: 1px solid #a8d5bc !important;
    color: #1a3a2e !important;
    border-radius: 8px !important;
}

/* ── HERO ── */
.hero-header {
    background: linear-gradient(135deg, #1a6b4a 0%, #0e5a3c 60%, #0a4a30 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -40%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255,255,255,0.07) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    font-weight: 400;
    color: #ffffff;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.3px;
}
.hero-subtitle {
    font-size: 0.88rem;
    color: rgba(255,255,255,0.65);
    font-weight: 300;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3);
    color: #ffffff;
    font-size: 0.72rem;
    font-weight: 500;
    padding: 3px 10px;
    border-radius: 20px;
    margin-right: 6px;
}

/* ── METRIC CARDS ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.metric-card {
    background: #ffffff;
    border: 1px solid #c8e6d8;
    border-radius: 12px;
    padding: 1.3rem 1.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(26,107,74,0.06);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 12px 12px 0 0;
}
.metric-card.blue::before  { background: #2196b0; }
.metric-card.green::before { background: #1a6b4a; }
.metric-card.purple::before{ background: #7b5ea7; }
.metric-card.orange::before{ background: #d4813a; }

.metric-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: #5a8a72;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    font-weight: 400;
    color: #1a3a2e;
    line-height: 1;
}
.metric-sub {
    font-size: 0.75rem;
    color: #8ab59e;
    margin-top: 0.3rem;
}

/* ── SECTION TITLE ── */
.section-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    color: #5a8a72;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #c8e6d8;
}

/* ── TABS ── */
[data-testid="stTabs"] [role="tablist"] {
    background: #ffffff;
    border: 1px solid #c8e6d8;
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
}
[data-testid="stTabs"] [role="tab"] {
    background: transparent !important;
    color: #5a8a72 !important;
    border-radius: 7px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 6px 16px !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: #1a6b4a !important;
    color: #ffffff !important;
}

/* ── ALERTS & DATAFRAME ── */
.stAlert {
    background: #ffffff !important;
    border: 1px solid #c8e6d8 !important;
    border-radius: 10px !important;
    color: #1a3a2e !important;
}
[data-testid="stDataFrame"] {
    border: 1px solid #c8e6d8 !important;
    border-radius: 10px !important;
    overflow: hidden;
}

/* ── ARTICLE CARD ── */
.article-card {
    background: #ffffff;
    border: 1px solid #c8e6d8;
    border-left: 3px solid #1a6b4a;
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 1rem;
    box-shadow: 0 1px 4px rgba(26,107,74,0.06);
}
.article-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem;
    font-weight: 400;
    color: #1a3a2e;
    margin-bottom: 0.8rem;
    line-height: 1.5;
}
.article-meta {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 1rem;
}
.article-meta-item {
    font-size: 0.8rem;
    color: #5a8a72;
}
.article-meta-item span {
    color: #1a3a2e;
    font-weight: 500;
}
.article-abstract {
    font-size: 0.85rem;
    color: #4a7060;
    line-height: 1.8;
    border-top: 1px solid #c8e6d8;
    padding-top: 1rem;
    margin-top: 0.5rem;
}
.doi-link {
    display: inline-block;
    margin-top: 0.8rem;
    font-size: 0.78rem;
    color: #1a6b4a;
    text-decoration: none;
    border: 1px solid #a8d5bc;
    padding: 4px 12px;
    border-radius: 6px;
}
.tag {
    display: inline-block;
    background: #e8f5ee;
    border: 1px solid #a8d5bc;
    color: #1a6b4a;
    font-size: 0.72rem;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 500;
}

/* ── SIDEBAR MISC ── */
.sidebar-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem;
    font-weight: 400;
    color: #1a3a2e !important;
    margin-bottom: 1rem;
}
.status-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    margin-right: 6px;
    vertical-align: middle;
}
.status-dot.online  { background: #1a6b4a; }
.status-dot.offline { background: #c0392b; }
</style>
""", unsafe_allow_html=True)


# ─── DATA LOADING ─────────────────────────────────────────────

@st.cache_data(ttl=60)
def load_summary():
    try:
        r = requests.get(f"{API_BASE}/stats/summary", timeout=5)
        return r.json(), True
    except Exception:
        return {}, False

@st.cache_data(ttl=60)
def load_articles(domain=None, source=None, year=None, limit=200):
    params = {"limit": limit}
    if domain: params["domain"] = domain
    if source: params["source"] = source
    if year:   params["year"] = year
    try:
        r = requests.get(f"{API_BASE}/articles/", params=params, timeout=10)
        return pd.DataFrame(r.json())
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_stats_by_year():
    try:
        r = requests.get(f"{API_BASE}/stats/by-year", timeout=5)
        df = pd.DataFrame(r.json()).rename(columns={"_id": "Année", "count": "Articles"})
        return df.sort_values("Année")
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_stats_by_domain():
    try:
        r = requests.get(f"{API_BASE}/stats/by-domain", timeout=5)
        return pd.DataFrame(r.json()).rename(columns={"_id": "Domaine", "count": "Articles"})
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_stats_by_journal(top=8):
    try:
        r = requests.get(f"{API_BASE}/stats/by-journal", params={"top": top}, timeout=5)
        return pd.DataFrame(r.json()).rename(columns={"_id": "Journal", "count": "Articles"})
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_domains():
    try:
        r = requests.get(f"{API_BASE}/articles/domains", timeout=5)
        return r.json()
    except Exception:
        return []

def search_articles(query):
    try:
        r = requests.get(f"{API_BASE}/articles/search", params={"q": query}, timeout=5)
        return pd.DataFrame(r.json())
    except Exception:
        return pd.DataFrame()

def import_articles(data: list):
    try:
        r = requests.post(f"{API_BASE}/articles/import", json=data, timeout=30)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


# ─── PLOTLY THEME ─────────────────────────────────────────────
CHART_BG   = "rgba(0,0,0,0)"
GRID_COLOR = "#d4ead8"
TEXT_COLOR = "#5a8a72"

def apply_layout(fig, height=300):
    fig.update_layout(
        plot_bgcolor=CHART_BG,
        paper_bgcolor=CHART_BG,
        font=dict(family="DM Sans", color=TEXT_COLOR, size=11),
        height=height,
        margin=dict(t=10, b=30, l=10, r=10),
        xaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(color=TEXT_COLOR)),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(color=TEXT_COLOR)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT_COLOR)),
    )
    return fig


# ─── SIDEBAR ──────────────────────────────────────────────────

def render_sidebar(api_online):
    st.sidebar.markdown('<p class="sidebar-title">🧬 BioMed Explorer</p>', unsafe_allow_html=True)

    if api_online:
        st.sidebar.markdown('<p style="font-size:0.78rem; color:#1a6b4a;"><span class="status-dot online"></span>Backend connecté</p>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown('<p style="font-size:0.78rem; color:#c0392b;"><span class="status-dot offline"></span>Backend hors ligne</p>', unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Recherche**")
    search_query = st.sidebar.text_input("", placeholder="cancer, CRISPR, genome…", label_visibility="collapsed")

    st.sidebar.markdown("**Domaine**")
    domains = load_domains()
    selected_domain = st.sidebar.selectbox("", ["Tous"] + domains, label_visibility="collapsed")
    domain = None if selected_domain == "Tous" else selected_domain

    st.sidebar.markdown("**Année**")
    year_filter = st.sidebar.number_input("", min_value=0, max_value=2030, value=0, label_visibility="collapsed")
    year = int(year_filter) if year_filter > 0 else None

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Importer des articles**")
    st.sidebar.markdown("""
<div style="background:#e8f5ee; border:1px dashed #a8d5bc; border-radius:10px; padding:0.3rem 0.5rem; margin-bottom:0.5rem;">
<p style="font-size:0.72rem; color:#5a8a72; margin:0;">JSON ou CSV · titre, auteurs, DOI, domaine...</p>
</div>""", unsafe_allow_html=True)

    uploaded_file = st.sidebar.file_uploader("", type=["json", "csv"], label_visibility="collapsed")

    if uploaded_file is not None:
        if st.sidebar.button("Envoyer vers MongoDB", use_container_width=True):
            try:
                if uploaded_file.name.endswith(".json"):
                    import json as _json
                    data = _json.load(uploaded_file)
                    if isinstance(data, dict):
                        data = [data]
                else:
                    df_imp = pd.read_csv(uploaded_file)
                    data = df_imp.to_dict(orient="records")
                result = import_articles(data)
                if "error" in result:
                    st.sidebar.error(f"Erreur : {result['error']}")
                else:
                    st.sidebar.success(f"{result.get('inserted', 0)} article(s) importé(s)")
                    if result.get("skipped"):
                        st.sidebar.caption(f"{result['skipped']} doublon(s) ignoré(s)")
                    st.cache_data.clear()
            except Exception as e:
                st.sidebar.error(f"Erreur lecture fichier : {e}")

    st.sidebar.markdown("---")
    st.sidebar.markdown('<p style="font-size:0.72rem; color:#5a8a72;">Sources · PubMed · Semantic Scholar<br>USTHB · Module EIDM · 2026</p>', unsafe_allow_html=True)

    return search_query, domain, year


# ─── MAIN ─────────────────────────────────────────────────────

def main():
    summary, api_online = load_summary()
    search_query, domain, year = render_sidebar(api_online)

    # ── Hero ──
    yr = summary.get("year_range", {})
    period = f"{yr.get('min','?')} – {yr.get('max','?')}" if yr else "–"
    st.markdown(f"""
    <div class="hero-header">
        <p class="hero-title">Biomedical Corpus Explorer</p>
        <p class="hero-subtitle">
            <span class="hero-badge">PubMed</span>
            <span class="hero-badge">Semantic Scholar</span>
            <span class="hero-badge">FastAPI</span>
            &nbsp;·&nbsp; Période : {period}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Metric Cards ──
    total    = summary.get("total_articles", 0)
    domains  = summary.get("total_domains", 0)
    sources  = summary.get("total_sources", 0)
    journals = summary.get("total_journals", 0)

    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card blue">
            <div class="metric-label">Articles</div>
            <div class="metric-value">{total:,}</div>
            <div class="metric-sub">corpus total</div>
        </div>
        <div class="metric-card green">
            <div class="metric-label">Domaines</div>
            <div class="metric-value">{domains}</div>
            <div class="metric-sub">spécialités</div>
        </div>
        <div class="metric-card purple">
            <div class="metric-label">Sources</div>
            <div class="metric-value">{sources}</div>
            <div class="metric-sub">bases de données</div>
        </div>
        <div class="metric-card orange">
            <div class="metric-label">Journaux</div>
            <div class="metric-value">{journals}</div>
            <div class="metric-sub">publications</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not api_online:
        st.warning("⚠️ Backend non accessible. Lancez `python -m uvicorn main:app --reload` dans le dossier `backend/`.")
        return

    # ── Tabs ──
    tab1, tab2, tab3, tab4 = st.tabs(["📈  Par année", "🧬  Par domaine", "📊  Autres statistiques", "📄  Articles"])

    # ══ TAB 1 ══
    with tab1:
        st.markdown('<p class="section-title">Nombre d\'articles par année de publication</p>', unsafe_allow_html=True)
        df_year = load_stats_by_year()
        if not df_year.empty:
            fig = go.Figure(go.Bar(
                x=df_year["Année"], y=df_year["Articles"],
                marker=dict(
                    color=df_year["Articles"],
                    colorscale=[[0, "#c8e6d8"], [0.5, "#5ab888"], [1, "#1a6b4a"]],
                    line=dict(width=0),
                ),
                text=df_year["Articles"],
                textposition="outside",
                textfont=dict(size=10, color=TEXT_COLOR),
                hovertemplate="<b>%{x}</b><br>%{y} articles<extra></extra>",
            ))
            fig = apply_layout(fig, height=420)
            fig.update_xaxes(title_text="Année", title_font=dict(color=TEXT_COLOR))
            fig.update_yaxes(title_text="Nombre d'articles", title_font=dict(color=TEXT_COLOR))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            st.markdown('<p class="section-title" style="margin-top:1.5rem;">Tableau récapitulatif</p>', unsafe_allow_html=True)
            total_sum = df_year["Articles"].sum()
            df_display = df_year.copy()
            df_display["% du corpus"] = (df_display["Articles"] / total_sum * 100).round(1).astype(str) + "%"
            st.dataframe(df_display, use_container_width=True, hide_index=True, height=250)
        else:
            st.info("Données non disponibles — vérifiez que le backend est lancé.")

    # ══ TAB 2 ══
    with tab2:
        st.markdown('<p class="section-title">Répartition du corpus par domaine spécialisé</p>', unsafe_allow_html=True)
        df_domain = load_stats_by_domain()
        if not df_domain.empty:
            colors = ["#1a6b4a","#2196b0","#7b5ea7","#d4813a","#c0392b","#16a085","#8e6b3e","#2980b9"]

            col_pie, col_bar = st.columns(2, gap="medium")
            with col_pie:
                fig2 = go.Figure(go.Pie(
                    labels=df_domain["Domaine"],
                    values=df_domain["Articles"],
                    hole=0.52,
                    marker=dict(colors=colors, line=dict(color="#ffffff", width=2)),
                    textfont=dict(color="#1a3a2e", size=11),
                    hovertemplate="<b>%{label}</b><br>%{value} articles (%{percent})<extra></extra>",
                ))
                fig2.update_layout(
                    plot_bgcolor=CHART_BG, paper_bgcolor=CHART_BG,
                    height=360, margin=dict(t=10, b=10, l=10, r=10),
                    legend=dict(font=dict(color=TEXT_COLOR, size=10), bgcolor="rgba(0,0,0,0)"),
                    annotations=[dict(
                        text=f"<b>{df_domain['Articles'].sum():,}</b><br><span style='font-size:10px'>articles</span>",
                        x=0.5, y=0.5, font=dict(size=16, color="#1a3a2e", family="DM Serif Display"), showarrow=False
                    )]
                )
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

            with col_bar:
                fig_bar = go.Figure(go.Bar(
                    x=df_domain["Articles"],
                    y=df_domain["Domaine"],
                    orientation="h",
                    marker=dict(color=colors[:len(df_domain)], line=dict(width=0), opacity=0.85),
                    text=df_domain["Articles"],
                    textposition="outside",
                    textfont=dict(size=10, color=TEXT_COLOR),
                    hovertemplate="<b>%{y}</b><br>%{x} articles<extra></extra>",
                ))
                fig_bar = apply_layout(fig_bar, height=360)
                fig_bar.update_layout(yaxis=dict(autorange="reversed"))
                st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

            st.markdown('<p class="section-title" style="margin-top:1.5rem;">Détail par domaine</p>', unsafe_allow_html=True)
            total_sum = df_domain["Articles"].sum()
            df_domain_display = df_domain.copy()
            df_domain_display["% du corpus"] = (df_domain_display["Articles"] / total_sum * 100).round(1).astype(str) + "%"
            st.dataframe(df_domain_display, use_container_width=True, hide_index=True)
        else:
            st.info("Données non disponibles.")

    # ══ TAB 3 ══
    with tab3:
        col_src, col_jour = st.columns(2, gap="medium")

        with col_src:
            st.markdown('<p class="section-title">Répartition par source</p>', unsafe_allow_html=True)
            try:
                r_src = requests.get(f"{API_BASE}/stats/by-source", timeout=5)
                df_src = pd.DataFrame(r_src.json()).rename(columns={"_id": "Source", "count": "Articles"})
                if not df_src.empty:
                    src_colors = ["#1a6b4a", "#2196b0", "#7b5ea7", "#d4813a"]
                    fig_src = go.Figure(go.Pie(
                        labels=df_src["Source"], values=df_src["Articles"],
                        hole=0.5,
                        marker=dict(colors=src_colors, line=dict(color="#ffffff", width=2)),
                        textfont=dict(color="#1a3a2e", size=12),
                        hovertemplate="<b>%{label}</b><br>%{value} articles (%{percent})<extra></extra>",
                    ))
                    fig_src.update_layout(
                        plot_bgcolor=CHART_BG, paper_bgcolor=CHART_BG,
                        height=280, margin=dict(t=10, b=10, l=10, r=10),
                        legend=dict(font=dict(color=TEXT_COLOR, size=11), bgcolor="rgba(0,0,0,0)"),
                    )
                    st.plotly_chart(fig_src, use_container_width=True, config={"displayModeBar": False})
            except Exception:
                st.info("Données source non disponibles.")

        with col_jour:
            st.markdown('<p class="section-title">Top 8 journaux</p>', unsafe_allow_html=True)
            df_journal = load_stats_by_journal(top=8)
            if not df_journal.empty:
                fig3 = go.Figure(go.Bar(
                    x=df_journal["Articles"],
                    y=df_journal["Journal"],
                    orientation="h",
                    marker=dict(
                        color=df_journal["Articles"],
                        colorscale=[[0, "#c8e6d8"], [0.5, "#5ab888"], [1, "#1a6b4a"]],
                        line=dict(width=0),
                    ),
                    text=df_journal["Articles"],
                    textposition="outside",
                    textfont=dict(size=10, color=TEXT_COLOR),
                    hovertemplate="<b>%{y}</b><br>%{x} articles<extra></extra>",
                ))
                fig3 = apply_layout(fig3, height=280)
                fig3.update_layout(yaxis=dict(autorange="reversed", gridcolor=GRID_COLOR))
                st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<p class="section-title" style="margin-top:1.5rem;">Évolution cumulative du corpus</p>', unsafe_allow_html=True)
        df_year2 = load_stats_by_year()
        if not df_year2.empty:
            df_year2["Cumulé"] = df_year2["Articles"].cumsum()
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=df_year2["Année"], y=df_year2["Cumulé"],
                mode="lines+markers",
                line=dict(color="#1a6b4a", width=2.5),
                marker=dict(size=6, color="#1a6b4a"),
                fill="tozeroy",
                fillcolor="rgba(26,107,74,0.08)",
                hovertemplate="<b>%{x}</b><br>%{y} articles cumulés<extra></extra>",
            ))
            fig_line = apply_layout(fig_line, height=250)
            fig_line.update_xaxes(title_text="Année", title_font=dict(color=TEXT_COLOR))
            fig_line.update_yaxes(title_text="Total cumulé", title_font=dict(color=TEXT_COLOR))
            st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})

    # ══ TAB 4 ══
    with tab4:
        df = load_articles(domain=domain, year=year, limit=200)

        if df.empty:
            st.warning("Aucun article trouvé pour ces filtres.")
        else:
            cols_display = [c for c in ["title", "authors", "journal", "domain", "year"] if c in df.columns]
            display_df = df[cols_display].copy()
            display_df.columns = [c.capitalize() for c in cols_display]

            header_cols = st.columns([3, 1])
            with header_cols[0]:
                st.markdown(f'<p class="section-title">{len(df)} articles trouvés</p>', unsafe_allow_html=True)
            with header_cols[1]:
                st.download_button("⬇️ Exporter CSV", df.to_csv(index=False), "articles.csv", "text/csv")

            event = st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
                height=340,
            )

            selected_rows = event.selection.rows if event.selection else []
            if selected_rows:
                article = df.iloc[selected_rows[0]]
                doi = article.get("doi", "")
                domain_val = article.get("domain", "–")
                abstract = article.get("abstract", "")
                doi_link = f'<a href="https://doi.org/{doi}" class="doi-link" target="_blank">📖 Ouvrir via DOI ↗</a>' if doi else ""

                st.markdown(f"""
                <div class="article-card">
                    <div class="article-title">{article.get('title', '–')}</div>
                    <div class="article-meta">
                        <div class="article-meta-item">📰 Journal · <span>{article.get('journal', '–')}</span></div>
                        <div class="article-meta-item">📅 Année · <span>{article.get('year', '–')}</span></div>
                        <div class="article-meta-item">🏷️ <span class="tag">{domain_val}</span></div>
                    </div>
                    <div class="article-meta-item" style="margin-bottom:0.5rem;">👥 Auteurs · <span style="color:#1a3a2e">{article.get('authors', '–')}</span></div>
                    {"<div class='article-abstract'>" + abstract + "</div>" if abstract else ""}
                    {doi_link}
                </div>
                """, unsafe_allow_html=True)

    # ── Recherche ──
    if search_query and len(search_query) >= 2:
        st.markdown("---")
        st.markdown(f'<p class="section-title">🔍 Résultats pour « {search_query} »</p>', unsafe_allow_html=True)
        df_search = search_articles(search_query)
        if df_search.empty:
            st.info(f"Aucun résultat pour « {search_query} »")
        else:
            st.markdown(f'<p style="font-size:0.82rem; color:#5a8a72; margin-bottom:0.8rem;">{len(df_search)} résultat(s) trouvé(s)</p>', unsafe_allow_html=True)
            cols_s = [c for c in ["title", "authors", "journal", "domain", "year"] if c in df_search.columns]
            st.dataframe(df_search[cols_s], use_container_width=True, hide_index=True, height=380)


if __name__ == "__main__":
    main()