#!/usr/bin/env python

"""Module for gyp1d functions"""

import numpy as np
import platform
import subprocess
import os
import data_expt as de

# Detect operating system
op_sys = platform.system()


def gen_input( k1, k2, k3, k4, rho_0, c_p1, c_p2, c_p3, eps, Y1_0,
             A1, A2, E1, E2, dh1, dh2 ):
    """Generate gyp1d input file from template.

    Keyword arguments:
    matl = [ k1, k2, k3, k4, rho_0, c_p1, c_p2, c_p3, eps, Y1_0,
             A1, A2, E1, E2, dh1, dh2 ]
    """

    template = """
&matl 
    k_temps = 273.15, 448.15, 1088.15, 1473.15
    k_vals = %(k1)s, %(k2)s, %(k3)s, %(k4)s
    rho_0 = %(rho_0)s
    c_p = %(c_p1)s, %(c_p2)s, %(c_p3)s
    eps = %(eps)s 
    Y1_0 = %(Y1_0)s
    A = %(A1)s, %(A2)s
    E = %(E1)s, %(E2)s
    dh = %(dh1)s, %(dh2)s /

&scen
    L = 0.0159
    L_a = 0.092
    t_end = 3601
    H = 3.048 /

&numr
    N = 30
    N_t = 160000
    N_sol = 100 /
"""

    #  ==================================================
    #  = Generate gyp1d input file                      =
    #  ==================================================

    outcase = template % {'k1':str(k1),
                          'k2':str(k2),
                          'k3':str(k3),
                          'k4':str(k4),
                          'rho_0':str(rho_0),
                          'c_p1':str(c_p1),
                          'c_p2':str(c_p2),
                          'c_p3':str(c_p3),
                          'eps':str(eps),
                          'Y1_0':str(Y1_0),
                          'A1':str(A1),
                          'A2':str(A2),
                          'E1':str(E1),
                          'E2':str(E2),
                          'dh1':str(dh1),
                          'dh2':str(dh2)}

    #  =====================
    #  = Write gyp1d files =
    #  =====================

    casename = 'case'
    filename = '../' + casename + '.inp'

    # Opens a new file, writes the gyp1d input file, and closes the file
    f = open(filename, 'w')
    f.write(outcase)
    f.close()

    return casename


def run_gyp1d(casename):
    """Run gyp1d on case file."""
    os.chdir('../')

    p = subprocess.Popen(['./gyp1d_osx_64', casename + '.inp'])
    p.wait()

    os.chdir('./Scripts')
#    os.chdir('../Example_Cases/FDS_Mass_Loss_Rate/Scripts')


def read_gyp1d(casename):
    """Read in gyp1d output."""
    temp_file = '../temp_nom.out'
    temps = np.genfromtxt(temp_file)
    #mlrs = np.genfromtxt(mlr_file, delimiter=',', skip_header=2)
    time = temps[:,0]
    T_1b = temps[:,1]
    T_2b = temps[:,2]

    # interpolate to experimental times
    time_expt = de.time
    T_1b_interp = np.interp(time_expt, time, T_1b)
    os.remove('../temp_nom.out')

    return T_1b_interp
