#!/usr/bin/env python

"""
PyMC Radiation Heat Flux Example Series
Example 5: PyMC simulation using maximum a posteriori estimate.

In this example, we use the point source radiation model
along with the maximum a posteriori (MAP) method to start
with better initial values. Also, information is calculated
for the AIC, BIC, and DIC criteria.
"""

import matplotlib
matplotlib.use("Agg")

import pylab as pl
import pymc as mc
import data_heat_flux
import models
import graphics

# Generate model
vars = models.point_source()

# Fit with MAP, find AIC and BIC
map = mc.MAP(vars)
map.fit(method='fmin_powell', verbose=1)
print 'AIC=%f' % map.AIC
print 'BIC=%f' % map.BIC

# Add a data posterior prediction deterministic
@mc.deterministic
def y_pred(mu=vars['y_mean'], sigma=vars['sigma']):
    return mc.rnormal(mu, sigma**-2)

vars['y_pred'] = y_pred

# Fit with MCMC, but not with default step methods
m = mc.MCMC(vars)

# Use adaptive Metropolis-Hastings step method
m.use_step_method(mc.AdaptiveMetropolis, [m.theta])

# Configure and run MCMC simulation
m.sample(50000, 25000, 10)

# Find DIC
print 'DIC = %f' % m.dic

# Plot residuals
pl.figure(figsize=(12,9))
y_err = m.y_obs.value - m.y_mean.stats()['mean']
pl.hlines([0], 0, 2.5, linewidth=3, linestyle='dashed')
pl.plot(data_heat_flux.distance, y_err, 'gs', mew=0, ms=10)
graphics.decorate_plot()
pl.ylabel("Residual ($\dot q''_{obs} - \dot q''_{expected}$)", fontsize=24)
pl.axis([0, 2.5, -3, 3])
pl.savefig('../Figures/example_heat_flux_5a.pdf')

# Generate a posterior predictive check
pl.figure(figsize=(12,9))
graphics.plot_predicted_data(y_pred)
pl.savefig('../Figures/example_heat_flux_5b.pdf')
