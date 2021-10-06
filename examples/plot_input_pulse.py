"""Calculates envelopes of various impulses and plots them.
Based on the chosen envelopes impulse, the aplitude envelope is
calculated and shown on the graph. There are three
available envelopes impulses models:
hyperbolic secant, gaussian and lorentzian.
"""

import numpy as np
import matplotlib.pyplot as plt

import gnlse

if __name__ == '__main__':
    # time full with half maximum of impulse
    FWHM = 2
    # Time grid [ps]
    T = np.linspace(-2 * FWHM, 2 * FWHM, 1000 * FWHM)
    # peak power [W]
    Pmax = 100

    # Amplitude envelope of gaussina impulse
    A1 = gnlse.GaussianEnvelope(Pmax, FWHM).A(T)
    # Amplitude envelope of hiperbolic secans impulse
    A2 = gnlse.SechEnvelope(Pmax, FWHM).A(T)
    # Amplitude envelope of lorentzian impulse
    A3 = gnlse.LorentzianEnvelope(Pmax, FWHM).A(T)
    # Amplitude envelope of continious wave
    A4 = gnlse.CWEnvelope(Pmax).A(T)

    plt.figure(figsize=(12, 8))
    plt.subplot(1, 2, 1)
    plt.plot(T, A1, label='gauss')
    plt.plot(T, A2, label='sech')
    plt.plot(T, A3, label='lorentz')
    plt.plot(T, A4, label='cw')
    plt.xlabel("Time [ps]")
    plt.ylabel("Amplitude [sqrt(W)]")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(T, A1**2, label='gauss')
    plt.plot(T, A2**2, label='sech')
    plt.plot(T, A3**2, label='lorentz')
    plt.plot(T, A4**2, label='cw')
    plt.xlabel("Time [ps]")
    plt.ylabel("Power [W]")
    plt.legend()

    plt.show()
