import time
import numpy as np
from option_pricer.core.pricing_state import PricingState
from option_pricer.utils import setTime

def checkNegativeValues(
        S: float,
        K: float,
        T: float,
        vol: float
) -> bool:
    return S <= 0 or K <= 0 or T <= 0 or vol <= 0

def binomial_formula(
    S :float, # Underlying Price
    K :float,  # Strike Price
    T :float, # Time to Expiration (6 mths)
    r :float, # Risk-Free Rate (yield of US 10 year treasury bond)
    q: float,
    vol :float, # volatility (σ), 
    option_type:str, # either call or put
    steps: int

) -> dict:
    
    start = time.perf_counter()
    
    if steps <= 0:
        raise ValueError("Steps for Binomial Model must be positive")
    if checkNegativeValues(S, K, T, vol):
        raise ValueError("Invalid input parameters")
    
    dt = T / steps
    u = np.exp(vol * np.sqrt(dt))
    d = 1.0 / u

    q = (np.exp(r * dt) - d) / (u - d)
    discount = np.exp(-r * dt)

    stock_prices = S * (d ** np.arange(steps, -1,-1)) * (u ** np.arange(0, steps + 1))

    if option_type.lower() == "call":
        option_values = np.maximum(stock_prices - K, 0.0)
    elif option_type.lower() == "put":
        option_values = np.maximum(K - stock_prices, 0.0)
    else:
        raise ValueError("Option type must be 'call' or 'put'")
    
    for _ in range(steps):
        option_values = discount * (
            q * option_values[1:] + (1 - q) * option_values[:-1]
        )
    end = time.perf_counter()
        
    bin_ = {
        "price": option_values[0],
        "meta": {
            "steps": steps,
            "u": u,
            "d": d,
            "q": q,
            "runtime": 0
        }
    }
    setTime(start, end, bin_)
        
    return bin_

def binomial_price(
    pricing: PricingState,
    steps: int
):
    return binomial_formula(
        pricing.S,
        pricing.K,
        pricing.T,
        pricing.r,
        pricing.q,
        pricing.vol,
        pricing.option_type,
        steps
    )
