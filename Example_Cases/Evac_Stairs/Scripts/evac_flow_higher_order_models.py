#!/usr/bin/env python

"""Module for setting up statistical models"""

from __future__ import division

from math import pi
import numpy as np
import pymc as mc
import evac_flow_higher_order_graphics as graphics
import data_evac


def model1():
    """
    PyMC configuration with Model 1.

    flow vs theta[0] * occupants^theta[1] * exit_distance^theta[2]
    """
    # Priors
    theta = mc.Uniform('theta',
                       lower=[0.0, 0.0, -1.0],
                       upper=[1.0, 1.0,  0.0],
                       value=[0.5, 0.5, -0.5])
    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)

    # Model
    @mc.deterministic
    def y_mean(theta=theta,
               occupants=data_evac.occupants,
               exit_distance=data_evac.exit_distance):
        return theta[0] * occupants**theta[1] * exit_distance**theta[2]

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_evac.flow,
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()


def model2():
    """
    PyMC configuration with Model 2.

    flow vs theta[0] * occupants^theta[1] * effective_width^theta[2]
    """
    # Priors
    theta = mc.Uniform('theta',
                       lower=[0.0, 0.0, 0.0],
                       upper=[1.0, 1.0, 2.0],
                       value=[0.5, 0.5, 1.0])
    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)

    # Model
    @mc.deterministic
    def y_mean(theta=theta,
               occupants=data_evac.occupants,
               effective_width=data_evac.effective_width):
        return theta[0] * occupants**theta[1] * effective_width**theta[2]

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_evac.flow,
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()


def model3():
    """
    PyMC configuration with Model 3.

    flow vs theta[0] * occupants^theta[1] * exit_distance^theta[2] * effective_width^theta[3]
    """
    # Priors
    theta = mc.Uniform('theta',
                       lower=[0.0, 0.0, -1.0, 0.0],
                       upper=[1.0, 1.0,  0.0, 2.0],
                       value=[0.5, 0.5, -0.5, 1.0])
    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)

    # Model
    @mc.deterministic
    def y_mean(theta=theta,
               occupants=data_evac.occupants,
               exit_distance=data_evac.exit_distance,
               effective_width=data_evac.effective_width):
        return theta[0] * occupants**theta[1] * exit_distance**theta[2] * effective_width**theta[3]

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_evac.flow,
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()


def model4():
    """
    PyMC configuration with Model 4.

    flow vs theta[0] * exit_distance^theta[1] * effective_width^theta[2]
    """
    # Priors
    theta = mc.Uniform('theta',
                       lower=[0.0, 0.0, 0.0],
                       upper=[1.0, 1.0, 2.0],
                       value=[0.5, 0.5, 1.0])
    sigma = mc.Uniform('sigma', lower=0., upper=100., value=1.)

    # Model
    @mc.deterministic
    def y_mean(theta=theta,
               exit_distance=data_evac.exit_distance,
               effective_width=data_evac.effective_width):
        return theta[0] * exit_distance**theta[1] * effective_width**theta[2]

    # Likelihood
    # The likelihood is N(y_mean, sigma^2), where sigma
    # is pulled from a uniform distribution.
    y_obs = mc.Normal('y_obs',
                      value=data_evac.flow,
                      mu=y_mean,
                      tau=sigma**-2,
                      observed=True)

    return vars()
