"""Calculates different Raman responses and plots them.
Based on the chosen Raman model, the response is
calculated and shown on the graph. There are three
available Raman reponse models.
"""

import numpy as np
import matplotlib.pyplot as plt
import gnlse


if __name__ == '__main__':
    # Initial paremeters
    ##########################################################################
    # Number of grid points
    n = 2 ** 13
    # Time window width [ps]
    time_window = 12.5
    # The speed of light [nm/ps]
    c = 299792458 * 1e-3
    # Central wavelength [nm]
    wavelength = 835
    # Central frequency [THz]
    w0 = (2 * np.pi * c) / wavelength
    # Time grid [ps]
    T = np.linspace(-time_window / 2, time_window / 2, n)

    # K. J. Blow and D. Wood Raman response
    fr, RT1 = gnlse.raman_blowwood(T)
    RT1 = RT1 / np.max(RT1)
    # Q. Lin and Govind P. Agrawal Raman response
    fr2, RT2 = gnlse.raman_linagrawal(T)
    RT2 = RT2 / np.max(RT2)
    # D. Hollenbeck and C. D. Cantrell Raman response
    fr3, RT3 = gnlse.raman_holltrell(T)
    RT3 = RT3 / np.max(RT3)

    plt.plot(T, RT1, label="Blow-Wood")
    plt.plot(T, RT2, label="Lin-Agrawal")
    plt.plot(T, RT3, label="Hollenbeck-Cantrell")

    plt.xlim(-0.025, 1)
    plt.ylabel("Raman response [a.u.]")
    plt.xlabel("Time [ps]")

    plt.legend()

    plt.show()
