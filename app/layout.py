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
    st.markdown("""#### An Interactive Dashboard of Three Popular Option Pricing Models""")
    footer_style = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #121212; /* Adjust background color as needed */
        color: #FFFFFF; /* Adjust text color as needed */
        text-align: center;
        padding: 10px 0; /* Add some padding */
        font-size: 14px;
    }
    </style>
    <div class="footer">
        <p>Developed by <a href="https://www.linkedin.com/in/sergio-insuasti/" target="_blank">Sergio Insuasti</a> © 2026</p>
    </div>
    """
    st.markdown(footer_style, unsafe_allow_html=True)
    
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

def render_disclaimer():
    st.caption("""DISCLAIMER:""")
    st.caption("""
                This application prices European options under user-assumed market parameters.
                All prices are computed using flat rates and assumed volatility levels.
                Market data is treated as a snapshot and does not represent live tradable prices.
                This project is intended for educational and training purposes only.
                No financial decisions should be made based on this application.
            """)
        