import numpy as np

def checkNegativeValues(
        S: float,
        K: float,
        T: float,
        vol: float
) -> bool:
    return S <= 0 or K <= 0 or T <= 0 or vol <= 0

def binomial_price(
    S :float, # Underlying Price
    K :float,  # Strike Price
    T :float, # Time to Expiration (6 mths)
    r :float, # Risk-Free Rate (yield of US 10 year treasury bond)
    vol :float, # volatility (σ), 
    steps: int,
    option_type:str # either call or put

) -> dict:
    # BINOMIAL TREE REPRESENTATION
    # Harcoded values for practice
    # S0 = 100 # initial stock price
    # K = 100 # strike price
    # T = 1 # time to maturity in years
    # r = 0.06 # annual risk-free rate
    # N = 3 # number of time steps
    # u = 1.1 # up-factor in binomial models
    # d = 1/u # ensure recombining tree
    # opttype = 'C' # Option Type 'C' or 'P'

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
    return {
        "price": option_values[0],
        "meta": {
            "steps": steps,
            "u": u,
            "d": d,
            "q": q
        }
    }
