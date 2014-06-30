#!/usr/bin/env python

"""
Read in normalized experimental data: [ T (K), w ]
"""

import numpy as np

def read_data( matl, beta ):
    
    # Read in experimental data from file
    data = np.genfromtxt('../Experimental_Data/'+ matl + '_' + beta + 'Cpm.csv', delimiter=',', skiprows=1)

    #T = data[:,0]       # temperature, K
    #w = data[:,1]       # normalized total mass

    return data
