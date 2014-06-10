#!/usr/bin/env python

"""
This script plots summary results from MCMC simulation

"""

from __future__ import division

import matplotlib.pyplot as plt
import numpy as np
import sqlite3
from pylab import *
from scipy import stats
import data_expt as de
import tga

plt.ion()

# get experimental data
T_0     = de.T[0] - 50.                 # initial simulation temperature, K
beta    = de.beta                       # heating rate, K/s
T_f     = de.T[-1]                      # final simulation temperature, K
w_f     = de.w[-1]                      # residual mass fraction

# numerical parameters
N_t     = 200                           # resolution of solution
T_sol   = np.linspace(T_0, T_f, N_t)    # solution temperatures, K

# Initialize connection to sqlite3 database file
conn = sqlite3.connect('../Figures/results.sqlite')

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
y_mean = y_mean[:,2]

# samples
params  = theta[:,2:]
N       = params.shape[0]               # number of samples
N_c     = int((params.shape[1] + 4)/3)
logA    = params[:,0:N_c-1]
E       = params[:,N_c-1:2*N_c-2]*1e-3  # kJ/mol
nu      = params[:,2*N_c-2:]

# sample extrema
logA_min = floor(logA.min(0))
logA_max = ceil(logA.max(0))
E_min = floor(E.min(0))
E_max = ceil(E.max(0))
nu_min = floor(nu.min(0))
nu_max = ceil(nu.max(0))

# sample grids
N_g = 200      # grid resolution
logA_g = np.zeros((N_g, N_c - 1))
E_g = np.zeros((N_g, N_c - 1))
for i in range(0, N_c - 1):
    logA_g[:,i] = np.linspace(logA_min[i], logA_max[i], N_g) 
    E_g[:,i] = np.linspace(E_min[i], E_max[i], N_g) 

nu_g = np.zeros((N_g, N_c - 2))
if N_c > 2:
    for i in range(0, N_c - 2):
        nu_g[:,i] = np.linspace(nu_min[i], nu_max[i], N_g)

# kernel density estimates

# ...univariate
f_logA = np.zeros((N_g, N_c - 1))
f_E = np.zeros((N_g, N_c - 1))
f_nu = np.zeros((N_g, N_c - 1))
for i in range(0, N_c - 1):
    kde = stats.gaussian_kde(logA[:,i])
    f_logA[:,i] = kde(logA_g[:,i])
    kde = stats.gaussian_kde(E[:,i])
    f_E[:,i] = kde(E_g[:,i])
for i in range(0, N_c - 2):
    kde = stats.gaussian_kde(nu[:,i])
    f_nu[:,i] = kde(nu_g[:,i])

# ...total kde
kde = stats.gaussian_kde(params.T)
f = kde(params.T)
f_mode = f.max()
params_mode = params.T[:,f.argmax()]
w_mode = tga.tga_solve( params_mode, beta, w_f, T_sol )

# plots
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('lines', linewidth=1.5)
plt.rc('xtick', labelsize=16)
plt.rc('ytick', labelsize=16)

j = 1   # initialize plot counter

# Univariate plots
for i in range(0, N_c-1):
    # pre-exponential
    plt.figure(j)
    plt.plot(logA[:,i], 'k-', rasterized=True)
    plt.xlabel(r'Iteration Number', fontsize=20)
    plt.ylabel(r'$\log (A_'+str(i+1)+',\  \mathrm{1/s})$', fontsize=20)
    plt.savefig('../Figures/logA'+str(i+1)+'_trace.pdf')
    j += 1

    plt.figure(j)
    plt.plot(logA_g[:,i], f_logA[:,i], 'k-')
    plt.xlabel(r'$\log (A_'+str(i+1)+',\  \mathrm{1/s})$', fontsize=20)
    plt.ylabel(r'$p ( \log A_'+str(i+1)+'|\mathbf{d})$', fontsize=20)
    plt.savefig('../Figures/logA'+str(i+1)+'_posterior.pdf')
    j += 1

    # activation energy
    plt.figure(j)
    plt.plot(E[:,i], 'k-', rasterized=True)
    plt.xlabel(r'Iteration Number', fontsize=20)
    plt.ylabel(r'$E_'+str(i+1)+'$, kJ/mol', fontsize=20)
    plt.savefig('../Figures/E'+str(i+1)+'_trace.pdf')
    j += 1
    
    plt.figure(j)
    plt.plot(E_g[:,i], f_E[:,i], 'k-')
    plt.xlabel(r'$E_'+str(i+1)+'$, kJ/mol', fontsize=20)
    plt.ylabel(r'$p ( E_'+str(i+1)+'|\mathbf{d})$', fontsize=20)
    plt.savefig('../Figures/E'+str(i+1)+'_posterior.pdf')
    j += 1

