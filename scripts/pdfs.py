from math import sqrt, pi, erf, exp

class Linear:
    def __init__(self, boundaries):
        self.boundaries = boundaries

    def _x_to_arg(self, x):
        l, r = self.boundaries
        return 2. * (x - l) / (r - l) - 1.

    def __call__(self, x, a):
        arg = self._x_to_arg(x)
        norm = self.boundaries[1] - self.boundaries[0]
        return (1. + a * arg) / norm

    def integral(self, x, a):
        arg = self._x_to_arg(x)
        return (arg + a / 2. * arg**2) / 2.


class Gaussian:
    SQRT2 = sqrt(2.)
    SQRTPI = sqrt(pi)
    
    def __init__(self, boundaries):
        self.boundaries = boundaries

    def _t(self, x, mean, width):
        return (x - mean) / self.SQRT2 / width
    
    def __call__(self, x, mean, width):
        tx, tl, tr = [self._t(y, mean, width)
                      for y in [x, *self.boundaries]]

        norm = self.SQRTPI / self.SQRT2 * width
        norm *= erf(tr) - erf(tl)
        
        return exp(-tx * tx) / norm

    def integral(self, x, mean, width):
        tx, tl, tr = [self._t(y, mean, width)
                      for y in [x, *self.boundaries]]
        return erf(tx) / (erf(tr) - erf(tl))
