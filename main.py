import streamlit as st
from prediction_helper import predict

st.set_page_config(page_title="Abhishek Finance: Credit Risk", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600;700&display=swap');

/* ══════════════════════════════════════════════
   FORCE DARK EVERYTHING — NO STREAMLIT DEFAULTS
══════════════════════════════════════════════ */

/* Page background */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
.stApp,
.block-container,
section.main,
div.main,
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stBottom"],
[data-testid="stStatusWidget"],
footer, header {
    background-color: #0f1729 !important;
    background: #0f1729 !important;
    color: #e2e8f0 !important;
    border-color: transparent !important;
}

.block-container {
    padding-top: 0.5rem !important;
    max-width: 1100px !important;
}

/* Hide all Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    visibility: hidden !important;
    display: none !important;
}

/* ══════════════════════════════════════════════
   NUMBER INPUTS — HARDCODED DARK
══════════════════════════════════════════════ */
div[data-testid="stNumberInput"],
div[data-testid="stNumberInput"] > label,
div[data-testid="stNumberInput"] > div,
div[data-testid="stNumberInput"] > div > div,
div[data-testid="stNumberInput"] > div > div > div {
    background-color: #1a2236 !important;
    background: #1a2236 !important;
}

div[data-testid="stNumberInput"] > div > div {
    border: 1.5px solid #2d3f5e !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
div[data-testid="stNumberInput"] > div > div:focus-within {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.18) !important;
}

/* THE INPUT TEXT — force white with every possible override */
div[data-testid="stNumberInput"] input,
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stNumberInput"] input:active,
div[data-testid="stNumberInput"] input:hover {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background-color: #1a2236 !important;
    background: #1a2236 !important;
    caret-color: #3b82f6 !important;
    font-size: 0.97rem !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

/* +/- buttons */
div[data-testid="stNumberInput"] button {
    background-color: #243048 !important;
    background: #243048 !important;
    color: #94a3b8 !important;
    border: none !important;
    border-radius: 7px !important;
}
div[data-testid="stNumberInput"] button:hover {
    background-color: #2d3f5e !important;
    background: #2d3f5e !important;
    color: #ffffff !important;
}
div[data-testid="stNumberInput"] button svg,
div[data-testid="stNumberInput"] button p {
    fill: #94a3b8 !important;
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
}

/* ══════════════════════════════════════════════
   SELECTBOX — HARDCODED DARK
══════════════════════════════════════════════ */
div[data-testid="stSelectbox"],
div[data-testid="stSelectbox"] > div,
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stSelectbox"] > div > div > div {
    background-color: #1a2236 !important;
    background: #1a2236 !important;
}
div[data-testid="stSelectbox"] > div > div {
    border: 1.5px solid #2d3f5e !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
    transition: border-color 0.2s !important;
}
div[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.18) !important;
}
/* Selected text — target every possible node Streamlit renders */
div[data-testid="stSelectbox"] span,
div[data-testid="stSelectbox"] p,
div[data-testid="stSelectbox"] div,
div[data-testid="stSelectbox"] input,
div[data-testid="stSelectbox"] * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background-color: transparent !important;
}
/* Re-allow background on the outer wrapper only */
div[data-testid="stSelectbox"] > div > div {
    background-color: #1a2236 !important;
    background: #1a2236 !important;
}
div[data-testid="stSelectbox"] svg {
    fill: #64748b !important;
    color: #64748b !important;
    -webkit-text-fill-color: unset !important;
}

