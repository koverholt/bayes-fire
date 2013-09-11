#!/usr/bin/env python

"""Module for setting up statistical models"""

from __future__ import division

import numpy as np
import pymc as mc


def linear(x, y):
    """
    PyMC configuration with linear model.

    y = theta[0]*x
    """
    # Priors
    theta = mc.Uniform('theta',
                       lower=[-10],
                       upper=[ 10],
                       value=[  5])
    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)

    # Model
    @mc.deterministic
    def y_mean(theta=theta,
               x=x,
               y=y):
        return theta[0] * x

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=y,
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()
