import streamlit as st
import pandas as pd

from app.model_directory import compute_models
def render_comparison():
    st.header("Model Comparison")
    st.write("Direct numerical comparison across pricing models.")

    bs_model, bin_model, mc_model = compute_models()

    comparison_df = pd.DataFrame({
        "Model": ["Black Scholes", "Binomial", "Monte Carlo"],
        "Price": [f"{bs_model['price']:.4f}", f"{bin_model['price']:.4f}", f"{mc_model['price']:.4f}"],
        "Delta": ["—", "—", "—"],
        "Gamma": ["—", "—", "—"],
        "Vega": ["—", "—", "—"],
        "Theta": ["—", "—", "—"],
        "Notes": ["Closed-form", "Discrete approximation", "Simulation ± CI"]
    })

    st.dataframe(comparison_df, use_container_width=True, hide_index=True)