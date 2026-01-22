import streamlit as st
import pandas as pd
import numpy as np

from app.state import initialise, defaults
from app.layout import render_layout
from app.sidebar import render_sidebar
from app.model_directory import bs_result, bin_result, mc_result

from option_pricer.models.black_scholes import black_scholes_price
from option_pricer.models.binomial import binomial_price
from option_pricer.models.monte_carlo import monte_carlo_price

initialise()

render_layout()
render_sidebar(defaults)

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
state = st.session_state
with tab1:
    st.header("Overview")
    st.write("What do the models say right now? Use the sidebar to set your parameters!")
    col1, col2, col3 = st.columns(3)

    col1.metric("Black Scholes Price", f"{bs_result['price']:.4f}")
    col2.metric("Binomial Price", f"{bin_result['price']:.4f}")
    col3.metric("Monte Carlo Price", f"{mc_result['price']:.4f}")

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
        "Price": [f"{bs_result['price']:.4f}", f"{bin_result['price']:.4f}", f"{mc_result['price']:.4f}"],
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
