import pytest
from option_pricer.core.pricing_state import PricingState

@pytest.fixture
def base_pricing_state():
    """
    Canonical pricing state used across tests.
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


def test_resolved_inputs_no_scenario(base_pricing_state):
    """
    With no scenario shocks, resolved inputs should equal base inputs.
    """
    inputs = base_pricing_state.resolved_inputs()

    assert inputs["S"] == 100.0
    assert inputs["K"] == 100.0
    assert inputs["T"] == 1.0
    assert inputs["r"] == 0.05
    assert inputs["q"] == 0.0
    assert inputs["vol"] == 0.20
    assert inputs["option_type"] == "call"


def test_volatility_multiplier_applied(base_pricing_state):
    base_pricing_state.vol_mult = 1.25
    inputs = base_pricing_state.resolved_inputs()

    assert inputs["vol"] == pytest.approx(0.25)


def test_negative_vol_multiplier_clipped(base_pricing_state):
    base_pricing_state.vol_mult = -1.0
    inputs = base_pricing_state.resolved_inputs()

    assert inputs["vol"] > 0.0


def test_time_shift_reduces_maturity(base_pricing_state):
    base_pricing_state.time_shift = 0.25
    inputs = base_pricing_state.resolved_inputs()

    assert inputs["T"] == pytest.approx(0.75)


def test_time_shift_clipped_at_zero(base_pricing_state):
    base_pricing_state.time_shift = 2.0
    inputs = base_pricing_state.resolved_inputs()

    assert inputs["T"] > 0.0


def test_rate_shift_applied(base_pricing_state):
    base_pricing_state.rate_shift = 0.01
    inputs = base_pricing_state.resolved_inputs()

    assert inputs["r"] == pytest.approx(0.06)


def test_negative_rate_allowed(base_pricing_state):
    base_pricing_state.rate_shift = -0.10
    inputs = base_pricing_state.resolved_inputs()

    assert inputs["r"] < 0.0


def test_from_dict_constructs_state_correctly():
    state = PricingState.from_dict({
        "spot": 100.0,
        "strike": 100.0,
        "maturity": 1.0,
        "r": 0.05,
        "vol": 0.20,
        "option_type": "call",
        "vol_mult": 1.1,
        "rate_shift": 0.005,
        "time_shift": 0.1,
    })

    inputs = state.resolved_inputs()

    assert inputs["S"] == 100.0
    assert inputs["K"] == 100.0
    assert inputs["vol"] == pytest.approx(0.22)
    assert inputs["r"] == pytest.approx(0.055)
    assert inputs["T"] == pytest.approx(0.9)
