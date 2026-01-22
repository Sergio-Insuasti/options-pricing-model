import streamlit as st
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