/* Dropdown popup */
div[data-baseweb="popover"] > div,
ul[data-baseweb="menu"],
div[data-baseweb="select"] [role="listbox"],
div[role="listbox"] {
    background-color: #1a2236 !important;
    background: #1a2236 !important;
    border: 1px solid #2d3f5e !important;
    border-radius: 12px !important;
    box-shadow: 0 16px 48px rgba(0,0,0,0.6) !important;
}
li[role="option"],
div[role="option"] {
    background-color: #1a2236 !important;
    color: #cbd5e1 !important;
    -webkit-text-fill-color: #cbd5e1 !important;
    font-family: 'Inter', sans-serif !important;
}
li[role="option"]:hover,
div[role="option"]:hover,
li[aria-selected="true"],
div[aria-selected="true"] {
    background-color: #243048 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* ══════════════════════════════════════════════
   LABELS
══════════════════════════════════════════════ */
label[data-testid="stWidgetLabel"] p,
div[data-testid="stWidgetLabel"] p,
label p {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
}

/* ══════════════════════════════════════════════
   SPINNER
══════════════════════════════════════════════ */
div[data-testid="stSpinner"] > div,
div[data-testid="stSpinner"] p {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
}

/* ══════════════════════════════════════════════
   HERO
══════════════════════════════════════════════ */
.hero {
    text-align: center;
    padding: 2rem 1rem 1.6rem;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: rgba(59,130,246,0.1);
    border: 1.5px solid rgba(59,130,246,0.3);
    color: #60a5fa;
    font-size: 0.67rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    padding: 0.3rem 1rem;
    border-radius: 100px;
    margin-bottom: 1rem;
}
.hero-dot {
    width: 7px; height: 7px;
    background: #3b82f6;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; box-shadow:0 0 0 0 rgba(59,130,246,0.5); }
    50%      { opacity:0.6; box-shadow:0 0 0 5px rgba(59,130,246,0); }
}
.hero-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 700;
    background: linear-gradient(135deg, #e2e8f0 20%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}
.hero-subtitle {
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.1rem, 2.2vw, 1.4rem);
    color: #cbd5e1;
    margin-bottom: 0.55rem;
    font-weight: 600;
}
.hero-desc { color: #94a3b8; font-size: 0.95rem; font-weight: 400; }

/* ══════════════════════════════════════════════
   SECTION LABELS
══════════════════════════════════════════════ */
.section-label {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #3b82f6;
    margin: 1.6rem 0 0.4rem;
    display: flex;
    align-items: center;
    gap: 0.55rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, rgba(59,130,246,0.4), transparent);
}

/* ══════════════════════════════════════════════
   LOAN-TO-INCOME BOX
══════════════════════════════════════════════ */
.ratio-outer { display:flex; flex-direction:column; gap:0.22rem; }
.ratio-lbl {
    color: #64748b;
    font-size: 0.71rem;
    font-weight: 600;
    letter-spacing: 0.09em;
    text-transform: uppercase;
}
.ratio-display {
    background: #1a2236;
    border: 1.5px solid #2d3f5e;
    border-radius: 12px;
    padding: 0.55rem 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 46px;
}
.ratio-num { font-size: 1.05rem; font-weight: 700; font-family: 'Inter', sans-serif; }
.ratio-tag {
    font-size: 0.75rem; font-weight: 700;
    letter-spacing: 0.04em; text-transform: uppercase;
    padding: 0.25rem 0.75rem; border-radius: 100px;
}
.tg-good   { background:rgba(22,163,74,0.15);  color:#4ade80; border:1px solid rgba(74,222,128,0.3); }
.tg-warn   { background:rgba(217,119,6,0.15);  color:#fbbf24; border:1px solid rgba(251,191,36,0.3); }
.tg-bad    { background:rgba(220,38,38,0.15);  color:#f87171; border:1px solid rgba(248,113,113,0.3); }

/* ══════════════════════════════════════════════
   BUTTON
══════════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.93rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    width: 100% !important;
    transition: all 0.22s ease !important;
    box-shadow: 0 4px 20px rgba(59,130,246,0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 32px rgba(59,130,246,0.5) !important;
}
.stButton > button p,
.stButton > button span {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* ══════════════════════════════════════════════
   RESULT CARDS
══════════════════════════════════════════════ */
.results-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-top: 0.8rem;
}
.result-card {
    background: #141e2e;
    border: 1px solid #2d3f5e;
    border-radius: 18px;
    padding: 1.75rem 1.4rem 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    transition: transform 0.2s, box-shadow 0.2s;
}
.result-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 14px 40px rgba(0,0,0,0.45);
}
.rc-accent { position:absolute; top:0; left:0; right:0; height:4px; }
.rc-icon { font-size: 1.6rem; margin-bottom: 0.5rem; line-height: 1; }
.rc-label {
    color: #94a3b8;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.55rem;
}
.rc-value {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.65rem;
}
.rc-sub {
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    padding: 0.35rem 1.1rem;
    border-radius: 100px;
    display: inline-block;
}
.c-green  { color:#4ade80; }
.c-yellow { color:#fbbf24; }
.c-red    { color:#f87171; }
.c-blue   { color:#60a5fa; }
.s-green  { background:rgba(74,222,128,0.12); color:#4ade80; border:1px solid rgba(74,222,128,0.25); }
.s-yellow { background:rgba(251,191,36,0.12); color:#fbbf24; border:1px solid rgba(251,191,36,0.25); }
.s-red    { background:rgba(248,113,113,0.12);color:#f87171; border:1px solid rgba(248,113,113,0.25); }
.s-blue   { background:rgba(96,165,250,0.12); color:#60a5fa; border:1px solid rgba(96,165,250,0.25); }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0f1729; }
::-webkit-scrollbar-thumb { background: #2d3f5e; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #3b82f6; }
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge"><span class="hero-dot"></span>&nbsp;ML-Powered Risk Engine</div>
  <div class="hero-title">Abhishek Finance</div>
  <div class="hero-subtitle">Credit Risk Modelling</div>
  <div class="hero-desc">Enter borrower details to generate an instant ML-driven credit risk assessment</div>
</div>
""", unsafe_allow_html=True)

# ── SECTION 1: Borrower Profile ───────────────────────────────────
st.markdown('<div class="section-label">01 &mdash; Borrower Profile</div>', unsafe_allow_html=True)
row1 = st.columns(3, gap="medium")
with row1[0]:
    age = st.number_input('Age (years)', min_value=18, step=1, max_value=100, value=28)
with row1[1]:
    income = st.number_input('Annual Income (₹)', min_value=0, value=1200000, step=10000)
with row1[2]:
    loan_amount = st.number_input('Loan Amount (₹)', min_value=0, value=2560000, step=10000)

# ── SECTION 2: Loan Details ───────────────────────────────────────
st.markdown('<div class="section-label">02 &mdash; Loan Details</div>', unsafe_allow_html=True)

loan_to_income_ratio = loan_amount / income if income > 0 else 0
if loan_to_income_ratio <= 2:
    r_color, r_tag_cls, r_tag = "#4ade80", "tg-good", "Healthy"
elif loan_to_income_ratio <= 5:
    r_color, r_tag_cls, r_tag = "#fbbf24", "tg-warn", "Moderate"
else:
    r_color, r_tag_cls, r_tag = "#f87171", "tg-bad", "High Risk"

row2 = st.columns(3, gap="medium")
with row2[0]:
    st.markdown(f"""
    <div class="ratio-outer">
      <div class="ratio-lbl">Loan to Income Ratio</div>
      <div class="ratio-display">
        <span class="ratio-num" style="color:{r_color};">{loan_to_income_ratio:.2f}&times;</span>
        <span class="ratio-tag {r_tag_cls}">{r_tag}</span>
      </div>
    </div>
    <div style="height:0.4rem"></div>
    """, unsafe_allow_html=True)
with row2[1]:
    loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=0, step=1, value=36)
with row2[2]:
    avg_dpd_per_delinquency = st.number_input('Avg DPD', min_value=0, value=20)

# ── SECTION 3: Risk Indicators ────────────────────────────────────
st.markdown('<div class="section-label">03 &mdash; Risk Indicators</div>', unsafe_allow_html=True)
row3 = st.columns(3, gap="medium")
with row3[0]:
    delinquency_ratio = st.number_input('Delinquency Ratio (%)', min_value=0, max_value=100, step=1, value=30)
with row3[1]:
    credit_utilization_ratio = st.number_input('Credit Utilization Ratio (%)', min_value=0, max_value=100, step=1, value=30)
with row3[2]:
    num_open_accounts = st.number_input('Open Loan Accounts', min_value=1, max_value=4, step=1, value=2)

# ── SECTION 4: Loan Classification ───────────────────────────────
st.markdown('<div class="section-label">04 &mdash; Loan Classification</div>', unsafe_allow_html=True)
row4 = st.columns(3, gap="medium")
with row4[0]:
    residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'])
with row4[1]:
    loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'])
with row4[2]:
    loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'])

# ── BUTTON ────────────────────────────────────────────────────────
st.markdown('<br>', unsafe_allow_html=True)
_, col_m, _ = st.columns([1, 2, 1])
with col_m:
    calculate = st.button('⚡  Calculate Risk Assessment')

# ── RESULTS ───────────────────────────────────────────────────────
if calculate:
    with st.spinner('Analysing risk profile...'):
        probability, credit_score, rating = predict(
            age, income, loan_amount, loan_tenure_months,
            avg_dpd_per_delinquency, delinquency_ratio,
            credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type
        )

    prob_pct = probability * 100

    # ── Probability
    if prob_pct > 60:
        pc, ps, pt, pi = "c-red",    "s-red",    "High Risk",   "🔴"
        pa = "background:linear-gradient(90deg,#f87171,#dc2626);"
    elif prob_pct > 30:
        pc, ps, pt, pi = "c-yellow", "s-yellow", "Medium Risk", "🟡"
        pa = "background:linear-gradient(90deg,#fbbf24,#d97706);"
    else:
        pc, ps, pt, pi = "c-green",  "s-green",  "Low Risk",    "🟢"
        pa = "background:linear-gradient(90deg,#4ade80,#16a34a);"

    # ── Credit Score
    if credit_score < 580:
        sc, ss, st_, si = "c-red",    "s-red",    "Poor",      "📉"
        sa = "background:linear-gradient(90deg,#f87171,#dc2626);"
    elif credit_score < 670:
        sc, ss, st_, si = "c-yellow", "s-yellow", "Fair",      "📊"
        sa = "background:linear-gradient(90deg,#fbbf24,#d97706);"
    elif credit_score < 740:
        sc, ss, st_, si = "c-green",  "s-green",  "Good",      "📈"
        sa = "background:linear-gradient(90deg,#4ade80,#16a34a);"
    else:
        sc, ss, st_, si = "c-blue",   "s-blue",   "Excellent", "⭐"
        sa = "background:linear-gradient(90deg,#60a5fa,#2563eb);"

    # ── Rating: match full word returned by predict()
    # Covers: "Excellent","Good","Average","Fair","Poor","Very Poor","A","B","C","D"
    rl = rating.strip().lower() if rating else ""
    if rl in ("excellent", "a"):
        rc, rs, ri = "c-blue",   "s-blue",   "⭐"
        ra = "background:linear-gradient(90deg,#60a5fa,#2563eb);"
    elif rl in ("good", "b"):
        rc, rs, ri = "c-green",  "s-green",  "✅"
        ra = "background:linear-gradient(90deg,#4ade80,#16a34a);"
    elif rl in ("average", "fair", "c"):
        rc, rs, ri = "c-yellow", "s-yellow", "📊"
        ra = "background:linear-gradient(90deg,#fbbf24,#d97706);"
    elif rl in ("poor", "d"):
        rc, rs, ri = "c-red",    "s-red",    "⚠️"
        ra = "background:linear-gradient(90deg,#f87171,#dc2626);"
    else:
        rc, rs, ri = "c-red",    "s-red",    "❌"
        ra = "background:linear-gradient(90deg,#f87171,#dc2626);"

    st.markdown('<div class="section-label">05 &mdash; Risk Assessment Results</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="results-grid">
      <div class="result-card">
        <div class="rc-accent" style="{pa}"></div>
        <div class="rc-icon">{pi}</div>
        <div class="rc-label">Default Probability</div>
        <div class="rc-value {pc}">{prob_pct:.1f}%</div>
        <span class="rc-sub {ps}">{pt}</span>
      </div>
      <div class="result-card">
        <div class="rc-accent" style="{sa}"></div>
        <div class="rc-icon">{si}</div>
        <div class="rc-label">Credit Score</div>
        <div class="rc-value {sc}">{credit_score}</div>
        <span class="rc-sub {ss}">{st_}</span>
      </div>
      <div class="result-card">
        <div class="rc-accent" style="{ra}"></div>
        <div class="rc-icon">{ri}</div>
        <div class="rc-label">Credit Rating</div>
        <div class="rc-value {rc}">{rating}</div>
        <span class="rc-sub {rs}">Risk Category</span>
      </div>
    </div>
    """, unsafe_allow_html=True)