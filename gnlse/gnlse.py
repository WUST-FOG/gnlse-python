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
        Central wavelength of the input impulse.
    fiber_length : float [m]
        Length of the simulated optical fiber.
    z_saves : int
        Number of snapshots to save along the fiber. Larger numbers require
        more memory to store the result.
    nonlinearity : float [1/W/m]
        Effective nonlinearity.
    impulse_model : Envelope
        Input impulse envelope model.
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
        self.impulse_model = None
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

    def __init__(self, t=None, W=None, Z=None, At=None, AW=None):
        self.t = t
        self.W = W
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
    Models propagation of an optical impulse in a fiber by integrating the
    generalized non-linear Schrödinger equation.

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
        if setup.impulse_model is None:
            raise ValueError("'impulse_model' not set")

        self.setup = setup

    def run(self):
        """
        Solve the problem described by the given ``GNLSESetup`` object.
        """

        N = self.setup.resolution
        # Time domain grid
        self.t = np.linspace(-self.setup.time_window / 2,
                             self.setup.time_window / 2, N)
        dt = self.t[1] - self.t[0]

        # Relative angular frequency grid
        V = 2 * np.pi * np.arange(-N / 2, N / 2) / (N * dt)

        # Input impulse
        A = self.setup.impulse_model.A(self.t)

        # Central angular frequency [10^12 rad]
        w_0 = (2.0 * np.pi * c) / self.setup.wavelength

        # Dispersion operator
        if self.setup.dispersion_model:
            D = self.setup.dispersion_model.D(V)
        else:
            D = np.zeros(V.shape)

        # Absolute angular frequency grid
        if self.setup.self_steepening and np.abs(w_0) > np.finfo(float).eps:
            W = V + w_0
        else:
            W = np.full(V.shape, w_0)

        # Nonlinearity
        if hasattr(self.setup.nonlinearity, 'gamma'):
            # in case in of frequency dependent nonlinearity
            gamma, scale = self.setup.nonlinearity.gamma(V + w_0)
            gamma /= w_0
        else:
            # in case in of direct introduced value
            gamma = self.setup.nonlinearity / w_0
            scale = None

        # Raman scattering
        if self.setup.raman_model:
            fr, RT = self.setup.raman_model(self.t)
            if np.abs(fr) < np.finfo(float).eps:
                self.raman_model = None
            else:
                RW = N * np.fft.ifft(
                    np.fft.fftshift(np.transpose(RT)))

        D = np.fft.fftshift(D)
        W = np.fft.fftshift(W)

        x = pyfftw.empty_aligned(N, dtype="complex128")
        X = pyfftw.empty_aligned(N, dtype="complex128")
        plan_forward = pyfftw.FFTW(x, X)
        plan_inverse = pyfftw.FFTW(X, x, direction="FFTW_BACKWARD")

        progress_bar = tqdm.tqdm(total=self.setup.fiber_length, unit='m')

        def rhs(z, AW):
            """
            The right hand side of the differential equation to integrate.
            """

            progress_bar.n = round(z, 3)
            progress_bar.update(0)

            # input modification by J. Lægsgaard
            if scale is not None:
                AW *= scale

            x[:] = AW * np.exp(D * z)
            At = plan_forward().copy()
            IT = np.abs(At)**2

            if self.setup.raman_model:
                X[:] = IT
                plan_inverse()
                x[:] *= RW
                plan_forward()
                RS = dt * fr * X
                X[:] = At * ((1 - fr) * IT + RS)
                M = plan_inverse()
            else:
                X[:] = At * IT
                M = plan_inverse()

            rv = 1j * gamma * W * M * np.exp(-D * z)

            # input modification by J. Lægsgaard
            if scale is not None:
                AW /= scale
            return rv

        Z = np.linspace(0, self.setup.fiber_length, self.setup.z_saves)
        solution = scipy.integrate.solve_ivp(
            rhs,
            t_span=(0, self.setup.fiber_length),
            y0=np.fft.ifft(A),
            t_eval=Z,
            rtol=self.setup.rtol,
            atol=self.setup.atol,
            method=self.setup.method)
        AW = solution.y.T

        progress_bar.close()

        # Transform the results into the time domain
        At = np.zeros(AW.shape, dtype=AW.dtype)
        for i in range(len(AW[:, 0])):
            AW[i, :] *= np.exp(np.transpose(D) * Z[i])
            At[i, :] = np.fft.fft(AW[i, :])
            AW[i, :] = np.fft.fftshift(AW[i, :]) / dt
        W = V + w_0

        return Solution(self.t, W, Z, At, AW)
