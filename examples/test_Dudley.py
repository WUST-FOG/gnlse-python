"""
Example of supercontinuum generation in anomalous dispersion regime at
a central wavelength of 835 nm in a 15 centimeter long fiber.
Data from J. M. Dudley, G. Genty, and S. Coen, Rev. Mod. Phys., vol. 78, no. 4,
pp. 1135–1184, 2006.

The python code based on MATLAB code published in
'Supercontinuum Generation in Optical Fibers'
by J. M. Dudley and J. R. Taylor, available at http://scgbook.info/.
"""

import numpy as np
import matplotlib.pyplot as plt

import gnlse


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
    peak_power = 10000  # W
    duration = 0.050  # ps

    # This example extends the original code with additional simulations for
    pulse_models = [
        gnlse.SechEnvelope(peak_power, duration),
        gnlse.GaussianEnvelope(peak_power, duration),
        gnlse.LorentzianEnvelope(peak_power, duration)
    ]

    count = len(pulse_models)
    plt.figure(figsize=(14, 8), facecolor='w', edgecolor='k')
    for i, pulse_model in enumerate(pulse_models):
        print('%s...' % pulse_model.name)

        setup.pulse_model = pulse_model
        solver = gnlse.GNLSE(setup)
        solution = solver.run()

        plt.subplot(2, count, i + 1)
        plt.title(pulse_model.name)
        gnlse.plot_wavelength_vs_distance(solution, WL_range=[400, 1400])

        plt.subplot(2, count, i + 1 + count)
        gnlse.plot_delay_vs_distance(solution, time_range=[-0.5, 5])

    plt.tight_layout()
    plt.show()
