:orphan:

Nonlinear coefficient
=====================

The time derivative term inside GNLSE models the dispersion of

the nonlinearity. This is usually associated with effects such
as self-steepening and optical shock formation, characterized by
a timescale :math:`\tau_0 = 1/\omega_0`. In the context of fibre
propagation, an additional dispersion of the nonlinearity arises
due to the frequency dependence of the effective mode area.
The last effect can be accounted in :math:`\tau_0`
coefficient in an approximate manner.

A better - still approximate - approach to include the dispersion
of the effective mode area is to
describe it directly in the frequency domain [J07]_.
In this case, we can derive a GNLSE for the pulse evolution using
:math:`\gamma(\omega)` defined as

.. math::

   \overline{\gamma}(\omega) = 
   \frac{n_2n_{\mathrm{eff}}(\omega_0)\omega_0}
   {\mathrm{c}n_\mathrm{eff}(\omega)\sqrt{A_{\mathrm{eff}}(\omega)A_{\mathrm{eff}}(\omega_0)}}.


This approach is more rigorous than the approximation
of (:math:`\gamma = \gamma(\omega_0)`)
and requires the definition of a pseudo-envelope :math:`C(z, \omega)` as


.. math::

   C(z, \omega) = \frac{A_{eff}^{1/4}(\omega_0 )}{A_{eff}^{1/4}(\omega )} A(z, \omega).

.. autoclass:: gnlse.NonlinearityFromEffectiveArea
