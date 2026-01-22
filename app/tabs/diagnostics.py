import streamlit as st
import pandas as pd
import numpy as np
def render_diagnostics():
    st.header("Monte Carlo Diagnostics")
    st.write("Understanding uncertainty and simulation behaviour.")

    st.subheader("Terminal Price Distribution")
    st.bar_chart(
        pd.DataFrame({
            "Frequency": [0, 0, 0, 0, 0]
        })
    )

    st.subheader("Confidence Interval Width vs Paths")
    ci_placeholder = pd.DataFrame({
        "Paths": np.arange(5_000, 55_000, 5_000),
        "CI Width": np.zeros(10)
    }).set_index("Paths")

    st.line_chart(ci_placeholder)