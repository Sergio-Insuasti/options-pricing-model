import streamlit as st
from app.state import (
    reset_contract_parameters,
    reset_market_parameters,
    reset_unique_parameters
)
def reset_button(type:str):
    if type=="contract":
        st.button(
            "Reset Contract Parameters",
            on_click=reset_contract_parameters
        )
    elif type=="market":
        st.button(
            "Reset Market Parameters",
            on_click=reset_market_parameters
        )
    elif type=="unique":
        st.button(
            "Reset Unique Parameters",
            on_click=reset_unique_parameters
        )
    else:
        raise ValueError("There are only three types of parameters: Contract, Market or Unique")
    
def synced_slider_input(
    label,
    min_value,
    max_value,
    default,
    step_slider,
    step_input,
    key
):
    if key not in st.session_state:
        st.session_state[key] = default

    def slider_changed():
        st.session_state[key] = st.session_state[f"{key}_slider"]

    def input_changed():
        st.session_state[key] = st.session_state[f"{key}_input"]

    col1, col2 = st.columns([3, 1])

    with col1:
        st.slider(
            label,
            min_value=min_value,
            max_value=max_value,
            value=st.session_state[key],
            step=step_slider,
            key=f"{key}_slider",
            on_change=slider_changed
        )

    with col2:
        st.number_input(
            "",
            min_value=min_value,
            max_value=max_value,
            value=st.session_state[key],
            step=step_input,
            key=f"{key}_input",
            on_change=input_changed
        )

    return st.session_state[key]

