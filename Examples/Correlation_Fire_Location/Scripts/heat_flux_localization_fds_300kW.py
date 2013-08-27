#!/usr/bin/env python

import matplotlib
matplotlib.use("Agg")

import pylab as pl
import pymc as mc

import models
import graphics
import data_fds_300kW

# Generate model
vars = models.point_source_radiation_fds(300, data_fds_300kW)

# Fit model with MAP estimates
map = mc.MAP(vars)
map.fit(method='fmin_powell', verbose=2)

# Import model variables and set database options
m = mc.MCMC(
        vars,
        db='sqlite',
        dbname='../Figures/heat_flux_localization_fds_300kW.sqlite')

# Configure and run MCMC simulation
m.sample(iter=50000, burn=25000, thin=10)

# Uncomment the line below to plot all MCMC steps
# graphics.show_mcmc_steps(m)

# Plot results
pl.figure()
graphics.plot_ps_radiation_model(m)
pl.savefig('../Figures/heat_flux_localization_fds_300kW.pdf')

# Plot results in a 3D grid
pl.figure()
graphics.plot_3d_hist(m)
pl.savefig('../Figures/heat_flux_localization_fds_300kW_3d.pdf')

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m,
                format='pdf',
                path='../Figures/heat_flux_localization_fds_300kW')

m.summary()
