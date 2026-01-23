from option_pricer.core.pricing_state import PricingState
from option_pricer.models.black_scholes import black_scholes_price
from option_pricer.models.binomial import binomial_price
from option_pricer.models.monte_carlo import monte_carlo_price

pricing = PricingState(
    spot=100.0,
    strike=100.0,
    maturity=1.0,
    rate=0.05,
    volatility=0.20,
    dividend_yield=0.0,
    option_type="call",
)

bs = black_scholes_price(pricing)
bin_ = binomial_price(pricing, steps=500)
mc = monte_carlo_price(
    pricing,
    n_steps=252,
    n_sims=100_000,
    seed=42,
    return_paths=False
)

print("Black Scholes:", bs["price"])
print("Binomial:     ", bin_["price"])
print("Monte Carlo:  ", mc["price"])
