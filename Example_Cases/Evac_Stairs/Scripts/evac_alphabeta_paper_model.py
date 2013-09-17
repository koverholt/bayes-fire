#!/usr/bin/env python

"""Module for setting up statistical models"""

from __future__ import division

import numpy as np
import pymc as mc
import evac_flow_exit_mu_single_graphics as graphics
import data_evac


def model1():
    """
    PyMC configuration with Model 1.

    preevac_alpha vs theta[0] + theta[1]*type + theta[2]*eff_wid + theta[3]*tread
    """
    # Priors
    theta = mc.Uniform('theta',
                       lower=[-10.0, -10.0],
                       upper=[ 10.0,  10.0],
                       value=[  0.1,   0.1])
    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)

    # Model
    @mc.deterministic
    def y_mean(theta=theta,
               beta = data_evac.data_alphabeta['beta']):
        return theta[0]*beta**theta[1]

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_evac.data_alphabeta['alpha'],
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()

def model2():
    """
        PyMC configuration with Model 2.
        
        preevac_alpha vs theta[0] + theta[1]*type + theta[2]*eff_wid + theta[3]*tread
        """
    # Priors
    theta = mc.Uniform('theta',
                       lower=[-10.0, -10.0],
                       upper=[ 10.0,  10.0],
                       value=[  0.1,   0.1])
    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)
    
    # Model
    @mc.deterministic
    def y_mean(theta=theta,
               alpha = data_evac.data_alphabeta['alpha']):
        return theta[0]*alpha**theta[1]
    
    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_evac.data_alphabeta['beta'],
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)
    
    return vars()
def model3():
    """
        PyMC configuration with Model 1.
        
        preevac_alpha vs theta[0] + theta[1]*type + theta[2]*eff_wid + theta[3]*tread
        """
    # Priors
    theta = mc.Uniform('theta',
                       lower=[-10.0, -10.0],
                       upper=[ 10.0,  10.0],
                       value=[  0.1,   0.1])
    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)
    
    # Model
    @mc.deterministic
    def y_mean(theta=theta,
               beta = data_evac.data_alphabeta['beta']):
        return theta[0]*beta + theta[1]
    
    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_evac.data_alphabeta['alpha'],
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)
    
    return vars()

def model4():
    """
        PyMC configuration with Model 2.
        
        preevac_alpha vs theta[0] + theta[1]*type + theta[2]*eff_wid + theta[3]*tread
        """
    # Priors
    theta = mc.Uniform('theta',
                       lower=[-10.0, -10.0],
                       upper=[ 10.0,  10.0],
                       value=[  0.1,   0.1])
    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)
    
    # Model
    @mc.deterministic
    def y_mean(theta=theta,
               alpha = data_evac.data_alphabeta['alpha']):
        return theta[0]*alpha + theta[1]
    
    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_evac.data_alphabeta['beta'],
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)
    
    return vars()




