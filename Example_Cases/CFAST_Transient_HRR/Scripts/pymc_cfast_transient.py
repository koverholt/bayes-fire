#!/usr/bin/env python

"""
PyMC simulation using CFAST to invert for a transient HRR.

In this example, we use PyMC to search for an inverse
transient HRR solution given synthetic temperature data.
"""

import matplotlib
matplotlib.use("Agg")

import pymc as mc
import models
import graphics

# Generate model
vars = models.cfast_transient()

# Fit model with MAP estimates
map = mc.MAP(vars)
map.fit(method='fmin_powell', verbose=2)

# Import model variables and set database options
m = mc.MCMC(vars,
            db='sqlite',
            dbname='../Figures/example_cfast_transient.sqlite')

# Use adaptive Metropolis-Hastings step method
m.use_step_method(mc.AdaptiveMetropolis, [m.theta])

# Configure and run MCMC simulation
m.sample(iter=50000, burn=25000, thin=10, verbose=2)

graphics.plot_cfast_transient_hrr(m)

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m,
                format='pdf',
                path='../Figures/example_cfast_transient',
                common_scale=False)

# Display results
m.theta.summary()
