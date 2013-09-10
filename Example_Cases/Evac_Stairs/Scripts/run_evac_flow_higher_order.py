#!/usr/bin/env python

"""
PyMC Bayesian Inference on Evacuation Data
Stage 0: Plot evac data.
Stage 1: flow vs theta[0] * occupants^theta[1] * exit_distance^theta[2]
Stage 2: flow vs theta[0] * occupants^theta[1] * effective_width^theta[2]
Stage 3: flow vs theta[0] * occupants^theta[1] * exit_distance^theta[2] * effective_width^theta[3]
Stage 4: flow vs theta[0] * exit_distance^theta[1] * effective_width^theta[2]
"""

import matplotlib
matplotlib.use("Agg")

import pylab as pl
import evac_flow_higher_order_graphics as graphics
import pymc as mc
import evac_flow_higher_order_models as models
import data_evac

#  ============
#  = Settings =
#  ============

mcmc_iterations = 300000
burn_iterations = 250000
thinning_parameter = 10

case_name = 'higher_order'

#  ============================
#  = Stage 0 (plot exp. data) =
#  ============================

# Plot evac data
pl.figure(figsize=(12,9))
graphics.plot_all_data()
pl.savefig('../Figures/flow_' + case_name + '_evac_data.pdf')

#  ============================================================================
#  = Stage 1 (flow vs theta[0] * occupants^theta[1] * exit_distance^theta[2]) =
#  ============================================================================

# Generate model
vars1 = models.model1()

# Fit model with MAP estimates
map = mc.MAP(vars1)
map.fit(method='fmin_powell', verbose=2)

# Import model variables and set database options
m1 = mc.MCMC(vars1, db='sqlite', dbname='../Figures/flow_' + case_name + '_evac_model1.sqlite')

# Use adaptive Metropolis-Hastings step method
m1.use_step_method(mc.AdaptiveMetropolis, [m1.theta])

# Configure and run MCMC simulation
m1.sample(iter=mcmc_iterations, burn=burn_iterations, thin=thinning_parameter)

# Plot traces and model with mean values
# pl.figure(figsize=(12,9))
# graphics.plot_evac_data()
# graphics.plot_model1(m1)
# pl.savefig('../Figures/flow_' + case_name + '_evac_model1.pdf')

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m1, format='pdf', path='../Figures/flow_' + case_name + '_evac_model1',
                common_scale=False)

#  ==============================================================================
#  = Stage 2 (flow vs theta[0] * occupants^theta[1] * effective_width^theta[2]) =
#  ==============================================================================

# Generate model
vars2 = models.model2()

# Fit model with MAP estimates
map = mc.MAP(vars2)
map.fit(method='fmin_powell', verbose=2)

# Import model variables and set database options
m2 = mc.MCMC(vars2, db='sqlite', dbname='../Figures/flow_' + case_name + '_evac_model2.sqlite')

# Use adaptive Metropolis-Hastings step method
m2.use_step_method(mc.AdaptiveMetropolis, [m2.theta])

# Configure and run MCMC simulation
m2.sample(iter=mcmc_iterations, burn=burn_iterations, thin=thinning_parameter)

# Plot traces and model with mean values
# pl.figure(figsize=(12,9))
# graphics.plot_evac_data()
# graphics.plot_model2(m2)
# pl.savefig('../Figures/flow_' + case_name + '_evac_model2.pdf')

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m2, format='pdf', path='../Figures/flow_' + case_name + '_evac_model2',
                common_scale=False)

#  =======================================================================================================
#  = Stage 3 (flow vs theta[0] * occupants^theta[1] * exit_distance^theta[2] * effective_width^theta[3]) =
#  =======================================================================================================

# Generate model
vars3 = models.model3()

# Fit model with MAP estimates
map = mc.MAP(vars3)
map.fit(method='fmin_powell', verbose=2)

# Import model variables and set database options
m3 = mc.MCMC(vars3, db='sqlite', dbname='../Figures/flow_' + case_name + '_evac_model3.sqlite')

# Use adaptive Metropolis-Hastings step method
m3.use_step_method(mc.AdaptiveMetropolis, [m3.theta])

# Configure and run MCMC simulation
m3.sample(iter=mcmc_iterations, burn=burn_iterations, thin=thinning_parameter)

# Plot traces and model with mean values
# pl.figure(figsize=(12,9))
# graphics.plot_evac_data()
# graphics.plot_model3(m3)
# pl.savefig('../Figures/flow_' + case_name + '_evac_model3.pdf')

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m3, format='pdf', path='../Figures/flow_' + case_name + '_evac_model3',
                common_scale=False)

#  ==================================================================================
#  = Stage 4 (flow vs theta[0] * exit_distance^theta[1] * effective_width^theta[2]) =
#  ==================================================================================

# Generate model
vars4 = models.model4()

# Fit model with MAP estimates
map = mc.MAP(vars4)
map.fit(method='fmin_powell', verbose=2)

# Import model variables and set database options
m4 = mc.MCMC(vars4, db='sqlite', dbname='../Figures/flow_' + case_name + '_evac_model4.sqlite')

# Use adaptive Metropolis-Hastings step method
m4.use_step_method(mc.AdaptiveMetropolis, [m4.theta])

# Configure and run MCMC simulation
m4.sample(iter=mcmc_iterations, burn=burn_iterations, thin=thinning_parameter)

# Plot traces and model with mean values
# pl.figure(figsize=(12,9))
# graphics.plot_evac_data()
# graphics.plot_model4(m4)
# pl.savefig('../Figures/flow_' + case_name + '_evac_model4.pdf')

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m4, format='pdf', path='../Figures/flow_' + case_name + '_evac_model4',
                common_scale=False)

#  =================
#  = Print results =
#  =================

# Display results
print "Results for Model 1"
m1.theta.summary()
print "Results for Model 2"
m2.theta.summary()
print "Results for Model 3"
m3.theta.summary()
print "Results for Model 4"
m4.theta.summary()

# Find DIC
print 'DIC (Model 1) = %f' % m1.dic
print 'DIC (Model 2) = %f' % m2.dic
print 'DIC (Model 3) = %f' % m3.dic
print 'DIC (Model 4) = %f' % m4.dic
