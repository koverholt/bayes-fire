#!/usr/bin/env python

"""
PyMC Radiation Heat Flux Example Series
Example 6: PyMC simulation with database output.

In this example, we use the point source radiation model
along with database output.
"""

import pymc as mc
import models

# Fit with MCMC, save results in a database db can be one of the
# following: no_trace, ram, pickle, txt, sqlite, mysql, hdf5

# Generate model
vars = models.point_source()
m = mc.MCMC(vars,
               db='sqlite',
               dbname='../Figures/point_source_heat_flux.sqlite')

m.use_step_method(mc.AdaptiveMetropolis, [m.theta])
m.sample(50000, 25000, 10)

# Load the database from disk
db = mc.database.sqlite.load(
        '../Figures/point_source_heat_flux.sqlite')
print db.theta.stats()

# Do it again with txt to compare size of output

vars = models.point_source()
m = mc.MCMC(vars,
               db='txt',
               dbname='../Figures/point_source_heat_flux.txt')

m.use_step_method(mc.AdaptiveMetropolis, [m.theta])
m.sample(50000, 25000, 10)

# Load the database from disk
db = mc.database.txt.load(
        '../Figures/point_source_heat_flux.txt')

# Display results
print db.theta.stats()
