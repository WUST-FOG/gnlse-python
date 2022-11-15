import numpy as np
import scipy.integrate
import pyfftw
import tqdm

from gnlse.common import c
from gnlse.import_export import write_mat, read_mat


class GNLSESetup:
    """
    Model inputs for the ``GNLSE`` class.

    Attributes
    ----------
    resolution : int
        Number of points on the computational grid. Determines time resolution
        and bandwidth. Avoid numbers with large prime factors.
    time_window : float [ps]
        Width of the time window.
    wavelength : float [nm]
        Central wavelength of the input pulse.
    fiber_length : float [m]
        Length of the simulated optical fiber.
    z_saves : int
        Number of snapshots to save along the fiber. Larger numbers require
        more memory to store the result.
    nonlinearity : float [1/W/m]
        Effective nonlinearity.
    pulse_model : Envelope
        Input pulse envelope model.
    dispersion_model : Dispersion, optional
        Fiber dispersion model or ``None`` to model a dispersionless fiber.
    raman_model : function, optional
        Raman scattering model or ``None`` if the effect is to be neglected.
    self_steepning : bool, optional
        Whether to include the effect of self-steepening. Disabled by default.
    rtol : float, optional
        Relative tolerance passed to the ODE solver.
    atol : float, optional
        Absolute tolerance passed to the ODE solver.
    method : str, optional
        Integration method passed to the ODE solver.
    """

    def __init__(self):
        self.resolution = None
        self.time_window = None
        self.wavelength = None
        self.fiber_length = None

        self.z_saves = 200
        self.nonlinearity = 0
        self.pulse_model = None
        self.dispersion_model = None
        self.raman_model = None
        self.self_steepening = False

        self.rtol = 1e-3
        self.atol = 1e-4
        self.method = 'RK45'


class Solution:
    """
    Represents a solution to a GNLSE problem.

    Attributes
    ----------
    t : ndarray, (n,)
        Time domain grid.
    W : ndarray, (n,)
        Absolute angular frequency grid.
    Z : ndarray (m,)
        Points at which intermediate steps were saved.
    At : ndarray, (n, m)
        Intermediate steps in the time domain.
    AW : ndarray, (n, m)
        Intermediate steps in the frequency domain.
    """

    def __init__(self, t=None, W=None, w_0=None, Z=None, At=None, AW=None,
                 Aty=None, AWy=None):
        self.t = t
        self.W = W
        self.w_0 = w_0
        self.Z = Z
        self.At = At
        self.AW = AW

    def to_file(self, path):
        """
        Saves a solution to a file.

        Parameters
        ----------
        path : str
            Path to file.
        """

        data = {'t': self.t, 'W': self.W, 'Z': self.Z, 'At': self.At,
                'AW': self.AW}
        write_mat(data, path)

    def from_file(self, path):
        """
        Load a solution from file.

        Parameters
        ----------
        path : str
            Path to file.
        """

        data = read_mat(path)
        self.t = data['t']
        self.W = data['W']
        self.Z = data['Z']
        self.At = data['At']
        self.AW = data['AW']


