"""Amplitude envelopes of different impulses

This module contains functions drawing envelopes of various impulses:
hyperbolic secant, gaussian and lorentzian.

"""

import numpy as np


class Envelope(object):
    def A(T):
        raise NotImplementedError()


class SechEnvelope(Envelope):
    """Amplitude envelope of hyperbolic secant impulse.

    Attributes
    ----------
    Pmax : float
        Peak power, [W].
    FWHM : float
        Pulse duration Full-Width Half-Maximum.
    """

    def __init__(self, Pmax, FWHM):
        self.name = 'Hyperbolic secant envelope'
        self.Pmax = Pmax
        self.FWHM = FWHM

    def A(self, T):
        """

        Parameters
        ----------
        T : ndarray, (n, )
            Time vector

        Returns
        -------
        ndarray, (n, )
            Amplitude envelope of hyperbolic secant impulse in time.
        """
        m = 2 * np.log(1 + np.sqrt(2))
        return np.sqrt(self.Pmax) * 2 / (np.exp(m * T / self.FWHM) +
                                         np.exp(-m * T / self.FWHM))


class GaussianEnvelope(Envelope):
    """Amplitude envelope of gaussian impulse.

    Attributes
    ----------
    Pmax : float
        Peak power [W].
    FWHM : float
        Pulse duration Full-Width Half-Maximum.
    """

    def __init__(self, Pmax, FWHM):
        self.name = 'Gaussian envelope'
        self.Pmax = Pmax
        self.FWHM = FWHM

    def A(self, T):
        """

        Parameters
        ----------
        T : ndarray, (n, )
            Time vector.

        Returns
        -------
        ndarray, (n, )
            Amplitude envelope of gaussian impulse in time.
        """
        m = 4 * np.log(2)
        return np.sqrt(self.Pmax) * np.exp(-m * .5 * T**2 / self.FWHM**2)


class LorentzianEnvelope(Envelope):
    """Amplitude envelope of lorentzian impulse.

    Attributes
    ----------
    Pmax : float
        Peak power [W].
    FWHM : float
        Pulse duration Full-Width Half-Maximum.
    """

    def __init__(self, Pmax, FWHM):
        self.name = 'Lorentzian envelope'
        self.Pmax = Pmax
        self.FWHM = FWHM

    def A(self, T):
        """

        Parameters
        ----------
        T : ndarray, (n, )
            Time vector.

        Returns
        -------
        ndarray, (n, )
            Amplitude envelope of lorentzian impulse in time.
        """
        m = 2 * np.sqrt(np.sqrt(2) - 1)
        return np.sqrt(self.Pmax) / (1 + (m * T / self.FWHM)**2)
