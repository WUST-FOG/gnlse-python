"""
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
    betas = np.array([-0.024948815481502, 8.875391917212998e-05,
                      -9.247462376518329e-08, 1.508210856829677e-10])
    setup.dispersion_model = gnlse.DispersionFiberFromTaylor(loss, betas)

    # Input impulse parameters
    power = 10000
    # pulse duration [ps]
    tfwhm = 0.05
    # hyperbolic secant
    setup.impulse_model = gnlse.SechEnvelope(power, tfwhm)

    # Simulation
    ###########################################################################
    # Type of dyspersion operator: build from Taylor expansion
    setup.dispersion = gnlse.DispersionFiberFromTaylor(loss, betas)
    solver = gnlse.GNLSE(setup)
    solution = solver.run()

    # Visualization
    ###########################################################################
    plt.figure(figsize=(10, 8))

    plt.subplot(2, 2, 1)
    plt.title("Results for Taylor expansion")
    gnlse.plot_wavelength_vs_distance(solution, WL_range=[400, 1400])
    plt.subplot(2, 2, 3)
    gnlse.plot_delay_vs_distance(solution, time_range=[-.5, 5])

    # read mat file for neffs
    mat_path = os.path.join(os.path.dirname(__file__), '..',
                            'data', 'neff_pcf.mat')
    mat = gnlse.read_mat(mat_path)
    # neffs
    neff = mat['neff'][:, 1]
    # wavelengths in nm
    lambdas = mat['neff'][:, 0] * 1e9

    # Type of dyspersion operator: build from interpolation of given neffs
    setup.dispersion = gnlse.DispersionFiberFromInterpolation(
        loss, neff, lambdas, setup.wavelength)
    solver = gnlse.GNLSE(setup)
    solution = solver.run()

    # Visualization
    ###########################################################################
    plt.subplot(2, 2, 2)
    plt.title("Results for interpolation")
    gnlse.plot_wavelength_vs_distance(solution, WL_range=[400, 1400])
    plt.subplot(2, 2, 4)
    gnlse.plot_delay_vs_distance(solution, time_range=[-.5, 5])

    plt.show()
