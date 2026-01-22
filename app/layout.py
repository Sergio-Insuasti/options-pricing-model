import streamlit as st

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
            """, unsafe_allow_html=True
        )

    st.title("Option Pricing Models Dashboard")
    LI_url = "https://www.linkedin.com/in/sergio-insuasti/"
    st.subheader(f"By [Sergio Insuasti]({LI_url})")
