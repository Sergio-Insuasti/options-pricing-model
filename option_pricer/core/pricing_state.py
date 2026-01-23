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
        vol_mult: float = 1.0,
        rate_shift: float = 0.0,
        time_shift: float = 0.0
    ):
        self.S = spot
        self.K = strike
        self.T = maturity
        self.r = rate
        self.vol = volatility
        self.option_type = option_type
        self.q = dividend_yield
        
        self.vol_mult = vol_mult
        self.rate_shift = rate_shift
        self.time_shift = time_shift

    def resolved_inputs(self) -> dict:
        vol_mult = max(self.vol_mult, 1e-6)
        time_shift = max(self.time_shift, 0.0)

        T_adj = max(self.T - time_shift, 1e-6)
        r_adj = self.r + self.rate_shift
        vol_adj = max(self.vol * vol_mult, 1e-6)
        return {
            "S": self.S,
            "K": self.K,
            "T": T_adj,
            "r": r_adj,
            "q": self.q,
            "vol": vol_adj,
            "option_type": self.option_type
        }
        
    @classmethod
    def from_dict(cls, state: dict):
        return cls(
            spot=state["spot"],
            strike=state["strike"],
            maturity=state["maturity"],
            rate=state["r"],
            volatility=state["vol"],
            option_type=state["option_type"],
            dividend_yield=state.get("q", 0.0),
            vol_mult=state.get("vol_mult", 1.0),
            rate_shift=state.get("rate_shift", 0.0),
            time_shift=state.get("time_shift", 0.0),
        )