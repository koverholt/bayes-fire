#!/usr/bin/env python

""" Module for setting up statistical models"""

from __future__ import division

import pymc as mc
import numpy as np
from math import pi

import data_fds_300kW
import data_fds_1000kW


def point_source_radiation_fds(hrr, fire_size):
    """In this example, the fire (radiation source) is located at (2,2) in
    x-y coordinates, and two heat flux gauges are located at (1,0) and (5,0).
    The point source radiation heat flux is calculated at the gauge,
    then used as the input. This method searches for the input x, y
    values to determine the best estimate of fire location in the room.
    """

    if hrr == 300:
        x_gauge = data_fds_300kW.x_gauge
        y_gauge = data_fds_300kW.y_gauge
        heat_flux = data_fds_300kW.heat_flux
    elif hrr == 1000:
        x_gauge = data_fds_1000kW.x_gauge
        y_gauge = data_fds_1000kW.y_gauge
        heat_flux = data_fds_1000kW.heat_flux

    # Priors
    x = mc.Uniform('x', lower=[0], upper=[10], value=[5])
    y = mc.Uniform('y', lower=[0], upper=[10], value=[5])
    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)

    # Model
    @mc.deterministic
    def y_mean(x=x, y=y):
        x = abs(x - x_gauge)
        y = abs(y - y_gauge)
        R = np.sqrt((x)**2 + (y)**2)
        return (y / R) * 0.35 * hrr / (4 * pi * (R)**2)

    # You can also try to guess Q.
    # Q = mc.Uniform('Q', lower=[0], upper=[3000])

    # This is the estimator.
    # @mc.deterministic
    # def y_mean(x=x, y=y, Q=Q):
        # x = abs(x - x_gauge)
        # y = abs(y - y_gauge)
        # R = np.sqrt((x)**2 + (y)**2)
        # return (y / R) * Q * 0.30 / (4 * pi * (R)**2)

    # Likelihood
    # The likelihood is N(mu_i, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs', value=heat_flux,
                      mu=y_mean, tau=sigma**-2,
                      observed=True)

    return vars()
