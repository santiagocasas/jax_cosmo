from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from jax.tree_util import register_pytree_node_class
import jax.numpy as np
from jax.experimental.ode import odeint

import jax_cosmo.constants as const
from jax_cosmo.utils import a2z, z2a

__all__ = ["Cosmology"]

@register_pytree_node_class
class Cosmology:

  def __init__(self, Omega_c, Omega_b, h, n_s, sigma8, Omega_k, w0, wa,
                     gamma=0.55):
    """
    Cosmology object, stores primary and derived cosmological parameters.

    Parameters:
    -----------
    Omega_c, float
      Cold dark matter density fraction.
    Omega_b, float
      Baryonic matter density fraction.
    h, float
      Hubble constant divided by 100 km/s/Mpc; unitless.
    n_s, float
      Primordial scalar perturbation spectral index.
    sigma8, float
      Variance of matter density perturbations at an 8 Mpc/h scale
    Omega_k, float
      Curvature density fraction.
    w0, float
      First order term of dark energy equation
    wa, float
      Second order term of dark energy equation of state
    """
    # Store primary parameters
    self._Omega_c = Omega_c
    self._Omega_b = Omega_b
    self._h = h
    self._n_s = n_s
    self._sigma8 = sigma8
    self._Omega_k = Omega_k
    self._w0 = w0
    self._wa = wa
    self._gamma = gamma

    # Create a workspace where functions can store some precomputed
    # results
    self._workspace = {}

  def __str__(self):
    return 'Cosmological parameters: \n' + \
        '    h:        ' + str(self.h) + ' \n' + \
        '    Omega_b:  ' + str(self.Omega_b) + ' \n' + \
        '    Omega_c:  ' + str(self.Omega_c) + ' \n' + \
        '    Omega_k:  ' + str(self.Omega_k) + ' \n' + \
        '    w0:       ' + str(self.w0) + ' \n' + \
        '    wa:       ' + str(self.wa) + ' \n' + \
        '    ns:        ' + str(self.n_s) + ' \n' + \
        '    sigma8:   ' + str(self.sigma8) + ' \n' + \
        '    gamma:       ' + str(self.gamma)

  def __repr__(self):
    return self.__str__()

  # Operations for flattening/unflattening representation
  def tree_flatten(self):
    return ((self._Omega_c, self._Omega_b, self._h, self._n_s, self._sigma8,
             self._Omega_k, self._w0, self._wa, self._gamma), None)
  @classmethod
  def tree_unflatten(cls, aux_data, children):
    Omega_c, Omega_b, h, n_s, sigma8, Omega_k, w0, wa, gamma = children
    return cls(Omega_c=Omega_c, Omega_b=Omega_b, h=h, n_s=n_s,
               sigma8=sigma8, Omega_k=Omega_k, w0=w0, wa=wa, gamma=gamma)

  # Cosmological parameters, base and derived
  @property
  def Omega(self):
    return 1.0 - self._Omega_k

  @property
  def Omega_b(self):
    return self._Omega_b

  @property
  def Omega_c(self):
    return self._Omega_c

  @property
  def Omega_m(self):
    return self._Omega_b + self._Omega_c

  @property
  def Omega_de(self):
    return self.Omega - self.Omega_m

  @property
  def Omega_k(self):
    return self._Omega_k

  @property
  def k(self):
    if self.Omega > 1.0:   # Closed universe
      k = 1.0
    elif self.Omega == 1.0:  # Flat universe
      k = 0
    elif self.Omega < 1.0:  # Open Universe
      k = -1.0
    return k

  @property
  def sqrtk(self):
    return np.sqrt(np.abs(self._Omega_k))

  @property
  def sqrtk(self):
    return self._sqrtk

  @property
  def h(self):
    return self._h

  @property
  def w0(self):
    return self._w0

  @property
  def wa(self):
    return self._wa

  @property
  def gamma(self):
    return self._gamma

  @property
  def n_s(self):
    return self._n_s

  @property
  def sigma8(self):
    return self._sigma8
