#/usr/bin/env python

# June 2014

"""Module for setting up statistical models"""

from __future__ import division

import numpy as np
from scipy.integrate import odeint
import pymc as mc
import data_expt as de

# constants
R       = 8.314         # J/mol-K

# scenario parameters
T_0     = de.T[0] - 50.                 # initial simulation temperature, K
beta    = de.beta                       # heating rate, K/s
T_f     = de.T[-1]                      # final simulation temperature, K
w_f     = de.w[-1]                      # residual mass fraction

# numerical parameters
N_t     = 200                           # resolution of solution
T_sol   = np.linspace(T_0, T_f, N_t)    # solution temperatures, K

# parameters
N_c     = 3                             # number of components
w_0     = np.zeros( N_c )               # initial component mass fractions
w_0[0]  = 1.


# parameters, logA, E, nu
E_1     = 120e3                         # lower bound activation energy, J/mol-K
E_2     = 250e3                         # upper bound activation energy, J/mol-K
logA    = 14.*np.ones( N_c - 1 )        # log of pre-exponential, log(1/s)
E       = np.linspace(E_1, E_2, N_c-1 ) # E, J/mol
nu      = 0.5*np.ones( N_c - 2 )        # vector of stoichiometric coefficients

logA_L  = 8.*np.ones( N_c - 1 )
logA_U  = 40.*np.ones( N_c - 1 )
E_L     = 90e3*np.ones( N_c - 1 )
E_U     = 500e3*np.ones( N_c - 1 )
nu_L    = np.zeros( N_c - 2 )
nu_U    = np.ones( N_c - 2 )


# parameter list: [ logA, E, nu ]
params      = np.append( logA, np.append(E, nu) )
params_L    = np.append( logA_L, np.append(E_L, nu_L) )
params_U    = np.append( logA_U, np.append(E_U, nu_U) )

print nu

print params

# ODE RHS
def func( w, T, logA, E, nu, nu_f ):
    
    # compute rate constants
    k       = 10.**logA*np.exp(-E/(R*T))

    # compute RHS
    dw_dT       = np.zeros( N_c )
    dw_dT[0]    = -k[0]*w[0]/beta
    dw_dT[1:-1] = (-k[1:-1]*w[1:-1] 
                    + k[0:-2]*nu*w[0:-2])/beta
    dw_dT[-1]   = k[-1]*nu_f*w[-2]/beta

    return dw_dT

def tga_w():
    """PyMC configuration with TGA model."""
    # Priors
    # TGA model inputs: A1, E1, A2, E2
    theta = mc.Uniform(
        'theta',
        value=params,
        lower=params_L,
        upper=params_U)
        
    sigma = mc.Uniform('sigma', lower=0., upper=1., value=0.05)

    # Model
    @mc.deterministic
    def y_mean(theta=theta):
     
        # parse parameter list
        logA    = theta[0:N_c-1]
        E       = theta[N_c-1:2*N_c-2]
        nu      = theta[2*N_c-2:]
        #print logA
        #print E
        #print nu
        #print theta.shape

        nu_f    = w_f/np.prod(nu)

        sol     = odeint( func, w_0, T_sol, args=(logA, E, nu, nu_f) ) 
      
        w_sol   = np.sum(sol, 1)

        T_exp   = de.T
        w_int   = np.interp( T_exp, T_sol, w_sol )
        
        return w_int

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=de.w,
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()
