#/usr/bin/env python

# May 2014

"""Module for setting up statistical models"""

from __future__ import division

import numpy as np
import pymc as mc
from scipy.integrate import odeint
import data_expt as de
from matplotlib import pyplot as plt

# constants
R       = 8.314         # J/mol-K
nu1     = 145./172.     # M2/M1
nu2     = 136./145.     # M3/M2

# material properties
wf      = de.w[-1]
w1_0    = (1. - wf)/(1. - nu1*nu2)
w2_0    = 0.
w3_0    = 1. - w1_0

# scenario parameters
T_0     = 320.0         # K
beta    = 5./60           # heating rate, K/min
T_f     = de.T[-1]         # K

# numerical parameters
N_t     = 200

# build arrays
w_0     = np.array([ w1_0, w2_0, w3_0 ])
T_sol   = np.linspace(T_0, T_f, N_t)

# parameter list: [ A1, E1, A2, E2 ]
#params      = [ 5e12, 100e3, 1e21, 175e3 ]
params      = [ 1.8e18, 160e3, 7.6e27, 250e3 ]
params_L    = [ 1e9, 80e3, 1e9, 80e3 ]
params_U    = [ 1e30, 400e3, 1e30, 400e3 ]

# ODE RHS
def func( w, T, K ):
    
    # compute rate constants
    k1          = K[0]*np.exp(-K[1]/(R*T))
    k2          = K[2]*np.exp(-K[3]/(R*T))

    dw_dT       = np.zeros(3)
    dw_dT[0]    = (-k1*w[0])/beta
    dw_dT[1]    = (nu1*k1*w[0] - k2*w[1])/beta
    dw_dT[2]    = (nu2*k2*w[1])/beta
   
    return dw_dT

def jac( w, T, K ):
    
    # compute rate constants
    k1          = K[0]*np.exp(-K[1]/(R*T))
    k2          = K[2]*np.exp(-K[3]/(R*T))

    J   = [ [    -k1/beta,     0.,   0.      ],
            [ nu1*k1/beta,    -k2/beta,   0.      ],
            [     0., nu2*k2/beta,   0.      ] ]

    return J

theta = params

sol     = odeint( func, w_0, T_sol, args=(theta,), Dfun=jac)
   
w_sol   = np.sum(sol, 1)
T_exp   = de.T
w_int   = np.interp( T_exp, T_sol, w_sol )

plt.ion()

plt.figure(1)
plt.plot(T_sol-273.15, w_sol)
plt.plot(de.T-273.15, de.w, 'kx')
plt.show()
