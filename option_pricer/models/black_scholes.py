import math
import time
from scipy.stats import norm
from option_pricer.core.pricing_state import PricingState
from option_pricer.utils import setTime

def checkNegativeValues(
        S: float,
        K: float,
        T: float,
        vol: float
) -> bool:
    return S <= 0 or K <= 0 or T <= 0 or vol <= 0

def get_black_scholes_price(
        S :float, # Underlying Price
        K :float,  # Strike Price
        T :float, # Time to Expiration (6 mths)
        q: float, # Dividend Yield
        r :float, # Risk-Free Rate (yield of US 10 year treasury bond)
        vol :float, # volatility (σ), 
        option_type:str # either call or put

) -> dict:
    start = time.perf_counter()
    
    if checkNegativeValues(S, K, T, vol):
        raise ValueError("Invalid input: S, K, T and volatility must be positive")

    sqrtT = math.sqrt(T)

    d1 = (math.log(S / K) + (r - q + 0.5 * vol ** 2) * T) / (vol * sqrtT)
    d2 = d1 - vol * sqrtT

    if option_type.lower() == "call":
        price = (
            S * math.exp(-q * T) * norm.cdf(d1)
            - K * math.exp(-r * T) * norm.cdf(d2)
        )
    elif option_type.lower() == "put":
        price = (
            K * math.exp(-r * T) * norm.cdf(-d2)
            - S * math.exp(-q * T) * norm.cdf(-d1)
        )
    else:
        raise ValueError("Option type must be 'call' or 'put'")
    end = time.perf_counter()
    bs = {
        "price": price,
        "runtime": 0
    }
    setTime(start, end, bs)
    return bs

def black_scholes_price(pricing: PricingState):
    inputs = pricing.resolved_inputs()
    return get_black_scholes_price(**inputs)