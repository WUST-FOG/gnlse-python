"""Dispersion operator in optical fibres.

Based on delivered frequency vector and damping indexes
script calculates linear dispersion operator in
frequency domain.

"""
import numpy as np
from scipy import interpolate


class Dispersion(object):
    def D(V):
        raise NotImplementedError('Dispersion not implemented')


class DispersionFiberFromTaylor(Dispersion):
    """Calculates the dispersion in frequency domain

    Parameters
     ----------
    loss : float
        Loss factor [dB/m]
    betas : ndarray (N)
        Derivatives of constant propagations at 835 nm [ps^2/km]
    Returns
    -------
    ndarray (N)
        vector representing linear dispersion of the fibre

    """

    def __init__(self, loss, betas):
        self.loss = loss
        self.betas = betas

    def D(self, V):
        """

        Parameters
        ----------
        V : ndarray, (N)
            Frequency vector

        Returns
        -------
        ndarray, (N)
            Linear dispersion operator in frequency domain
        """
        # Damping
        alpha = np.log(10**(self.loss / 10))
        # Taylor series for subsequent derivatives
        # of constant propagation
        B = sum(beta / np.math.factorial(i + 2) * V**(i + 2)
                for i, beta in enumerate(self.betas))
        L = 1j * B - alpha / 2
        return L


class DispersionFiberFromInterpolation(Dispersion):
    """Calculates the propagation function in frequency domain, using
    the extrapolation method based on delivered refractive indexes
    and corresponding wavelengths. The returned value is a vector
    of dispersion operator.

    Parameters
     ----------
    loss : float
        Loss factor [dB/m]
    betas : ndarray (N)
        Derivatives of constant propagations at
        central wavelength in nm [ps^2/km]
    neff : ndarray (N)
        Effective refractive index
    wavelength : ndarray (N)
        Wavelength corresponding to refractive index
    Returns
    -------
    ndarray (N)
        Vector representing linear dispersion of the fibre

    """

    def __init__(self, loss, neff, lambdas, central_wavelength):
        self.loss = loss
        # refractive indices
        self.neff = neff
        # wavelengths for neffs in [nm]
        self.lambdas = lambdas
        # central wavelength in [nm]
        self.central_wavelength = central_wavelength

    def D(self, V):
        """

        Parameters
        ----------
        V : ndarray, (N)
            Frequency vector

        Returns
        -------
        ndarray, (N)
            Linear dispersion operator in frequency domain
        """
        # The speed of light [nm / ps]
        c = 299792458 * 1e-3
        # Central frequency [1/ps = THz]
        w0 = (2.0 * np.pi * c) / self.central_wavelength
        Z = V + w0

        omega = 2 * np.pi * c / self.lambdas
        dOmega = Z[1] - Z[0]
        Bet = self.neff * omega / c

        # Extrapolate betas for a frequency vector
        fun_interpolation = interpolate.interp1d(omega,
                                                 Bet,
                                                 kind='cubic',
                                                 fill_value="extrapolate")

        B = fun_interpolation(Z)
        # Propagation constant at central frequency [1/m]
        B0 = fun_interpolation(w0)
        # Value of propagation at a lower end of interval [1/m]
        B0plus = fun_interpolation(w0 + dOmega)
        # Value of propagation at a higher end of interval [1/m]
        B0minus = fun_interpolation(w0 - dOmega)

        # Difference quotient, approximation of
        # derivative of a function at a point [ps/m]
        B1 = (B0plus - B0minus) / (2 * dOmega)

        # Loss factor [dB / m]
        alpha = np.log(10**(self.loss / 10))

        # Linear dispersion operator
        L = 1j * (B - (B0 + B1 * V)) - alpha / 2
        return L
