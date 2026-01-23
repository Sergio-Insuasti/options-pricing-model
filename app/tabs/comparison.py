import streamlit as st
import pandas as pd
from app.model_directory import compute_models
from option_pricer.utils import colour, diff, pct_diff

def render_comparison():
    st.header("Model Comparison")
    st.write("Direct numerical comparison across pricing models.")

    # Run pricing models
    bs_model, bin_model, mc_model = compute_models()

    comparison_df = pd.DataFrame({
        "Model": [
            "Black Scholes",
            "Binomial",
            "Monte Carlo"
        ],
        "Price": [
            f"{bs_model['price']:.4f}",
            f"{bin_model['price']:.4f}",
            f"{mc_model['price']:.4f}"
        ],
        "Diff vs BS": [
            "—",
            f"{colour(diff(bin_model['price'], bs_model['price']))}",
            f"{colour(diff(mc_model['price'], bs_model['price']))}"
        ],
        "% Diff vs BS": [
            "—",
            f"{colour(pct_diff(bin_model['price'], bs_model['price']))}",
            f"{colour(pct_diff(mc_model['price'], bs_model['price']))}"        
        ],
        "Standard Error": [
            "—",
            "—",
            f"±{round(mc_model['standard_error'], 4)}"
        ],
        "Runtime (ms)": [
            f"{round(bs_model['runtime'], 2)}",
            f"{round(bin_model['runtime'], 2)}",
            f"{round(mc_model['runtime'], 2)}"
        ],
        "Notes": [
            "Closed-form solution",
            "Discrete lattice approximation",
            "Simulation (SE shown)"
        ]
    })

    st.markdown(
        comparison_df.to_html(index=False, escape=False),
        unsafe_allow_html=True
    )

    st.caption(
        "Black Scholes is used as the reference model for all comparisons."
    )
