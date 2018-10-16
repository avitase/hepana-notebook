import numpy as np
from bisect import bisect
from uncertainties import ufloat
from math import sqrt

class WHist:
    def __init__(self, bin_edges):
        self.dim = np.array(bin_edges).ndim
        self._bin_edges = [bin_edges,] if self.dim == 1 else bin_edges
        self.entries = 0

        data = ufloat(0., 0.)
        sumw2 = 0.
        for i in range(self.dim):
            data = [data,] * (len(self._bin_edges[i]) - 1)
            sumw2 = [sumw2,] * (len(self._bin_edges[i]) - 1)

        self.data = np.array(data)
        self.sumw2 = np.array(sumw2)

    def add(self, x, weight=1):
        if self.dim == 1:
            x = [x,]
        assert self.dim == len(x)

        n = self.dim
        find_bin = lambda n, bin_edges: bisect(bin_edges, n)
        bin_idxs = [find_bin(x[i], self._bin_edges[i]) for i in range(n)]

        is_valid = lambda bin_idx, n_bins: bin_idx > 0 and bin_idx <= n_bins
        n_bins = lambda i: len(self._bin_edges[i]) - 1
        if all([is_valid(bin_idxs[i], n_bins(i)) for i in range(n)]):
            self.entries += 1
            idxs = tuple([bin_idx - 1 for bin_idx in bin_idxs])
            self.sumw2[idxs] += weight**2
            n = self.data[idxs].n
            u = sqrt(self.sumw2[idxs])
            self.data[idxs] = ufloat(n + weight, u)
