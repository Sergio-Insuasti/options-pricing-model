import numpy as np
import time
from typing import Optional

from option_pricer.utils import setTime
from option_pricer.core.pricing_state import PricingState

def monte_carlo_formula(
    S: float,
    K: float,
    T: float,
    r: float,
    q: float,
    vol: float,
    option_type: str,
    n_steps: int = 100,
    n_sims: int = 50_000,
    seed: Optional[int] = None,
    return_paths: bool = False,
) -> dict:
    
    start = time.perf_counter()
    
    if n_steps <= 0:
        raise ValueError("Number of Monte Carlo Steps must be positive")

    if seed is not None:
        np.random.seed(seed)

    # Time increment
    dt = T / n_steps

    # Drift and diffusion terms
    drift = (r - q - 0.5 * vol ** 2) * dt
    diffusion = vol * np.sqrt(dt)

    # Generate random shocks
    Z = np.random.normal(size=(n_steps, n_sims))

    # Log-price paths
    log_S0 = np.log(S)
    log_paths = log_S0 + np.cumsum(drift + diffusion * Z, axis=0)

    # Include initial price
    log_paths = np.vstack([np.full(n_sims, log_S0), log_paths])

    # Convert to price paths
    paths = np.exp(log_paths)

    # Terminal prices
    ST = paths[-1]

    # Payoff for European call
    if option_type.lower() == "call":
        payoff = np.maximum(ST - K, 0.0)
    elif option_type.lower() == "put":
        payoff = np.maximum(K - ST, 0.0)
    else:
        raise ValueError("Option type must be 'call' or 'put'")

    # Discounted price
    price = np.exp(-r * T) * payoff.mean()

    # Standard error
    std_dev = payoff.std(ddof=1)
    standard_error = np.exp(-r * T) * std_dev / np.sqrt(n_sims)

    # 95% confidence interval
    ci_low = price - 1.96 * standard_error
    ci_high = price + 1.96 * standard_error
    
    end = time.perf_counter()
    
    mc = {
        "price": float(price),
        "standard_error": float(standard_error),
        "confidence_interval": (float(ci_low), float(ci_high)),
        "n_steps": n_steps,
        "n_simulations": n_sims,
        "paths": paths if return_paths else None,
        "runtime": 0
    }
    
    setTime(start, end, mc)

    return mc

def monte_carlo_price(
    pricing: PricingState,
    n_steps: int,
    n_sims: int,
    seed: Optional[int],
    return_paths: bool
):
    inputs = pricing.resolved_inputs()
    return monte_carlo_formula(
        n_steps = n_steps,
        n_sims = n_sims,
        seed = seed,
        return_paths = return_paths,
        **inputs
    )
