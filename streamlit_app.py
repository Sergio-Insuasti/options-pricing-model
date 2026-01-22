import streamlit as st

from app.state import initialise
from app.layout import render_layout
from app.sidebar import render_sidebar
from app.tabs.overview import render_overview
from app.tabs.comparison import render_comparison
from app.tabs.convergence import render_convergence
from app.tabs.sensitivity import render_sensitivity
from app.tabs.diagnostics import render_diagnostics

initialise()
render_layout()
render_sidebar()

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
    
