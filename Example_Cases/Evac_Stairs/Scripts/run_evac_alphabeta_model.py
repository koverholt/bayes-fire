#!/usr/bin/env python

"""
PyMC Bayesian Inference on Evacuation Data
Model 1: preevac_mu vs theta[0] + theta[1]*occupants + theta[2]*type
Model 2: exit_mu vs theta[0] + theta[1]*occupants + theta[2]*exit_distance + theta[3]*type
Model 3: traveltime_mu vs theta[0] + theta[1]*exit_distance + theta[2]*type
"""

import matplotlib
matplotlib.use("Agg")

import pylab as pl
import evac_flow_exit_mu_single_graphics as graphics
import pymc as mc
import evac_alphabeta_paper_model as models
import data_evac

#  ============
#  = Settings =
#  ============

mcmc_iterations = 1000000
burn_iterations = 800000
thinning_parameter = 200

case_name = 'final_models'
dir_name = '../Figures/Mu_Paper_Models/'
project_name = 'alpha_model_'

#  ===========================================================================================
#  = Model 1 beta vs alpha                                                                   =
#  ===========================================================================================

# Generate model
model1_name = '_alphabeta_1'
vars1 = models.model1()

# Fit model with MAP estimates
map = mc.MAP(vars1)
map.fit(method='fmin_powell', verbose=2)

# Import model variables and set database options
m1 = mc.MCMC(vars1, db='sqlite', dbname=dir_name + project_name + case_name + model1_name + '.sqlite')

# Use adaptive Metropolis-Hastings step method
m1.use_step_method(mc.AdaptiveMetropolis, [m1.theta])

# Configure and run MCMC simulation
m1.sample(iter=mcmc_iterations, burn=burn_iterations, thin=thinning_parameter)

# Plot traces and model with mean values
# pl.figure(figsize=(12,9))
# graphics.plot_evac_data()
# graphics.plot_model1(m1)
# pl.savefig('../Figures/Higher_Order_Models/flow_' + case_name + '_evac_model1.pdf')

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m1, format='pdf', path=dir_name + project_name + case_name + model1_name,
                common_scale=False)


#  ===========================================================================================
#  = Model 2 beta vs alpha                                                                   =
#  ===========================================================================================

# Generate model
model2_name = '_alphabeta_2'
vars2 = models.model2()

# Fit model with MAP estimates
map = mc.MAP(vars2)
map.fit(method='fmin_powell', verbose=2)

# Import model variables and set database options
m2 = mc.MCMC(vars2, db='sqlite', dbname=dir_name + project_name + case_name + model2_name + '.sqlite')

# Use adaptive Metropolis-Hastings step method
m2.use_step_method(mc.AdaptiveMetropolis, [m2.theta])

# Configure and run MCMC simulation
m2.sample(iter=mcmc_iterations, burn=burn_iterations, thin=thinning_parameter)

# Plot traces and model with mean values
# pl.figure(figsize=(12,9))
# graphics.plot_evac_data()
# graphics.plot_model1(m1)
# pl.savefig('../Figures/Higher_Order_Models/flow_' + case_name + '_evac_model1.pdf')

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m2, format='pdf', path=dir_name + project_name + case_name + model2_name,
                common_scale=False)

#  ===========================================================================================
#  = Model 3 beta vs alpha                                                                   =
#  ===========================================================================================

# Generate model
model3_name = '_alphabeta_3'
vars3 = models.model3()

# Fit model with MAP estimates
map = mc.MAP(vars3)
map.fit(method='fmin_powell', verbose=2)

# Import model variables and set database options
m3 = mc.MCMC(vars3, db='sqlite', dbname=dir_name + project_name + case_name + model3_name + '.sqlite')

# Use adaptive Metropolis-Hastings step method
m3.use_step_method(mc.AdaptiveMetropolis, [m3.theta])

# Configure and run MCMC simulation
m3.sample(iter=mcmc_iterations, burn=burn_iterations, thin=thinning_parameter)

# Plot traces and model with mean values
# pl.figure(figsize=(12,9))
# graphics.plot_evac_data()
# graphics.plot_model1(m1)
# pl.savefig('../Figures/Higher_Order_Models/flow_' + case_name + '_evac_model1.pdf')

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m3, format='pdf', path=dir_name + project_name + case_name + model3_name,
                common_scale=False)


#  ===========================================================================================
#  = Model 4 beta vs alpha                                                                   =
#  ===========================================================================================

# Generate model
model4_name = '_alphabeta_4'
vars4 = models.model4()

# Fit model with MAP estimates
map = mc.MAP(vars4)
map.fit(method='fmin_powell', verbose=2)

# Import model variables and set database options
m4 = mc.MCMC(vars4, db='sqlite', dbname=dir_name + project_name + case_name + model4_name + '.sqlite')

# Use adaptive Metropolis-Hastings step method
m4.use_step_method(mc.AdaptiveMetropolis, [m4.theta])

# Configure and run MCMC simulation
m4.sample(iter=mcmc_iterations, burn=burn_iterations, thin=thinning_parameter)

# Plot traces and model with mean values
# pl.figure(figsize=(12,9))
# graphics.plot_evac_data()
# graphics.plot_model1(m1)
# pl.savefig('../Figures/Higher_Order_Models/flow_' + case_name + '_evac_model1.pdf')

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m4, format='pdf', path=dir_name + project_name + case_name + model4_name,
                common_scale=False)



#  =================
#  = Print results =
#  =================

# Display results
print "Results for Model 1 " + model1_name
m1.theta.summary()
print "Results for Model 2 " + model2_name
m2.theta.summary()
print "Results for Model 3 " + model3_name
m3.theta.summary()
print "Results for Model 4 " + model4_name
m4.theta.summary()

# Write results to file
m1.write_csv(dir_name + project_name + case_name + model1_name + '.csv')
m2.write_csv(dir_name + project_name + case_name + model2_name + '.csv')
m3.write_csv(dir_name + project_name + case_name + model3_name + '.csv')
m4.write_csv(dir_name + project_name + case_name + model4_name + '.csv')

# Find DIC
print 'DIC (Model 1) = %f' % m1.dic
print 'DIC (Model 2) = %f' % m2.dic
print 'DIC (Model 3) = %f' % m3.dic
print 'DIC (Model 4) = %f' % m4.dic