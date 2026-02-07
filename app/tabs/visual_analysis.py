import streamlit as st
import pandas as pd
import numpy as np

from app.state import getState
from app.model_directory import compute_models
from app.tabs.graphs.binomial_convergence import display_binomial_convergence

# ============================
# Cached convergence computation
# ============================

@st.cache_data(show_spinner=False)
def compute_binomial_convergence(state_snapshot: dict):
    """
    Compute relative deviation of binomial pricing vs Black Scholes
    for a sweep of binomial step counts.

    Cached to avoid recomputation on Streamlit reruns.
    """
    steps_grid = np.logspace(
        np.log10(10),
        np.log10(500),
        80,
        dtype=int
    )
    steps_grid = np.unique(steps_grid)

    # Benchmark price (Black–Scholes)
    bs, _, _ = compute_models(state_override=state_snapshot)
    bs_price = bs["price"]

    rows = []

    for steps in steps_grid:
        _, bin_, _ = compute_models(
            state_override={**state_snapshot, "binomial_steps": int(steps)}
        )

        bin_price = bin_["price"]
        rel_dev = (bin_price - bs_price) / bs_price

        rows.append({
            "binomial_steps": int(steps),
            "relative_deviation": rel_dev,
        })

    return pd.DataFrame(rows)


# ============================
# Visual Analysis Tab
# ============================

def render_visuals():
    st.header("Visual Analysis")
    
    display_binomial_convergence(
        compute_binomial_convergence(dict(getState()))
    )

    # --------------------------------
    # Interpretation
    # --------------------------------
    st.caption(
        "Black Scholes is treated as the theoretical reference. "
        "The binomial model exhibits oscillatory convergence due to lattice parity effects, "
        "with the magnitude of deviation shrinking as the number of steps increases."
    )
