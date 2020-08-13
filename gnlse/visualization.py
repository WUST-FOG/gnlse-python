"""
Various plotting functions for visualizing GNLSE simulations using Matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import interp2d

from gnlse.common import c


def plot_wavelength_vs_distance(solver, WL_range=[400, 1350], ax=None,
                                norm=None):
    if ax is None:
        ax = plt.gca()

    if norm is None:
        norm = np.max(np.abs(solver.AW)**2)

    lIW = np.fliplr(
        10 * np.log10(np.abs(solver.AW)**2 / norm,
                      where=(np.abs(solver.AW)**2 > 0)))
    WL = 2 * np.pi * c / solver.W  # wavelength grid
    WL_asc = np.flip(WL, )  # ascending order for interpolation
    iis = np.logical_and(WL_asc > WL_range[0],
                         WL_asc < WL_range[1])  # indices of interest

    WL_asc = WL_asc[iis]
    lIW = lIW[:, iis]

    interpolator = interp2d(WL_asc, solver.Z, lIW)
    newWL = np.linspace(np.min(WL_asc), np.max(WL_asc), lIW.shape[1])
    toshow = interpolator(newWL, solver.Z)

    ax.imshow(toshow, origin='lower', aspect='auto', cmap="magma",
              extent=[np.min(WL_asc), np.max(WL_asc), 0, np.max(solver.Z)],
              vmin=-40)
    ax.set_xlabel("Wavelength [nm]")
    ax.set_ylabel("Distance [m]")
    return ax


def plot_delay_vs_distance(solver, time_range=None, ax=None, norm=None):
    if ax is None:
        ax = plt.gca()

    if time_range is None:
        time_range = [np.min(solver.t), np.max(solver.t)]

    if norm is None:
        norm = np.max(np.abs(solver.At)**2)

    lIT = 10 * np.log10(np.abs(solver.At)**2 / norm,
                        where=(np.abs(solver.At)**2 > 0))

    ax.pcolormesh(solver.t, solver.Z, lIT, shading="auto", vmin=-40,
                  cmap="magma")
    ax.set_xlim(time_range)
    ax.set_xlabel("Delay [ps]")
    ax.set_ylabel("Distance [m]")
    return ax


def quick_plot(solution):
    plt.suptitle('GNLSE solution')

    plt.subplot(1, 2, 1)
    plot_wavelength_vs_distance(solution)

    plt.subplot(1, 2, 2)
    plot_delay_vs_distance(solution)

    plt.show()
