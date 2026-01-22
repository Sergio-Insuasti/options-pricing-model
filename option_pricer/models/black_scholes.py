import math
from scipy.stats import norm

def checkNegativeValues(
        S: float,
        K: float,
        T: float,
        vol: float
) -> bool:
    return S <= 0 or K <= 0 or T <= 0 or vol <= 0

def black_scholes_price(
        S :float, # Underlying Price
        K :float,  # Strike Price
        T :float, # Time to Expiration (6 mths)
        q: float, # Dividend Yield
        r :float, # Risk-Free Rate (yield of US 10 year treasury bond)
        vol :float, # volatility (σ), 
        option_type:str # either call or put

) -> dict:
    if checkNegativeValues(S, K, T, r):
        raise ValueError("Invalid input: S, K, T and volatility must be positive")
    # Calculate d1
    d1 = (math.log(S/K) + (r + 0.5*(vol **2)) * T) / (vol * (math.sqrt(T))) 
    # Calculate d2
    d2 = d1 - (vol * (math.sqrt(T)))

    if option_type.lower() == "call":
        # Calculate Call Option Price
        price = (S * norm.cdf(d1)) - (K * math.exp(-r*T) * norm.cdf(d2))
    elif option_type.lower() == "put":
        # Calculate Put Option Price
        price = (K * math.exp(-r*T) * norm.cdf(-d2)) - (S * norm.cdf(-d1))
    else:
        raise ValueError("Option type must be 'call' or 'put'")

    return {
        "price": price,
        "d1": d1,
        "d2": d2
    }