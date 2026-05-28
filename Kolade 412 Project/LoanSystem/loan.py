import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime
from dataclasses import dataclass

st.set_page_config(
    page_title="NeoLoan",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Global font */
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* Page background */
.stApp { background: #f0f2f8; }
.block-container { padding: 0 2.5rem 3rem !important; max-width: 1380px; }

/* Hide Streamlit default chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
    border-radius: 0 0 28px 28px;
    padding: 2.8rem 3rem 2.6rem;
    margin: 0 -2.5rem 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 8px 40px rgba(67,56,202,.25);
}
.hero-left { display: flex; align-items: center; gap: 1.2rem; }
.hero-icon {
    width: 56px; height: 56px;
    background: rgba(255,255,255,.15);
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.8rem;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,.2);
}
.hero-title { font-size: 2.2rem; font-weight: 800; color: #fff; margin: 0; letter-spacing: -0.5px; }
.hero-sub { font-size: 0.9rem; color: rgba(255,255,255,.65); font-weight: 400; margin-top: 2px; }
.hero-badge {
    background: rgba(255,255,255,.12);
    border: 1px solid rgba(255,255,255,.2);
    color: rgba(255,255,255,.9);
    padding: 0.45rem 1rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 500;
    backdrop-filter: blur(8px);
}

/* ── Section label ── */
.section-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 0.6rem;
}

/* ── Input cards ── */
.input-card {
    background: #fff;
    border-radius: 20px;
    padding: 1.6rem 1.8rem 1.4rem;
    border: 1px solid #e0e3ef;
    box-shadow: 0 2px 12px rgba(0,0,0,.04);
    margin-bottom: 1rem;
}
.input-card-title {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #4f46e5;
    padding-bottom: 0.9rem;
    margin-bottom: 0.2rem;
    border-bottom: 2px solid #eef0fb;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

/* ── KPI cards ── */
.kpi-row { display: flex; gap: 1rem; margin-bottom: 0.5rem; }
.kpi-card {
    flex: 1;
    background: #fff;
    border-radius: 20px;
    padding: 1.5rem 1.6rem;
    border: 1px solid #e0e3ef;
    box-shadow: 0 2px 12px rgba(0,0,0,.04);
    position: relative;
    overflow: hidden;
    transition: transform .18s ease, box-shadow .18s ease;
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 28px rgba(0,0,0,.09); }
.kpi-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: var(--kpi-color, #4f46e5);
    border-radius: 20px 20px 0 0;
}
.kpi-icon {
    font-size: 1.5rem;
    margin-bottom: 0.7rem;
    display: block;
}
.kpi-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 0.35rem;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
    line-height: 1;
}
.kpi-sub {
    font-size: 0.78rem;
    color: #94a3b8;
    margin-top: 0.4rem;
    font-weight: 500;
}
.kpi-tag {
    display: inline-block;
    background: #f0fdf4;
    color: #16a34a;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.2em 0.6em;
    border-radius: 999px;
    margin-top: 0.5rem;
    border: 1px solid #bbf7d0;
}

/* ── Chart card ── */
.chart-card {
    background: #fff;
    border-radius: 20px;
    padding: 1.4rem 1.6rem 0.6rem;
    border: 1px solid #e0e3ef;
    box-shadow: 0 2px 12px rgba(0,0,0,.04);
    margin-bottom: 1rem;
}

/* ── Divider ── */
hr[data-testid="stDivider"] {
    border-color: #e0e3ef !important;
    margin: 1.6rem 0 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #e8eaf6;
    border-radius: 14px;
    padding: 4px;
    gap: 3px;
    border: none !important;
    box-shadow: none !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    font-size: 0.88rem;
    font-weight: 600;
    color: #64748b;
    padding: 0.48rem 1.3rem;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    color: #1e1b4b !important;
    box-shadow: 0 1px 6px rgba(0,0,0,.1) !important;
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.4rem !important; }

/* ── Buttons ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    padding: 0.65rem 1.4rem !important;
    box-shadow: 0 4px 16px rgba(79,70,229,.35) !important;
    letter-spacing: 0.01em !important;
    transition: all .2s ease !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 6px 22px rgba(79,70,229,.45) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:not([kind="primary"]) {
    border-radius: 10px !important;
    border-color: #c7d2fe !important;
    color: #4f46e5 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    border-color: #c7d2fe !important;
    color: #4f46e5 !important;
}

/* ── Inputs & selects ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    border-radius: 10px !important;
    border-color: #e0e3ef !important;
    font-weight: 500 !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,.15) !important;
}

/* ── Slider ── */
[data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(90deg, #6366f1, #818cf8) !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    border-radius: 10px !important;
    border-color: #e0e3ef !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden;
    border: 1px solid #e0e3ef !important;
}

/* ── Metric (native st.metric) ── */
[data-testid="stMetric"] {
    background: white;
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    border: 1px solid #e0e3ef;
    box-shadow: 0 2px 10px rgba(0,0,0,.04);
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #94a3b8 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    letter-spacing: -0.3px !important;
}

/* ── Success alert ── */
.stAlert { border-radius: 12px !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: white !important;
    border-right: 1px solid #e0e3ef !important;
}

/* ── Subheader ── */
h3 { color: #1e1b4b !important; font-weight: 700 !important; }
h2 { color: #1e1b4b !important; font-weight: 800 !important; }

/* ── Extra payments row card ── */
.extras-card {
    background: linear-gradient(135deg, #eef2ff 0%, #f5f3ff 100%);
    border-radius: 18px;
    padding: 1.4rem 1.8rem;
    border: 1px solid #c7d2fe;
    margin-bottom: 0.5rem;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: #94a3b8;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.04em;
}
</style>
""", unsafe_allow_html=True)


# ── Domain types ──────────────────────────────────────────────────────────────
@dataclass
class LoanResult:
    periodic_payment: float
    total_paid: float
    total_interest: float
    total_principal: float
    total_fees: float
    total_extra: float
    periods: int
    schedule: pd.DataFrame
    periods_saved: int


# ── Core calculation ──────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def calculate_loan(
    principal: float,
    annual_rate: float,
    term_years: int,
    compounds_per_year: int,
    payments_per_year: int,
    extra_monthly: float,
    extra_start_month: int,
    processing_fee_pct: float,
    payment_method: str,
) -> LoanResult:
    """Compute a full amortisation schedule and summary metrics."""
    period_rate = annual_rate / 100 / compounds_per_year
    total_periods = term_years * payments_per_year
    total_principal = principal * (1 + processing_fee_pct / 100)
    total_fees = principal * processing_fee_pct / 100

    if period_rate > 0:
        pmt = (
            total_principal
            * (period_rate * (1 + period_rate) ** total_periods)
            / ((1 + period_rate) ** total_periods - 1)
        )
    else:
        pmt = total_principal / total_periods

    balance = total_principal
    rows: list[dict] = []
    total_interest = 0.0
    total_extra_paid = 0.0
    extra_threshold = extra_start_month * (payments_per_year / 12)
    start_date = datetime.date(datetime.date.today().year, 1, 1)

    for period in range(1, int(total_periods) + 1):
        interest = balance * period_rate
        extra = 0.0

        if extra_monthly > 0 and period >= extra_threshold:
            extra = extra_monthly * (payments_per_year / 12)
            total_extra_paid += extra

        if payment_method == "Aggressive Payoff":
            principal_pmt = min(balance, (pmt - interest) + extra * 1.5)
        else:
            principal_pmt = (pmt - interest) + extra

        balance = max(0.0, balance - principal_pmt)
        total_interest += interest

        rows.append({
            "Period": period,
            "Date": start_date + datetime.timedelta(days=30 * period),
            "Payment": round(pmt, 2),
            "Interest": round(interest, 2),
            "Principal": round(principal_pmt, 2),
            "Extra": round(extra, 2),
            "Balance": round(balance, 2),
            "Cumulative Interest": 0.0,
        })

        if balance <= 0:
            break

    df = pd.DataFrame(rows)
    df["Cumulative Interest"] = df["Interest"].cumsum().round(2)
    total_paid = df["Payment"].sum()
    periods_saved = max(0, int(total_periods) - len(df))

    return LoanResult(
        periodic_payment=pmt,
        total_paid=total_paid,
        total_interest=total_interest,
        total_principal=total_principal,
        total_fees=total_fees,
        total_extra=total_extra_paid,
        periods=len(df),
        schedule=df,
        periods_saved=periods_saved,
    )


# ── Helpers ───────────────────────────────────────────────────────────────────
PAYMENT_FREQ_MAP = {"Monthly": 12, "Bi-weekly": 26, "Weekly": 52}
COMP_FREQ_MAP = {"Monthly": 12, "Quarterly": 4, "Bi-weekly": 26, "Weekly": 52, "Daily": 365}

CHART_COLORS = {
    "indigo": "#6366f1",
    "emerald": "#10b981",
    "rose": "#f43f5e",
    "amber": "#f59e0b",
    "sky": "#0ea5e9",
    "violet": "#8b5cf6",
}

CHART_TITLE = dict(font=dict(size=14, color="#1e1b4b"), pad=dict(b=12))

CHART_BASE = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#475569", size=12),
    margin=dict(l=0, r=0, t=48, b=0),
    legend=dict(orientation="h", y=-0.18, x=0, font=dict(size=11)),
    hoverlabel=dict(bgcolor="white", bordercolor="#e0e3ef", font_color="#0f172a", font_size=13),
    xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=11)),
    yaxis=dict(showgrid=True, gridcolor="#f1f5f9", zeroline=False, tickfont=dict(size=11)),
)


def period_label(payments_per_year: int) -> str:
    return {12: "Monthly", 26: "Bi-weekly", 52: "Weekly"}.get(payments_per_year, "Periodic")


def months_saved(result: LoanResult, payments_per_year: int) -> int:
    return round(result.periods_saved * 12 / payments_per_year)


# ── Charts ────────────────────────────────────────────────────────────────────
def chart_balance(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure(go.Scatter(
        x=df["Date"], y=df["Balance"],
        fill="tozeroy",
        fillcolor="rgba(99,102,241,.08)",
        line=dict(color=CHART_COLORS["indigo"], width=2.5),
        name="Remaining Balance",
        hovertemplate="<b>%{x|%b %Y}</b><br>Balance: $%{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="Loan Balance Over Time", **CHART_TITLE),
        yaxis_tickprefix="$", yaxis_tickformat=",.0f",
        **CHART_BASE,
    )
    return fig


def chart_breakdown(result: LoanResult, original_principal: float) -> go.Figure:
    labels = ["Principal", "Interest", "Processing Fee"]
    values = [original_principal, result.total_interest, result.total_fees]
    colors = [CHART_COLORS["emerald"], CHART_COLORS["rose"], CHART_COLORS["amber"]]
    if result.total_extra > 0:
        labels.append("Extra Payments")
        values.append(result.total_extra)
        colors.append(CHART_COLORS["sky"])

    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.58,
        marker=dict(colors=colors, line=dict(color="white", width=3)),
        textinfo="label+percent",
        insidetextorientation="radial",
        hovertemplate="<b>%{label}</b><br>$%{value:,.0f} (%{percent})<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="Total Cost Breakdown", **CHART_TITLE),
        showlegend=False,
        **{k: v for k, v in CHART_BASE.items() if k not in ("xaxis", "yaxis", "legend", "margin")},
        margin=dict(l=0, r=0, t=48, b=40),
    )
    return fig


def chart_cumulative(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["Principal"].cumsum(),
        fill="tozeroy",
        fillcolor="rgba(16,185,129,.09)",
        line=dict(color=CHART_COLORS["emerald"], width=2.5),
        name="Cumulative Principal",
        hovertemplate="$%{y:,.0f}<extra>Principal</extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["Cumulative Interest"],
        fill="tozeroy",
        fillcolor="rgba(244,63,94,.07)",
        line=dict(color=CHART_COLORS["rose"], width=2.5),
        name="Cumulative Interest",
        hovertemplate="$%{y:,.0f}<extra>Interest</extra>",
    ))
    fig.update_layout(
        title=dict(text="Cumulative Principal vs Interest", **CHART_TITLE),
        yaxis_tickprefix="$", yaxis_tickformat=",.0f",
        **CHART_BASE,
    )
    return fig


def chart_composition(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["Date"], y=df["Principal"],
        name="Principal",
        marker_color=CHART_COLORS["emerald"],
        marker_line_width=0,
        opacity=0.9,
    ))
    fig.add_trace(go.Bar(
        x=df["Date"], y=df["Interest"],
        name="Interest",
        marker_color=CHART_COLORS["rose"],
        marker_line_width=0,
        opacity=0.9,
    ))
    fig.update_layout(
        barmode="stack",
        title=dict(text="Payment Composition Per Period", **CHART_TITLE),
        yaxis_tickprefix="$", yaxis_tickformat=",.0f",
        bargap=0.1,
        **CHART_BASE,
    )
    return fig


# ── Session state ─────────────────────────────────────────────────────────────
if "saved_loans" not in st.session_state:
    st.session_state.saved_loans = []


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📂 Saved Scenarios")
    if not st.session_state.saved_loans:
        st.caption("No scenarios saved yet. Go to the **Compare** tab to save one.")
    else:
        for i, loan in enumerate(reversed(st.session_state.saved_loans[-8:])):
            idx = len(st.session_state.saved_loans) - i
            with st.expander(f"#{idx} — ${loan['principal']:,.0f} @ {loan['rate']}%"):
                st.metric("Payment", f"${loan['monthly_payment']:,.0f}")
                st.metric("Total Interest", f"${loan['total_interest']:,.0f}")
                st.caption(f"{loan['term']} yr · saved {loan['saved_at']}")
        if st.button("Clear all", use_container_width=True):
            st.session_state.saved_loans = []
            st.rerun()


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-left">
    <div class="hero-icon">💎</div>
    <div>
      <div class="hero-title">NeoLoan</div>
      <div class="hero-sub">Advanced compound-interest loan calculator</div>
    </div>
  </div>
  <div class="hero-badge">Results update live</div>
</div>
""", unsafe_allow_html=True)


# ── Input section ─────────────────────────────────────────────────────────────
col_l, col_r = st.columns(2, gap="large")

with col_l:
    st.markdown('<div class="input-card"><div class="input-card-title">💰 Loan Details</div>', unsafe_allow_html=True)
    principal = st.number_input(
        "Loan Amount ($)", min_value=1_000.0, max_value=5_000_000.0,
        value=100_000.0, step=1_000.0, format="%.0f",
    )
    annual_rate = st.slider("Annual Interest Rate (%)", 0.0, 30.0, 7.5, 0.05)
    term_years = st.slider("Loan Term (Years)", 1, 40, 30)
    st.markdown("</div>", unsafe_allow_html=True)

with col_r:
    st.markdown('<div class="input-card"><div class="input-card-title">⚙️ Advanced Options</div>', unsafe_allow_html=True)
    comp_freq = st.selectbox("Compounding Frequency", list(COMP_FREQ_MAP.keys()))
    compounds_per_year = COMP_FREQ_MAP[comp_freq]

    payment_freq = st.selectbox("Payment Frequency", list(PAYMENT_FREQ_MAP.keys()))
    payments_per_year = PAYMENT_FREQ_MAP[payment_freq]

    processing_fee = st.number_input(
        "Processing Fee (%)", min_value=0.0, max_value=5.0, value=1.0, step=0.1,
    )
    st.markdown("</div>", unsafe_allow_html=True)


# Extra payments
st.markdown('<div class="extras-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Extra Payments Strategy</div>', unsafe_allow_html=True)
ep1, ep2, ep3 = st.columns(3, gap="medium")
with ep1:
    extra_monthly = st.number_input("Extra Monthly Payment ($)", 0.0, 10_000.0, 0.0, 25.0)
with ep2:
    extra_start = st.slider("Start After (Months)", 0, 120, 0)
with ep3:
    strategy = st.selectbox(
        "Strategy",
        ["Apply to Principal", "Standard Allocation", "Aggressive Payoff"],
    )
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ── Live calculation ──────────────────────────────────────────────────────────
with st.spinner("Calculating…"):
    result = calculate_loan(
        principal, annual_rate, term_years,
        compounds_per_year, payments_per_year,
        extra_monthly, extra_start, processing_fee, strategy,
    )

freq = period_label(payments_per_year)
interest_pct = result.total_interest / result.total_principal * 100

# ── KPI cards (custom HTML) ───────────────────────────────────────────────────
if result.periods_saved > 0:
    saved_mo = months_saved(result, payments_per_year)
    time_saved_value = f"{saved_mo} months"
    time_saved_sub = "ahead of schedule"
    time_saved_tag = True
else:
    time_saved_value = "—"
    time_saved_sub = "Add extra payments to save time"
    time_saved_tag = False

tag_html = '<span class="kpi-tag">✓ Ahead of schedule</span>' if time_saved_tag else ""

st.markdown(f"""
<div class="kpi-row">
  <div class="kpi-card" style="--kpi-color:#6366f1">
    <span class="kpi-icon">💳</span>
    <div class="kpi-label">{freq} Payment</div>
    <div class="kpi-value">${result.periodic_payment:,.2f}</div>
    <div class="kpi-sub">Every {freq.lower()} · {result.periods} periods total</div>
  </div>
  <div class="kpi-card" style="--kpi-color:#0ea5e9">
    <span class="kpi-icon">💰</span>
    <div class="kpi-label">Total Cost</div>
    <div class="kpi-value">${result.total_paid:,.0f}</div>
    <div class="kpi-sub">Principal + interest + fees</div>
  </div>
  <div class="kpi-card" style="--kpi-color:#f43f5e">
    <span class="kpi-icon">📈</span>
    <div class="kpi-label">Total Interest</div>
    <div class="kpi-value">${result.total_interest:,.0f}</div>
    <div class="kpi-sub">{interest_pct:.1f}% of loan amount</div>
  </div>
  <div class="kpi-card" style="--kpi-color:#10b981">
    <span class="kpi-icon">⏱️</span>
    <div class="kpi-label">Time Saved</div>
    <div class="kpi-value">{time_saved_value}</div>
    <div class="kpi-sub">{time_saved_sub}</div>
    {tag_html}
  </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_charts, tab_schedule, tab_compare = st.tabs(["📊  Charts", "📋  Schedule", "💾  Compare Scenarios"])

# ── Charts ────────────────────────────────────────────────────────────────────
with tab_charts:
    r1c1, r1c2 = st.columns(2, gap="medium")
    with r1c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(chart_balance(result.schedule), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)
    with r1c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(chart_breakdown(result, principal), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    r2c1, r2c2 = st.columns(2, gap="medium")
    with r2c1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(chart_cumulative(result.schedule), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)
    with r2c2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(chart_composition(result.schedule), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

# ── Schedule ──────────────────────────────────────────────────────────────────
with tab_schedule:
    view = st.radio(
        "Show",
        ["First 12 periods", "First 52 periods", "All periods"],
        horizontal=True,
        label_visibility="collapsed",
    )
    df_view = result.schedule[
        ["Date", "Payment", "Principal", "Interest", "Extra", "Balance", "Cumulative Interest"]
    ]
    if view == "First 12 periods":
        df_view = df_view.head(12)
    elif view == "First 52 periods":
        df_view = df_view.head(52)

    money_cfg = {
        c: st.column_config.NumberColumn(c, format="$%.2f")
        for c in ["Payment", "Principal", "Interest", "Extra", "Balance", "Cumulative Interest"]
    }
    st.dataframe(df_view, width="stretch", hide_index=True, column_config=money_cfg)

    st.download_button(
        "⬇️  Download Full Schedule (CSV)",
        data=result.schedule.to_csv(index=False),
        file_name=f"neoloan_{datetime.date.today()}.csv",
        mime="text/csv",
    )

# ── Compare scenarios ─────────────────────────────────────────────────────────
with tab_compare:
    st.subheader("Save & Compare Scenarios")
    sa, sb = st.columns([3, 1], gap="medium")
    with sa:
        label = st.text_input(
            "Scenario label",
            placeholder=f"{term_years}yr @ {annual_rate}% — ${principal:,.0f}",
        )
    with sb:
        st.write("")
        if st.button("💾  Save Scenario", type="primary", use_container_width=True):
            name = label.strip() or f"${principal:,.0f} @ {annual_rate}% ({term_years}yr)"
            st.session_state.saved_loans.append({
                "label": name,
                "principal": principal,
                "rate": annual_rate,
                "term": term_years,
                "monthly_payment": result.periodic_payment,
                "total_interest": result.total_interest,
                "total_paid": result.total_paid,
                "saved_at": datetime.datetime.now().strftime("%H:%M %d %b %Y"),
            })
            st.success(f"Saved: {name}")

    if st.session_state.saved_loans:
        st.divider()
        compare_df = pd.DataFrame(st.session_state.saved_loans)[[
            "label", "principal", "rate", "term",
            "monthly_payment", "total_interest", "total_paid",
        ]].rename(columns={
            "label": "Scenario",
            "principal": "Principal ($)",
            "rate": "Rate (%)",
            "term": "Term (yr)",
            "monthly_payment": "Payment ($)",
            "total_interest": "Total Interest ($)",
            "total_paid": "Total Paid ($)",
        })

        money_cols = ["Principal ($)", "Payment ($)", "Total Interest ($)", "Total Paid ($)"]
        cmp_cfg = {c: st.column_config.NumberColumn(c, format="$%.0f") for c in money_cols}
        st.dataframe(compare_df, width="stretch", hide_index=True, column_config=cmp_cfg)

        fig_cmp = go.Figure()
        fig_cmp.add_trace(go.Bar(
            name="Total Interest",
            x=compare_df["Scenario"],
            y=compare_df["Total Interest ($)"],
            marker_color=CHART_COLORS["rose"],
            marker_line_width=0,
            opacity=0.9,
        ))
        fig_cmp.add_trace(go.Bar(
            name="Principal",
            x=compare_df["Scenario"],
            y=compare_df["Principal ($)"],
            marker_color=CHART_COLORS["indigo"],
            marker_line_width=0,
            opacity=0.9,
        ))
        fig_cmp.update_layout(
            barmode="group",
            title=dict(text="Principal vs Total Interest by Scenario", **CHART_TITLE),
            yaxis_tickprefix="$",
            yaxis_tickformat=",.0f",
            bargap=0.25,
            bargroupgap=0.08,
            **CHART_BASE,
        )
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_cmp, width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🗑️  Clear all saved scenarios"):
            st.session_state.saved_loans = []
            st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">NeoLoan · Advanced Compound Interest Calculator · Built with Streamlit</div>',
    unsafe_allow_html=True,
)
