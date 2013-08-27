#!/usr/bin/env python

"""
PyMC Radiation Heat Flux Example Series
Example 1: PyMC simulation to fit a line to heat flux data.

In this example, we fit a line of the form
\dot Q = theta_0 * R + theta_1 to the measured heat flux data.
"""

import matplotlib
matplotlib.use("Agg")

import pylab as pl
import pymc as mc
import models
import graphics

# Generate model
vars = models.linear()

# Import model variables and set database options
m = mc.MCMC(vars,
            db='sqlite',
            dbname='../Figures/example_heat_flux_1.sqlite')

# Configure and run MCMC simulation
m.sample(iter=50000, burn=25000, thin=10)

# Plot traces and model with mean values
pl.figure(figsize=(12,9))
graphics.plot_hf_data()
graphics.plot_linear_model(m)
pl.savefig('../Figures/example_heat_flux_1.pdf')

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m,
                format='pdf',
                path='../Figures/example_heat_flux_1',
                common_scale=False)

# Find DIC
print 'DIC = %f' % m.dic

# Display results
m.theta.summary()
