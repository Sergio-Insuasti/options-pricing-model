from app.state import getState
from option_pricer.models.black_scholes import black_scholes_price
from option_pricer.models.binomial import binomial_price
from option_pricer.models.monte_carlo import monte_carlo_price

def compute_models():
    state = getState()
    bs = black_scholes_price(
        S=state["spot"],
        K=state["strike"],
        T=state["maturity"],
        q=state["q"],
        r=state["r"],
        vol=state["vol"],
        option_type=state["option_type"]
    )
    
    bin_ = binomial_price(
        S=state["spot"],
        K=state["strike"],
        T=state["maturity"],
        q=state["q"],
        r=state["r"],
        vol=state["vol"],
        steps=state["binomial_steps"],
        option_type=state["option_type"]
    )
    
    mc = monte_carlo_price(
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
    
    return bs, bin_, mc