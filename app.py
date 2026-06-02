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
    page_title="AquaChem IKA",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS — TEMA: AURORA SCIENTIFIC
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg:      #F0F4F8;
    --surface: #FFFFFF;
    --card:    #FFFFFF;
    --border:  #DDE3ED;
    --emerald: #059669;
    --emerald2:#047857;
    --teal:    #0D9488;
    --amber:   #D97706;
    --red:     #DC2626;
    --text:    #1A202C;
    --muted:   #64748B;
    --light:   #F8FAFC;
    --good:    #059669;
    --warn:    #D97706;
    --bad:     #DC2626;
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
    background: linear-gradient(135deg, #064E3B 0%, #065F46 40%, #0F766E 100%);
    border-radius: 20px;
    padding: 44px 40px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(5, 150, 105, 0.25);
}
.hero::before {
    content: "";
    position: absolute;
    top: -80px; right: -40px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 65%);
    border-radius: 50%;
}
.hero::after {
    content: "";
    position: absolute;
    bottom: -60px; left: 5%;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3);
    color: #A7F3D0;
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
    text-shadow: 0 2px 20px rgba(0,0,0,0.2);
}
.hero-title span { color: #6EE7B7; }
.hero-sub {
    color: #A7F3D0;
    font-size: 1rem;
    margin: 0;
    font-weight: 400;
    opacity: 0.9;
}

/* ── Param Cards ── */
.param-card {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: 16px;
    padding: 26px 22px;
    height: 100%;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    transition: all 0.2s ease;
}
.param-card:hover {
    border-color: var(--emerald);
    box-shadow: 0 8px 30px rgba(5,150,105,0.12);
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
    font-size: 2.8rem;
    font-weight: 800;
    color: var(--text);
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
.status-good { background: #D1FAE5; color: #065F46; border: 1.5px solid #6EE7B7; }
.status-warn { background: #FEF3C7; color: #92400E; border: 1.5px solid #FCD34D; }
.status-bad  { background: #FEE2E2; color: #991B1B; border: 1.5px solid #FCA5A5; }

/* ── Section Header ── */
.sec-head {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 2.5px;
    color: var(--emerald);
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

/* ── IKA Score ── */
.ika-ring { text-align: center; padding: 16px 0; }
.ika-score {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 4rem;
    font-weight: 700;
    line-height: 1;
}
.ika-label { font-size: 0.85rem; color: var(--muted); margin-top: 8px; font-weight: 500; }
.ika-cat   { font-size: 1.1rem; font-weight: 700; margin-top: 10px; }

/* ── Info Boxes ── */
.info-box {
    background: #ECFDF5;
    border: 1px solid #6EE7B7;
    border-left: 4px solid var(--emerald);
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: #065F46;
    margin: 10px 0;
    line-height: 1.6;
}
.warn-box {
    background: #FFFBEB;
    border: 1px solid #FCD34D;
    border-left: 4px solid var(--amber);
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: #78350F;
    margin: 10px 0;
    line-height: 1.6;
}
.bad-box {
    background: #FFF1F2;
    border: 1px solid #FCA5A5;
    border-left: 4px solid var(--red);
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: #7F1D1D;
    margin: 10px 0;
    line-height: 1.6;
}

/* ── Reference Table ── */
.ref-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.ref-table th {
    background: #ECFDF5;
    color: var(--emerald2);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    padding: 12px 16px;
    text-align: left;
    border-bottom: 2px solid var(--border);
    text-transform: uppercase;
    letter-spacing: 1px;
}
.ref-table td {
    padding: 11px 16px;
    border-bottom: 1px solid var(--border);
    color: var(--text);
}
.ref-table tr:last-child td { border-bottom: none; }
.ref-table tr:hover td { background: #F0FDF4; }

/* ── About Card ── */
.about-card {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: 16px;
    padding: 28px 26px;
    margin-bottom: 18px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.about-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 2px;
    color: var(--emerald);
    text-transform: uppercase;
    margin-bottom: 8px;
}
.about-title { font-size: 1.2rem; font-weight: 700; color: var(--text); margin-bottom: 10px; }
.about-body  { color: var(--muted); font-size: 0.9rem; line-height: 1.75; }

/* ── Metric Strip ── */
.metric-strip { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px; }
.metric-item {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 16px 22px;
    flex: 1;
    min-width: 120px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.metric-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--emerald);
}
.metric-desc { font-size: 0.78rem; color: var(--muted); margin-top: 2px; }

/* ── Streamlit Overrides ── */
.stButton > button {
    background: linear-gradient(135deg, #059669, #0D9488);
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.82rem !important;
    letter-spacing: 1px !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
    width: 100%;
    box-shadow: 0 4px 14px rgba(5,150,105,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 20px rgba(5,150,105,0.4) !important;
}

div[data-testid="stExpander"] {
    background: var(--card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
}
div[data-testid="stExpander"] summary { color: var(--text) !important; font-weight: 600; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 5px;
    gap: 4px;
    border: 1.5px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #D1FAE5, #CCFBF1) !important;
    color: #065F46 !important;
}

/* Number inputs */
div[data-testid="stNumberInput"] input {
    background: var(--light) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'IBM Plex Mono', monospace !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: var(--emerald) !important;
    box-shadow: 0 0 0 3px rgba(5,150,105,0.1) !important;
}

/* Radio */
.stRadio > label { color: var(--text) !important; font-weight: 600 !important; font-size: 0.88rem !important; }

/* Divider */
.divider { border: none; border-top: 1.5px solid var(--border); margin: 24px 0; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "app_name" not in st.session_state:
    st.session_state.app_name = "AquaChem IKA"
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
        "Aplikasi ini dikembangkan untuk membantu analisis kualitas air "
        "berdasarkan parameter kimia utama yaitu pH, BOD, dan COD. "
        "Gunakan slider di panel kiri untuk memasukkan nilai pengukuran lapangan."
    )

# ─────────────────────────────────────────────
#  REFERENCE DATA
# ─────────────────────────────────────────────
PH_REF = [
    {"Kategori": "Sangat Asam / Sangat Basa (Berbahaya)", "Rentang": "< 5.0 atau > 9.0",
     "Status": "Tercemar Berat", "Kelas": "bad"},
    {"Kategori": "Asam / Basa Ringan", "Rentang": "5.0-6.0 atau 8.5-9.0",
     "Status": "Tercemar Sedang", "Kelas": "warn"},
    {"Kategori": "Mendekati Normal", "Rentang": "6.0-6.5 atau 8.0-8.5",
     "Status": "Tercemar Ringan", "Kelas": "warn"},
    {"Kategori": "Normal / Baku Mutu", "Rentang": "6.5 - 8.0",
     "Status": "Memenuhi Baku Mutu", "Kelas": "good"},
]
BOD_REF = [
    {"Kategori": "Sangat Baik (Air Bersih)", "Rentang": "< 2 mg/L",
     "Status": "Tidak Tercemar", "Kelas": "good"},
    {"Kategori": "Baik (Air Bersih)", "Rentang": "2 - 3 mg/L",
     "Status": "Memenuhi Baku Mutu", "Kelas": "good"},
    {"Kategori": "Tercemar Sedang", "Rentang": "3 - 6 mg/L",
     "Status": "Tercemar Sedang", "Kelas": "warn"},
    {"Kategori": "Tercemar Berat", "Rentang": "6 - 12 mg/L",
     "Status": "Tercemar Berat", "Kelas": "bad"},
    {"Kategori": "Sangat Tercemar Berat", "Rentang": "> 12 mg/L",
     "Status": "Sangat Tercemar", "Kelas": "bad"},
]
COD_REF = [
    {"Kategori": "Sangat Baik", "Rentang": "< 10 mg/L",
     "Status": "Tidak Tercemar", "Kelas": "good"},
    {"Kategori": "Baik (Baku Mutu Kelas I/II)", "Rentang": "10 - 25 mg/L",
     "Status": "Memenuhi Baku Mutu", "Kelas": "good"},
    {"Kategori": "Tercemar Ringan-Sedang", "Rentang": "25 - 50 mg/L",
     "Status": "Tercemar Sedang", "Kelas": "warn"},
    {"Kategori": "Tercemar Berat", "Rentang": "50 - 100 mg/L",
     "Status": "Tercemar Berat", "Kelas": "bad"},
    {"Kategori": "Sangat Tercemar Berat", "Rentang": "> 100 mg/L",
     "Status": "Sangat Tercemar", "Kelas": "bad"},
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
    if score >= 80:   return "Baik", "#059669"
    elif score >= 50: return "Tercemar Ringan-Sedang", "#D97706"
    elif score >= 25: return "Tercemar Berat", "#DC2626"
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
      <thead><tr><th>Kategori</th><th>Rentang</th><th>Status</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:18px 0 8px 0;">
        <div style="font-family:'IBM Plex Mono',monospace; font-size:1.1rem; font-weight:700; color:#059669;">
            💧 AquaChem IKA
        </div>
        <div style="color:#64748B; font-size:0.78rem; margin-top:4px;">
            Indeks Kualitas Air — Parameter Kimia
        </div>
    </div>
    <hr style="border:none; border-top:1.5px solid #DDE3ED; margin:12px 0 20px 0;">
    """, unsafe_allow_html=True)

    st.markdown("**Masukkan Nilai Parameter**")

    input_mode = st.radio("Mode Input", ["Langsung (Nilai)", "Dari Titrasi"], horizontal=True)

    ph_val = st.number_input("pH", min_value=0.0, max_value=14.0, value=7.0, step=0.1,
                             help="Skala 0-14. Baku mutu: 6.5-8.0")

    if input_mode == "Langsung (Nilai)":
        bod_val = st.number_input("BOD (mg/L)", min_value=0.0, max_value=200.0, value=2.0, step=0.1,
                                  help="Biochemical Oxygen Demand. Baku mutu: < 3 mg/L")
        cod_val = st.number_input("COD (mg/L)", min_value=0.0, max_value=500.0, value=15.0, step=0.1,
                                  help="Chemical Oxygen Demand. Baku mutu: < 25 mg/L")
    else:
        st.markdown("""<div style="font-size:0.8rem; color:#059669; font-family:'IBM Plex Mono',monospace;
                       margin:10px 0 4px 0; font-weight:600;">BOD — Titrasi Winkler</div>
                    <div style="font-size:0.72rem; color:#64748B; margin-bottom:8px;">
                    BOD = (V_blanko - V_sampel) x N x 8000 / V_sampel</div>""",
                    unsafe_allow_html=True)
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            bod_v_blanko   = st.number_input("V Blanko (mL)",  min_value=0.0, value=10.0,  step=0.01, key="bod_vb")
            bod_v_sampel_t = st.number_input("V Sampel (mL)",  min_value=0.0, value=8.5,   step=0.01, key="bod_vs")
        with col_b2:
            bod_n        = st.number_input("N Na2S2O3",  min_value=0.0, value=0.025, step=0.001, format="%.4f", key="bod_n")
            bod_v_sampel = st.number_input("V Air (mL)", min_value=0.1, value=100.0, step=1.0,   key="bod_ml")
        bod_val = round((bod_v_blanko - bod_v_sampel_t) * bod_n * 8000 / bod_v_sampel, 3) if bod_v_sampel > 0 else 0.0
        st.markdown(f"""<div style="background:#ECFDF5; border:1px solid #6EE7B7; border-radius:8px;
                    padding:8px 14px; font-size:0.83rem; margin:4px 0 14px 0; color:#065F46;">
                    BOD terhitung: <b style="font-family:'IBM Plex Mono',monospace;">{bod_val} mg/L</b>
                    </div>""", unsafe_allow_html=True)

        st.markdown("""<div style="font-size:0.8rem; color:#7C3AED; font-family:'IBM Plex Mono',monospace;
                       margin:4px 0 4px 0; font-weight:600;">COD — Titrasi FAS/Dikromat</div>
                    <div style="font-size:0.72rem; color:#64748B; margin-bottom:8px;">
                    COD = (V_blanko - V_sampel) x N x 8000 / V_sampel</div>""",
                    unsafe_allow_html=True)
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            cod_v_blanko   = st.number_input("V Blanko (mL)",  min_value=0.0, value=15.0, step=0.01, key="cod_vb")
            cod_v_sampel_t = st.number_input("V Sampel (mL)",  min_value=0.0, value=12.0, step=0.01, key="cod_vs")
        with col_c2:
            cod_n        = st.number_input("N FAS/KMnO4", min_value=0.0, value=0.1,  step=0.001, format="%.4f", key="cod_n")
            cod_v_sampel = st.number_input("V Air (mL)",  min_value=0.1, value=20.0, step=1.0,   key="cod_ml")
        cod_val = round((cod_v_blanko - cod_v_sampel_t) * cod_n * 8000 / cod_v_sampel, 3) if cod_v_sampel > 0 else 0.0
        st.markdown(f"""<div style="background:#F5F3FF; border:1px solid #C4B5FD; border-radius:8px;
                    padding:8px 14px; font-size:0.83rem; margin:4px 0 4px 0; color:#4C1D95;">
                    COD terhitung: <b style="font-family:'IBM Plex Mono',monospace;">{cod_val} mg/L</b>
                    </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1.5px solid #DDE3ED;margin:20px 0;'>",
                unsafe_allow_html=True)

    with st.expander("Pengaturan Aplikasi"):
        new_app   = st.text_input("Nama Aplikasi",      value=st.session_state.app_name)
        new_grp   = st.text_input("Nama Kelompok",      value=st.session_state.group_name)
        new_gdesc = st.text_area("Deskripsi Kelompok",  value=st.session_state.group_desc, height=80)
        new_wdesc = st.text_area("Deskripsi Website",   value=st.session_state.web_desc,   height=100)
        if st.button("SIMPAN PENGATURAN"):
            st.session_state.app_name  = new_app
            st.session_state.group_name = new_grp
            st.session_state.group_desc = new_gdesc
            st.session_state.web_desc   = new_wdesc
            st.success("Pengaturan tersimpan!")

    st.markdown("""
    <div style="margin-top:24px; padding:14px; background:#F0FDF4;
                border-radius:10px; border:1.5px solid #6EE7B7; font-size:0.75rem; color:#065F46;">
        Referensi: PP No. 22/2021 & PermenLHK<br>Baku mutu air kelas II
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CALCULATE
# ─────────────────────────────────────────────
ika_score, ph_si, bod_si, cod_si = calc_ika(ph_val, bod_val, cod_val)
ika_cat, ika_color = ika_category(ika_score)
ph_label,  ph_cls,  _ = get_ph_status(ph_val)
bod_label, bod_cls, _ = get_bod_status(bod_val)
cod_label, cod_cls, _ = get_cod_status(cod_val)

# ─────────────────────────────────────────────
#  MAIN CONTENT — TABS
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-badge">AQUACHEM IKA v2.0</div>
    <div class="hero-title">Water Quality <span>Index</span></div>
    <div class="hero-sub">Analisis kualitas air berbasis parameter kimia — pH, BOD, dan COD</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Dashboard", "Referensi Baku Mutu", "Tentang"])

# ══════════════════════ TAB 1 — DASHBOARD ══════════════════════
with tab1:
    # IKA Score strip
    c_ika, c_ph, c_bod, c_cod = st.columns([1.4, 1, 1, 1])

    with c_ika:
        st.markdown(f"""
        <div class="param-card" style="border-color:{ika_color}; background:linear-gradient(135deg,#FFFFFF,#F0FDF4);">
            <div class="param-title">INDEKS KUALITAS AIR</div>
            <div class="param-fullname">Skor IKA Gabungan (pH+BOD+COD)</div>
            <div class="param-value" style="color:{ika_color};">{ika_score}</div>
            <div class="param-unit">dari 100</div>
            <span class="status-chip status-{'good' if ika_score>=80 else 'warn' if ika_score>=50 else 'bad'}">{ika_cat}</span>
        </div>
        """, unsafe_allow_html=True)

    for label, fullname, val, unit, lbl, cls in [
        ("pH",  "Derajat Keasaman",       ph_val,  "skala",  ph_label,  ph_cls),
        ("BOD", "Biochemical Oxygen Demand", bod_val, "mg/L", bod_label, bod_cls),
        ("COD", "Chemical Oxygen Demand",    cod_val, "mg/L", cod_label, cod_cls),
    ]:
        col = c_ph if label == "pH" else c_bod if label == "BOD" else c_cod
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

    # Gauge charts
    st.markdown('<div class="sec-head">VISUALISASI SUB-INDEKS</div>', unsafe_allow_html=True)

    def make_gauge(title, value, color):
        c = {"good": "#059669", "warn": "#D97706", "bad": "#DC2626"}[color]
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            number={"font": {"size": 36, "family": "IBM Plex Mono"}, "suffix": "%"},
            title={"text": title, "font": {"size": 13, "family": "Inter", "color": "#64748B"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#DDE3ED",
                          "tickfont": {"size": 10, "color": "#64748B"}},
                "bar": {"color": c, "thickness": 0.28},
                "bgcolor": "#F8FAFC",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 25],  "color": "#FEE2E2"},
                    {"range": [25, 50], "color": "#FEF3C7"},
                    {"range": [50, 80], "color": "#D1FAE5"},
                    {"range": [80, 100],"color": "#A7F3D0"},
                ],
                "threshold": {"line": {"color": c, "width": 3}, "thickness": 0.8, "value": value},
            }
        ))
        fig.update_layout(
            height=220, margin=dict(t=40, b=10, l=20, r=20),
            paper_bgcolor="#FFFFFF", font_color="#1A202C",
        )
        return fig

    g1, g2, g3 = st.columns(3)
    with g1: st.plotly_chart(make_gauge("Sub-Indeks pH",  ph_si,  ph_cls),  use_container_width=True)
    with g2: st.plotly_chart(make_gauge("Sub-Indeks BOD", bod_si, bod_cls), use_container_width=True)
    with g3: st.plotly_chart(make_gauge("Sub-Indeks COD", cod_si, cod_cls), use_container_width=True)

    # Radar + Bar
    st.markdown('<div class="sec-head">GRAFIK ANALISIS</div>', unsafe_allow_html=True)
    left, right = st.columns(2)

    with left:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[ph_si, bod_si, cod_si, ph_si],
            theta=["pH", "BOD", "COD", "pH"],
            fill="toself",
            fillcolor="rgba(5,150,105,0.15)",
            line=dict(color="#059669", width=2.5),
            name="Sub-Indeks"
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[100, 100, 100, 100],
            theta=["pH", "BOD", "COD", "pH"],
            fill="toself",
            fillcolor="rgba(221,227,237,0.3)",
            line=dict(color="#DDE3ED", width=1.5, dash="dot"),
            name="Ideal"
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor="#F8FAFC",
                radialaxis=dict(visible=True, range=[0, 100],
                                tickfont=dict(size=9, color="#64748B"),
                                gridcolor="#DDE3ED"),
                angularaxis=dict(tickfont=dict(size=11, color="#1A202C", family="IBM Plex Mono"),
                                 gridcolor="#DDE3ED"),
            ),
            showlegend=True,
            legend=dict(font=dict(size=10, color="#64748B")),
            height=280, margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor="#FFFFFF",
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with right:
        bar_colors = {
            "good": "#059669", "warn": "#D97706", "bad": "#DC2626"
        }
        fig_bar = go.Figure()
        params_bar = [("pH", ph_val, ph_cls), ("BOD", bod_val, bod_cls), ("COD", cod_val, cod_cls)]
        bm_vals    = [7.25, 3, 25]
        for (pname, pval, pcls), bmv in zip(params_bar, bm_vals):
            fig_bar.add_trace(go.Bar(
                name=pname,
                x=[pname],
                y=[pval],
                marker_color=bar_colors[pcls],
                marker_line_width=0,
                opacity=0.9,
            ))
            fig_bar.add_trace(go.Scatter(
                x=[pname], y=[bmv],
                mode="markers",
                marker=dict(symbol="line-ew", size=22, color="#1A202C",
                            line=dict(width=2.5, color="#1A202C")),
                name=f"BM {pname}",
                showlegend=False,
            ))
        fig_bar.update_layout(
            barmode="group",
            height=280,
            margin=dict(t=20, b=20, l=20, r=20),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#F8FAFC",
            showlegend=False,
            xaxis=dict(tickfont=dict(size=12, color="#1A202C", family="IBM Plex Mono"),
                       gridcolor="#DDE3ED"),
            yaxis=dict(tickfont=dict(size=10, color="#64748B"), gridcolor="#DDE3ED"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Status boxes
    box_map = {"good": "info-box", "warn": "warn-box", "bad": "bad-box"}
    st.markdown(f"""
    <div class="{box_map[ph_cls]}">
        <b>pH {ph_val:.1f}</b> — {ph_label}.
        Baku mutu kelas II: 6.5–8.0. Nilai {"dalam" if ph_cls=="good" else "di luar"} rentang normal.
    </div>
    <div class="{box_map[bod_cls]}">
        <b>BOD {bod_val:.2f} mg/L</b> — {bod_label}.
        Baku mutu: &lt;3 mg/L. {"Memenuhi" if bod_cls=="good" else "Melebihi"} standar kualitas air.
    </div>
    <div class="{box_map[cod_cls]}">
        <b>COD {cod_val:.2f} mg/L</b> — {cod_label}.
        Baku mutu: &lt;25 mg/L. {"Memenuhi" if cod_cls=="good" else "Melebihi"} standar kualitas air.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════ TAB 2 — REFERENSI ══════════════════════
with tab2:
    st.markdown('<div class="sec-head">BAKU MUTU pH</div>', unsafe_allow_html=True)
    render_ref_table(PH_REF)
    st.markdown('<div class="sec-head">BAKU MUTU BOD</div>', unsafe_allow_html=True)
    render_ref_table(BOD_REF)
    st.markdown('<div class="sec-head">BAKU MUTU COD</div>', unsafe_allow_html=True)
    render_ref_table(COD_REF)
    st.markdown("""
    <div class="info-box" style="margin-top:20px;">
        Referensi: <b>PP No. 22 Tahun 2021</b> tentang Penyelenggaraan Perlindungan dan
        Pengelolaan Lingkungan Hidup, dan <b>PermenLHK</b> tentang Baku Mutu Air Nasional.
        Kelas II digunakan untuk prasarana/sarana rekreasi air, budidaya ikan air tawar,
        peternakan, dan pengairan pertanaman.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════ TAB 3 — TENTANG ══════════════════════
with tab3:
    st.markdown(f"""
    <div class="about-card">
        <div class="about-label">Tentang Aplikasi</div>
        <div class="about-title">{st.session_state.app_name}</div>
        <div class="about-body">{st.session_state.web_desc}</div>
    </div>
    <div class="about-card">
        <div class="about-label">Tim Pengembang</div>
        <div class="about-title">{st.session_state.group_name}</div>
        <div class="about-body" style="white-space:pre-line;">{st.session_state.group_desc}</div>
    </div>
    <div class="about-card">
        <div class="about-label">Metodologi</div>
        <div class="about-title">Perhitungan IKA</div>
        <div class="about-body">
            Indeks Kualitas Air dihitung menggunakan sub-indeks tertimbang:<br><br>
            <b>IKA = 0.30 × SI_pH + 0.35 × SI_BOD + 0.35 × SI_COD</b><br><br>
            Kategori hasil: <b>Baik</b> (80-100) | <b>Tercemar Ringan-Sedang</b> (50-79) |
            <b>Tercemar Berat</b> (25-49) | <b>Sangat Tercemar Berat</b> (0-24)
        </div>
    </div>
    """, unsafe_allow_html=True)
