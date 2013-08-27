#!/usr/bin/env python

"""
This script plots the measured and predicted mass loss rates for
the PMMA case: exp. data, posterior mean, posterior low, and posterior high.
"""

from __future__ import division

import matplotlib
matplotlib.use("Agg")

import numpy as np
from pylab import *
import sqlite3

# Initialize connection to sqlite3 database file
conn = sqlite3.connect(
    '../PyMC_Output_Files/FDS_Adaptive_100000_Runs/example_fds.sqlite')

# Create a cursor object to execute commands on
cur = conn.cursor()

# Use SQL select command to query all data from the table called 'y_mean'
cur.execute('select * from y_mean')
y_mean = np.array(cur.fetchall())

#  ============
#  = Plotting =
#  ============

data_exp = np.genfromtxt(
            '../Experimental_Data/PMMA.csv',
            delimiter=',', names=True)

data_FDS = np.genfromtxt(
            '../FDS_Output_Files/FAA_Polymers_PMMA_FDS_devc.csv',
            delimiter=',', names=True, skip_header=1)

data_bayes_mean = np.genfromtxt(
            '../FDS_Output_Files/FAA_Polymers_PMMA_Bayes_Mean_devc.csv',
            delimiter=',', names=True, skip_header=1)

bayes_results = np.genfromtxt(
            '../PyMC_Output_Files/Chain_0/y_mean.csv', delimiter=',')

#  ==========
#  = Figure =
#  ==========

figure(figsize=(9,6))

plot(data_exp['Time'], data_exp['MLR'],
     'k-', lw=2, label='Exp')

xlabel('Time (s)', fontsize=20)
ylabel('Mass Loss Rate (kg/m$^2 \cdot \,$s)', fontsize=20)
xlim([0, 600])
# legend(loc=0)
grid(True)
xticks(fontsize=16)
yticks(fontsize=16)
savefig('../Figures/Mass_Loss_Rate_Exp.pdf')

#  ==========
#  = Figure =
#  ==========

figure(figsize=(9,6))

for i in np.arange(0, len(y_mean), 10):
    plot(np.arange(0,520,5), y_mean[i,2:],
         ls='-', lw=2, alpha=0.1, color=(0.9,0.9,0))

plot(data_exp['Time'], data_exp['MLR'],
     'k-', lw=2, label='Exp')

plot(data_FDS['Time'], data_FDS['MLR'],
     'k--', lw=2, label='FDS, Lit. Values')

plot(data_bayes_mean['Time'], data_bayes_mean['MLR'],
     ls='-', marker='s', ms=6, markevery=10, color='b', lw=2,
     label='FDS, Posterior Mean Values')

xlabel('Time (s)', fontsize=20)
ylabel('Mass Loss Rate (kg/m$^2 \cdot \,$s)', fontsize=20)
xlim([0, 600])
legend(loc=0)
grid(True)
xticks(fontsize=16)
yticks(fontsize=16)
savefig('../Figures/Mass_Loss_Rates.pdf')
