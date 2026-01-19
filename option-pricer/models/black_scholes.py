import math
from scipy.stats import norm

# UPDATE TO INTAKE FROM USER INPUT !!!

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

# CHANGE RETURN TO PROVIDE VALUE

# Printing the results (d1/2 rounded to 4dp, C and P rounded to 2dp)
print(f'The value of d1 is: {round(d1, 4)}')
print(f'The value of d2 is: {round(d2, 4)}')
print(f'The price of the call option is: ${round(C, 2)}')
print(f'The price of the put option is: ${round(P, 2)}')