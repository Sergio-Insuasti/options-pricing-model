import streamlit as st
import pandas as pd
import numpy as np
from app.model_directory import compute_models
from app.state import getState
import matplotlib.pyplot as plt
@st.cache_data(show_spinner=False)
def compute_mc_convergence(state_snapshot: dict):
    paths_grid = np.logspace(
        np.log10(1_000),
        np.log10(500_000),
        40,
        dtype=int
    )
    
    paths_grid = np.unique(paths_grid)
    
    bs, _, _ = compute_models(state_override=state_snapshot)
    bs_price = bs["price"]
    
    rows = []
    
    for n_paths in paths_grid:
        _, _, mc = compute_models(state_override={**state_snapshot, "mc_paths":int(n_paths)})
        
        rows.append({
            "n_paths": int(n_paths),
            "mc_price": mc["price"],
            "standard_error": mc["standard_error"],
            "bs_price": bs_price
        })
    return pd.DataFrame(rows)

def display_mc_convergence():
    df: pd.DataFrame = compute_mc_convergence(dict(getState()))
    
    st.subheader("Monte Carlo Convergence and Uncertainty")
    st.write(
        "This plot illustrates how Monte Carlo option pricing stabilises as the number "
        "of simulated paths increases. Uncertainty is shown via one standard error bands."
    )

    fig, ax = plt.subplots(facecolor="#121212")
    ax.set_facecolor("#121212")
    ax.grid(visible=True)

    # Uncertainty band (±1 SE)
    ax.fill_between(
        df["n_paths"],
        df["mc_price"] - df["standard_error"],
        df["mc_price"] + df["standard_error"],
        color="#4EA8DE",
        alpha=0.25,
        linewidth=0
    )

    # Monte Carlo mean estimate
    ax.plot(
        df["n_paths"],
        df["mc_price"],
        color="#4EA8DE",
        linewidth=2.2,
        alpha=0.95
    )

    # Black–Scholes reference
    ax.axhline(
        df["bs_price"].iloc[0],
        color="#E0E0E0",
        linewidth=1,
        alpha=0.8
    )

    # Axes labels
    ax.set_xlabel(
        "Number of Monte Carlo paths (increasing)",
        color="#EAEAEA"
    )
    ax.set_ylabel(
        "Option price estimate",
        color="#EAEAEA"
    )
    ax.set_title(
        "Monte Carlo Price Stabilisation with Increasing Paths",
        color="#EAEAEA"
    )

    # Tick styling
    ax.tick_params(
        axis="both",
        colors="#EAEAEA"
    )

    # Remove spines for dark UI
    for spine in ax.spines.values():
        spine.set_visible(False)

    st.pyplot(fig)

    st.caption(
        "Unlike the binomial model, Monte Carlo pricing converges stochastically. "
        "As the number of simulated paths increases, variance shrinks and the price "
        "estimate stabilises around the Black–Scholes benchmark."
    )
    
    