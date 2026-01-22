import streamlit as st
from app.state import (
    reset_contract_parameters,
    reset_market_parameters,
    reset_unique_parameters
)
from app.widgets import synced_slider_input
def render_sidebar(defaults: dict):
    with st.sidebar:
        st.header("Contract Parameters")

        spot = synced_slider_input(
            label="Spot Price (S)",
            min_value=50.0,
            max_value=150.0,
            default=defaults["spot"],
            step_slider=1.0,
            step_input=0.01,
            key="spot"
        )

        strike = synced_slider_input(
            label="Strike Price (K)",
            min_value=50.0,
            max_value=150.0,
            default=defaults["strike"],
            step_slider=1.0,
            step_input=0.01,
            key="strike"
        )

        maturity = synced_slider_input(
            label="Time to Maturity (Years)",
            min_value=0.01,
            max_value=5.0,
            default=defaults["maturity"],
            step_slider=0.05,
            step_input=0.001,
            key="maturity"
        )

        option_type = st.selectbox(
            "Option Type",
            ["Call", "Put"],
            key="option_type"
        )

        st.button(
            "Reset Contract Parameters",
            on_click=reset_contract_parameters
        )

        st.divider()

        st.header("Market Parameters")

        r = synced_slider_input(
            label="Risk-free Rate (r)",
            min_value=0.0,
            max_value=0.10,
            default=defaults["r"],
            step_slider=0.001,
            step_input=0.0001,
            key="r"
        )

        q = synced_slider_input(
            label="Dividend Yield (q)",
            min_value=0.0,
            max_value=0.10,
            default=defaults["q"],
            step_slider=0.001,
            step_input=0.0001,
            key="q"
        )

        vol = synced_slider_input(
            label="Volatility (σ)",
            min_value=0.05,
            max_value=0.80,
            default=defaults["vol"],
            step_slider=0.01,
            step_input=0.001,
            key="vol"
        )

        st.button(
            "Reset Market Parameters",
            on_click=reset_market_parameters
        )

        st.divider()

        st.header("Unique Model Parameters")
        binomial_steps = st.slider(
            "Binomial Steps",
            min_value=10,
            max_value=500,
            value=defaults["binomial_steps"],
            step=10,
            key="binomial_steps"
        )

        mc_steps = st.slider(
            "Monte Carlo Time Steps",
            min_value=10,
            max_value=365,
            value=defaults["mc_steps"],
            step=5,
            key="mc_steps"
        )

        mc_paths = st.slider(
            "Monte Carlo Paths",
            min_value=1_000,
            max_value=500_000,
            value=defaults["mc_paths"],
            step=1_000,
            key="mc_paths"
        )

        seed = st.number_input(
            "Random Seed",
            value=defaults["seed"],
            step=1,
            key="seed"
        )

        st.button(
            "Reset Unique Parameters",
            on_click=reset_unique_parameters
        )

        