#!/usr/bin/env python

"""Module for setting up statistical models"""

from __future__ import division

from math import pi
import numpy as np
import pymc as mc
import data_cfast_steady
import external_cfast


def cfast_steady():
    """
    PyMC configuration with CFAST as the model.

    This is an example of the Bayes MCMC model with CFAST
    as the model.

    In this example, we are trying to recover a steady-state
    HRR to cause a measured HGL temperature
    """
    # Priors
    # If you uncomment the below theta line,
    # then the prior is N(mu, sigma^2),
    # where in the uniform setup, the lower
    # is 0 and the upper is 100.
    theta = mc.Uniform('theta', lower=[1], upper=[100], value=[50])

    # If you uncomment the below theta line,
    # then the prior is N(mu, sigma^2),
    # where mu is specified as 60 and sigma^2 is 10,000.
    # theta = mc.Normal('theta', mu=[60], tau=[0.0001])

    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)

    # Model
    @mc.deterministic
    def y_mean(theta=theta,
               W_v=data_cfast_steady.door_width,
               H_v=data_cfast_steady.door_height,
               tmp_a=data_cfast_steady.tmp_a):
        resulting_temps = external_cfast.run_multiple_cases(
            x=2.8, y=2.8, z=2.13,
            door_height=H_v,
            door_width=W_v,
            t_amb=tmp_a,
            HoC=50000,
            time_ramp=[0, 1800],
            hrr_ramp=np.array([theta, theta]),
            num=1,
            door='Open',
            wall='fiberboard',
            simulation_time=1800,
            dt_data=10)

        return resulting_temps

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_cfast_steady.temperature,
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()
