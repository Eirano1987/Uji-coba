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

# ─── CSS Kustom ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    body { background-color: #0d1b2a; }
    .main { background-color: #0d1b2a; }
    .block-container { padding-top: 1.5rem; }

    .header-box {
        background: linear-gradient(135deg, #0a1628, #132237);
        border: 1px solid #1565c0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 24px;
    }
    .header-box h1 {
        color: #4fc3f7;
        font-family: 'Courier New', monospace;
        font-size: 1.7rem;
        margin: 0;
    }
    .header-box p {
        color: #78909c;
        font-family: 'Courier New', monospace;
        font-size: 0.8rem;
        margin-top: 6px;
    }

    .result-box {
        border-radius: 10px;
        padding: 18px;
        text-align: center;
        margin-top: 10px;
    }
    .result-skor {
        font-family: 'Courier New', monospace;
        font-size: 1.1rem;
        color: #cce7ff;
    }
    .result-kategori {
        font-family: 'Courier New', monospace;
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 6px;
    }

    .info-card {
        background: #132237;
        border-left: 4px solid #1565c0;
        border-radius: 6px;
        padding: 10px 14px;
        font-family: 'Courier New', monospace;
        font-size: 0.82rem;
        color: #90caf9;
        margin-bottom: 10px;
    }

    div[data-testid="stMetric"] {
        background: #132237;
        border-radius: 10px;
        padding: 12px 16px;
        border: 1px solid #1a3a5c;
    }
    div[data-testid="stMetric"] label {
        color: #4fc3f7 !important;
        font-family: 'Courier New', monospace;
    }
    div[data-testid="stMetric"] div {
        color: #e0f4ff !important;
        font-family: 'Courier New', monospace;
    }
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

# ─── Fungsi Perhitungan ──────────────────────────────────────────────────────
def metode_ip(bod, cod):
    rasio_bod = bod / BAKU_MUTU["BOD"]["nilai"]
    rasio_cod = cod / BAKU_MUTU["COD"]["nilai"]
    rasio = [rasio_bod, rasio_cod]
    r_max = max(rasio)
    r_avg = sum(rasio) / len(rasio)
    ip = ((r_max**2 + r_avg**2) / 2) ** 0.5
    if ip <= 1.0:   return round(ip, 3), "Baik"
    elif ip <= 5.0: return round(ip, 3), "Cemar Ringan"
    elif ip <= 10.0:return round(ip, 3), "Cemar Sedang"
    else:           return round(ip, 3), "Cemar Berat"

def metode_storet(bod, cod):
    skor = 0
    if bod > BAKU_MUTU["BOD"]["nilai"]: skor -= 8
    if cod > BAKU_MUTU["COD"]["nilai"]: skor -= 8
    if skor == 0:       return skor, "Baik"
    elif skor >= -10:   return skor, "Cemar Ringan"
    elif skor >= -31:   return skor, "Cemar Sedang"
    else:               return skor, "Cemar Berat"

def status_param(param, nilai):
    return "✓ Memenuhi" if nilai <= BAKU_MUTU[param]["nilai"] else "✗ Melebihi"

# ─── Grafik ──────────────────────────────────────────────────────────────────
def buat_grafik(bod, cod):
    params       = ["BOD", "COD"]
    nilai_input  = [bod, cod]
    nilai_bm     = [BAKU_MUTU["BOD"]["nilai"], BAKU_MUTU["COD"]["nilai"]]
    warna_bar    = [
        "#2ecc71" if bod <= BAKU_MUTU["BOD"]["nilai"] else "#e74c3c",
        "#2ecc71" if cod <= BAKU_MUTU["COD"]["nilai"] else "#e74c3c",
    ]

    fig, ax = plt.subplots(figsize=(6, 3.5))
    fig.patch.set_facecolor("#132237")
    ax.set_facecolor("#1a2f45")

    x = np.arange(len(params))
    w = 0.3
    ax.bar(x - w/2, nilai_input, w, color=warna_bar, alpha=0.88, zorder=3)
    ax.bar(x + w/2, nilai_bm,    w, color="#4fc3f7",  alpha=0.55, zorder=3)

    for xi, vi, vb in zip(x, nilai_input, nilai_bm):
        ax.text(xi - w/2, vi + 0.2, f"{vi:.1f}", ha="center", va="bottom",
                color="#e0f4ff", fontsize=9, fontfamily="monospace")
        ax.text(xi + w/2, vb + 0.2, f"{vb:.1f}", ha="center", va="bottom",
                color="#4fc3f7",  fontsize=9, fontfamily="monospace")

    ax.set_xticks(x)
    ax.set_xticklabels(params, color="#cce7ff", fontsize=11, fontfamily="monospace")
    ax.tick_params(axis="y", colors="#cce7ff", labelsize=8)
    ax.set_ylabel("Konsentrasi (mg/L)", color="#78909c",
                  fontsize=9, fontfamily="monospace")
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

# ─── Ekspor PDF ──────────────────────────────────────────────────────────────
def buat_pdf(bod, cod, metode, skor, kategori, fig):
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
    pdf.cell(0, 10, "Parameter: BOD & COD  |  Baku Mutu PP No. 22 Tahun 2021 Kelas II",
             ln=True, align="C")

    pdf.ln(6)
    pdf.set_text_color(0)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 7, f"Tanggal Analisis : {datetime.now().strftime('%d %B %Y  %H:%M')}", ln=True)
    pdf.cell(0, 7, f"Metode           : {metode}", ln=True)
    pdf.ln(4)

    # Tabel
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(13, 27, 42)
    pdf.cell(0, 8, "Hasil Parameter", ln=True)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(21, 101, 192)
    pdf.set_text_color(255)
    col_w = [40, 35, 35, 50, 40]
    for h, w in zip(["Parameter", "Nilai", "Satuan", "Baku Mutu", "Status"], col_w):
        pdf.cell(w, 8, h, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(0)
    for i, (param, nilai) in enumerate([("BOD", bod), ("COD", cod)]):
        bm = BAKU_MUTU[param]
        st = status_param(param, nilai)
        pdf.set_fill_color(240, 248, 255) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        for val, w in zip([param, f"{nilai:.2f}", bm["satuan"],
                           f"<= {bm['nilai']} mg/L", st], col_w):
            pdf.cell(w, 7, val, border=1, fill=True, align="C")
        pdf.ln()

    pdf.ln(8)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(21, 101, 192)
    skor_str = f"{skor:.3f}" if isinstance(skor, float) else str(skor)
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

# Header
st.markdown("""
<div class="header-box">
  <h1>💧 Kalkulator Indeks Kualitas Air</h1>
  <p>Parameter Kimia: BOD & COD  |  Baku Mutu PP No. 22 Tahun 2021 Kelas II</p>
</div>
""", unsafe_allow_html=True)

# Info baku mutu
st.markdown("""
<div class="info-card">
  📋 <b>Baku Mutu Referensi:</b>&nbsp;
  BOD ≤ 3 mg/L &nbsp;|&nbsp; COD ≤ 25 mg/L
</div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    bod = st.number_input("BOD (mg/L)", min_value=0.0, value=3.0,
                          step=0.1, format="%.2f",
                          help="Biological Oxygen Demand — Baku Mutu ≤ 3 mg/L")
with col2:
    cod = st.number_input("COD (mg/L)", min_value=0.0, value=10.0,
                          step=0.5, format="%.2f",
                          help="Chemical Oxygen Demand — Baku Mutu ≤ 25 mg/L")

metode = st.radio("Metode Perhitungan",
                  ["Indeks Pencemar (IP)", "STORET"],
                  horizontal=True)

hitung = st.button("⚡ HITUNG IKA", use_container_width=True, type="primary")

# ── Hasil ─────────────────────────────────────────────────────────────────────
if hitung:
    if metode == "Indeks Pencemar (IP)":
        skor, kategori = metode_ip(bod, cod)
        skor_str = f"{skor:.3f}"
        metode_label = "Indeks Pencemar (IP)"
    else:
        skor, kategori = metode_storet(bod, cod)
        skor_str = str(skor)
        metode_label = "STORET"

    warna_fg, warna_bg = WARNA_KATEGORI[kategori]

    st.divider()

    # Kotak hasil
    st.markdown(f"""
    <div class="result-box" style="background:{warna_bg}; border: 2px solid {warna_fg};">
        <div class="result-skor">Skor IKA ({metode_label}) : <b>{skor_str}</b></div>
        <div class="result-kategori" style="color:{warna_fg};">● {kategori}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Metrik per parameter
    m1, m2 = st.columns(2)
    st_bod = status_param("BOD", bod)
    st_cod = status_param("COD", cod)
    with m1:
        st.metric("BOD", f"{bod:.2f} mg/L",
                  delta=f"BM ≤ 3 mg/L  |  {st_bod}",
                  delta_color="normal" if "Memenuhi" in st_bod else "inverse")
    with m2:
        st.metric("COD", f"{cod:.2f} mg/L",
                  delta=f"BM ≤ 25 mg/L  |  {st_cod}",
                  delta_color="normal" if "Memenuhi" in st_cod else "inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabel ringkasan
    st.markdown("#### 📋 Tabel Hasil Parameter")
    import pandas as pd
    df = pd.DataFrame([
        {
            "Parameter": "BOD",
            "Nilai (mg/L)": f"{bod:.2f}",
            "Baku Mutu": "≤ 3 mg/L",
            "Status": status_param("BOD", bod)
        },
        {
            "Parameter": "COD",
            "Nilai (mg/L)": f"{cod:.2f}",
            "Baku Mutu": "≤ 25 mg/L",
            "Status": status_param("COD", cod)
        },
    ])

    def warnai_status(val):
        if "Memenuhi" in val:
            return "color: #2ecc71; font-weight: bold"
        return "color: #e74c3c; font-weight: bold"

    st.dataframe(
       df.style.map(warnai_status, subset=["Status"]),
        use_container_width=True,
        hide_index=True
    )

    # Grafik
    st.markdown("#### 📊 Grafik Perbandingan vs Baku Mutu")
    fig = buat_grafik(bod, cod)
    st.pyplot(fig, use_container_width=True)

    # Ekspor PDF
    st.markdown("---")
    pdf_buf = buat_pdf(bod, cod, metode_label, skor, kategori, fig)
    if pdf_buf:
        fname = f"IKA_BOD_COD_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        st.download_button(
            label="📄 UNDUH LAPORAN PDF",
            data=pdf_buf,
            file_name=fname,
            mime="application/pdf",
            use_container_width=True
        )
    else:
        st.info("💡 Install `fpdf2` untuk mengaktifkan ekspor PDF: `pip install fpdf2`")
