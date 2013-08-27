#!/usr/bin/env python

"""
This script demonstrates how to read in data from a sqlite3
database file that is output from a PyMC simulation.
The resulting object is a numpy array.

"""

from __future__ import division

import matplotlib
matplotlib.use("Agg")

import numpy as np
import sqlite3
from pylab import *

# Initialize connection to sqlite3 database file
conn = sqlite3.connect('../Figures/example_heat_flux_2.sqlite')

# Create a cursor object to execute commands on
cur = conn.cursor()

# Use SQL select command to query all data from the table called 'deviance'
cur.execute('select * from deviance')

# Fetch all rows from the output of the select query
deviance = np.array(cur.fetchall())

# Repeat the above two steps for the remaining tables
cur.execute('select * from sigma')
sigma = np.array(cur.fetchall())
cur.execute('select * from theta')
theta = np.array(cur.fetchall())
cur.execute('select * from y_mean')
y_mean = np.array(cur.fetchall())

# Read in the third column of each data array as numpy arrays
deviance = deviance[:,2]
sigma = sigma[:,2]
theta = theta[:,2]
y_mean = y_mean[:,2]

# Generate plot
fig = figure()
ax = fig.add_subplot(111)
plot(theta, 'b-', lw=1.5)
xlabel('Iteration Number', fontsize=20)
ylabel('theta', fontsize=20)
grid(True)
xticks(fontsize=16)
yticks(fontsize=16)
savefig('theta.pdf')
