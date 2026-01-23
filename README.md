# Options Pricing Model

## By Sergio Insuasti

# About
Designing a full-stack dashboard which explores the three most common
theoretical option pricing models: Black Scholes, Monte Carlo and Binomial.


# Directory
```powershell
option_pricer/
├── .devcontainer/
│   │   ├── devcontainer.json
├── .streamlit/
│   ├── config.toml
├── app/
│   ├── tabs/
│   │   ├── comparison.py
│   │   ├── convergence.py
│   │   ├── diagnostics.py
│   │   ├── overview.py
│   │   └── sensitivity.py
│   ├── layout.py/
│   ├── model_directory.py/
│   ├── sidebar.py/
│   ├── state.py/
│   └── widgets.py/
├── assets/
│   │   ├── /
├── option_pricer/    
│   ├── models/
│   │   ├── black_scholes.py
│   │   ├── binomial.py
│   │   └── monte_carlo.py
│   ├── greeks/
│   ├── implied_vol/
│   └── core/
└── streamlit_app.py
└── requirements.txt
├── tests/
└── README.md
```


# Log 1: INTERACTIVE DASHBOARD (19-01-26)
For this phase, my intention is to create an interactive dashboard through my knowledge
of Python. With this dashboard users can configure option parameters,
run the three most popular option pricing models and compare prices, Greeks,
convergence and uncertainty.

For the frontend dashboard, I have made the decision to use StreamLit instead
of React. StreamLit is a frontend library that has native widgets such as sliders
and contains zero frontend overhead. Its simplicity is widely used by researchers
and will highlight the intended simplicity of this software.

# Log 2: MODEL IMPLEMENTATION (19/20-01-26)
As the front end has been established, focus is now on coding implementations
of the three models that will be explored.
## Black Scholes Option Pricing Model
First was the Black Scholes model: https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model </br>
Initially, to understand the process of the model, I made sure to mathematically
write formulae for calculating call/put option prices. With this initial version,
parameters of the model were hard-coded, to ensure the model worked correctly
for controlled values.
```python
import math
from scipy.stats import norm

S = 42 # Underlying Price
K = 40 # Strike Price
T = 0.5 # Time to Expiration (6 mths)
r = 0.1 # Risk-Free Rate (yield of US 10 year treasury bond)
vol = 0.2 # volatility (σ)

# Calculate d1
d1 = (math.log(S/K) + (r + 0.5*(vol **2)) * T) / (vol * (math.sqrt(T))) 
# Calculate d2
d2 = d1 - (vol * (math.sqrt(T)))

# Calculate Call Option Price
C = (S * norm.cdf(d1)) - (K * math.exp(-r*T) * norm.cdf(d2))
# Calculate Put Option Price
P = (K * math.exp(-r*T) * norm.cdf(-d2)) - (S * norm.cdf(-d1))

# Printing the results (d1/2 rounded to 4dp, C and P rounded to 2dp)
print(f'The value of d1 is: {round(d1, 4)}')
print(f'The value of d2 is: {round(d2, 4)}')
print(f'The price of the call option is: ${round(C, 2)}')
print(f'The price of the put option is: ${round(P, 2)}')
```

From there, I knew that having these functionalities separate from the front end
meant that I could refactor this code to instead be a function that is now called
from the front end to determine option price via Black Scholes.
```python
import math
from scipy.stats import norm

def black_scholes_price(
        S :float, # Underlying Price
        K :float,  # Strike Price
        T :float, # Time to Expiration (6 mths)
        r :float, # Risk-Free Rate (yield of US 10 year treasury bond)
        vol :float, # volatility (σ), 
        option_type:str # either call or put

) -> dict:
    if S <= 0 or K <= 0 or T <= 0 or vol <= 0:
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
```
Along with error checking, this allows a separation of concerns between the frontend
and backend. This will prove to be extremely useful in determining prices for
multitudes of data streams.

Following this, a "connection" needs to be made on the front end side to efficiently
call this function to determine option pricing.

### Assumptions:
- The original BS Model assumes that the option is a European-style option and can only be exercised at expiration
- No dividends are paid out during the option's life cycle
- Market movements follow a random walk
- There are no transaction costs in buying an option
- Risk-free rate and volatility are known and constant
- The underlying price of an option (S) follows a log-normal distribution

## Binomial Option Pricing Model
The Binomial Model prices an option by approximating the continuous evolution of an asset price with a discrete-time recombining tree. It will split time into N discrete steps and with the asset at each time point either moving up or down by a factor of $u$ or $d$ respectively. To implement this, I used Python and Numpy as such:
``` python
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
    if steps <= 0:
        raise ValueError("Steps for Binomial Model must be positive")
    if checkNegativeValues(S, K, T, vol):
        raise ValueError("Invalid input parameters")
    
    dt = T / steps
    u = np.exp(vol * np.sqrt(dt))
    d = 1.0 / u

    q = (np.exp(r * dt) - d) / (u - d)
    discount = np.exp(-r * dt)

    # Here are stock prices at maturity
    stock_prices = S * (d ** np.arange(steps, -1,-1)) * (u ** np.arange(0, steps + 1))

    # Using the options type to find payoff at maturity
    if option_type.lower() == "call":
        option_values = np.maximum(stock_prices - K, 0.0)
    elif option_type.lower() == "put":
        option_values = np.maximum(K - stock_prices, 0.0)
    else:
        raise ValueError("Option type must be 'call' or 'put'")
    
    # Then by backwards induction, we then find the approximate option payoff
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
```

