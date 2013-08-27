#!/usr/bin/env python

"""Module for setting up plotting routines"""

import time
from math import pi
import pylab as pl
import numpy as np
import data_heat_flux
import data_cfast_transient
import data_fds


def plot_all_data():
    """Plot the measured heat flux data and decorates the output."""
    plot_hf_data()
    decorate_plot()


def plot_hf_data():
    """Plot the measured heat flux data."""
    pl.plot(data_heat_flux.distance,
            data_heat_flux.heat_flux,
            'bs', ms=10, mew=0, label='Exp. Data')


def plot_linear_model(m):
    """
    Plot each linear realization for the radiation example.

    Generate a plot for each realization throughout the
    simulation using the linear model.
    """
    R = pl.arange(0., 2.5, .01)
    for theta_t in m.theta.trace():
        heat_flux = theta_t[0]*R + theta_t[1]
        pl.plot(R, heat_flux,
                color='gray', alpha=.75, zorder=-1)

    theta = m.theta.stats()['mean']
    heat_flux = theta[0]*R + theta[1]
    pl.plot(R, heat_flux,
            color='purple', linewidth=5,
            label='Linear')
    decorate_plot()


def plot_point_source_model(m,
                            color='green',
                            label='Point Source Radiation'):
    """
    Plot each point source realization for the radiation example.

    Generate a plot for each realization throughout the
    simulation using the point source radiation model on
    a single plot.
    """
    R = pl.arange(0.01, 2.5, .01)
    y_trace = []
    for theta in m.theta.trace():
        y = 0.30 * theta / (4 * pi * (R)**2)
        pl.plot(R, y,
                color='gray', alpha=.75, zorder=-1)
        y_trace.append(y)

    pl.plot(R, pl.mean(y_trace, axis=0),
            color=color, linewidth=5,
            label=label)
    decorate_plot()


def decorate_plot():
    """Decorate the plot with labels."""
    pl.axis([0, 2.5, 0., 10.])
    pl.legend(numpoints=1, prop=dict(size=20), fancybox=True)
    pl.xticks(fontsize=20)
    pl.xlabel('Distance (m)', fontsize=24)
    pl.yticks(fontsize=20)
    pl.ylabel('Heat Flux (kW/m$^2$)', fontsize=24)


def plot_joint_density(X, Y, bounds=None):
    """
    Plot joint density of X and Y.

    Used in example 4 to explore model convergence.
    """
    if bounds:
        X_min, X_max, Y_min, Y_max = bounds
    else:
        X_min = X.min()
        X_max = X.max()
        Y_min = Y.min()
        Y_max = Y.max()

    pl.plot(X, Y,
            linestyle='none', marker='o',
            color='green', mec='green',
            alpha=.75, zorder=-99)

    import scipy.stats
    gkde = scipy.stats.gaussian_kde([X, Y])
    x, y = pl.mgrid[X_min:X_max:(X_max-X_min)/25.,
                    Y_min:Y_max:(Y_max-Y_min)/25.]
    z = pl.array(gkde.evaluate([x.flatten(), y.flatten()])).reshape(x.shape)
    pl.contour(x, y, z, linewidths=2)

    pl.axis([X_min, X_max, Y_min, Y_max])


def plot_predicted_data(y_pred):
    """
    Plot predicted data side-by-side in subplots.

    Used in example 5 to explore model convergence.
    """
    pl.subplot(3,1,1)
    plot_hf_data()
    decorate_plot()
    pl.xlabel('')
    pl.ylabel('')

    pl.subplot(3,1,2)
    plot_predicted_sample(data_heat_flux.distance, y_pred)
    decorate_plot()
    pl.xlabel('')

    pl.subplot(3,1,3)
    plot_predicted_sample(data_heat_flux.distance, y_pred)
    decorate_plot()
    pl.ylabel('')

    pl.subplots_adjust(hspace=0.)


def plot_predicted_sample(x, y_pred):
    """Used by the plot_predicted_data function."""
    t = pl.rand() * len(y_pred.trace())
    y_t = y_pred.trace()[t]
    pl.plot(x, y_t, 'g^', ms=12, mew=0, label='Prediction')


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

    ramp_t = np.linspace(1, 600, 100)

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
