import numpy as np

from functools import wraps
from time import time

# GENERIC TIME WRAPPER FUNCTION
def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result =f(*args, **kw)
        te = time()
        print('func:%r args:[%r, %r] took %2.4f sec' % \
              (f.__name__, args, kw, te-ts))
        return result
    return wrap

# BINOMIAL TREE REPRESENTATION
S0 = 100 # initial stock price
K = 100 # strike price
T = 1 # time to maturity in years
r = 0.06 # annual risk-free rate
N = 3 # number of time steps
u = 1.1 # up-factor in binomial models
d = 1/u # ensure recombining tree
opttype = 'C' # Option Type 'C' or 'P'

# BINOMIAL TREE SLOW
# def binomialTreeSlow(K, T, S0, r, N, u, d, opttype='C'):
#     # precompute constants
#     dt = T/N
#     q = (np.exp(r*dt) - d)/(u-d)
#     discount = np.exp(-r * dt)

#     # Initialise asset prices at maturity -> Time Step N
#     S = np.zeros(N+1)
#     S[0] = S0 * d**N
#     for j in range(1, N + 1):
#         S[j] = S[j-1]*u/d

#     # initialise option values at maturity
#     C = np.zeros(N+1)
#     for j in range(N+1):
#         C[j] = max(0, S[j]-K)

#     # step backwards through tree
#     for i in np.arange(N, 0, -1):
#         for j in range(0, i):
#             C[j] = discount * (q * C[j+1] + (1-q) * C[j])
    
#     return C[0]
# binomialTreeSlow(K, T, S0, r, N, u, d, opttype='C')

# BINOMIAL TREE FAST
def binomialTreeFast(K, T, S0, r, N, u, d, opttype='C'):
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
print(binomialTreeFast(K, T, S0, r, N, u, d, opttype='C'))