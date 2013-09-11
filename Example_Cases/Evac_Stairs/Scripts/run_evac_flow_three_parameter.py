#!/usr/bin/env python

"""
PyMC Bayesian Inference on Evacuation Data
"""

import matplotlib
matplotlib.use("Agg")

import pylab as pl
import evac_flow_three_parameter_graphics as graphics
import pymc as mc
import evac_flow_three_parameter_models as models
import data_evac

#  ============
#  = Settings =
#  ============

mcmc_iterations = 100000
burn_iterations = 90000
thinning_parameter = 10

#  =========================
#  = Parameters and labels =
#  =========================

independent_parameters = ['occupants', 'exit_distance', 'type', 'riser',
                          'tread', 'evac_chair']
dependent_parameters = ['pre_evac_int', 'travel_int', 'exit_int']

independent_labels = {'occupants':'Number of Occupants (people)',
                    'exit_distance':'Exit Distance (m)',
                    'type':'Type (-)',
                    'riser':'Riser (m)',
                    'tread':'Tread (m)',
                    'evac_chair':'Evacuation Chair (-)'}
dependent_labels = {'pre_evac_int':'Pre-Evacuation Intensity',
                    'travel_int':'Travel Intensity',
                    'exit_int':'Exit Intensity'}

#  ===============================
#  = Run model on all parameters =
#  ===============================

for dep in dependent_parameters:
    for ind in independent_parameters:

        x = data_evac.data_three_parameter[ind]
        y = data_evac.data_three_parameter[dep]

        xlabel = independent_labels[ind]
        ylabel = dependent_labels[dep]

        #  ==================
        #  = Plot data only =
        #  ==================

        # Plot evac data
        pl.figure(figsize=(12,9))
        graphics.plot_all_data(x, y, xlabel, ylabel)
        pl.savefig('../Figures/Three_Parameter_Models/three_parameter_' + dep + '_vs_' + ind + '_data.pdf')

        #  ================
        #  = Linear model =
        #  ================

        # Generate model
        vars = models.linear(x, y)

        # Fit model with MAP estimates
        map = mc.MAP(vars)
        map.fit(method='fmin_powell', verbose=2)

        # Import model variables and set database options
        m = mc.MCMC(vars, db='sqlite', dbname='../Figures/Three_Parameter_Models/three_parameter_' + dep + '_vs_' + ind + '.sqlite')

        # # Use adaptive Metropolis-Hastings step method
        m.use_step_method(mc.AdaptiveMetropolis, [m.theta])

        # Configure and run MCMC simulation
        m.sample(iter=mcmc_iterations, burn=burn_iterations, thin=thinning_parameter)

        # Plot traces and model with mean values
        pl.figure(figsize=(12,9))
        graphics.plot_evac_data(x, y, xlabel, ylabel)
        graphics.plot_model(m, x, y, xlabel, ylabel)
        pl.savefig('../Figures/Three_Parameter_Models/three_parameter_' + dep + '_vs_' + ind + '_results.pdf')

        # Plot resulting distributions and convergence diagnostics
        mc.Matplot.plot(m, format='pdf', path='../Figures/Three_Parameter_Models/three_parameter_' + dep + '_vs_' + ind,
                        common_scale=False)

        m.write_csv('../Figures/Three_Parameter_Models/three_parameter_' + dep + '_vs_' + ind + '_stats.csv')
