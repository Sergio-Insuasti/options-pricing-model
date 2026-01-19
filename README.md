# Options Pricing Model

## By Sergio Insuasti

### About
Designing a full-stack dashboard which explores the three most common
theoretical option pricing models: Black Scholes, Monte Carlo and Binomial.


### Directory
option_pricer/
├── option_pricer/          # pricing library (NO UI CODE)
│   ├── models/
│   │   ├── black_scholes.py
│   │   ├── binomial.py
│   │   └── monte_carlo.py
│   ├── greeks/
│   ├── implied_vol/
│   └── core/
├── dashboard/
│   └── streamlit_app.py              # Streamlit UI
├── tests/
└── README.md

## Log 1: INTERACTIVE DASHBOARD (19-01-26)
For this phase, my intention is to create an interactive dashboard through my knowledge
of Python. With this dashboard users can configure option parameters,
run the three most popular option pricing models and compare prices, Greeks,
convergence and uncertainty.

For the frontend dashboard, I have made the decision to use StreamLit instead
of React. StreamLit is a frontend library that has native widgets such as sliders
and contains zero frontend overhead. Its simplicity is widely used by researchers
and will highlight the intended simplicity of this software.

## Log 2: MODEL IMPLEMENTATION (19/20-01-26)
As the front end has been established, focus is now on coding implementations
of the three models that will be explored.
### Black Scholes Model
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



