#!/usr/bin/env python

"""
PyMC simulation using FDS to invert for pyrolysis parameters.

In this example, the mass loss rate (MLR) (g/s) from a cone test of a
2-inch thick sample of PMMA. The inputs are A, E, emissivity,
heat of reaction, heat of combustion, thermal conductivity,
and specific heat. These # inputs are fed into FDS with a model of
the "virtual material", and the MLR is attempted to be recovered.
"""

import matplotlib
matplotlib.use("Agg")

import pymc as mc
import models

# Generate model
vars = models.fds_mlr()

# Fit model with MAP estimates
map = mc.MAP(vars)
map.fit(method='fmin_ncg', verbose=2)

# Import model variables and set database options
m = mc.MCMC(vars,
            db='sqlite',
            dbname='../Figures/example_fds.sqlite')

# Use adaptive Metropolis-Hastings step method
m.use_step_method(mc.AdaptiveMetropolis, [m.theta])

# Configure and run MCMC simulation
m.sample(iter=100000, burn=50000, thin=10, verbose=2)

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m,
                format='pdf',
                path='../Figures/example_fds',
                common_scale=False)

# Display results
m.theta.summary()
