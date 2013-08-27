#!/usr/bin/env python

"""Module for setting up plotting routines"""

import time
from math import pi
import pylab as pl
import numpy as np
import data_fds


def plot_fds_mlr(mlr):
    """
    Plot each FDS realization individually (with a timestamp).

    Generate plots throughout the simulation using the FDS model.

    WARNING: This produces a large number of output figures.
    """
    pl.figure(figsize=(9,6))
    pl.plot(data_fds.time, data_fds.mlr,
            'k-', ms=10, label='Exp (MLR)', lw=2)
    pl.plot(data_fds.time, mlr,
            'k--', ms=10, label='FDS (MLR)', lw=2)
    pl.xlabel('Time (s)', fontsize=20)
    pl.ylabel('Mass Loss Rate (kg/m$^2$/s)', fontsize=20)
    pl.legend(loc='upper left')
    pl.ylim([0, 0.05])
    pl.xticks(fontsize=16)
    pl.yticks(fontsize=16)
    pl.grid(True)
    pl.savefig('../Figures/FDS_MLR_Figures/FDS_MLR_' +
               time.strftime('%Y%m%d_%H%M%S') +
               '.pdf')
    pl.close()
