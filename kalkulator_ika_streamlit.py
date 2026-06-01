import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime
import io

# ─── Konfigurasi Halaman ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kalkulator IKA — BOD & COD",
    page_icon="💧",
    layout="centered"
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    .header-box {
        background: linear-gradient(135deg, #0a1628, #132237);
        border: 1px solid #1565c0; border-radius: 12px;
        padding: 20px; text-align: center; margin-bottom: 20px;
    }
    .header-box h1 { color: #4fc3f7; font-family: 'Courier New', monospace; font-size: 1.6rem; margin: 0; }
    .header-box p  { color: #78909c; font-family: 'Courier New', monospace; font-size: 0.8rem; margin-top: 6px; }
    .section-card {
        background: #132237; border-left: 4px solid #1565c0;
        border-radius: 8px; padding: 14px 16px; margin-bottom: 14px;
    }
    .section-title { color: #4fc3f7; font-family: 'Courier New', monospace;
                     font-size: 1rem; font-weight: bold; margin-bottom: 4px; }
    .result-box    { border-radius: 10px; padding: 18px; text-align: center; margin-top: 10px; }
    .result-skor   { font-family: 'Courier New', monospace; font-size: 1.1rem; color: #cce7ff; }
    .result-kategori { font-family: 'Courier New', monospace; font-size: 1.5rem;
                       font-weight: bold; margin-top: 6px; }
    .rumus-box {
        background: #0d1f30; border: 1px dashed #1565c0; border-radius: 6px;
        padding: 8px 12px; font-family: 'Courier New', monospace;
        font-size: 0.8rem; color: #90caf9; margin-top: 6px;
    }
    div[data-testid="stMetric"] { background: #132237; border-radius: 10px;
        padding: 12px 16px; border: 1px solid #1a3a5c; }
    div[data-testid="stMetric"] label { color: #4fc3f7 !important; font-family: 'Courier New', monospace; }
    div[data-testid="stMetric"] div   { color: #e0f4ff !important; font-family: 'Courier New', monospace; }
</style>
""", unsafe_allow_html=True)

# ─── Baku Mutu ───────────────────────────────────────────────────────────────
BAKU_MUTU = {
    "BOD": {"nilai": 3,  "satuan": "mg/L"},
    "COD": {"nilai": 25, "satuan": "mg/L"},
}

WARNA_KATEGORI = {
    "Baik":         ("#2ecc71", "#0d2b1a"),
    "Cemar Ringan": ("#f1c40f", "#2b2500"),
    "Cemar Sedang": ("#e67e22", "#2b1800"),
    "Cemar Berat":  ("#e74c3c", "#2b0d0d"),
}

# ─── Rumus Titrasi ────────────────────────────────────────────────────────────
def hitung_bod(v_blanko, v_sampel, n_tiosulfat, v_sampel_ml):
    """BOD (mg/L) = (V_blanko - V_sampel) x N x 8000 / V_sampel"""
    if v_sampel_ml <= 0:
        return 0.0
    return (v_blanko - v_sampel) * n_tiosulfat * 8000 / v_sampel_ml

def hitung_cod(v_blanko, v_sampel, n_fas, v_sampel_ml):
    """COD (mg/L) = (V_blanko - V_sampel) x N_FAS x 8000 / V_sampel"""
    if v_sampel_ml <= 0:
        return 0.0
    return (v_blanko - v_sampel) * n_fas * 8000 / v_sampel_ml

# ─── Metode IKA ──────────────────────────────────────────────────────────────
def metode_ip(bod, cod):
    rasio = [bod / 3, cod / 25]
    r_max = max(rasio)
    r_avg = sum(rasio) / 2
    ip = ((r_max**2 + r_avg**2) / 2) ** 0.5
    if ip <= 1.0:    return round(ip, 3), "Baik"
    elif ip <= 5.0:  return round(ip, 3), "Cemar Ringan"
    elif ip <= 10.0: return round(ip, 3), "Cemar Sedang"
    else:            return round(ip, 3), "Cemar Berat"

def metode_storet(bod, cod):
    skor = 0
    if bod > 3:  skor -= 8
    if cod > 25: skor -= 8
    if skor == 0:     return skor, "Baik"
    elif skor >= -10: return skor, "Cemar Ringan"
    elif skor >= -31: return skor, "Cemar Sedang"
    else:             return skor, "Cemar Berat"

def status_param(param, nilai):
    return "Memenuhi" if nilai <= BAKU_MUTU[param]["nilai"] else "Melebihi"

# ─── Grafik ──────────────────────────────────────────────────────────────────
def buat_grafik(bod, cod):
    params      = ["BOD", "COD"]
    nilai_input = [bod, cod]
    nilai_bm    = [3, 25]
    warna_bar   = [
        "#2ecc71" if bod <= 3  else "#e74c3c",
        "#2ecc71" if cod <= 25 else "#e74c3c",
    ]
    fig, ax = plt.subplots(figsize=(6, 3.5))
    fig.patch.set_facecolor("#132237")
    ax.set_facecolor("#1a2f45")
    x, w = np.arange(2), 0.3
    ax.bar(x - w/2, nilai_input, w, color=warna_bar, alpha=0.88, zorder=3)
    ax.bar(x + w/2, nilai_bm,    w, color="#4fc3f7",  alpha=0.55, zorder=3)
    for xi, vi, vb in zip(x, nilai_input, nilai_bm):
        ax.text(xi - w/2, vi + 0.2, f"{vi:.2f}", ha="center", va="bottom",
                color="#e0f4ff", fontsize=9, fontfamily="monospace")
        ax.text(xi + w/2, vb + 0.2, f"{vb:.1f}", ha="center", va="bottom",
                color="#4fc3f7",  fontsize=9, fontfamily="monospace")
    ax.set_xticks(x)
    ax.set_xticklabels(params, color="#cce7ff", fontsize=11, fontfamily="monospace")
    ax.tick_params(axis="y", colors="#cce7ff", labelsize=8)
    ax.set_ylabel("Konsentrasi (mg/L)", color="#78909c", fontsize=9, fontfamily="monospace")
    ax.set_title("Nilai Input vs Baku Mutu", color="#4fc3f7",
                 fontsize=11, fontfamily="monospace", pad=10)
    ax.spines[:].set_color("#264b6a")
    ax.grid(axis="y", color="#264b6a", linestyle="--", alpha=0.5, zorder=0)
    p1 = mpatches.Patch(color="#2ecc71", label="Input (Memenuhi)")
    p2 = mpatches.Patch(color="#e74c3c", label="Input (Melebihi)")
    p3 = mpatches.Patch(color="#4fc3f7", alpha=0.6, label="Baku Mutu")
    ax.legend(handles=[p1, p2, p3], fontsize=8,
              facecolor="#132237", labelcolor="#cce7ff", loc="upper right")
    fig.tight_layout()
    return fig

# ─── Ekspor PDF ───────────────────────────────────────────────────────────────
def buat_pdf(bod, cod, metode, skor, kategori, fig,
             bod_data, cod_data):
    try:
        from fpdf import FPDF
    except ImportError:
        return None

    chart_buf = io.BytesIO()
    fig.savefig(chart_buf, format="png", dpi=150,
                bbox_inches="tight", facecolor="#132237")
    chart_buf.seek(0)
    import tempfile, os
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    tmp.write(chart_buf.read())
    tmp.close()

    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_fill_color(13, 27, 42)
    pdf.rect(0, 0, 210, 32, "F")
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(79, 195, 247)
    pdf.cell(0, 18, "LAPORAN INDEKS KUALITAS AIR", ln=True, align="C")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, 10, "Parameter: BOD & COD  |  Baku Mutu PP 22/2021 Kelas II",
             ln=True, align="C")
    pdf.ln(6)

    pdf.set_text_color(0)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 7, f"Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(0, 7, f"Metode IKA: {metode}", ln=True)
    pdf.ln(4)

    # Data Titrasi BOD
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(21, 101, 192)
    pdf.cell(0, 8, "Data Titrasi BOD (Winkler/Iodometri)", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0)
    pdf.cell(0, 6, f"  Volume Sampel       : {bod_data['v_sampel']} mL", ln=True)
    pdf.cell(0, 6, f"  V Titran Blanko     : {bod_data['v_blanko']} mL", ln=True)
    pdf.cell(0, 6, f"  V Titran Sampel     : {bod_data['v_tiosulfat']} mL", ln=True)
    pdf.cell(0, 6, f"  Normalitas Na2S2O3  : {bod_data['n_tiosulfat']} N", ln=True)
    pdf.cell(0, 6, f"  Hasil BOD           : {bod:.4f} mg/L", ln=True)
    pdf.ln(3)

    # Data Titrasi COD
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(21, 101, 192)
    pdf.cell(0, 8, "Data Titrasi COD (FAS)", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0)
    pdf.cell(0, 6, f"  Volume Sampel   : {cod_data['v_sampel']} mL", ln=True)
    pdf.cell(0, 6, f"  V FAS Blanko    : {cod_data['v_blanko']} mL", ln=True)
    pdf.cell(0, 6, f"  V FAS Sampel    : {cod_data['v_fas']} mL", ln=True)
    pdf.cell(0, 6, f"  Normalitas FAS  : {cod_data['n_fas']} N", ln=True)
    pdf.cell(0, 6, f"  Hasil COD       : {cod:.4f} mg/L", ln=True)
    pdf.ln(4)

    # Tabel Hasil
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(13, 27, 42)
    pdf.cell(0, 8, "Hasil Parameter vs Baku Mutu", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(21, 101, 192)
    pdf.set_text_color(255)
    col_w = [40, 40, 35, 50, 40]
    for h, w in zip(["Parameter", "Nilai (mg/L)", "Satuan", "Baku Mutu", "Status"], col_w):
        pdf.cell(w, 8, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(0)
    for i, (param, nilai, bm_str) in enumerate([
        ("BOD", bod, "<= 3 mg/L"),
        ("COD", cod, "<= 25 mg/L"),
    ]):
        st_val = status_param(param, nilai)
        pdf.set_fill_color(240, 248, 255) if i % 2 == 0 else pdf.set_fill_color(255)
        for val, w in zip([param, f"{nilai:.4f}", "mg/L", bm_str, st_val], col_w):
            pdf.cell(w, 7, val, border=1, fill=True, align="C")
        pdf.ln()

    pdf.ln(6)
    skor_str = f"{skor:.3f}" if isinstance(skor, float) else str(skor)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(21, 101, 192)
    pdf.cell(0, 10, f"Skor IKA ({metode}) : {skor_str}", ln=True, align="C")
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"Kategori : {kategori}", ln=True, align="C")

    if os.path.exists(tmp.name):
        pdf.ln(4)
        pdf.image(tmp.name, x=25, w=160)
        os.unlink(tmp.name)

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return buf

# ═══════════════════════════════════════════════════════════════════════════════
#  TAMPILAN STREAMLIT
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="header-box">
  <h1>💧 Kalkulator Indeks Kualitas Air</h1>
  <p>BOD (Winkler/Iodometri) & COD (FAS)  |  Baku Mutu PP No. 22 Tahun 2021 Kelas II</p>
</div>
""", unsafe_allow_html=True)

# ── Input BOD ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-card">
  <div class="section-title">🧪 Data Titrasi BOD — Metode Winkler (Iodometri)</div>
  <div class="rumus-box">Rumus: BOD = (V_blanko - V_sampel) x N x 8000 / V_sampel</div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    bod_v_sampel   = st.number_input("Volume Sampel BOD (mL)",   min_value=0.01, value=300.0, step=1.0, format="%.2f")
    bod_v_blanko   = st.number_input("Volume Titran Blanko (mL)", min_value=0.0,  value=10.0,  step=0.01, format="%.4f")
with c2:
    bod_v_tiosulfat = st.number_input("Volume Titran Sampel (mL)", min_value=0.0, value=7.5,  step=0.01, format="%.4f")
    bod_n           = st.number_input("Normalitas Na₂S₂O₃ (N)",   min_value=0.0001, value=0.025, step=0.001, format="%.4f")

bod_hasil = hitung_bod(bod_v_blanko, bod_v_tiosulfat, bod_n, bod_v_sampel)
st.info(f"**Hasil BOD = {bod_hasil:.4f} mg/L**")

st.markdown("<br>", unsafe_allow_html=True)

# ── Input COD ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-card">
  <div class="section-title">🧪 Data Titrasi COD — Metode FAS</div>
  <div class="rumus-box">Rumus: COD = (V_blanko - V_sampel) x N_FAS x 8000 / V_sampel</div>
</div>
""", unsafe_allow_html=True)

c3, c4 = st.columns(2)
with c3:
    cod_v_sampel = st.number_input("Volume Sampel COD (mL)", min_value=0.01, value=20.0, step=1.0,  format="%.2f")
    cod_v_blanko = st.number_input("Volume FAS Blanko (mL)", min_value=0.0,  value=15.0, step=0.01, format="%.4f")
with c4:
    cod_v_fas = st.number_input("Volume FAS Sampel (mL)", min_value=0.0,    value=9.0,  step=0.01, format="%.4f")
    cod_n_fas = st.number_input("Normalitas FAS (N)",     min_value=0.0001, value=0.1,  step=0.001, format="%.4f")

cod_hasil = hitung_cod(cod_v_blanko, cod_v_fas, cod_n_fas, cod_v_sampel)
st.info(f"**Hasil COD = {cod_hasil:.4f} mg/L**")

st.markdown("<br>", unsafe_allow_html=True)

# ── Metode IKA ────────────────────────────────────────────────────────────────
metode = st.radio("Metode Perhitungan IKA",
                  ["Indeks Pencemar (IP)", "STORET"],
                  horizontal=True)

hitung = st.button("HITUNG IKA", use_container_width=True, type="primary")

# ── Hasil ─────────────────────────────────────────────────────────────────────
if hitung:
    if bod_hasil < 0 or cod_hasil < 0:
        st.error("Nilai BOD atau COD tidak valid (negatif). Periksa data titrasi.")
    else:
        if metode == "Indeks Pencemar (IP)":
            skor, kategori = metode_ip(bod_hasil, cod_hasil)
            skor_str       = f"{skor:.3f}"
            metode_label   = "Indeks Pencemar (IP)"
        else:
            skor, kategori = metode_storet(bod_hasil, cod_hasil)
            skor_str       = str(skor)
            metode_label   = "STORET"

        warna_fg, warna_bg = WARNA_KATEGORI[kategori]

        st.divider()

        st.markdown(f"""
        <div class="result-box" style="background:{warna_bg}; border: 2px solid {warna_fg};">
            <div class="result-skor">Skor IKA ({metode_label}) : <b>{skor_str}</b></div>
            <div class="result-kategori" style="color:{warna_fg};">● {kategori}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Metrik
        m1, m2 = st.columns(2)
        st_bod = status_param("BOD", bod_hasil)
        st_cod = status_param("COD", cod_hasil)
        with m1:
            st.metric("BOD", f"{bod_hasil:.4f} mg/L",
                      delta=f"BM <= 3 mg/L  |  {st_bod}",
                      delta_color="normal" if st_bod == "Memenuhi" else "inverse")
        with m2:
            st.metric("COD", f"{cod_hasil:.4f} mg/L",
                      delta=f"BM <= 25 mg/L  |  {st_cod}",
                      delta_color="normal" if st_cod == "Memenuhi" else "inverse")

        st.markdown("<br>", unsafe_allow_html=True)

        # Tabel
        st.markdown("#### Tabel Hasil Parameter")
        import pandas as pd
        df = pd.DataFrame([
            {"Parameter": "BOD", "Nilai (mg/L)": f"{bod_hasil:.4f}",
             "Baku Mutu": "<= 3 mg/L",  "Status": st_bod},
            {"Parameter": "COD", "Nilai (mg/L)": f"{cod_hasil:.4f}",
             "Baku Mutu": "<= 25 mg/L", "Status": st_cod},
        ])

        def warnai_status(val):
            return "color: #2ecc71; font-weight: bold" if val == "Memenuhi" \
                   else "color: #e74c3c; font-weight: bold"

        st.dataframe(
            df.style.map(warnai_status, subset=["Status"]),
            use_container_width=True, hide_index=True
        )

        # Grafik
        st.markdown("#### Grafik Perbandingan vs Baku Mutu")
        fig = buat_grafik(bod_hasil, cod_hasil)
        st.pyplot(fig, use_container_width=True)

        # PDF
        st.markdown("---")
        bod_data = {"v_sampel": bod_v_sampel, "v_blanko": bod_v_blanko,
                    "v_tiosulfat": bod_v_tiosulfat, "n_tiosulfat": bod_n}
        cod_data = {"v_sampel": cod_v_sampel, "v_blanko": cod_v_blanko,
                    "v_fas": cod_v_fas, "n_fas": cod_n_fas}
        pdf_buf = buat_pdf(bod_hasil, cod_hasil, metode_label, skor, kategori,
                           fig, bod_data, cod_data)
        if pdf_buf:
            fname = f"IKA_BOD_COD_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            st.download_button(
                label="Unduh Laporan PDF",
                data=pdf_buf, file_name=fname,
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.info("Install fpdf2 untuk ekspor PDF: pip install fpdf2")
        
