#!/usr/bin/env python

"""Module for setting up statistical models"""

from __future__ import division

from math import pi
import numpy as np
import pymc as mc
import evac_flow_exit_dist_graphics as graphics
import data_evac


def linear():
    """
    PyMC configuration with a linear model.

    This is an example of the Bayes MCMC model with
    the linear model as the model.
    """
    # Priors
    theta = mc.Uninformative('theta', value=[1., 1.])
    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)

    # Model
    @mc.deterministic
    def y_mean(theta=theta, exit_distance=data_evac.exit_distance):
        return theta[0]*exit_distance + theta[1]

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_evac.flow,
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()


def power_law():
    """
    PyMC configuration with a point source radiation model.

    This is an example of the Bayes MCMC model with
    the point source radiation equation as the model.
    """
    # Priors
    # If you uncomment the below theta line,
    # then the prior is N(mu, sigma^2),
    # where in the uninformed setup, mu is any value,
    # and sigma^2 approaches infinity.
    # theta = mc.Uninformative('theta', value=[0])

    # If you uncomment the below theta line, then the prior is
    # a uniform distribution with a range of 50 to 300.
    theta = mc.Uniform('theta',
                       lower=[-10, -5], upper=[10, 5], value=[0, 0])

    # If you uncomment the below theta line,
    # then the prior is N(mu, sigma^2),
    # where mu is specified as 100 and sigma^2 is 10,000.
    # theta = mc.Normal('theta', mu=[100], tau=[0.0001])

    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)

    # Model
    @mc.deterministic
    def y_mean(theta=theta, exit_distance=data_evac.exit_distance):
        return theta[0] * (exit_distance**theta[1])

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_evac.flow,
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()
