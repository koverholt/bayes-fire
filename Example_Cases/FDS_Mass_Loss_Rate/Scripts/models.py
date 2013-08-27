#!/usr/bin/env python

"""Module for setting up statistical models"""

from __future__ import division

from math import pi
import numpy as np
import pymc as mc
import graphics
import data_fds
import external_fds


def fds_mlr():
    """PyMC configuration with FDS as the model."""
    # Priors
    # FDS inputs: abs_coeff, A, E, emissivity, HoR, k, rho, c
    theta = mc.Uniform(
        'theta',
        lower=[1,    7.5e12, 187e3, 0.75, 500,  0.01, 500,  0.5],
        value=[2500, 8.5e12, 188e3, 0.85, 750,  0.25, 1000, 3.0],
        upper=[5000, 9.5e12, 189e3, 1.00, 2000, 0.50, 2000, 6.0])

    sigma = mc.Uniform('sigma', lower=0., upper=10., value=0.100)

    # Model
    @mc.deterministic
    def y_mean(theta=theta):
        casename = external_fds.gen_input(
            abs_coeff=theta[0],
            A=theta[1],
            E=theta[2],
            emissivity=theta[3],
            HoR=theta[4],
            k=theta[5],
            rho=theta[6],
            c=theta[7])

        external_fds.run_fds(casename)
        mlrs = external_fds.read_fds(casename)
        mlr = mlrs[:, 2]

        # Print MLR vs. time for each iteration
        graphics.plot_fds_mlr(mlr)

        return mlr

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_fds.mlr,
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()
