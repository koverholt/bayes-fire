#/usr/bin/env python

# July 2014

"""Module for setting up statistical models"""

import numpy as np
from scipy.integrate import odeint
import pymc as mc
import tga

def tga_w( data, beta, N_k ):

    # scenario parameters
    beta    = float(beta)/60.                       # heating rate, K/s
    T_exp   = data[:-1,0]                     # experimental temperatures, K
    w_exp   = data[:-1,1]                     # experimental mass fractions
    T_0     = T_exp[0] - 50.                 # initial simulation temperature, K
    T_f     = data[-2,0]                      # final simulation temperature, K
    w_f     = data[-1,1]                      # residual mass fraction
    
    # numerical parameters
    N_t     = 200                           # resolution of solution
    T_sol   = np.linspace(T_0, T_f, N_t)    # solution temperatures, K
    
    # specified parameters
    N_c     = int(N_k) + 1                  # number of components
    
    # uncertain parameters, logA, E, nu
    E_1     = 150e3                         # lower bound activation energy, J/mol-K
    E_2     = 350e3                         # upper bound activation energy, J/mol-K
    E_L     = 40e3*np.ones( N_c - 1 )
    E       = np.linspace(E_1, E_2, N_c-1 ) # E, J/mol
    E_U     = 800e3*np.ones( N_c - 1 )
    
    logA_L  = 1.*np.ones( N_c - 1 )
    logA    = 20.*np.ones( N_c - 1 )        # log of pre-exponential, log(1/s)
    logA_U  = 70.*np.ones( N_c - 1 )
    
    nu_L    = w_f*np.ones( N_c - 2 )
    nu      = w_f**(1./(N_c-1))*np.ones( N_c - 2 )  # vector of stoichiometric coefficients
    nu_U    = np.ones( N_c - 2 )
    
    # parameter list: [ logA, E, nu ]
    params      = np.append( logA, np.append(E, nu) )
    params_L    = np.append( logA_L, np.append(E_L, nu_L) )
    params_U    = np.append( logA_U, np.append(E_U, nu_U) )
    
    """PyMC configuration with TGA model."""
    # Priors
    # TGA model inputs: logA, E, nu
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
                      value=w_exp,
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()
