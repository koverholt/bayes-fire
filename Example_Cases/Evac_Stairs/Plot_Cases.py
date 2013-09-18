#!/usr/bin/env python

from __future__ import division

import matplotlib
matplotlib.use("Agg")

import os
import sqlite3
import numpy as np
import scipy as sp
import scipy.integrate
from pylab import *

database_files = np.array([])

for r,d,f in os.walk('./'):
    for files in f:
        if files.endswith('.sqlite'):
            database_files = np.append(database_files, os.path.join(r,files))

for dbase in database_files:
    database_file_name = os.path.splitext(os.path.basename(dbase))[0]
    
    conn = sqlite3.connect(dbase)

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
    theta_all = np.array(cur.fetchall())
    cur.execute('select * from y_mean')
    y_mean = np.array(cur.fetchall())

    # Read in the third column of each data array as numpy arrays
    deviance = deviance[:,2]
    sigma = sigma[:,2]
    y_mean = y_mean[:,2]

    for i in range(1, np.shape(theta_all)[1]-2):

        theta = theta_all[:,i+1]

        # Generate plot
        fig = figure()
        n, bins, rectangles = hist(theta, 50, normed=True)
        xlabel('Value', fontsize=20)
        ylabel('Count', fontsize=20)
        grid(True)
        # xticks(fontsize=16)
        # yticks(fontsize=16)
        savefig('Figures/Summary/' + database_file_name + '_theta_' + str(i-1) + '.pdf')

        print database_file_name + '_theta_' + str(i-1)

        posterior_mean = np.mean(theta)

        print 'Posterior mean value: ' + str(posterior_mean)

        count = 0
        # Case 1: Sign of parameter is positive
        if posterior_mean > 0:
            for j in range(len(bins)):
                # If all bins are positive
                if (j == 0) and (bins[0] > 0):
                    P = 0
                    break
                # Find the bin that is positive
                if bins[j] > 0:
                    P = np.sum(n[:count] * np.diff(bins[:count+1]))
                    break
                # Count the bins that are negative
                else:
                    count += 1
                # If all bins are negative
                P = 1
        # Case 2: Sign of parameter is negative
        elif posterior_mean < 0:
            for j in reversed(xrange(len(bins))):
                # If all bins are negative
                if (j == 0) and (bins[0] < 0):
                    # print "No bins greater than zero"
                    P = 0
                    break
                # Find the bin that is negative
                if bins[j] < 0:
                    P = np.sum(n[:count] * np.diff(bins[:count+1]))
                    break
                # Count the bins that are positive
                else:
                    count += 1
                # If all bins are positive
                P = 1

        print 'Probability of opposite sign = ' + str(P)
        print
