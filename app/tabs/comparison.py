import streamlit as st
import pandas as pd
from app.model_directory import compute_models


def colour(val):
    # Returns a coloured string using HTML.
    if val > 0:
        return f"<span style='color: green;'>{val}</span>"
    elif val < 0:
        return f"<span style='color: red;'>{val}</span>"
    else:
        return f"{val:.4f}"


def render_comparison():
    st.header("Model Comparison")
    st.write("Direct numerical comparison across pricing models.")

    # Run pricing models
    bs_model, bin_model, mc_model = compute_models()

    # Extract prices
    bs_price = bs_model["price"]
    bin_price = bin_model["price"]
    mc_price = mc_model["price"]

    # Build comparison table
    comparison_df = pd.DataFrame({
        "Model": [
            "Black Scholes",
            "Binomial",
            "Monte Carlo"
        ],
        "Price": [
            f"{bs_price:.4f}",
            f"{bin_price:.4f}",
            f"{mc_price:.4f}"
        ],
        "Diff vs BS": [
            "—",
            f"{colour(round(bin_price - bs_price, 4))}",
            f"{colour(round(mc_price - bs_price, 4))}"
        ],
        "% Diff vs BS": [
            "—",
            f"{colour(round((bin_price - bs_price / bs_price) * 100, 4))}",
            f"{colour(round((mc_price - bs_price / bs_price) * 100, 4))}"        
        ],
        "Uncertainty": [
            "—",
            "—",
            f"±{round(mc_model['standard_error'], 4)}"
        ],
        "Runtime (ms)": [
            f"{round(bs_model["runtime"], 2)}",
            f"{round(bin_model["runtime"], 2)}",
            f"{round(mc_model["runtime"], 2)}"
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
