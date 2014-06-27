#!/usr/bin/env python

"""
PyMC simulation using TGA data to infer kinetic parameters for serial reaction
network
"""

import matplotlib
matplotlib.use("Agg")
import pymc as mc
import models

# Generate model
vars = models.tga_w()

## Fit model with MAP estimates
#map = mc.MAP(vars)
#map.fit(method='fmin_ncg', verbose=2)

# Import model variables and set database options
m = mc.MCMC(vars,
            db='sqlite',
            dbname='../Figures/results.sqlite')

# Use adaptive Metropolis-Hastings step method
m.use_step_method(mc.AdaptiveMetropolis, [m.theta])

# Configure and run MCMC simulation
m.sample(iter=1000000, burn=500000, thin=500, verbose=2)
#m.sample(iter=1000000, burn=500000, thin=200, verbose=2)

# Plot resulting distributions and convergence diagnostics
mc.Matplot.plot(m,
                format='pdf',
                path='../Figures/example_tga',
                common_scale=False)

# Display results
m.theta.summary()

# Plot summary results

