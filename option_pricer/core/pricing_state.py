from app.state import defaults
class PricingState:
    def __init__(
        self,
        spot: float,
        strike: float,
        maturity: float,
        rate: float,
        volatility: float,
        option_type: str,
        dividend_yield: float = 0.0,
        scenario_rate: float | None = None,
        scenario_vol: float | None = None,
        time_shift: float = 0.0
    ):
        self.S = spot
        self.K = strike
        self.T = maturity

        self.base_r = rate
        self.base_vol = volatility

        self.scenario_r = scenario_rate
        self.scenario_vol = scenario_vol

        self.option_type = option_type
        self.q = dividend_yield
        self.time_shift = time_shift

    def resolved_inputs(self) -> dict:
    # If user supplied scenario values, use them
        r = self.scenario_r if self.scenario_r is not None else self.base_r
        vol = self.scenario_vol if self.scenario_vol is not None else self.base_vol

        T_adj = max(self.T - self.time_shift, 1e-6)

        return {
            "S": self.S,
            "K": self.K,
            "T": T_adj,
            "r": r,
            "q": self.q,
            "vol": max(vol, 1e-6),
            "option_type": self.option_type
        }
        
    @classmethod
    def from_dict(cls, state: dict):
        return cls(
            spot=state["spot"],
            strike=state["strike"],
            maturity=state["maturity"],
            rate=defaults["r"],          # base
            volatility=defaults["vol"],  # base
            scenario_rate=state["r"],    # slider
            scenario_vol=state["vol"],   # slider
            option_type=state["option_type"],
            dividend_yield=state.get("q", 0.0),
        )
