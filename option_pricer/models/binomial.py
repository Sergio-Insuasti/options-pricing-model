import numpy as np

# BINOMIAL TREE REPRESENTATION
S0 = 100 # initial stock price
K = 100 # strike price
T = 1 # time to maturity in years
r = 0.06 # annual risk-free rate
N = 3 # number of time steps
u = 1.1 # up-factor in binomial models
d = 1/u # ensure recombining tree
opttype = 'C' # Option Type 'C' or 'P'


# BINOMIAL TREE FAST
def binomialTree(K, T, S0, r, N, u, d, opttype='C'):
    # precompute constants
    dt = T/N
    q = (np.exp(r*dt) - d)/(u-d)
    discount = np.exp(-r * dt)

    # Initialise asset prices at maturity -> Time Step N
    C = S0*d**(np.arange(N, -1, -1))*u**(np.arange(0, N+1,1))

    # initialise option values at maturity
    C = np.maximum( C - K, np.zeros(N+1) )

    # step backwards through tree
    for i in np.arange(N, 0, -1):
        C = discount * ( q * C[1:i+1] + (1-q)* C[0:i])
    
    return C[0]
print(binomialTree(K, T, S0, r, N, u, d, opttype='C'))