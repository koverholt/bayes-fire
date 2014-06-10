#/usr/bin/env python

# June 2014

"""Module for doing TGA model calculations """

import numpy as np
from scipy.integrate import odeint

# constants
R       = 8.314         # J/mol-K

# ODE RHS
def func( w, T, logA, E, nu, nu_f, beta ):
    
    # compute rate constants
    k       = 10.**logA*np.exp(-E/(R*T))/beta
    
    # compute RHS
    dw_dT       = np.zeros( len(w) )
    dw_dT[0]    = -k[0]*w[0]
    for i in range(1, len(w)-1):
        dw_dT[i] = -k[i]*w[i] + k[i-1]*nu[i-1]*w[i-1]
    dw_dT[-1]   = k[-1]*nu_f*w[-2]

    return dw_dT

# solve ODE
def tga_solve( params, beta, w_f, T_sol ):

    # parse parameter list
    N_c     = (len(params) + 4)/3
    logA    = params[0:N_c-1]
    E       = params[N_c-1:2*N_c-2]
    nu      = params[2*N_c-2:]
    nu_f    = w_f/np.prod(nu)

    # initial conditions
    w_0     = np.zeros( N_c )
    w_0[0]  = 1.

    # solve
    sol     = odeint( func, w_0, T_sol, args=(logA, E, nu, nu_f, beta) ) 

    return np.sum(sol, 1)
