from scipy.stats import chi2
import math
import numpy as np
import os

def poisson_interval(k, alpha=2.*0.159):
    if k == 0: return -math.log(alpha)
    high = chi2.ppf(1.-alpha/2., 2*k + 2) / 2.
    low = chi2.ppf(alpha/2., 2*k) / 2. if k > 0 else 0.
    return low, high

def dump_hist(hist, bin_edges, file_name, error_fct=poisson_interval, errors=[]):
    assert len(errors) == 0 or len(errors) == len(hist)

    file_name = os.path.join('img', file_name)

    columns = ['lower bin edge', 'bin center', 'upper bin edge',
               'lower error', 'bin content', 'upper error']
    with open(file_name, 'w') as f:
        f.write(','.join(['\"{}\"'.format(x) for x in columns]) + '\n')

        i = 0 
        row_temp = ','.join(['{:.5g}',] * len(columns))
        for n in hist:
            bin_edge = bin_edges[i], bin_edges[i+1]
            bin_center = np.mean(bin_edge)

            if errors: 
                error_low, error_up = n - errors[i], n + errors[i]
            else:
                error_low, error_up = error_fct(n)

            i = i + 1

            values = bin_edge[0], bin_center, bin_edge[1], error_low, n, error_up
            f.write(row_temp.format(*values) + '\n')

def dump_hist2d(hist, xbin_edges, ybin_edges, file_name):
    file_name = os.path.join('img', file_name)

    columns = ['x', 'y', 'xlow', 'xhigh', 'ylow', 'yhigh', 'n']
    with open(file_name, 'w') as f:
        f.write(','.join(['\"{}\"'.format(x) for x in columns]) + '\n')

        row_temp = ','.join(['{:.5g}',] * len(columns))

        for j in range(len(ybin_edges)-1):
            for i in range(len(xbin_edges)-1):
                x_low, x_high = xbin_edges[i:i+2]
                y_low, y_high = ybin_edges[j:j+2]
                x = (x_low + x_high) / 2.
                y = (y_low + y_high) / 2.
                n = hist[i][j]
                values = x, y, x_low, x_high, y_low, y_high, n
                f.write(row_temp.format(*values) + '\n')

def make_hist_file(data, bin_edges, file_name, error_fct=poisson_interval, errors=[]):
    hist, bin_edges = np.histogram(data, bin_edges)
    dump_hist(hist, bin_edges, file_name, error_fct, errors)

def dump_hist_with_given_uncertainties(data, bin_edges, file_name):
    data = [(float(x.n), float(x.s)) for x in data]
    data, errors = zip(*data)
    dump_hist(data, bin_edges, file_name, errors=errors)

def make_steps_file(func, bin_edges, file_name, n=100):
    file_name = os.path.join('img', file_name)
    columns = ['left edge', 'height']
    with open(file_name, 'w') as f:
        f.write(','.join(['\"{}\"'.format(x) for x in columns]) + '\n')
        row_temp = ','.join(['{:.5g}',] * len(columns))

        height = 0.
        for i in range(len(bin_edges) - 1):
            l, r = bin_edges[i:i+2]
            xs = [l + (r-l) * float(i) / float(n-1) for i in range(n)]
            height = sum([func(x) / float(n) for x in xs])
            f.write(row_temp.format(l, height) + '\n')
        f.write(row_temp.format(bin_edges[-1], height))
