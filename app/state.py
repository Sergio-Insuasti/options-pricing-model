import streamlit as st

defaults = {
    "spot": 100.0,
    "strike": 100.0,
    "maturity": 1.0,
    "r": 0.03,
    "q": 0.00,
    "vol": 0.20,
    "binomial_steps": 100,
    "mc_steps": 50,
    "mc_paths": 50_000,
    "seed": 42,
    "option_type": "Call",
}

def initialise():
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

