import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Random Number Generator",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# CUSTOM CSS FOR MODERN DESIGN
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* Metrics Cards Styling */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
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

    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR - INPUTS
# ---------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Algorithm Selection
    algorithm = st.selectbox(
        "Generation Method",
        ["Linear Congruential", "Middle Square"]
    )
    
    st.markdown("---")
    
    # Parameters based on selection
    if algorithm == "Linear Congruential":
        st.subheader("Parameters (Mixed Congruential)")
        
        X0 = st.number_input("Seed (X0)", min_value=0, value=27, step=1)
        a = st.number_input("Multiplier (a)", min_value=0, value=17, step=1)
        c = st.number_input("Increment (c)", min_value=0, value=43, step=1)
        m = st.number_input("Modulus (m)", min_value=1, value=100, step=1)
        
    else:  # Middle Square
        st.subheader("Parameters (Middle Square)")
        
        seed_digits = st.selectbox("Seed Digits", [4, 6, 8])
        X0 = st.number_input("Seed Value", min_value=0, value=1234, step=1)
        
    st.markdown("---")
    
    n_numbers = st.slider("How many numbers to generate?", 5, 100, 10)

# ---------------------------------------------------------
# MAIN CONTENT
# ---------------------------------------------------------
st.markdown('<p class="hero-title">Random Number Generator</p>', unsafe_allow_html=True)
st.markdown(f'<p class="hero-subtitle">Method: {algorithm}</p>', unsafe_allow_html=True)

# ---------------------------------------------------------
# GENERATION LOGIC
# ---------------------------------------------------------

def linear_congruential(X0, a, c, m, n):
    """Linear Congruential Method: Xi+1 = (a*Xi + c) mod m"""
    numbers = []
    seeds = []
    uniforms = []
    
    Xi = X0
    
    for _ in range(n):
        Xi_next = (a * Xi + c) % m
        
        Ri = Xi_next / m
        
        numbers.append(Xi_next)
        uniforms.append(round(Ri, 4))
        seeds.append(Xi)
        
        Xi = Xi_next
        
    return numbers, uniforms, seeds

def middle_square(seed_digits, X0, n):
    """Middle Square Method"""
    numbers = []
    seeds = []
    uniforms = []
    
    Xi = X0
    
    # Determine padding length based on digits
    digits = seed_digits
    padding = 10 ** digits
    
    for _ in range(n):
        # Square the current value
        sq = Xi ** 2
        
        # Convert to string and pad with zeros to ensure we can extract middle
        sq_str = str(sq).zfill(digits * 2)
        
        # Extract middle digits
        start_idx = (len(sq_str) - digits) // 2
        Xi_next = int(sq_str[start_idx : start_idx + digits])
        
        # If result is 0, we can't divide, so just store 0
        if Xi_next == 0:
            Ri = 0
        else:
            Ri = Xi_next / (10 ** digits)
        
        numbers.append(Xi_next)
        uniforms.append(round(Ri, 4))
        seeds.append(Xi)
        
        Xi = Xi_next
        
    return numbers, uniforms, seeds

# ---------------------------------------------------------
# CALCULATION & DISPLAY
# ---------------------------------------------------------

try:
    if algorithm == "Linear Congruential":
        nums, unis, seeds = linear_congruential(X0, a, c, m, n_numbers)
    else:
        nums, unis, seeds = middle_square(seed_digits, X0, n_numbers)
        
    # Create DataFrame
    df = pd.DataFrame({
        "Iteration": range(1, n_numbers + 1),
        "Seed (Xi)": seeds,
        "Random Integer (Xi+1)": nums,
        "Uniform Random (Ri)": unis
    })
    
    # Display Metrics
    m1, m2 = st.columns(2)
    
    m1.metric("Generated Count", n_numbers)
    m2.metric("Unique Values", len(set(nums)))

    # Display Tabs - FIXED syntax here
    tab1, tab2 = st.tabs(["📋 Data Table", "📈 Visualization"])
    
    with tab1:
        st.dataframe(df, use_container_width=True, hide_index=True)
        
    with tab2:
        # Bar chart of Random Integers
        st.bar_chart(df.set_index("Iteration")["Random Integer (Xi+1)"], color="#FF4B4B", height=350)
        
    # Stats Expander
    with st.expander("📊 Statistics Summary"):
        st.write(f"**Min:** {min(nums)} | **Max:** {max(nums)} | **Average:** {round(sum(nums)/len(nums), 2)}")

except Exception as e:
    st.error(f"An error occurred: {e}")

# ---------------------------------------------------------
# HELPER INFO
# ---------------------------------------------------------
with st.expander("ℹ️ Input Help", expanded=False):
    if algorithm == "Linear Congruential":
        st.markdown("""
        **Formula:** Xi+1 = (a × Xi + c) mod m
        
        - **Seed:** Initial value X0
        - **Multiplier (a):** Controls the sequence
        - **Increment (c):** Added before modulo
        - **Modulus (m):** The range limit
        """)
    else:
        st.markdown("""
        **Formula:** Square the seed and take middle digits
        
        - **Seed:** Initial number (e.g., 1234)
        - **Middle Digits:** Extracted from squared value (1234² = 01522756 → 5227)
        """)