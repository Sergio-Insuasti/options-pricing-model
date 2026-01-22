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
            getState()[key] = value

def getState():
    return st.session_state

def reset_contract_parameters():
    cParams = ["spot", "strike", "maturity", "option_type"]
    for p in cParams:
        getState()[p] = defaults[p]

def reset_market_parameters():
    mParams = ["r", "q", "vol"]
    for p in mParams:
        getState()[p] = defaults[p]

def reset_unique_parameters():
    uParams = ["binomial_steps", "mc_steps", "mc_paths", "seed",]
    for p in uParams:
        getState()[p] = defaults[p]
