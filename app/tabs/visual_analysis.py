import streamlit as st

from app.tabs.graphs.binomial_convergence import display_binomial_convergence
from app.tabs.graphs.monte_carlo_convergence import display_mc_convergence

# ============================
# Visual Analysis Tab
# ============================

def render_visuals():
    st.header("Visual Analysis")
    
    display_binomial_convergence()
    display_mc_convergence()
    # --------------------------------
    # Interpretation
    # --------------------------------
    st.caption(
        "Black Scholes is treated as the theoretical reference. "
        "The binomial model exhibits oscillatory convergence due to lattice parity effects, "
        "with the magnitude of deviation shrinking as the number of steps increases."
    )
