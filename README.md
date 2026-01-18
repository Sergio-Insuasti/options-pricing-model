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
│   └── app.py              # Streamlit UI
├── tests/
└── README.md

## PHASE 1: INTERACTIVE DASHBOARD
For this phase, my intention is to create an interactive dashboard through my knowledge
of Python. With this dashboard users can configure option parameters,
run the three most popular option pricing models and compare prices, Greeks,
convergence and uncertainty.

