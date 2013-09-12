#!/usr/bin/env python

"""Module for setting up statistical models"""

from __future__ import division

import numpy as np
import pymc as mc
import evac_flow_three_parameter_graphics as graphics
import data_evac


def model1():
    """
    PyMC configuration with Model 1.
    """
    # Priors
    theta = mc.Uniform('theta',
                       lower=[-30, -30, -30, -30],
                       upper=[ 30,  30,  30,  30],
                       value=[ 15,  15,  15,  15])
    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)

    # Model
    @mc.deterministic
    def y_mean(theta=theta,
               occupants=data_evac.data_three_parameter['occupants'],
               exit_distance=data_evac.data_three_parameter['exit_distance'],
               type=data_evac.data_three_parameter['type']):
        return (theta[0] * occupants +
                theta[1] * exit_distance +
                theta[2] * type +
                theta[3])

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_evac.data_three_parameter['pre_evac_int'],
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()


def model2():
    """
    PyMC configuration with Model 2.
    """
    # Priors
    theta = mc.Uniform('theta',
                       lower=[-30, -30, -30, -30, -30, -30],
                       upper=[ 30,  30,  30,  30,  30,  30],
                       value=[ 15,  15,  15,  15,  15,  15])
    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)

    # Model
    @mc.deterministic
    def y_mean(theta=theta,
               occupants=data_evac.data_three_parameter['occupants'],
               exit_distance=data_evac.data_three_parameter['exit_distance'],
               type=data_evac.data_three_parameter['type'],
               riser=data_evac.data_three_parameter['riser'],
               tread=data_evac.data_three_parameter['tread']):
        return (theta[0] * occupants +
                theta[1] * exit_distance +
                theta[2] * type +
                theta[3] * riser +
                theta[4] * tread +
                theta[5])

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_evac.data_three_parameter['travel_int'],
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()


def model3():
    """
    PyMC configuration with Model 3.
    """
    # Priors
    theta = mc.Uniform('theta',
                       lower=[-30, -30, -30, -30, -30, -30, -30],
                       upper=[ 30,  30,  30,  30,  30,  30,  30],
                       value=[ 15,  15,  15,  15,  15,  15,  15])
    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)

    # Model
    @mc.deterministic
    def y_mean(theta=theta,
               occupants=data_evac.data_three_parameter['occupants'],
               exit_distance=data_evac.data_three_parameter['exit_distance'],
               type=data_evac.data_three_parameter['type'],
               riser=data_evac.data_three_parameter['riser'],
               tread=data_evac.data_three_parameter['tread'],
               evac_chair=data_evac.data_three_parameter['evac_chair']):
        return (theta[0] * occupants +
                theta[1] * exit_distance +
                theta[2] * type +
                theta[3] * riser +
                theta[4] * tread +
                theta[5] * evac_chair +
                theta[6])

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_evac.data_three_parameter['exit_int'],
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()
