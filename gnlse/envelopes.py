"""Amplitude envelopes of different impulses

This module contains functions drawing envelopes of various impulses:
hyperbolic secant, gaussian and lorentzian.

"""

import numpy as np


class Envelope(object):
    def A(T):
        raise NotImplementedError()


class SechEnvelope(Envelope):
    """Amplitude envelope of hyperbolic secant impulse

    Parameters
    ----------
    Pmax : float
        Peak power [W]
    FWHM : float
        Pulse duration Full-Width Half-Maximum
    """

    def __init__(self, Pmax, FWHM):
        self.name = 'Hyperbolic secant envelope'
        self.Pmax = Pmax
        self.FWHM = FWHM

    def A(self, T):
        """

        Parameters
        ----------
        T : ndarray, (N)
            Time vector

        Returns
        -------
        ndarray, (N)
        """
        m = 2 * np.log(1 + np.sqrt(2))
        return np.sqrt(self.Pmax) * 2 / (np.exp(m * T / self.FWHM) +
                                         np.exp(-m * T / self.FWHM))


class GaussianEnvelope(Envelope):
    """Amplitude envelope of gaussian impulse

    Parameters
    ----------
    Pmax : float
        Peak power [W]
    FWHM : float
        Pulse duration Full-Width Half-Maximum
    """

    def __init__(self, Pmax, FWHM):
        self.name = 'Gaussian envelope'
        self.Pmax = Pmax
        self.FWHM = FWHM

    def A(self, T):
        """

        Parameters
        ----------
        T : ndarray, (N)
            Time vector

        Returns
        -------
        ndarray
            a list of strings representing the header columns
        """
        m = 4 * np.log(2)
        return np.sqrt(self.Pmax) * np.exp(-m * .5 * T**2 / self.FWHM**2)


class LorentzianEnvelope(Envelope):
    """Amplitude envelope of lorentzian impulse

    Parameters
    ----------
    Pmax : float
        Peak power [W]
    FWHM : float
        Pulse duration Full-Width Half-Maximum
    """

    def __init__(self, Pmax, FWHM):
        self.name = 'Lorentzian envelope'
        self.Pmax = Pmax
        self.FWHM = FWHM

    def A(self, T):
        """

        Parameters
        ----------
        T : ndarray, (N)
            Time vector

        Returns
        -------
        ndarray
            a list of strings representing the header columns
        """
        m = 2 * np.sqrt(np.sqrt(2) - 1)
        return np.sqrt(self.Pmax) / (1 + (m * T / self.FWHM)**2)


if __name__ == '__main__':
    from matplotlib import pyplot as plt

    FWHM = 2
    T = np.linspace(-2 * FWHM, 2 * FWHM, 1000 * FWHM)
    Pmax = 100

    A1 = GaussianEnvelope(Pmax, FWHM).A(T)
    A2 = SechEnvelope(Pmax, FWHM).A(T)
    A3 = LorentzianEnvelope(Pmax, FWHM).A(T)

    plt.figure()
    plt.plot(T, A1, label='gauss')
    plt.plot(T, A2, label='sech')
    plt.plot(T, A3, label='lorentz')
    plt.xlabel("Time / ps")
    plt.ylabel("Amplitude / sqrt(W)")
    plt.legend()

    plt.figure()
    plt.plot(T, A1**2, label='gauss')
    plt.plot(T, A2**2, label='sech')
    plt.plot(T, A3**2, label='lorentz')
    plt.xlabel("Time / ps")
    plt.ylabel("Power / W")
    plt.legend()

    plt.show()
