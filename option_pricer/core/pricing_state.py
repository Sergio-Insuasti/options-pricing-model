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
    ):
        self.S = spot
        self.K = strike
        self.T = maturity
        self.r = rate
        self.vol = volatility
        self.option_type = option_type
        self.q = dividend_yield
        
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
    )