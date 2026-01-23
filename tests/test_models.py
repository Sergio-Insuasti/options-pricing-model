import math
import pytest

from option_pricer.core.pricing_state import PricingState
from option_pricer.models.black_scholes import black_scholes_price
from option_pricer.models.binomial import binomial_price
from option_pricer.models.monte_carlo import monte_carlo_price


@pytest.fixture
def base_pricing_state():
    """
    Canonical pricing state used across all model tests.
    """
    return PricingState(
        spot=100.0,
        strike=100.0,
        maturity=1.0,
        rate=0.05,
        volatility=0.20,
        dividend_yield=0.0,
        option_type="call",
    )


def test_black_scholes_atm_call(base_pricing_state):
    """
    ATM European call sanity check against known reference value.
    """
    result = black_scholes_price(base_pricing_state)
    assert abs(result["price"] - 10.4506) < 1e-3


def test_black_scholes_put_call_parity():
    """
    Put–call parity: C - P = S - K * exp(-rT) (q = 0).
    """
    call = PricingState(100, 100, 1.0, 0.05, 0.20, "call")
    put  = PricingState(100, 100, 1.0, 0.05, 0.20, "put")

    C = black_scholes_price(call)["price"]
    P = black_scholes_price(put)["price"]

    rhs = 100.0 - 100.0 * math.exp(-0.05)
    assert abs((C - P) - rhs) < 1e-3



def test_binomial_converges_to_black_scholes(base_pricing_state):
    """
    Binomial price should converge to BS price as steps increase.
    """
    bs_price = black_scholes_price(base_pricing_state)["price"]
    bin_price = binomial_price(base_pricing_state, steps=500)["price"]

    assert abs(bin_price - bs_price) < 0.02


def test_binomial_invalid_steps_raises(base_pricing_state):
    """
    Binomial model should reject non-positive step counts.
    """
    with pytest.raises(ValueError):
        binomial_price(base_pricing_state, steps=0)


def test_monte_carlo_reproducible_with_seed(base_pricing_state):
    """
    Fixed seed should produce identical Monte Carlo prices.
    """
    r1 = monte_carlo_price(
        base_pricing_state,
        n_steps=252,
        n_sims=50_000,
        seed=42,
        return_paths=False
    )
    r2 = monte_carlo_price(
        base_pricing_state,
        n_steps=252,
        n_sims=50_000,
        seed=42,
        return_paths=False
    )

    assert abs(r1["price"] - r2["price"]) < 1e-8


def test_monte_carlo_within_black_scholes_confidence_band(base_pricing_state):
    """
    Black–Scholes price should lie within MC 95% confidence interval.
    """
    bs_price = black_scholes_price(base_pricing_state)["price"]

    mc = monte_carlo_price(
        base_pricing_state,
        n_steps=252,
        n_sims=100_000,
        seed=1,
        return_paths=False
    )

    ci_low, ci_high = mc["confidence_interval"]
    assert ci_low <= bs_price <= ci_high


# ============================================================
# Cross-model consistency tests
# ============================================================

def test_all_models_agree_within_tolerance(base_pricing_state):
    """
    All pricing models should agree within reasonable tolerances.
    """
    bs = black_scholes_price(base_pricing_state)["price"]
    bin_ = binomial_price(base_pricing_state, steps=500)["price"]
    mc = monte_carlo_price(
        base_pricing_state,
        n_steps=252,
        n_sims=100_000,
        seed=0,
        return_paths=False
    )["price"]

    assert abs(bs - bin_) < 0.02
    assert abs(bs - mc) < 0.05
