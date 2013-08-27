#!/usr/bin/env python

"""
PyMC Radiation Heat Flux Example Series
Example 3: PyMC simulation using different initial values.

In this example, we use the point source radiation model,
but we start from two different initial conditions to
see if they converge to the same posterior distribution.
"""

import matplotlib
matplotlib.use("Agg")

import pylab as pl
import pymc as mc
import models
import graphics

# Generate model and fit model
vars = models.point_source()
vars['theta'].value = [60]
m1 = mc.MCMC(vars)
m1.sample(iter=50000, burn=25000, thin=10)

# Generate model and fit model with different initial value
vars = models.point_source()
vars['theta'].value = [250]
m2 = mc.MCMC(vars)
m2.sample(iter=50000, burn=25000, thin=10)

# Plot traces and model with mean values
pl.figure(figsize=(12,9))
graphics.plot_hf_data()

graphics.plot_point_source_model(m1, color='g', label='Replicate 1')
pl.savefig('../Figures/example_heat_flux_3a.pdf')

graphics.plot_point_source_model(m2, color='b', label='Replicate 2')
pl.savefig('../Figures/example_heat_flux_3b.pdf')

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m1,
                format='pdf',
                path='../Figures/example_heat_flux_3',
                common_scale=False)
