#/usr/bin/env python

# May 2014

"""Module for setting up statistical models"""

from __future__ import division

import numpy as np
import pymc as mc
from scipy.integrate import odeint
import data_expt as de

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
beta    = 5./60.           # heating rate, K/min
T_f     = de.T[-1]         # K

# numerical parameters
N_t     = 200

# build arrays
w_0     = np.array([ w1_0, w2_0, w3_0 ])
T_sol   = np.linspace(T_0, T_f, N_t)

# parameter list: [ logA1, E1, logA2, E2 ]
params      = [ 16.5, 146e3, 27.5, 249e3 ]
params_L    = [ 9., 80e3, 9., 80e3 ]
params_U    = [ 40., 400e3, 40., 400e3 ]
#params_0    = [ 1., 1., 1., 1. ]
#params_L    = [ 0.4, 0.4, 0.4, 0.4 ]
#params_U    = [ 2.2, 2.2, 2.2, 2.2 ]

# ODE RHS
def func( w, T, K ):
    
    # compute rate constants
    k1          = 10.**K[0]*np.exp(-K[1]/(R*T))
    k2          = 10.**K[2]*np.exp(-K[3]/(R*T))

    dw_dT       = np.zeros(3)
    dw_dT[0]    = (-k1*w[0])/beta
    dw_dT[1]    = (nu1*k1*w[0] - k2*w[1])/beta
    dw_dT[2]    = (nu2*k2*w[1])/beta
   
    return dw_dT

def jac( w, T, K ):
    
    # compute rate constants
    k1          = 10.**K[0]*np.exp(-K[1]/(R*T))
    k2          = 10.**K[2]*np.exp(-K[3]/(R*T))

    J   = [ [    -k1/beta,          0.,   0.      ],
            [ nu1*k1/beta,    -k2/beta,   0.      ],
            [          0., nu2*k2/beta,   0.      ] ]

    return J

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
    #sigma = mc.Uniform('sigma', lower=0., upper=1., value=0.01)

    # Model
    @mc.deterministic
    def y_mean(theta=theta):
       
        sol     = odeint( func, w_0, T_sol, args=(theta,), Dfun=jac )
   
        w_sol   = np.sum(sol, 1)
        #w_sol   = (1. - nu)*np.sum(sol, 1) + nu*w_0[0] + w_0[1]

        T_exp   = de.T
        #w_exp   = de.w
        w_int   = np.interp( T_exp, T_sol, w_sol )
        
        #print theta
        #print w_int
        #print w_exp
        #print np.sum((w_int - w_exp)**2)

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