class GNLSE:
    """
    Models propagation of an optical pulse in a fiber by integrating
    the generalized non-linear Schrödinger equation.

    Attributes
    ----------
    setup : GNLSESetup
        Model inputs in the form of a ``GNLSESetup`` object.
    """

    def __init__(self, setup):
        if not isinstance(setup, GNLSESetup):
            raise TypeError("setup is not an instance of GNLSESetup")

        if setup.resolution is None:
            raise ValueError("'resolution' not set")
        if setup.time_window is None:
            raise ValueError("'time_window' not set")
        if setup.wavelength is None:
            raise ValueError("'wavelength' not set")
        if setup.fiber_length is None:
            raise ValueError("'fiber_length' not set")
        if setup.pulse_model is None:
            raise ValueError("'pulse_model' not set")

        # simulation parameters
        self.fiber_length = setup.fiber_length
        self.z_saves = setup.z_saves
        self.rtol = setup.rtol
        self.atol = setup.atol
        self.method = setup.method
        self.N = setup.resolution

        # Time domain grid
        self.t = np.linspace(-setup.time_window / 2,
                             setup.time_window / 2,
                             self.N)

        # Relative angular frequency grid
        self.V = 2 * np.pi * np.arange(-self.N / 2,
                                       self.N / 2
                                       ) / (self.N * (self.t[1] - self.t[0]))
        # Central angular frequency [10^12 rad]
        self.w_0 = (2.0 * np.pi * c) / setup.wavelength
        self.Omega = self.V + self.w_0

        # Absolute angular frequency grid
        if setup.self_steepening and np.abs(self.w_0) > np.finfo(float).eps:
            W = self.V + self.w_0
        else:
            W = np.full(self.V.shape, self.w_0)
        self.W = np.fft.fftshift(W)

        # Nonlinearity
        if hasattr(setup.nonlinearity, 'gamma'):
            # in case in of frequency dependent nonlinearity
            gamma, self.scale = setup.nonlinearity.gamma(self.V)
            self.gamma = gamma / self.w_0
            self.gamma = np.fft.fftshift(self.gamma)
            self.scale = np.fft.fftshift(self.scale)
        else:
            # in case in of direct introduced value
            self.gamma = setup.nonlinearity / self.w_0
            self.scale = 1

        # Raman scattering
        self.RW = None
        if setup.raman_model:
            self.fr, RT = setup.raman_model(self.t)
            if np.abs(self.fr) < np.finfo(float).eps:
                self.RW = None
            else:
                self.RW = self.N * np.fft.ifft(
                    np.fft.fftshift(np.transpose(RT)))

        # Dispersion operator
        if setup.dispersion_model:
            self.D = setup.dispersion_model.D(self.V)
        else:
            self.D = np.zeros(self.V.shape)

        # Input pulse
        if hasattr(setup.pulse_model, 'A'):
            self.A = setup.pulse_model.A(self.t)
        else:
            self.A = setup.pulse_model

    def run(self):
        """
        Solve one mode GNLSE equation described by the given
        ``GNLSESetup`` object.

        Returns
        -------
        setup : Solution
            Simulation results in the form of a ``Solution`` object.
        """
        dt = self.t[1] - self.t[0]
        self.D = np.fft.fftshift(self.D)
        x = pyfftw.empty_aligned(self.N, dtype="complex128")
        X = pyfftw.empty_aligned(self.N, dtype="complex128")
        plan_forward = pyfftw.FFTW(x, X)
        plan_inverse = pyfftw.FFTW(X, x, direction="FFTW_BACKWARD")

        progress_bar = tqdm.tqdm(total=self.fiber_length, unit='m')

        def rhs(z, AW):
            """
            The right hand side of the differential equation to integrate.
            """

            progress_bar.n = round(z, 3)
            progress_bar.update(0)

            x[:] = AW * np.exp(self.D * z)
            At = plan_forward().copy()
            IT = np.abs(At)**2

            if self.RW is not None:
                X[:] = IT
                plan_inverse()
                x[:] *= self.RW
                plan_forward()
                RS = dt * self.fr * X
                X[:] = At * ((1 - self.fr) * IT + RS)
                M = plan_inverse()
            else:
                X[:] = At * IT
                M = plan_inverse()

            rv = 1j * self.gamma * self.W * M * np.exp(
                -self.D * z)

            return rv

        Z = np.linspace(0, self.fiber_length, self.z_saves)
        solution = scipy.integrate.solve_ivp(
            rhs,
            t_span=(0, self.fiber_length),
            y0=np.fft.ifft(self.A) * self.scale,
            t_eval=Z,
            rtol=self.rtol,
            atol=self.atol,
            method=self.method)
        AW = solution.y.T

        progress_bar.close()

        # Transform the results into the time domain
        At = np.zeros(AW.shape, dtype=AW.dtype)
        for i in range(len(AW[:, 0])):
            AW[i, :] *= np.exp(np.transpose(
                self.D) * Z[i]) / self.scale
            At[i, :] = np.fft.fft(AW[i, :])
            AW[i, :] = np.fft.fftshift(AW[i, :]) * self.N * dt

        return Solution(self.t, self.Omega, self.w_0, Z, At, AW)
