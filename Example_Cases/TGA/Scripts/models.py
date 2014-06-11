#/usr/bin/env python

# June 2014

"""Module for setting up statistical models"""

from __future__ import division

import numpy as np
from scipy.integrate import odeint
import pymc as mc
import data_expt as de
import tga

# scenario parameters
T_exp   = de.T                          # experimental temperatures, K
T_0     = de.T[0] - 50.                 # initial simulation temperature, K
beta    = de.beta                       # heating rate, K/s
T_f     = de.T[-1]                      # final simulation temperature, K
w_f     = de.w[-1]                      # residual mass fraction

# numerical parameters
N_t     = 200                           # resolution of solution
T_sol   = np.linspace(T_0, T_f, N_t)    # solution temperatures, K

# specified parameters
N_c     = 4                             # number of components

# uncertain parameters, logA, E, nu
E_1     = 120e3                         # lower bound activation energy, J/mol-K
E_2     = 250e3                         # upper bound activation energy, J/mol-K
E_L     = 60e3*np.ones( N_c - 1 )
E       = np.linspace(E_1, E_2, N_c-1 ) # E, J/mol
E_U     = 500e3*np.ones( N_c - 1 )

logA_L  = 4.*np.ones( N_c - 1 )
logA    = 14.*np.ones( N_c - 1 )        # log of pre-exponential, log(1/s)
logA_U  = 40.*np.ones( N_c - 1 )

nu_L    = w_f*np.ones( N_c - 2 )
nu      = w_f**(1./(N_c-1))*np.ones( N_c - 2 )  # vector of stoichiometric coefficients
nu_U    = np.ones( N_c - 2 )

# parameter list: [ logA, E, nu ]
params      = np.append( logA, np.append(E, nu) )
params_L    = np.append( logA_L, np.append(E_L, nu_L) )
params_U    = np.append( logA_U, np.append(E_U, nu_U) )

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
     
        w_sol   = tga.tga_solve( theta, beta, w_f, T_sol )
        
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
