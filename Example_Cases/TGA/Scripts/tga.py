#/usr/bin/env python

# July 2014

"""Module for doing TGA model calculations """

import numpy as np
from scipy.integrate import odeint
import odefort

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
def tga_solve( params, beta, w_f, T_s ):

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
    #sol     = odeint( func, w_0, T_sol, args=(logA, E, nu, nu_f, beta) ) 

    # # ------------------------------------
    # # explicit Euler
    # # ------------------------------------
   
    # N_t     = 1000
    # T_int   = np.linspace(T_sol[0], T_sol[-1], num=N_t)
    # dT      = (T_sol[-1] - T_sol[0])/(N_t - 1)

    # w = w_0
    # w_tot = np.ones(N_t)

    # for i in range(1, N_t):
    #     
    #     # compute unmodified rate constants
    #     r       = w[0:-1]*10.**logA*np.exp(-E/(R*T_int[i]))/beta

    #     r[0]    = min(r[0], w[0]/dT)
    #     w[0]    = w[0] - dT*r[0]

    #     for j in range(1, N_c-1):
    #         r[j]    = min(r[j], w[j]/dT + nu[j-1]*r[j-1])
    #         w[j]    = w[j] - dT*(r[j] - nu[j-1]*r[j-1])

    #     w[-1]  = min(w_f, w[-1] - dT*(-nu_f*r[-1]))

    #     w_tot[i] = np.sum(w)
   
    # # interpolate to solution temperatures
    # w_sol = np.interp(T_sol, T_int, w_tot)
    
    # ------------------------------------ 
    # explicit Euler -- Fortran
    # ------------------------------------ 
   
    N_t = 1000
    N_s = len(T_s)
    nu = np.append( nu, nu_f )

    w_s = odefort.solve( N_t, w_0, w_f, T_s, logA, E, nu, beta, N_c, N_s)
    
    return w_s

