import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Queueing Model Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed" # Start with sidebar collapsed for cleaner look
)

# ---------------------------------------------------------
# CUSTOM CSS FOR MODERN DESIGN
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Metrics Cards Styling */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
    }
    
    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 2rem;
    }
    
    /* Custom container for inputs */
    .input-card {
        background-color: white;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    
    /* Modern Slider/Input Styling */
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #ced4da;
    }
    
    /* Title Styling */
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #6c757d;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR - INPUTS (Modernized)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    st.markdown("#### Input Parameters")
    
    col_lambda, col_mu = st.columns(2)
    with col_lambda:
        lambda_input = st.number_input(
            "λ (Arrivals/hr)", 
            min_value=0.1, 
            value=8.0, 
            step=0.5,
            key="lambda_val"
        )
    with col_mu:
        mu_input = st.number_input(
            "μ (Service/hr)", 
            min_value=0.1, 
            value=9.0, 
            step=0.5,
            key="mu_val"
        )
    
    st.markdown("---")
    
    # Explanation of parameters in minimal text
    st.caption("""
    **Traffic Intensity (ρ)** = λ / μ  
    ρ < 1 for stable system.
    """)
    
    rho = lambda_input / mu_input
    
    # Visual indicator for stability
    if rho >= 1:
        st.error("⚠️ System Unstable")
    else:
        st.success(f"✓ System Stable (ρ = {rho:.2f})")

# ---------------------------------------------------------
# MAIN CONTENT
# ---------------------------------------------------------
st.markdown('<p class="hero-title">M/M/1 Queue Calculator</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Analyze single-server queuing system performance metrics</p>', unsafe_allow_html=True)

# ---------------------------------------------------------
# STABILITY CHECK
# ---------------------------------------------------------
if rho >= 1.0:
    st.error(f"⚠️ The system is unstable because λ ({lambda_input}) ≥ μ ({mu_input}). The queue will grow infinitely.")
else:
    # ==========================================================
    # METRICS DASHBOARD (Top Row)
    # ==========================================================
    
    # Calculations
    p0 = 1 - rho
    L_q = (rho**2) / p0
    L_s = L_q + rho
    
    W_s = 1 / (mu_input - lambda_input)
    W_q = rho / (mu_input - lambda_input)
    
    # Display Metrics
    m1, m2, m3, m4 = st.columns(4)
    
    m1.metric(
        label="Expected in System (Ls)", 
        value=f"{L_s:.2f}", 
        delta_color="normal"
    )
    m2.metric(
        label="Expected in Queue (Lq)", 
        value=f"{L_q:.2f}"
    )
    m3.metric(
        label="Wait in System (Ws)", 
        value=f"{W_s:.2f} hrs", 
        delta=f"{W_s*60:.1f} min"
    )
    m4.metric(
        label="Wait in Queue (Wq)", 
        value=f"{W_q:.2f} hrs", 
        delta=f"{W_q*60:.1f} min"
    )

    # ==========================================================
    # DETAILED ANALYSIS (Two Columns)
    # ==========================================================
    st.markdown("---")
    
    col_detail1, col_detail2 = st.columns([2, 1])
    
    with col_detail1:
        st.subheader("Probability Distribution")
        
        # Generate Chart Data
        n_range = 20
        n_values = list(range(0, n_range))
        p_values = [p0 * (rho**n) for n in n_values]
        
        df = pd.DataFrame({
            "People (n)": n_values,
            "Probability": p_values
        })
        
        # Modern Bar Chart
        st.bar_chart(
            data=df.set_index("People (n)"), 
            color="#4e8cff",
            height=350
        )
        
    with col_detail2:
        st.subheader("Quick Stats")
        
        st.markdown("##### System Utilization")
        st.progress(rho)
        st.caption(f"Server busy **{rho*100:.1f}%** of the time")
        
        st.markdown("##### Probability Queries")
        
        # P0
        st.markdown(f"**P(Empty)**")
        st.write(f"{p0:.2%}")
        
        # P(N>=2) = 1 - P0 - P1
        p_n1 = p0 * rho
        p_n_gt_2 = 1 - p0 - p_n1
        st.markdown(f"**P(Queue ≥ 1)**")
        st.write(f"{p_n_gt_2:.2%}")
        
        # Specific query example: Prob of exactly 5 people
        p_5 = p0 * (rho**5)
        st.markdown(f"**P(n = 5)**")
        st.write(f"{p_5:.4f}")

# ---------------------------------------------------------
# INPUT SECTION (Bottom Card - For user reference)
# ---------------------------------------------------------
with st.expander("ℹ️ How to use inputs", expanded=False):
    st.write("""
    **λ (Lambda):** Average number of arrivals per hour.
    
    **μ (Mu):** Average number of people served per hour.
    
    *Example: If λ=8 and μ=9, on average 8 people arrive every hour, and the server can serve 9 people per hour.*
    """)