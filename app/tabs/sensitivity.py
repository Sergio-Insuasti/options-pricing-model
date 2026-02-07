import streamlit as st
import pandas as pd
import numpy as np

def render_sensitivity():
    pass
    # st.header("Sensitivity (Greeks)")
    # st.write("Economic intuition via parameter sensitivity.")

    # sensitivity_axis = st.selectbox(
    #     "Sensitivity Variable",
    #     ["Spot Price", "Volatility", "Time to Maturity"]
    # )

    # sensitivity_placeholder = pd.DataFrame({
    #     "x": np.linspace(0, 1, 20),
    #     "Price": np.zeros(20),
    #     "Delta": np.zeros(20)
    # }).set_index("x")

    # st.line_chart(sensitivity_placeholder)