#!/usr/bin/env python

"""Module for setting up plotting routines"""

import time
from math import pi
import pylab as pl
import numpy as np
import data_cfast_transient


def plot_cfast_transient_temp(hgl):
    """
    Plot each CFAST realization individually (in overwrite mode).

    Generate plots throughout the simulation using
    the CFAST zone model.
    """
    pl.figure()
    pl.plot(data_cfast_transient.time,
            data_cfast_transient.temperature,
            'r-', lw=2, label='Target Temperature ($^\circ$C)')

    pl.plot(data_cfast_transient.time, hgl,
            'b--', lw=2, label='Predicted Temperature ($^\circ$C)')

    pl.xlabel('Time (s)', fontsize=20)
    pl.ylabel('Temperature ($^\circ$C)', fontsize=20)
    pl.xticks(fontsize=16)
    pl.yticks(fontsize=16)
    pl.grid(True)
    pl.legend(loc='upper left')
    pl.savefig('../Figures/example_cfast_transient_temp.pdf')
    pl.close()


def plot_cfast_transient_hrr(m):
    """
    Plot each CFAST realization throughout the simulation.

    Generate plot of the CFAST zone model realizations
    on a single plot.
    """
    pl.plot([0, 100, 100, 200, 200, 400, 400, 600],
            [0,   0, 100, 100, 200, 200, 300, 300],
            'r-', zorder=-1, lw=2,
            label='Input HRR')

    ramp_t = np.linspace(1, 600, 61)

    for hrr_set in m.theta.trace():
        pl.plot(ramp_t, hrr_set,
                color='gray', alpha=.75, zorder=-1)

    pl.plot(ramp_t, m.theta.stats()['mean'],
            'b--', lw=2, zorder=-1, label='Inverse HRR')

    pl.xlabel('Time (s)', fontsize=20)
    pl.ylabel('HRR (kW)', fontsize=20)
    pl.ylim([0, 350])
    pl.xticks(fontsize=16)
    pl.yticks(fontsize=16)
    pl.grid(True)
    pl.legend(loc='upper left')
    pl.savefig('../Figures/example_cfast_transient_hrr.pdf')
    pl.close()
