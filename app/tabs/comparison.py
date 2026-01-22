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

    # Differences vs Black–Scholes
    bin_diff = bin_price - bs_price
    mc_diff = mc_price - bs_price

    pct_bin = (bin_diff / bs_price) * 100
    pct_mc = (mc_diff / bs_price) * 100

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
            f"{colour(round(bin_diff, 4))}",
            f"{colour(round(mc_diff, 4))}"
        ],
        "% Diff vs BS": [
            "—",
            f"{colour(round(pct_bin, 4))}",
            f"{colour(round(pct_mc, 4))}"        
        ],
        "Uncertainty": [
            "—",
            "—",
            f"±{mc_model['standard_error']:.4f}"
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
