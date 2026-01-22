import streamlit as st
import pandas as pd
import numpy as np

from option_pricer.models.black_scholes import black_scholes_price
from option_pricer.models.binomial import binomial_price
from option_pricer.models.monte_carlo import monte_carlo_price

# ===============================
# Page Config
# ===============================
st.set_page_config(
    page_title="Option Pricing Models Dashboard",
    layout="wide"
)

st.title("Option Pricing Models Dashboard")
LI_url = "https://www.linkedin.com/in/sergio-insuasti/"
st.subheader(f"By [Sergio Insuasti]({LI_url})")

# ===============================
# Helper: Synced Slider + Number Input
# ===============================
def synced_slider_input(
    label,
    min_value,
    max_value,
    default,
    step_slider,
    step_input,
    key
):
    if key not in st.session_state:
        st.session_state[key] = default

    def slider_changed():
        st.session_state[key] = st.session_state[f"{key}_slider"]

    def input_changed():
        st.session_state[key] = st.session_state[f"{key}_input"]

    col1, col2 = st.columns([3, 1])

    with col1:
        st.slider(
            label,
            min_value=min_value,
            max_value=max_value,
            value=st.session_state[key],
            step=step_slider,
            key=f"{key}_slider",
            on_change=slider_changed
        )

    with col2:
        st.number_input(
            "",
            min_value=min_value,
            max_value=max_value,
            value=st.session_state[key],
            step=step_input,
            key=f"{key}_input",
            on_change=input_changed
        )

    return st.session_state[key]


# ===============================
# Sidebar — Inputs
# ===============================
with st.sidebar:
    st.header("Contract Parameters")

    spot = synced_slider_input(
        label="Spot Price (S)",
        min_value=50.0,
        max_value=150.0,
        default=100.0,
        step_slider=1.0,
        step_input=0.01,
        key="spot"
    )

    strike = synced_slider_input(
        label="Strike Price (K)",
        min_value=50.0,
        max_value=150.0,
        default=100.0,
        step_slider=1.0,
        step_input=0.01,
        key="strike"
    )

    maturity = synced_slider_input(
        label="Time to Maturity (Years)",
        min_value=0.01,
        max_value=5.0,
        default=1.0,
        step_slider=0.05,
        step_input=0.001,
        key="maturity"
    )

    option_type = st.selectbox(
        "Option Type",
        ["Call", "Put"]
    )

    st.divider()

    st.header("Market Parameters")

    r = synced_slider_input(
        label="Risk-free Rate (r)",
        min_value=0.0,
        max_value=0.10,
        default=0.03,
        step_slider=0.001,
        step_input=0.0001,
        key="r"
    )

    q = synced_slider_input(
        label="Dividend Yield (q)",
        min_value=0.0,
        max_value=0.10,
        default=0.00,
        step_slider=0.001,
        step_input=0.0001,
        key="q"
    )

    sigma = synced_slider_input(
        label="Volatility (σ)",
        min_value=0.05,
        max_value=0.80,
        default=0.20,
        step_slider=0.01,
        step_input=0.001,
        key="sigma"
    )

    st.divider()

    with st.expander("Unique Model Parameters"):
        binomial_steps = st.slider(
            "Binomial Steps",
            min_value=10,
            max_value=500,
            value=100,
            step=10
        )

        mc_steps = st.slider(
            "Monte Carlo Time Steps",
            min_value=10,
            max_value=365,
            value=50,
            step=5
        )

        mc_paths = st.slider(
            "Monte Carlo Paths",
            min_value=1_000,
            max_value=500_000,
            value=50_000,
            step=1_000
        )

        seed = st.number_input(
            "Random Seed",
            value=42,
            step=1
        )

# ===============================
# Main Area — Tabs
# ===============================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Model Comparison",
    "Convergence",
    "Sensitivity (Greeks)",
    "MC Diagnostics"
])

