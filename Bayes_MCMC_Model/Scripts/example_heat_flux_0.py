#!/usr/bin/env python

"""
PyMC Radiation Heat Flux Example Series
Example 0: Plot heat flux vs. distance data.

This example only plots the experimental data
that we will be conditioning to in later examples.
"""

import matplotlib
matplotlib.use("Agg")

import pylab as pl
import graphics

# Plot heat flux data
pl.figure(figsize=(12,9))
graphics.plot_all_data()
pl.savefig('../Figures/example_heat_flux_0.pdf')
