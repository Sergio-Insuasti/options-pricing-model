import streamlit as st
import pandas as pd
from numpy.random import default_rng as rng


st.title("Hello World!")

with st.sidebar:
    st.header("About App")
    st.write("Hey! You found the sidebar!")

st.header("_Streamlit_ is :blue[cool] :sunglasses:")
st.header("This is a header with a divider", divider="gray")

st.markdown("This is created using st.markdown")

col1, col2 = st.columns(2)

with col1:
    x = st.slider("Choose an x value", 1, 10)
with col2:
    st.write("The value of :red[x] is", x)

df = pd.DataFrame(rng(0).standard_normal((20, 3)), columns=["a", "b", "c"])

st.bar_chart(df, horizontal=True)