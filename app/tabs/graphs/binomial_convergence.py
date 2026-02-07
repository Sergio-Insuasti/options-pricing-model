import streamlit as st
import pandas as pd
import numpy as np
from app.model_directory import compute_models
from app.state import getState
import matplotlib.pyplot as plt
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


def display_binomial_convergence():
    df: pd.DataFrame = compute_binomial_convergence(dict(getState()))
    
    st.subheader("Binomial Convergence to Black Scholes")
    st.write(
        "This plot visualises how the binomial pricing model converges "
        "to the Black Scholes benchmark under the current parameter assumptions."
    )
    fig, ax = plt.subplots(facecolor="#121212")
    ax.set_facecolor("#121212")
    ax.grid(visible=True)

    window = 7
    df["upper"] = (
        df["relative_deviation"]
        .rolling(window=window, center=True, min_periods=1)
        .max()
    )
    df["lower"] = (
        df["relative_deviation"]
        .rolling(window=window, center=True, min_periods=1)
        .min()
    )

    ax.fill_between(
        df["binomial_steps"],
        df["lower"],
        df["upper"],
        color="#4EA8DE",
        alpha=0.25,
        linewidth=0
    )

    ax.plot(
        df["binomial_steps"],
        df["relative_deviation"],
        color="#4EA8DE",
        linewidth=2.2,
        alpha=0.95
    )

    ax.scatter(
        df["binomial_steps"],
        df["relative_deviation"],
        s=10,
        color="#F4A261",
        alpha=0.6
    )

    ax.axhline(
        0.0,
        color="#E0E0E0",
        linewidth=1,
        alpha=0.8
    )

    ax.set_xlabel(
        "Number of Binomial Steps",
        color="#EAEAEA"
    )
    ax.set_ylabel(
        "Relative deviation (Binomial to Black Scholes)",
        color="#EAEAEA"
    )

    ax.tick_params(
        axis="both",
        colors="#EAEAEA"
    )

    for spine in ax.spines.values():
        spine.set_visible(False)

    st.pyplot(fig)