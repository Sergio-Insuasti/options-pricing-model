import streamlit as st

from option_pricer.models.black_scholes import black_scholes_price
from option_pricer.models.binomial import binomial_price
from option_pricer.models.monte_carlo import monte_carlo_price

state = st.session_state

bs_result = black_scholes_price(
    S=state["spot"],
    K=state["strike"],
    T=state["maturity"],
    q=state["q"],
    r=state["r"],
    vol=state["vol"],
    option_type=state["option_type"]
)

bin_result = binomial_price(
    S=state["spot"],
    K=state["strike"],
    T=state["maturity"],
    q=state["q"],
    r=state["r"],
    vol=state["vol"],
    steps=state["binomial_steps"],
    option_type=state["option_type"]
)

mc_result = monte_carlo_price(
    S=state["spot"],
    K=state["strike"],
    T=state["maturity"],
    q=state["q"],
    r=state["r"],
    vol=state["vol"],
    option_type=state["option_type"],
    n_steps=state["mc_steps"],
    n_sims=state["mc_paths"],
    seed=state["seed"],
    return_paths=True
)