from app.state import getState
from option_pricer.models.black_scholes import black_scholes_price
from option_pricer.models.binomial import binomial_price
from option_pricer.models.monte_carlo import monte_carlo_price
from option_pricer.core.pricing_state import PricingState

def compute_models(state_override: dict | None = None):
    base_state = getState()

    state = dict(base_state)

    if state_override:
        state.update(state_override)

    pricing = PricingState.from_dict(state)

    bs = black_scholes_price(pricing)

    bin_ = binomial_price(
        pricing,
        steps=state["binomial_steps"]
    )

    mc = monte_carlo_price(
        pricing,
        n_steps=state["mc_steps"],
        n_sims=state["mc_paths"],
        seed=state["seed"],
        return_paths=True
    )

    return bs, bin_, mc

