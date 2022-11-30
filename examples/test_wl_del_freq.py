"""
This example is here to test new plot functions. This test is based on file
test_dispersion:
Example:  Example of supercontinuum generation in anomalous dispersion regime
at a central wavelength of 835 nm in a 15 centimeter long fiber.
Comparision of results obtained with two dispersion input:
1. dispersion calculated from Taylor expansion
2. dispersion calculated from effective refractive indicies

The python code based on MATLAB code published in
'Supercontinuum Generation in Optical Fibers'
by J. M. Dudley and J. R. Taylor, available at http://scgbook.info/.
"""

import numpy as np
import matplotlib.pyplot as plt

import gnlse

import os

if __name__ == '__main__':
    setup = gnlse.GNLSESetup()

    # Numerical parameters
    setup.resolution = 2**14
    setup.time_window = 12.5  # ps
    setup.z_saves = 200

    # Physical parameters
    setup.wavelength = 835  # nm
    setup.fiber_length = 0.15  # m
    setup.nonlinearity = 0.11  # 1/W/m
    setup.raman_model = gnlse.raman_blowwood
    setup.self_steepening = True

    # The dispersion model is built from a Taylor expansion with coefficients
    # given below.
    loss = 0
    betas = np.array([
        -11.830e-3, 8.1038e-5, -9.5205e-8, 2.0737e-10, -5.3943e-13, 1.3486e-15,
        -2.5495e-18, 3.0524e-21, -1.7140e-24
    ])
    setup.dispersion_model = gnlse.DispersionFiberFromTaylor(loss, betas)

    # Input pulse parameters
    power = 10000
    # pulse duration [ps]
    tfwhm = 0.05
    # hyperbolic secant
    setup.pulse_model = gnlse.SechEnvelope(power, tfwhm) 
    solver = gnlse.GNLSE(setup)
    solution = solver.run()

    plt.figure(figsize=(14, 8), facecolor='w', edgecolor='k')

    plt.subplot(4, 3, 1)
    gnlse.plot_delay_vs_distance(solution, time_range=[-.5, 5], cmap="jet")

    plt.subplot(4, 3, 2)
    gnlse.plot_frequency_vs_distance(solution, frequency_range=[-300, 200],
                                     cmap="plasma")

    plt.subplot(4, 3, 3)
    gnlse.plot_wavelength_vs_distance(solution, WL_range=[400, 1400])

    plt.subplot(4, 3, 4)
    gnlse.plot_delay_vs_distance_logarithmic(solution, time_range=[-.5, 5],
                                             cmap="jet")

    plt.subplot(4, 3, 5)
    gnlse.plot_frequency_vs_distance_logarithmic(solution,
                                                 frequency_range=[-300, 200],
                                                 cmap="plasma")

    plt.subplot(4, 3, 6)
    gnlse.plot_wavelength_vs_distance_logarithmic(solution,
                                                  WL_range=[400, 1400])

    plt.subplot(4, 3, 7)
    gnlse.plot_delay_for_distance_slice(solution, time_range=[-.5, 5])

    plt.subplot(4, 3, 8)
    gnlse.plot_frequency_for_distance_slice(solution,
                                            frequency_range=[-300, 200])

    plt.subplot(4, 3, 9)
    gnlse.plot_wavelength_for_distance_slice(solution, WL_range=[400, 1400])

    plt.subplot(4, 3, 10)
    ax = gnlse.plot_delay_for_distance_slice_logarithmic(solution,
                                                    time_range=[-.5, 5])

    plt.subplot(4, 3, 11)
    gnlse.plot_frequency_for_distance_slice_logarithmic(solution,
                                                frequency_range=[-300, 200])

    plt.subplot(4, 3, 12)
    gnlse.plot_wavelength_for_distance_slice_logarithmic(solution,
                                                         WL_range=[400, 1400])

    plt.tight_layout()
    plt.show()
