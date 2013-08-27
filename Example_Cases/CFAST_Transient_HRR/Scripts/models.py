#!/usr/bin/env python

"""Module for setting up statistical models"""

from __future__ import division

from math import pi
import numpy as np
import pymc as mc
import graphics
import data_cfast_transient
import external_cfast


def cfast_transient():
    """
    PyMC configuration with CFAST as the model.

    This is an example of the Bayes MCMC model with CFAST
    as the model.

    In this example, the HRR linearly increases
    from 0 kW to 100 kW in the compartment from 0 s to 100 s
    """

    # Gen number of rows from time data
    num_rows = len(data_cfast_transient.time)

    # Specify number of time divisions for HRR
    num_rows_time_hrr = 61

    # Priors
    theta = mc.Uniform('theta',
                       lower=[0.01]*num_rows_time_hrr,
                       value=[50]*num_rows_time_hrr,
                       upper=[500]*num_rows_time_hrr)

    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)

    # Model
    @mc.deterministic
    def y_mean(theta=theta,
               ramp_t=np.linspace(0, 600, num_rows_time_hrr+1)):
        casename = external_cfast.gen_input(
            x=5.82, y=4.78, z=2.44,
            door_height=1.8,
            door_width=0.9,
            t_amb=20,
            HoC=50000,
            time_ramp=ramp_t,
            hrr_ramp=theta,
            num=1,
            door='Open',
            wall='gypsum',
            simulation_time=600,
            dt_data=1)

        external_cfast.run_cfast(casename)
        temps, outfile = external_cfast.read_cfast(casename)
        outfile.close()

        # Truncate array if greater than num_rows
        hgl = temps[:num_rows, 1]

        # Grow array with zeros if less than num_rows
        if len(hgl) < num_rows:
            hgl = np.append(hgl, np.zeros(num_rows - len(hgl)))

        # Print time-temperature searches
        graphics.plot_cfast_transient_temp(hgl)

        return hgl

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_cfast_transient.temperature,
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()
