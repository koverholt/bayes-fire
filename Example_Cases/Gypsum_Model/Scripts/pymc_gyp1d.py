#!/usr/bin/env python

"""
PyMC simulation using gyp1dl to invert for material properties.

In this example, the temperatures (K) are at the back surfaces of
exposed and unexposed boards in a standard two-wall ASTM E119 furnace
test. There are 16 material properties considered.
"""

import matplotlib
matplotlib.use("Agg")

import pymc as mc
import models

# Generate model
vars = models.gyp1d_temps()

# Fit model with MAP estimates
#map = mc.MAP(vars)
#map.fit(method='fmin_ncg', verbose=2)

# Import model variables and set database options
m = mc.MCMC(vars,
            db='sqlite',
            dbname='../Figures/example_gyp1d.sqlite')

# Use adaptive Metropolis-Hastings step method
#m.use_step_method(mc.AdaptiveMetropolis, [m.theta])

# Configure and run MCMC simulation
m.sample(iter=2500, burn=50, thin=5, verbose=2)
#m.sample(iter=100000, burn=50000, thin=10, verbose=2)

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m,
                format='pdf',
                path='../Figures/example_gyp1d',
                common_scale=False)

# Display results
m.theta.summary()
