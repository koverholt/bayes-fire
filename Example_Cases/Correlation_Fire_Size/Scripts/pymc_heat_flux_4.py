#!/usr/bin/env python

"""
PyMC Radiation Heat Flux Example Series
Example 4: PyMC simulation using a different step method.

In this example, we use the point source radiation model,
but we use the adaptive Metropolis-Hastings step method
instead of the standard Metropolis-Hastings method.
"""

import matplotlib
matplotlib.use("Agg")

import pylab as pl
import pymc as mc
import models
import graphics

# Generate model
vars = models.point_source()

# Fit with MCMC, but not with default step methods
m = mc.MCMC(vars)

# Use adaptive Metropolis-Hastings step method
m.use_step_method(mc.AdaptiveMetropolis, [m.theta])

# Configure and run MCMC simulation
m.sample(50000, 25000, 10)

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m,
                format='pdf',
                path='../Figures/example_heat_flux_4',
                common_scale=False)

# Look at joint posterior distribution of theta_0
# and theta_1 as well as theta_2 and gamma
pl.figure(figsize=(12,9))
graphics.plot_joint_density(m.theta.trace()[:,0], m.sigma.trace())
pl.xticks(fontsize=20)
pl.yticks(fontsize=20)
pl.xlabel('HRR, $\\theta$ (kW)', fontsize=24)
pl.ylabel('Sigma, $\\sigma_L$ (kW)', fontsize=24)
pl.savefig('../Figures/example_heat_flux_4.pdf')
