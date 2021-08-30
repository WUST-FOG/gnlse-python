:orphan:

Nonlinear coefficient
=====================

The time derivative term inside GNLSE models the dispersion of
the nonlinearity. This is usually assiociated with effects such
as self-steepening and optical shock formation, characterized by
a timescale :math:`\tau_0 = 1/\omega_0`. In the context of fibre
propagation, additional disperison of the nonlinearity arises
from the frequency dependence of the effective area,
and :math:`\tau_0 = 1/\omega_0` can be generalized for this in
an approximate manner.

A better aproach is to include the dispersion of the nonlinear response is to
describe it directly in the frequency domain [J07]_.
In this case we can derive a GNLSE for the pulse evolution using
:math:`\gamma(\omega)` defined as

.. math::

   \gamma(\omega) = \frac{n_2 n_0 \omega}{c n_{eff}( \omega ) A_{eff}^{1/4}(\omega )},

with the substitution for the envelope of amplitude as scaled variable

.. math::

   C(z, \omega) = \frac{A_{eff}^{1/4}(\omega_0 )}{A_{eff}^{1/4}(\omega )} A(z, \omega).

.. autoclass:: gnlse.NonlinearityFromEffectiveArea
