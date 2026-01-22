import streamlit as st
from app.tabs.overview import render_overview
from app.tabs.comparison import render_comparison
from app.tabs.convergence import render_convergence
from app.tabs.sensitivity import render_sensitivity
from app.tabs.diagnostics import render_diagnostics
# ===============================
# Page Config
# ===============================

def render_layout():
    st.set_page_config(
        page_title="Option Pricing Models Dashboard",
        layout="wide"
    )
    st.markdown("""
        <style>
        html {
            scroll-behavior: smooth;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    st.title("Option Pricing Models Dashboard")
    LI_url = "https://www.linkedin.com/in/sergio-insuasti/"
    st.subheader(f"By [Sergio Insuasti]({LI_url})")
    
def render_tabs():
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overview",
        "Model Comparison",
        "Convergence",
        "Sensitivity (Greeks)",
        "MC Diagnostics"
    ])
    with tab1:
        render_overview()

    with tab2:
        render_comparison()

    with tab3:
        render_convergence()

    with tab4:
        render_sensitivity()

    with tab5:
        render_diagnostics()
        