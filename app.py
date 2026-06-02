import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AquaChem IKA Pro",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS — TEMA: MICRO-ATOMIC BIO-CHEMISTRY
# ─────────────────────────────────────────────
# Menggunakan palet neon kuantum (deep indigo/teal) dengan aksen bio-partikel, elektron, kation/anion
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg:      #0b0f19;
    --surface: #141b2d;
    --card:    #1f293d;
    --border:  #2d3d5a;
    --emerald: #00f5a0;
    --emerald2:#00d184;
    --teal:    #00d2ff;
    --amber:   #ffb300;
    --red:     #ff4a4a;
    --text:    #e2e8f0;
    --muted:   #94a3b8;
    --light:   #1e293b;
    --good:    #00f5a0;
    --warn:    #ffb300;
    --bad:     #ff4a4a;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}

#MainMenu, footer, header {visibility: hidden;}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 2px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }
section[data-testid="stSidebar"] .stMarkdown p { color: var(--muted) !important; }

/* ── Hero Banner ── */
.hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #115e59 100%);
    border-radius: 20px;
    padding: 44px 40px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    border: 1px solid rgba(0, 245, 160, 0.2);
}
/* Efek Ornamen Sains (Elektron Orbit & Partikel Bakteri) */
.hero::before {
    content: "⚡ e⁻ [OH]⁻ [H]⁺ 🦠";
    position: absolute;
    top: 15px; right: 20px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.2rem;
    color: rgba(0, 245, 160, 0.25);
    letter-spacing: 5px;
}
.hero::after {
    content: "✨ [Ca]²⁺ [SO₄]²⁻ 🔬";
    position: absolute;
    bottom: 15px; left: 20px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1rem;
    color: rgba(0, 210, 255, 0.2);
    letter-spacing: 4px;
}
.hero-badge {
    display: inline-block;
    background: rgba(0, 245, 160, 0.1);
    border: 1px solid rgba(0, 245, 160, 0.3);
    color: #00f5a0;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.72rem;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 1.5px;
    margin-bottom: 14px;
    text-transform: uppercase;
}
.hero-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2.5rem;
    font-weight: 600;
    color: #FFFFFF;
    margin: 0 0 10px 0;
    line-height: 1.2;
}
.hero-title span { color: #00d2ff; }
.hero-sub {
    color: var(--muted);
    font-size: 1rem;
    margin: 0;
    font-weight: 400;
}

/* ── Param Cards ── */
.param-card {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: 16px;
    padding: 26px 22px;
    height: 100%;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    transition: all 0.2s ease;
}
.param-card:hover {
    border-color: var(--emerald);
    box-shadow: 0 8px 30px rgba(0, 245, 160, 0.15);
    transform: translateY(-2px);
}
.param-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.9rem;
    color: var(--emerald);
    margin-bottom: 4px;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.param-fullname { color: var(--muted); font-size: 0.78rem; margin-bottom: 16px; }
.param-value {
    font-size: 2.5rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1;
    margin-bottom: 4px;
    font-family: 'IBM Plex Mono', monospace;
}
.param-unit { font-size: 0.8rem; color: var(--muted); margin-bottom: 14px; }

/* ── Status Chips ── */
.status-chip {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.3px;
}
.status-good { background: rgba(0, 245, 160, 0.15); color: #00f5a0; border: 1.5px solid #00f5a0; }
.status-warn { background: rgba(255, 179, 0, 0.15); color: #ffb300; border: 1.5px solid #ffb300; }
.status-bad  { background: rgba(255, 74, 74, 0.15); color: #ff4a4a; border: 1.5px solid #ff4a4a; }

/* ── Section Header ── */
.sec-head {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 2.5px;
    color: var(--teal);
    text-transform: uppercase;
    margin: 36px 0 18px 0;
    display: flex;
    align-items: center;
    gap: 12px;
}
.sec-head::after {
    content: "";
    flex: 1;
    height: 1.5px;
    background: var(--border);
}

/* ── Info Boxes ── */
.info-box {
    background: rgba(0, 245, 160, 0.05);
    border: 1px solid rgba(0, 245, 160, 0.2);
    border-left: 4px solid var(--emerald);
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: #e2e8f0;
    margin: 10px 0;
}
.warn-box {
    background: rgba(255, 179, 0, 0.05);
    border: 1px solid rgba(255, 179, 0, 0.2);
    border-left: 4px solid var(--amber);
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: #e2e8f0;
    margin: 10px 0;
}
.bad-box {
    background: rgba(255, 74, 74, 0.05);
    border: 1px solid rgba(255, 74, 74, 0.2);
    border-left: 4px solid var(--red);
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: #e2e8f0;
    margin: 10px 0;
}

/* ── Reference Table ── */
.ref-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; background: var(--card); border-radius: 8px; overflow: hidden; }
.ref-table th {
    background: var(--surface);
    color: var(--teal);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    padding: 12px 16px;
    text-align: left;
    border-bottom: 2px solid var(--border);
    text-transform: uppercase;
}
.ref-table td { padding: 11px 16px; border-bottom: 1px solid var(--border); color: var(--text); }
.ref-table tr:hover td { background: rgba(255,255,255,0.02); }

/* ── About Card ── */
.about-card {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: 16px;
    padding: 28px 26px;
    margin-bottom: 18px;
}
.about-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 2px;
    color: var(--emerald);
    text-transform: uppercase;
    margin-bottom: 8px;
}
.about-title { font-size: 1.2rem; font-weight: 700; color: #ffffff; margin-bottom: 10px; }
.about-body  { color: var(--muted); font-size: 0.9rem; line-height: 1.75; }

/* ── Streamlit Overrides ── */
.stButton > button {
    background: linear-gradient(135deg, #00f5a0, #00d2ff);
    color: #0f172a !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 700 !important;
    padding: 10px 24px !important;
    width: 100%;
    box-shadow: 0 4px 14px rgba(0, 245, 160, 0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(0, 245, 160, 0.4) !important;
}

div[data-testid="stExpander"] {
    background: var(--card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface);
    border-radius: 12px;
    padding: 5px;
    border: 1.5px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    color: var(--muted) !important;
    font-size: 0.85rem;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: rgba(0, 210, 255, 0.15) !important;
    color: #00d2ff !important;
}

/* Base Dataframe override for Dark mode */
div[data-testid="stDataFrame"] { background-color: var(--card) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "app_name" not in st.session_state:
    st.session_state.app_name = "AquaChem IKA Pro"
if "group_name" not in st.session_state:
    st.session_state.group_name = "Anggota Kelompok 4"
if "group_desc" not in st.session_state:
    st.session_state.group_desc = (
        "Aqiila Rahmania Mumtaza (2560577)\n"
        "Gevan Eirano Yusuf (2560635)\n"
        "Magali Wahyudi (2560663)\n"
        "Naufa Afifah (2560715)\n"
        "Siti Halimah Tusysyadiyah Tsany (2560785)"
    )
if "web_desc" not in st.session_state:
    st.session_state.web_desc = (
        "Aplikasi analisis kimia air kuantum untuk melacak indeks kualitas air, "
        "keseimbangan anion-kation (aktivitas elektron bebas), serta beban organik mikrobial (bakteri) via pH, BOD, dan COD."
    )
# Inisialisasi Database Penyimpanan Berulang
if "sample_history" not in st.session_state:
    st.session_state.sample_history = []

# ─────────────────────────────────────────────
#  REFERENCE DATA
# ─────────────────────────────────────────────
PH_REF = [
    {"Kategori": "Sangat Asam / Basa (Beban Ion Berbahaya)", "Rentang": "< 5.0 atau > 9.0", "Status": "Tercemar Berat", "Kelas": "bad"},
    {"Kategori": "Asam / Basa Ringan (Ketidakseimbangan Anion/Kation)", "Rentang": "5.0-6.0 atau 8.5-9.0", "Status": "Tercemar Sedang", "Kelas": "warn"},
    {"Kategori": "Mendekati Baku Mutu", "Rentang": "6.0-6.5 atau 8.0-8.5", "Status": "Tercemar Ringan", "Kelas": "warn"},
    {"Kategori": "Normal / Keseimbangan Proton Ideal", "Rentang": "6.5 - 8.0", "Status": "Memenuhi Baku Mutu", "Kelas": "good"},
]
BOD_REF = [
    {"Kategori": "Sangat Baik (Aktivitas Bakteri Rendah)", "Rentang": "< 2 mg/L", "Status": "Tidak Tercemar", "Kelas": "good"},
    {"Kategori": "Baik (Aman Konsumsi)", "Rentang": "2 - 3 mg/L", "Status": "Memenuhi Baku Mutu", "Kelas": "good"},
    {"Kategori": "Tercemar Sedang (Koloni Bakteri Meningkat)", "Rentang": "3 - 6 mg/L", "Status": "Tercemar Sedang", "Kelas": "warn"},
    {"Kategori": "Tercemar Berat (Dekomposisi Masif)", "Rentang": "6 - 12 mg/L", "Status": "Tercemar Berat", "Kelas": "bad"},
    {"Kategori": "Sangat Tercemar (Anoksik / Bakteri Membludak)", "Rentang": "> 12 mg/L", "Status": "Sangat Tercemar", "Kelas": "bad"},
]
COD_REF = [
    {"Kategori": "Sangat Baik (Bebas Reduktor Kimia)", "Rentang": "< 10 mg/L", "Status": "Tidak Tercemar", "Kelas": "good"},
    {"Kategori": "Baik (Oksidasi Elektron Stabil)", "Rentang": "10 - 25 mg/L", "Status": "Memenuhi Baku Mutu", "Kelas": "good"},
    {"Kategori": "Tercemar Ringan-Sedang", "Rentang": "25 - 50 mg/L", "Status": "Tercemar Sedang", "Kelas": "warn"},
    {"Kategori": "Tercemar Berat (Polutan Kimiawi Tinggi)", "Rentang": "50 - 100 mg/L", "Status": "Tercemar Berat", "Kelas": "bad"},
    {"Kategori": "Sangat Tercemar (Redoks Kritis)", "Rentang": "> 100 mg/L", "Status": "Sangat Tercemar", "Kelas": "bad"},
]

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────
def get_ph_status(v):
    if 6.5 <= v <= 8.0:   return "Memenuhi Baku Mutu", "good", 100
    elif (6.0 <= v < 6.5) or (8.0 < v <= 8.5): return "Tercemar Ringan", "warn", 60
    elif (5.0 <= v < 6.0) or (8.5 < v <= 9.0): return "Tercemar Sedang", "warn", 35
    else: return "Tercemar Berat", "bad", 10

def get_bod_status(v):
    if v < 2:    return "Tidak Tercemar",      "good", 100
    elif v <= 3: return "Memenuhi Baku Mutu",  "good", 85
    elif v <= 6: return "Tercemar Sedang",     "warn", 50
    elif v <= 12:return "Tercemar Berat",      "bad",  25
    else:        return "Sangat Tercemar Berat","bad",  5

def get_cod_status(v):
    if v < 10:    return "Tidak Tercemar",      "good", 100
    elif v <= 25: return "Memenuhi Baku Mutu",  "good", 80
    elif v <= 50: return "Tercemar Sedang",     "warn", 45
    elif v <= 100:return "Tercemar Berat",      "bad",  20
    else:         return "Sangat Tercemar Berat","bad",  5

def calc_ika(ph_val, bod_val, cod_val):
    _, _, ph_score  = get_ph_status(ph_val)
    _, _, bod_score = get_bod_status(bod_val)
    _, _, cod_score = get_cod_status(cod_val)
    ika = 0.30 * ph_score + 0.35 * bod_score + 0.35 * cod_score
    return round(ika, 1), ph_score, bod_score, cod_score

def ika_category(score):
    if score >= 80:   return "Baik (Lestari)", "#00f5a0"
    elif score >= 50: return "Tercemar Ringan-Sedang", "#ffb300"
    elif score >= 25: return "Tercemar Berat", "#ff4a4a"
    else:             return "Sangat Tercemar Berat", "#991B1B"

def status_chip(label, cls):
    return f'<span class="status-chip status-{cls}">{label}</span>'

def render_ref_table(data):
    rows = ""
    for r in data:
        chip = status_chip(r["Status"], r["Kelas"])
        rows += f"<tr><td>{r['Kategori']}</td><td>{r['Rentang']}</td><td>{chip}</td></tr>"
    st.markdown(f"""
    <table class="ref-table">
      <thead><tr><th>Entitas Kimia / Bio</th><th>Rentang Nilai</th><th>Status Kuantum</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:18px 0 8px 0;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:1.2rem; font-weight:700; color:#00f5a0;">
            ⚛️ AquaChem IKA Pro
        </div>
        <div style="color:#94a3b8; font-size:0.78rem; margin-top:4px;">
            Atoms, Microbes & Water Quality Index
        </div>
    </div>
    <hr style="border:none; border-top:1.5px solid #2d3d5a; margin:12px 0 20px 0;">
    """, unsafe_allow_html=True)

    st.markdown("### 📥 1. Entry Data Spektroskopi / Titrasi")
    sample_id = st.text_input("Kode/Nama Sampel Air", value=f"SAMPEL-{len(st.session_state.sample_history)+1:03d}")
    
    input_mode = st.radio("Metode Analisis Lab", ["Langsung (Nilai)", "Dari Titrasi"], horizontal=True)

    # Indikator Aktivitas Ion [H]+ dan [OH]-
    ph_val = st.number_input("Derajat Keasaman (pH)", min_value=0.0, max_value=14.0, value=7.0, step=0.1,
                             help="Mengukur konsentrasi aktivitas elektron & ion Hidrogen.")

    if input_mode == "Langsung (Nilai)":
        bod_val = st.number_input("BOD (mg/L)", min_value=0.0, max_value=200.0, value=2.0, step=0.1,
                                  help="Konsumsi Oksigen oleh Mikroba/Bakteri dekomposer.")
        cod_val = st.number_input("COD (mg/L)", min_value=0.0, max_value=500.0, value=15.0, step=0.1,
                                  help="Kebutuhan oksidasi kimia terhadap senyawa reduktor & ion polutan.")
    else:
        st.markdown("""<div style="font-size:0.8rem; color:#00f5a0; font-family:'IBM Plex Mono',monospace;
                       margin:10px 0 4px 0; font-weight:600;">🦠 BOD — Respirasi Bakteri (Winkler)</div>""", unsafe_allow_html=True)
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            bod_v_blanko   = st.number_input("V Blanko (mL)",  min_value=0.0, value=10.0,  step=0.01, key="bod_vb")
            bod_v_sampel_t = st.number_input("V Sampel (mL)",  min_value=0.0, value=8.5,   step=0.01, key="bod_vs")
        with col_b2:
            bod_n        = st.number_input("Normalitas Na2S2O3",  min_value=0.0, value=0.025, step=0.001, format="%.4f", key="bod_n")
            bod_v_sampel = st.number_input("V Air Sampel (mL)", min_value=0.1, value=100.0, step=1.0,   key="bod_ml")
        bod_val = round((bod_v_blanko - bod_v_sampel_t) * bod_n * 8000 / bod_v_sampel, 3) if bod_v_sampel > 0 else 0.0

        st.markdown("""<div style="font-size:0.8rem; color:#00d2ff; font-family:'IBM Plex Mono',monospace;
                       margin:4px 0 4px 0; font-weight:600;">⚡ COD — Redoks Kation-Anion (FAS)</div>""", unsafe_allow_html=True)
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            cod_v_blanko   = st.number_input("V Blanko (mL)",  min_value=0.0, value=15.0, step=0.01, key="cod_vb")
            cod_v_sampel_t = st.number_input("V Sampel (mL)",  min_value=0.0, value=12.0, step=0.01, key="cod_vs")
        with col_c2:
            cod_n        = st.number_input("Normalitas FAS", min_value=0.0, value=0.1,  step=0.001, format="%.4f", key="cod_n")
            cod_v_sampel = st.number_input("V Air Sampel (mL)",  min_value=0.1, value=20.0, step=1.0,   key="cod_ml")
        cod_val = round((cod_v_blanko - cod_v_sampel_t) * cod_n * 8000 / cod_v_sampel, 3) if cod_v_sampel > 0 else 0.0

    # ─────────────────────────────────────────────
    #  LOGIKA INPUT BERULANG (SIMPAN DATA)
    # ─────────────────────────────────────────────
    st.markdown("### 🗄️ 2. Penyimpanan Kuantum")
    current_ika, p_s, b_s, c_s = calc_ika(ph_val, bod_val, cod_val)
    current_cat, _ = ika_category(current_ika)
    
    if st.button("🧬 SIMPAN KE DATABASE HISTORIS"):
        st.session_state.sample_history.append({
            "ID Sampel": sample_id,
            "pH": ph_val,
            "BOD (mg/L)": bod_val,
            "COD (mg/L)": cod_val,
            "Skor IKA": current_ika,
            "Kategori": current_cat
        })
        st.success(f"Sukses mengabadikan data {sample_id}!")

    if st.session_state.sample_history:
        if st.button("🗑️ Reset Riwayat Tabel"):
            st.session_state.sample_history = []
            st.rerun()

    st.markdown("<hr style='border:none;border-top:1.5px solid #2d3d5a;margin:20px 0;'>", unsafe_allow_html=True)

    with st.expander("⚙️ Konfigurasi Inti"):
        new_app   = st.text_input("Nama Sistem",      value=st.session_state.app_name)
        new_grp   = st.text_input("Konsorsium Pengembang", value=st.session_state.group_name)
        new_gdesc = st.text_area("Manifestasi Tim",  value=st.session_state.group_desc, height=80)
        new_wdesc = st.text_area("Deskripsi Operasional",   value=st.session_state.web_desc,   height=100)
        if st.button("APPLY SIMULASI"):
            st.session_state.app_name  = new_app
            st.session_state.group_name = new_grp
            st.session_state.group_desc = new_gdesc
            st.session_state.web_desc   = new_wdesc
            st.success("Modifikasi matriks berhasil!")

# ─────────────────────────────────────────────
#  LOGIKA PERHITUNGAN UTAMA (DATA AKTIF)
# ─────────────────────────────────────────────
ika_score, ph_si, bod_si, cod_si = calc_ika(ph_val, bod_val, cod_val)
ika_cat, ika_color = ika_category(ika_score)
ph_label,  ph_cls,  _ = get_ph_status(ph_val)
bod_label, bod_cls, _ = get_bod_status(bod_val)
cod_label, cod_cls, _ = get_cod_status(cod_val)

# ─────────────────────────────────────────────
#  MAIN CONTENT — TABS VIA NEON DESIGN
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-badge">Bio-Chemical Redoks Matrix v3.0</div>
    <div class="hero-title">{st.session_state.app_name}</div>
    <div class="hero-sub">{st.session_state.web_desc}</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Live Analytics Dashboard", "🗃️ Database Multi-Sampel", "🔬 Regulasi Baku Mutu", "🧬 Tim Riset"])

# ══════════════════════ TAB 1 — DASHBOARD ══════════════════════
with tab1:
    st.markdown(f"##### 📍 Hasil Analisis Sampel Aktif: `{sample_id}`")
    c_ika, c_ph, c_bod, c_cod = st.columns([1.4, 1, 1, 1])

    with c_ika:
        st.markdown(f"""
        <div class="param-card" style="border-color:{ika_color}; background:linear-gradient(135deg, #1f293d, #11222e);">
            <div class="param-title">TOTAL WATER QUALITY INDEX</div>
            <div class="param-fullname">Skor Integrasi Redoks & Bakteri</div>
            <div class="param-value" style="color:{ika_color};">{ika_score}</div>
            <div class="param-unit">Skala Kuantum / 100</div>
            <span class="status-chip status-{'good' if ika_score>=80 else 'warn' if ika_score>=50 else 'bad'}">{ika_cat}</span>
        </div>
        """, unsafe_allow_html=True)

    for label, fullname, val, unit, lbl, cls in [
        ("pH (Ion H⁺)",  "Aktivitas Proton Elektron", ph_val,  "⚡ Log Konsetrasi",  ph_label,  ph_cls),
        ("BOD (Mikroba)", "Dekomposisi Koloni Bakteri", bod_val, "🦠 mg O₂/L", bod_label, bod_cls),
        ("COD (Anion/Kation)", "Oksidasi Kimia Polutan",    cod_val, "🧪 mg O₂/L", cod_label, cod_cls),
    ]:
        col = c_ph if "pH" in label else c_bod if "BOD" in label else c_cod
        with col:
            st.markdown(f"""
            <div class="param-card">
                <div class="param-title">{label}</div>
                <div class="param-fullname">{fullname}</div>
                <div class="param-value">{val:.2f}</div>
                <div class="param-unit">{unit}</div>
                {status_chip(lbl, cls)}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Gauge charts (Dark Mode Styling)
    st.markdown('<div class="sec-head">POTENSIAL SUB-INDEKS ENERGI</div>', unsafe_allow_html=True)

    def make_gauge(title, value, color):
        c = {"good": "#00f5a0", "warn": "#ffb300", "bad": "#ff4a4a"}[color]
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            number={"font": {"size": 36, "family": "IBM Plex Mono", "color": "#ffffff"}, "suffix": "%"},
            title={"text": title, "font": {"size": 13, "family": "Inter", "color": "#94a3b8"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#2d3d5a", "tickfont": {"size": 10, "color": "#94a3b8"}},
                "bar": {"color": c, "thickness": 0.28},
                "bgcolor": "#141b2d",
                "borderwidth": 1,
                "bordercolor": "#2d3d5a",
                "steps": [
                    {"range": [0, 25],  "color": "rgba(255, 74, 74, 0.1)"},
                    {"range": [25, 50], "color": "rgba(255, 179, 0, 0.1)"},
                    {"range": [50, 80], "color": "rgba(0, 210, 255, 0.1)"},
                    {"range": [80, 100],"color": "rgba(0, 245, 160, 0.1)"},
                ],
            }
        ))
        fig.update_layout(
            height=200, margin=dict(t=40, b=10, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0",
        )
        return fig

    g1, g2, g3 = st.columns(3)
    with g1: st.plotly_chart(make_gauge("Keseimbangan Proton [pH]",  ph_si,  ph_cls),  use_container_width=True)
    with g2: st.plotly_chart(make_gauge("Respirasi Bio-Massa [BOD]", bod_si, bod_cls), use_container_width=True)
    with g3: st.plotly_chart(make_gauge("Redoks Elektron Polutan [COD]", cod_si, cod_cls), use_container_width=True)

    # Radar + Bar
    st.markdown('<div class="sec-head">VEKTOR AFINITAS AIR</div>', unsafe_allow_html=True)
    left, right = st.columns(2)

    with left:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[ph_si, bod_si, cod_si, ph_si],
            theta=["Ion Hidrogen (pH)", "Respirasi Bakteri (BOD)", "Stabilitas Redoks (COD)", "Ion Hidrogen (pH)"],
            fill="toself",
            fillcolor="rgba(0, 245, 160, 0.1)",
            line=dict(color="#00f5a0", width=2.5),
            name="Kondisi Aktual Sampel"
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[100, 100, 100, 100],
            theta=["Ion Hidrogen (pH)", "Respirasi Bakteri (BOD)", "Stabilitas Redoks (COD)", "Ion Hidrogen (pH)"],
            fill="none",
            line=dict(color="#00d2ff", width=1.5, dash="dot"),
            name="Ambang Ideal Murni"
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor="#141b2d",
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="#2d3d5a", tickfont=dict(color="#94a3b8")),
                angularaxis=dict(gridcolor="#2d3d5a", tickfont=dict(color="#e2e8f0", family="IBM Plex Mono")),
            ),
            showlegend=True,
            legend=dict(font=dict(color="#94a3b8"), bgcolor="rgba(0,0,0,0)"),
            height=300, margin=dict(t=30, b=30, l=40, r=40),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with right:
        bar_colors = {"good": "#00f5a0", "warn": "#ffb300", "bad": "#ff4a4a"}
        fig_bar = go.Figure()
        params_bar = [("pH Ion", ph_val, ph_cls), ("BOD Bakteri", bod_val, bod_cls), ("COD Kation", cod_val, cod_cls)]
        bm_vals    = [7.25, 3, 25]
        
        for (pname, pval, pcls), bmv in zip(params_bar, bm_vals):
            fig_bar.add_trace(go.Bar(
                name=pname, x=[pname], y=[pval],
                marker_color=bar_colors[pcls], opacity=0.85,
            ))
            fig_bar.add_trace(go.Scatter(
                x=[pname], y=[bmv], mode="markers",
                marker=dict(symbol="line-ew", size=24, color="#00d2ff", line=dict(width=3, color="#00d2ff")),
                name="Baku Mutu", showlegend=False
            ))
        fig_bar.update_layout(
            height=300, margin=dict(t=30, b=30, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#141b2d",
            xaxis=dict(gridcolor="#2d3d5a", tickfont=dict(color="#e2e8f0", family="IBM Plex Mono")),
            yaxis=dict(gridcolor="#2d3d5a", tickfont=dict(color="#94a3b8")),
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Status boxes
    box_map = {"good": "info-box", "warn": "warn-box", "bad": "bad-box"}
    st.markdown(f"""
    <div class="{box_map[ph_cls]}">
        ⚡ <b>Keseimbangan [H⁺] / [OH⁻] (pH {ph_val:.1f})</b> — {ph_label}.
        Rentang normal fisis air berada pada pH 6.5–8.0. Tingkat keasaman yang radikal mengganggu afinitas transfer elektron substansi terlarut.
    </div>
    <div class="{box_map[bod_cls]}">
        🦠 <b>Metabolisme Bakteri Organik (BOD {bod_val:.2f} mg/L)</b> — {bod_label}.
        Baku Mutu Kelas II menetapkan batas kritis &lt;3 mg/L. Kenaikan nilai ini menandakan populasi mikroba dekomposer membludak akibat akumulasi nutrien karbonaseus.
    </div>
    <div class="{box_map[cod_cls]}">
        🧪 <b>Daya Oksidasi Kimia Anion-Kation (COD {cod_val:.2f} mg/L)</b> — {cod_label}.
        Ambang batas standard &lt;25 mg/L. Ketidaksesuaian nilai merefleksikan tingginya reduktor polutan non-biodegradable serta interaksi redoks eksternal yang toksik.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════ TAB 2 — DATABASE MULTI-SAMPEL (INPUT BERULANG) ══════════════════════
with tab2:
    st.markdown('<div class="sec-head">🗄️ REPOSITORI HISTORIS KUANTUM (REPEATED INPUTS)</div>', unsafe_allow_html=True)
    st.write("Daftar sampel air yang telah Anda rekam berulang kali melalui panel input kiri:")
    
    if st.session_state.sample_history:
        df_history = pd.DataFrame(st.session_state.sample_history)
        
        # Tampilkan tabel interaktif
        st.dataframe(df_history, use_container_width=True, hide_index=True)
        
        # Visualisasi Komparasi Antar Sampel yang diinput berulang
        st.markdown('<div class="sec-head">📈 GRAFIK TREN MULTI-SAMPEL</div>', unsafe_allow_html=True)
        
        fig_trend = px.line(
            df_history, x="ID Sampel", y="Skor IKA", 
            markers=True, text="Skor IKA",
            title="Fluktuasi Kualitas Air Antar Komparasi Sampel Berulang"
        )
        fig_trend.update_traces(line_color="#00f5a0", marker=dict(size=10, color="#00d2ff"), textposition="top center")
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#141b2d",
            font_color="#e2e8f0", title_font_family="IBM Plex Mono",
            xaxis=dict(gridcolor="#2d3d5a"), yaxis=dict(gridcolor="#2d3d5a", range=[0, 105])
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    else:
        st.info("Belum ada sampel yang disimpan. Masukkan nilai parameter di sidebar kiri lalu klik tombol '🧬 SIMPAN KE DATABASE HISTORIS'.")

# ══════════════════════ TAB 3 — REFERENSI ══════════════════════
with tab3:
    st.markdown('<div class="sec-head">⚛️ MATRIKS AMBANG ION pH</div>', unsafe_allow_html=True)
    render_ref_table(PH_REF)
    st.markdown('<div class="sec-head">🦠 MATRIKS BIO-DEKOMPOSISI BOD</div>', unsafe_allow_html=True)
    render_ref_table(BOD_REF)
    st.markdown('<div class="sec-head">🧪 AMBANG REDOKS KATION-ANION COD</div>', unsafe_allow_html=True)
    render_ref_table(COD_REF)
    st.markdown("""
    <div class="info-box" style="margin-top:20px;">
        📌 <b>Dasar Hukum & Validasi Teoretis:</b><br>
        Mengacu pada ketetapan regulasi nasional <b>PP No. 22 Tahun 2021</b> (Lampiran VI, Kelas II). Baku mutu ini disusun secara spesifik guna menjaga kestabilan rantai trofik akuatik, kehidupan organisme mikro/makro pertambakan, sirkulasi kation magnesium/kalsium, pembatasan konsentrasi elektron hidrogen bebas, dan ekosistem air tawar nasional dari degradasi ekosistem anoksik.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════ TAB 4 — TENTANG TIM ══════════════════════
with tab4:
    st.markdown(f"""
    <div class="about-card">
        <div class="about-label">Sistem Operasi Digital</div>
        <div class="about-title">{st.session_state.app_name}</div>
        <div class="about-body">{st.session_state.web_desc}</div>
    </div>
    <div class="about-card">
        <div class="about-label">Laboratorium Riset Pemilik Proyek</div>
        <div class="about-title">{st.session_state.group_name}</div>
        <div class="about-body" style="white-space:pre-line; font-family:'IBM Plex Mono', monospace; color:#00d2ff;">{st.session_state.group_desc}</div>
    </div>
    <div class="about-card">
        <div class="about-label">Algoritma Penimbang Bio-Kimia</div>
        <div class="about-title">Formulasi Integral Sub-Indeks Kualitas Air</div>
        <div class="about-body">
            Fungsi objektif perhitungan IKA dihitung menggunakan kombinasi koefisien stoikiometri dampak lingkungan fisis-biologis:<br><br>
            <span style="font-family:'IBM Plex Mono', monospace; color:#00f5a0; font-size:1.1rem;">
            <b>IKA = 0.30 × SI_pH + 0.35 × SI_BOD + 0.35 × SI_COD</b>
            </span><br><br>
            Di mana tiap nilai <i>Sub-Index</i> (SI) diekstraksi dari efisiensi kurva baku konversi ion terlarut dan laju respirasi mikroba oksigen terlarut.
        </div>
    </div>
    """, unsafe_allow_html=True)
