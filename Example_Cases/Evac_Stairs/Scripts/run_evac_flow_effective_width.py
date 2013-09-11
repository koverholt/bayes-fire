#!/usr/bin/env python

"""
PyMC Bayesian Inference on Evacuation Data
Stage 0: Plot evac data.
Stage 1: Fit evac data with linear model.
Stage 2: Fit evac data with power law model.
"""

import matplotlib
matplotlib.use("Agg")

import pylab as pl
import evac_flow_effective_width_graphics as graphics
import pymc as mc
import evac_flow_effective_width_models as models
import data_evac

#  ============
#  = Settings =
#  ============

mcmc_iterations = 300000
burn_iterations = 250000
thinning_parameter = 10

case_name = 'effective_width'

independent_var = data_evac.effective_width

#  ============================
#  = Stage 0 (plot exp. data) =
#  ============================

# Plot evac data
pl.figure(figsize=(12,9))
graphics.plot_all_data()
pl.savefig('../Figures/flow_' + case_name + '_evac_data.pdf')

#  ==========================
#  = Stage 1 (linear model) =
#  ==========================

# Generate model
vars1 = models.linear()

# Fit model with MAP estimates
map = mc.MAP(vars1)
map.fit(method='fmin_powell', verbose=2)

### Initilaize posterior predictive check ###
# Add a data posterior prediction deterministic
@mc.deterministic
def y_pred1(mu=vars1['y_mean'], sigma=vars1['sigma']):
    return mc.rnormal(mu, sigma**-2)

vars1['y_pred1'] = y_pred1
### End initialize posterior predictive check ###

# Import model variables and set database options
m1 = mc.MCMC(vars1, db='sqlite', dbname='../Figures/flow_' + case_name + '_evac_linear.sqlite')

# Use adaptive Metropolis-Hastings step method
m1.use_step_method(mc.AdaptiveMetropolis, [m1.theta])

# Configure and run MCMC simulation
m1.sample(iter=mcmc_iterations, burn=burn_iterations, thin=thinning_parameter)

# Plot traces and model with mean values
pl.figure(figsize=(12,9))
graphics.plot_evac_data()
graphics.plot_linear_model(m1)
pl.savefig('../Figures/flow_' + case_name + '_evac_linear.pdf')

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m1, format='pdf', path='../Figures/flow_' + case_name + '_evac_linear',
                common_scale=False)

### Posterior predictive check ###
# Plot residuals
pl.figure(figsize=(12,9))
y_err1 = m1.y_obs.value - m1.y_mean.stats()['mean']
pl.hlines([0], 0.6, 1.3, linewidth=3, linestyle='dashed')
pl.plot(independent_var, y_err1, 'gs', mew=0, ms=10)
graphics.decorate_plot()
pl.ylabel("Residual (observed - expected)", fontsize=24)
pl.axis([0.6, 1.3, -3, 3])
pl.savefig('../Figures/PPC/flow_' + case_name + '_evac_linear_residuals.pdf')

# Generate a posterior predictive check
pl.figure(figsize=(12,9))
graphics.plot_predicted_data(y_pred1)
pl.savefig('../Figures/PPC/flow_' + case_name + '_evac_linear_ppc.pdf')
### End posterior predictive check ###

#  =============================
#  = Stage 2 (power law model) =
#  =============================

# Generate model
vars2 = models.power_law()

# Fit model with MAP estimates
map = mc.MAP(vars2)
map.fit(method='fmin_powell', verbose=2)

### Initilaize posterior predictive check ###
# Add a data posterior prediction deterministic
@mc.deterministic
def y_pred2(mu=vars2['y_mean'], sigma=vars2['sigma']):
    return mc.rnormal(mu, sigma**-2)

vars2['y_pred2'] = y_pred2
### End initialize posterior predictive check ###

# Import model variables and set database options
m2 = mc.MCMC(vars2, db='sqlite', dbname='../Figures/flow_' + case_name + '_evac_power_law.sqlite')

# Use adaptive Metropolis-Hastings step method
m2.use_step_method(mc.AdaptiveMetropolis, [m2.theta])

# Configure and run MCMC simulation
m2.sample(iter=mcmc_iterations, burn=burn_iterations, thin=thinning_parameter)

# Plot traces and model with mean values
pl.figure(figsize=(12,9))
graphics.plot_evac_data()
graphics.plot_power_law_model(m2)
pl.savefig('../Figures/flow_' + case_name + '_evac_power_law.pdf')

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m2, format='pdf', path='../Figures/flow_' + case_name + '_evac_power_law',
                common_scale=False)

### Posterior predictive check ###
# Plot residuals
pl.figure(figsize=(12,9))
y_err2 = m2.y_obs.value - m2.y_mean.stats()['mean']
pl.hlines([0], 0.6, 1.3, linewidth=3, linestyle='dashed')
pl.plot(independent_var, y_err2, 'gs', mew=0, ms=10)
graphics.decorate_plot()
pl.ylabel("Residual (observed - expected)", fontsize=24)
pl.axis([0.6, 1.3, -3, 3])
pl.savefig('../Figures/PPC/flow_' + case_name + '_evac_power_law_residuals.pdf')

# Generate a posterior predictive check
pl.figure(figsize=(12,9))
graphics.plot_predicted_data(y_pred2)
pl.savefig('../Figures/PPC/flow_' + case_name + '_evac_power_law_ppc.pdf')
### End posterior predictive check ###

#  =================
#  = Print results =
#  =================

# Display results
print "Results for Linear Model"
m1.theta.summary()
print "Results for Power Law Model"
m2.theta.summary()

# Write results to file
m1.write_csv('../Figures/flow_' + case_name + '_evac_linear.csv')
m2.write_csv('../Figures/flow_' + case_name + '_evac_power_law.csv')

# Find DIC
print 'DIC (Linear Model) = %f' % m1.dic
print 'DIC (Power Law Model) = %f' % m2.dic
