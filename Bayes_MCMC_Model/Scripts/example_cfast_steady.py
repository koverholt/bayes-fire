#!/usr/bin/env python

"""
PyMC simulation using CFAST to invert for a steady-state HRR.

In this example, we use PyMC to search for an inverse
steady-state HRR solution given measured temperature data
from comparment fire experiments by Steckler.
"""

import matplotlib
matplotlib.use("Agg")

import pymc as mc
import models

# Generate model
vars = models.cfast_steady()

# Fit model with MAP estimates
map = mc.MAP(vars)
map.fit(method='fmin_powell', verbose=2)

# Import model variables and set database options
m = mc.MCMC(vars,
            db='sqlite',
            dbname='../Figures/example_cfast_steady.sqlite')

# Configure and run MCMC simulation
m.sample(iter=50000, burn=25000, thin=10)

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m,
                format='pdf',
                path='../Figures/example_cfast_steady',
                common_scale=False)

# Display results
m.theta.summary()
