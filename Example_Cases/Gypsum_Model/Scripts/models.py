#!/usr/bin/env python

"""Module for setting up statistical models"""

from __future__ import division

from math import pi
import numpy as np
import pymc as mc
#import graphics
import data_expt
import external_gyp1d


def gyp1d_temps():
    """PyMC configuration with gyp1d as the model."""
    # Priors
    # gyp1d inputs:    k1, k2, k3, k4, rho_0, c_p1, c_p2, c_p3, eps, Y1_0,
    #                  A1, A2, E1, E2, dh1, dh2 
    theta = mc.Uniform(
        'theta',
        lower=[0.896, 0.163, 0.361, 6.10, 583., 49.9, 4120.,
                4640., 0.9, 0.761, 5.00e12, 9.09e20, 9.00e4,
                1.57e5, 2.39e4, 1.06e6],
        value=[0.995, 0.181, 0.401, 6.78, 648., 55.4, 4580.,
                5160., 1.0, 0.846, 5.56e12, 1.01e21, 1.00e5,
                1.74e5, 2.65e4, 1.18e6],
        upper=[1.09, 0.199, 0.441, 7.46, 713., 60.9, 5038.,
                5676., 1.0, 0.931, 6.12e12, 1.11e21, 1.10e5,
                1.91e5, 2.92e4, 1.30e6])

    sigma = mc.Uniform('sigma', lower=0., upper=10., value=0.100)

    # Model
    @mc.deterministic
    def y_mean(theta=theta):
        casename = external_gyp1d.gen_input(
                k1=theta[0], 
                k2=theta[1], 
                k3=theta[2], 
                k4=theta[3], 
                rho_0=theta[4], 
                c_p1=theta[5], 
                c_p2=theta[6], 
                c_p3=theta[7], 
                eps=theta[8], 
                Y1_0=theta[9],
                A1=theta[10], 
                A2=theta[11], 
                E1=theta[12], 
                E2=theta[13], 
                dh1=theta[14], 
                dh2=theta[15])

        external_gyp1d.run_gyp1d(casename)
        T_1b = external_gyp1d.read_gyp1d(casename)

        return T_1b

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_expt.T_1b,
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()
