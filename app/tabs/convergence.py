import streamlit as st
import pandas as pd
import numpy as np

def render_convergence():
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