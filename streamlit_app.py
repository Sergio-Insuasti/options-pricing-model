import streamlit as st

from app.state import initialise
from app.layout import render_layout, render_tabs
from app.sidebar import render_sidebar


initialise()
render_layout()
render_sidebar()
render_tabs()

