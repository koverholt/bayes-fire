#!/usr/bin/env python

"""Module for computing TGA curve assuming serial reactions """

import numpy as np
from scipy.integrate import odeint

# constants
R       = 8.314         # J/mol-K

# scenario parameters
T_0     = 298.          # K
T_f     = 900.         # K
#T_f     = T[-1]         # K

# numerical parameters
N_t     = 200
N_c     = 3             # number of components

# initial component mass fractions
w_0     = np.zeros( N_c )
w_0[0]  = 1.
T_sol   = np.linspace(T_0, T_f, N_t)

#nu[-1,1] = 0.

# ODE RHS
def func( w, T, logA, E, nu ):
    
    # compute rate constants
    k       = 10.**logA*np.exp(-E/(R*T))

    # compute RHS
    dw_dT   = (-k*w + np.append(0., k[0:-1]*nu[0:-1]*w[0:-1]))/beta

    return dw_dT

#def jac( w, T, K ):
#    
#    # compute rate constants
#    k1          = 10.**K[0]*np.exp(-K[1]/(R*T))
#    k2          = 10.**K[2]*np.exp(-K[3]/(R*T))
#
#    J   = [ [    -k1/beta,          0.,   0.      ],
#            [ nu1*k1/beta,    -k2/beta,   0.      ],
#            [          0., nu2*k2/beta,   0.      ] ]
#
#    return J
#
# solve ODE
def tga_solve( theta ):

    # parse parameter list
    logA    = theta[0]
    E       = theta[1]
    nu      = theta[2]

    sol     = odeint( func, w_0, T_sol, args=(logA, E, nu) ) #, Dfun=jac )
    
    return np.sum(sol, 1)