# stoichiometric coefficients
if N_c > 2:
    for i in range(0, N_c - 2):
        plt.figure(j)
        plt.plot(nu[:,i], 'k-', rasterized=True)
        plt.xlabel(r'Iteration Number', fontsize=20)
        plt.ylabel(r'$\nu_'+str(i+1)+'$', fontsize=20)
        plt.savefig('../Figures/nu'+str(i+1)+'_trace.pdf')
        j += 1
        
        plt.figure(j)
        plt.plot(nu_g[:,i], f_nu[:,i], 'k-')
        plt.xlabel(r'$\nu_'+str(i+1)+'$', fontsize=20)
        plt.ylabel(r'$p ( \nu_'+str(i+1)+'|\mathbf{d})$', fontsize=20)
        plt.savefig('../Figures/nu'+str(i+1)+'_posterior.pdf')
        j += 1
  
## ...cross rxns
#
#plt.figure(13)
#plt.plot(logA1, logA2, 'kx', rasterized=True, label='MCMC sample')
##plt.plot(logA1_mod, E1_mod, 'r-', label='fit')
#plt.xlabel(r'$\log \left(A_1,\  \mathrm{1/s} \right)$', fontsize=20)
#plt.ylabel(r'$\log \left(A_2,\  \mathrm{1/s} \right)$', fontsize=20)
##plt.legend(loc=2)
##plt.text(18, 127, r'$E  = 7.1\log A + 5.3$', fontsize=18, color='r')
#plt.savefig('logA2_vs_logA1.pdf')
#
#plt.figure(14)
#plt.plot(logA1, E2, 'kx', rasterized=True, label='MCMC sample')
##plt.plot(logA1_mod, E1_mod, 'r-', label='fit')
#plt.xlabel(r'$\log \left(A_1,\  \mathrm{1/s} \right)$', fontsize=20)
#plt.ylabel(r'$E_2$, kJ/mol', fontsize=20)
##plt.legend(loc=2)
##plt.text(18, 127, r'$E  = 7.1\log A + 5.3$', fontsize=18, color='r')
#plt.savefig('E2_vs_logA1.pdf')
#
#plt.figure(15)
#plt.plot(logA2, E1, 'kx', rasterized=True, label='MCMC sample')
##plt.plot(logA1_mod, E1_mod, 'r-', label='fit')
#plt.xlabel(r'$\log \left(A_2,\  \mathrm{1/s} \right)$', fontsize=20)
#plt.ylabel(r'$E_1$, kJ/mol', fontsize=20)
##plt.legend(loc=2)
##plt.text(18, 127, r'$E  = 7.1\log A + 5.3$', fontsize=18, color='r')
#plt.savefig('E1_vs_logA2.pdf')
#
#plt.figure(16)
#plt.plot(E1, E2, 'kx', rasterized=True, label='MCMC sample')
##plt.plot(logA1_mod, E1_mod, 'r-', label='fit')
#plt.xlabel(r'$E_1$, kJ/mol', fontsize=20)
#plt.ylabel(r'$E_2$, kJ/mol', fontsize=20)
##plt.legend(loc=2)
##plt.text(18, 127, r'$E  = 7.1\log A + 5.3$', fontsize=18, color='r')
#plt.savefig('E2_vs_E1.pdf')
#
#
## ...compute and plot sampled solutions
#plt.figure(17)
#for i in range(0, logA1.size):
#    w_sol = tga.tga_solve( [ logA1[i], E1[i]*1e3, logA2[i], E2[i]*1e3 ] )
#    plt.plot(tga.T_sol-273.15, w_sol, color='0.5')
#
#plt.plot(T-273.15, w, 'ko', label='Experiment')
#plt.axis([80, 240, 0.8, 1.0])
#plt.xlabel(r'$T,\ ^{\circ}$C', fontsize=20)
#plt.ylabel(r'$w$', fontsize=20)
#plt.legend(loc=1)
#plt.savefig('tga_mcmc.pdf')
#
plt.figure(j)
plt.plot(T_sol-273.15, w_mode, 'k', label='KDE mode' )
plt.plot(de.T-273.15, de.w, 'ko', label='Experiment')
plt.axis([80, 240, 0.8, 1.00])
plt.xlabel(r'$T,\ ^{\circ}$C', fontsize=20)
plt.ylabel(r'$w$', fontsize=20)
plt.legend(loc=1)
plt.savefig('../Figures/tga_mode.pdf')
