#!/usr/bin/env python

"""Module for setting up statistical models"""

from __future__ import division

from math import pi
import numpy as np
import pymc as mc
import graphics
import data_heat_flux


def linear():
    """
    PyMC configuration with a linear model.

    This is an example of the Bayes MCMC model with
    the linear model as the model.
    """
    # Priors
    theta = mc.Uninformative('theta', value=[0., 0.])
    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)

    # Model
    @mc.deterministic
    def y_mean(theta=theta, R=data_heat_flux.distance):
        return theta[0]*R + theta[1]

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_heat_flux.heat_flux,
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()


def point_source():
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
                       lower=[50.], upper=[300.], value=[200.])

    # If you uncomment the below theta line,
    # then the prior is N(mu, sigma^2),
    # where mu is specified as 100 and sigma^2 is 10,000.
    # theta = mc.Normal('theta', mu=[100], tau=[0.0001])

    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)

    # Model
    @mc.deterministic
    def y_mean(theta=theta, R=data_heat_flux.distance):
        return 0.30 * theta / (4 * pi * (R)**2)

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_heat_flux.heat_flux,
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()


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
