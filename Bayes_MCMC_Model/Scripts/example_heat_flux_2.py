#!/usr/bin/env python

"""
PyMC Radiation Heat Flux Example Series
Example 2: PyMC simulation using a point source radiation model.
"""

import matplotlib
matplotlib.use("Agg")

import pylab as pl
import pymc as mc
import models
import graphics

# Generate model
vars = models.point_source()

# Fit model with MAP estimates
map = mc.MAP(vars)
map.fit(method='fmin_powell', verbose=2)

# Import model variables and set database options
m = mc.MCMC(vars, db='sqlite',
            dbname='../Figures/example_heat_flux_2.sqlite')

# Configure and run MCMC simulation
m.sample(iter=50000, burn=25000, thin=10)

# Plot traces and model with mean values
pl.figure(figsize=(12,9))
graphics.plot_hf_data()
graphics.plot_point_source_model(m)
pl.savefig('../Figures/example_heat_flux_2.pdf')

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m,
                format='pdf',
                path='../Figures/example_heat_flux_2',
                common_scale=False)

# Find DIC
print 'DIC = %f' % m.dic

# Display results
m.theta.summary()
