import streamlit as st

from app.model_directory import compute_models

def render_overview():
    st.header("Overview")
    st.write("What do the models say right now? Use the sidebar to set your parameters!")
    col1, col2, col3 = st.columns(3)

    bs_result, bin_result, mc_result = compute_models()

    col1.metric("Black Scholes Price", f"{bs_result['price']:.4f}")
    col2.metric("Binomial Price", f"{bin_result['price']:.4f}")
    col3.metric("Monte Carlo Price", f"{mc_result['price']:.4f}")

    st.caption(
        "All models use the same contract and market assumptions. "
        "Monte Carlo estimates will later include confidence intervals."
    )