# ===============================
# Tab 1 — Overview
# ===============================
with tab1:
    st.header("Overview")
    st.write("What do the models say right now?")

    col1, col2, col3 = st.columns(3)
    bs_result = black_scholes_price(
        S=spot,
        K=strike,
        T=maturity,
        q=q,
        r=r,
        vol=sigma,
        option_type=option_type
    )

    bin_result = binomial_price(
        S=spot,
        K=strike,
        T=maturity,
        q=q,
        r=r,
        vol=sigma,
        steps=binomial_steps,
        option_type=option_type
    )

    mc_result = monte_carlo_price(
        S=spot,
        K=strike,
        T=maturity,
        q=q,
        r=r,
        vol=sigma,
        option_type=option_type,
        n_steps=mc_steps,
        n_sims=mc_paths,
        seed=seed,
        return_paths=True
    )

    col1.metric("Black Scholes Price", f"{bs_result['price']:.4f}")
    col2.metric("Binomial Price", f"{bin_result['price']:.4f}")
    col3.metric("Monte Carlo Price", f"{mc_result['price']:.4f}", f"± {mc_result['standard_error']:.4f}")

    st.caption(
        "All models use the same contract and market assumptions. "
        "Monte Carlo estimates will later include confidence intervals."
    )

# ===============================
# Tab 2 — Model Comparison
# ===============================
with tab2:
    st.header("Model Comparison")
    st.write("Direct numerical comparison across pricing models.")

    comparison_df = pd.DataFrame({
        "Model": ["Black Scholes", "Binomial", "Monte Carlo"],
        "Price": ["—", "—", "—"],
        "Delta": ["—", "—", "—"],
        "Gamma": ["—", "—", "—"],
        "Vega": ["—", "—", "—"],
        "Theta": ["—", "—", "—"],
        "Notes": ["Closed-form", "Discrete approximation", "Simulation ± CI"]
    })

    st.dataframe(comparison_df, use_container_width=True)

# ===============================
# Tab 3 — Convergence
# ===============================
with tab3:
    st.header("Convergence")
    st.write("Why do the models differ numerically?")

    st.subheader("Binomial Convergence")
    binomial_placeholder = pd.DataFrame({
        "Steps": np.arange(10, 110, 10),
        "Price": np.zeros(10)
    }).set_index("Steps")

    st.line_chart(binomial_placeholder)

    st.subheader("Monte Carlo Convergence")
    mc_placeholder = pd.DataFrame({
        "Paths": np.arange(5_000, 55_000, 5_000),
        "Price": np.zeros(10)
    }).set_index("Paths")

    st.line_chart(mc_placeholder)

# ===============================
# Tab 4 — Sensitivity (Greeks)
# ===============================
with tab4:
    st.header("Sensitivity (Greeks)")
    st.write("Economic intuition via parameter sensitivity.")

    sensitivity_axis = st.selectbox(
        "Sensitivity Variable",
        ["Spot Price", "Volatility", "Time to Maturity"]
    )

    sensitivity_placeholder = pd.DataFrame({
        "x": np.linspace(0, 1, 20),
        "Price": np.zeros(20),
        "Delta": np.zeros(20)
    }).set_index("x")

    st.line_chart(sensitivity_placeholder)

# ===============================
# Tab 5 — Monte Carlo Diagnostics
# ===============================
with tab5:
    st.header("Monte Carlo Diagnostics")
    st.write("Understanding uncertainty and simulation behaviour.")

    st.subheader("Terminal Price Distribution")
    st.bar_chart(
        pd.DataFrame({
            "Frequency": [0, 0, 0, 0, 0]
        })
    )

    st.subheader("Confidence Interval Width vs Paths")
    ci_placeholder = pd.DataFrame({
        "Paths": np.arange(5_000, 55_000, 5_000),
        "CI Width": np.zeros(10)
    }).set_index("Paths")

    st.line_chart(ci_placeholder)
