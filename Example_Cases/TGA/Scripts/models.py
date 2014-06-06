#/usr/bin/env python

# June 2014

"""Module for setting up statistical models"""

from __future__ import division

import numpy as np
import pymc as mc
import data_expt as de
import tga

# scenario parameters
T_0     = de.T[0] - 50.                 # initial simulation temperature, K
beta    = de.beta                       # heating rate, K/s
T_f     = de.T[-1]                      # final simulation temperature, K

# numerical parameters
N_t     = 200                           # resolution of solution
T_sol   = np.linspace(T_0, T_f, N_t)    # solution temperatures, K

# parameters, logA, E, nu
E_l     = 120e3                         # lower bound activation energy, J/mol-K
E_u     = 250e3                         # upper bound activation energy, J/mol-K
N_c     = 2                             # number of components
logA    = 14.*np.ones( N_c )            # log of pre-exponential, log(1/s)
E       = np.linspace(E_l, E_u, N_c)    # E, J/mol
nu      = 0.5*np.ones( N_c )            # vector of stoichiometric coefficients

# parameter list: [ logA, E, nu ]
params      = np.append( logA, np.append(E, nu) )
#params_L    = [ 9., 80e3, 9., 80e3 ]
#params_U    = [ 40., 400e3, 40., 400e3 ]
##params_0    = [ 1., 1., 1., 1. ]
##params_L    = [ 0.4, 0.4, 0.4, 0.4 ]
##params_U    = [ 2.2, 2.2, 2.2, 2.2 ]
#
#def tga_w():
#    """PyMC configuration with TGA model."""
#    # Priors
#    # TGA model inputs: A1, E1, A2, E2
#    theta = mc.Uniform(
#        'theta',
#        value=params,
#        lower=params_L,
#        upper=params_U)
#        
#    sigma = mc.Uniform('sigma', lower=0., upper=1., value=0.05)
#    #sigma = mc.Uniform('sigma', lower=0., upper=1., value=0.01)
#
#    # Model
#    @mc.deterministic
#    def y_mean(theta=theta):
#       
#        sol     = odeint( func, w_0, T_sol, args=(theta,), Dfun=jac )
#   
#        w_sol   = np.sum(sol, 1)
#        #w_sol   = (1. - nu)*np.sum(sol, 1) + nu*w_0[0] + w_0[1]
#
#        T_exp   = de.T
#        #w_exp   = de.w
#        w_int   = np.interp( T_exp, T_sol, w_sol )
#        
#        #print theta
#        #print w_int
#        #print w_exp
#        #print np.sum((w_int - w_exp)**2)
#
#        return w_int
#
#    # Likelihood
#    # The likelihood is N(y_mean, sigma^2), where sigma
#    # is pulled from a uniform distribution.
#    y_obs = mc.Normal('y_obs',
#                      value=de.w,
#                      mu=y_mean,
#                      tau=sigma**-2,
#                      observed=True)
#
#    return vars()