Continuing with the implementation of the Black Scholes model, we are ensuring a separation of concerns and low coupling by calling on binomial.py instead of having that implementation in our frontend.
Furthermore, this model has taught me how 

### Assumptions
- The underlying price follows a discrete-time multiplicative process
- Markets are arbitrage-free
- Risk-free rate and volatility are constant
- Trading occurs at discrete time intervals
- The option is European-style

# Log 3: MONTE CARLO MODEL (22-01-26)
Unlike Black Scholes and Binomial, the Monte Carlo model estimates option prices through large-scale simulation of possible future price paths. To esure this, flexibility was essential, due to the model being computationally more expensive than the others. To implement this flexibility, I used NumPy for vectorised computation (in a similar fashion to binomial) to ensure the solution remains efficient if considering a large number of paths.
``` python
import numpy as np
from typing import Optional, Dict, Tuple

def monte_carlo_price(
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
) -> Dict:
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

    return {
        "price": float(price),
        "standard_error": float(standard_error),
        "confidence_interval": (float(ci_low), float(ci_high)),
        "n_steps": n_steps,
        "n_simulations": n_sims,
        "paths": paths if return_paths else None,
    }

```
Following on from previous models, we ensure that coupling is loose and dependencies are minimised by separating the friont and backend to only engage via functional calls. Parameters are passed into the frontend and functionality is executed in the backend, with each model contained in their own scripts.
While the simulation itself is rather straightforward, care was taken to ensure reproducability, numerical stability and compatibility with the front end.
Now with this complete, we now had a complete overview of all three models and their option price estimates given a determined set of parameters. With this major component complete, we can now shift our focus to the analytical components such as model comparison and convergence.

# Log 4: REFACTORING (22-01-26)
Having finished the first major component of the app (implementing the three pricing models and presenting them in the overview), it became super clear that keeping all the frontend logic in the one file (streamlit_app.py) would be increasingly unmanageable. While Streamlit makes it easier to see what could be done, the more this application grows, the more brittle it will become. 
To address this, I took the time to refactor the app into a modular architecture with clearly defined responsibilities. This decision came from a variety of principles: Maintainability, Separation of Concerns and Extensibility. The overall goal is to now make streamlit_app.py an orchestrator. This communicates with the server to execute all the frontend (and eventually backend) without the server directly accessing this. From this, new files were introduced:
- state.py
  - Initialises the session state variables once and once only. Also encapsulates session state ensuring other files can only access the session state via `getState()`. 
- layout.py
  - This handles the global layout of the app. This handles the main display as well as calls for the creation for each of the five proposed tabs
- sidebar.py
  - Handles all the parameters in the sidebar, logic in updating/resetting parameter values
- widgets.py
  - Handles current logic involving synced slider (a feature that updates parameter value by moving the slider or typing value)
Refactoring the system early now gives a leg up for extending the implementation to the other elements in this app, such as comparison and convergence.

# Log 5: COMPARISON (23-01-26)
With all three pricing models implemented and unified across the frontend and backend, the next step was to introduce a formal comparison layer. The purpose of the Comparison tab is to analyse how theoretically equivalent models differ numerically under finite approximations.
This tab serves as a quantitative checkpoint between theory and computation. Given a single, consistent set of contract and market parameters, all three models are evaluated simultaneously and compared directly, alongside their respective runtimes.
From a design perspective, the Comparison tab was intentionally kept thin. It consumes only the structured dictionary returned by compute_models in model_directory.py, without embedding any pricing or recalculation logic within the frontend itself. This ensures that the comparison layer remains model-agnostic and easily extensible. Future models (e.g. variance-reduced Monte Carlo schemes) can be incorporated into the system without requiring changes to the comparison interface, provided they conform to the same output structure.
Black–Scholes is treated as the reference point due to its closed-form solution under idealised assumptions. Differences observed in the Binomial and Monte Carlo estimates are therefore interpreted as approximation error, rather than disagreement in theoretical valuation.
To preserve strict separation of concerns, all recalculation and performance measurement logic was removed from the frontend tabs and relocated to the backend. Timing capture, numerical differences, and colour-coded deltas are computed outside the UI layer and exposed only as data. This prevents the frontend from becoming coupled to implementation details and ensures that performance statistics are gathered consistently across models.
By centralising model execution, timing, and output formatting in the backend, the system provides a fast, reliable, and uniform interface for both current and future pricing models. The Comparison tab therefore functions purely as a presentation and interpretation layer, reinforcing the modular design of the overall application.

# Log 6: FURTHER ANALYSIS (24-01-26)
