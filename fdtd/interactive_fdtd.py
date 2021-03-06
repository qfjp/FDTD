"""
interactiveFDTD.m
"""
import numpy

SCALE_FACTOR_2 = 0.8

ARB_MATRIX = numpy.matrix([[1.00000, 1.00000, 1.00000],
                           [0.85714, 1.00000, 1.00000],
                           [0.71429, 1.00000, 1.00000],
                           [0.57143, 1.00000, 1.00000],
                           [0.42857, 1.00000, 1.00000],
                           [0.28571, 1.00000, 1.00000],
                           [0.14286, 1.00000, 1.00000],
                           [0.00000, 1.00000, 1.00000],
                           [0.00000, 0.90000, 1.00000],
                           [0.00000, 0.80000, 1.00000],
                           [0.00000, 0.70000, 1.00000],
                           [0.00000, 0.60000, 1.00000],
                           [0.00000, 0.50000, 1.00000],
                           [0.00000, 0.40000, 1.00000],
                           [0.00000, 0.30000, 1.00000],
                           [0.00000, 0.20000, 1.00000],
                           [0.00000, 0.10000, 1.00000],
                           [0.00000, 0.00000, 1.00000],
                           [0.00000, 0.00000, 0.93333],
                           [0.00000, 0.00000, 0.86667],
                           [0.00000, 0.00000, 0.80000],
                           [0.00000, 0.00000, 0.73333],
                           [0.00000, 0.00000, 0.66667],
                           [0.00000, 0.00000, 0.60000],
                           [0.00000, 0.00000, 0.53333],
                           [0.00000, 0.00000, 0.46667],
                           [0.00000, 0.00000, 0.40000],
                           [0.00000, 0.00000, 0.33333],
                           [0.00000, 0.00000, 0.26667],
                           [0.00000, 0.00000, 0.20000],
                           [0.00000, 0.00000, 0.13333],
                           [0.00000, 0.00000, 0.06667],
                           [0.00000, 0.00000, 0.00000],
                           [0.03333, 0.00000, 0.00000],
                           [0.06667, 0.00000, 0.00000],
                           [0.10000, 0.00000, 0.00000],
                           [0.13333, 0.00000, 0.00000],
                           [0.16667, 0.00000, 0.00000],
                           [0.20000, 0.00000, 0.00000],
                           [0.23333, 0.00000, 0.00000],
                           [0.26667, 0.00000, 0.00000],
                           [0.30000, 0.00000, 0.00000],
                           [0.33333, 0.00000, 0.00000],
                           [0.36667, 0.00000, 0.00000],
                           [0.40000, 0.00000, 0.00000],
                           [0.45455, 0.00000, 0.00000],
                           [0.50909, 0.00000, 0.00000],
                           [0.56364, 0.00000, 0.00000],
                           [0.61818, 0.00000, 0.00000],
                           [0.67273, 0.00000, 0.00000],
                           [0.72727, 0.00000, 0.00000],
                           [0.78182, 0.00000, 0.00000],
                           [0.83636, 0.00000, 0.00000],
                           [0.89091, 0.00000, 0.00000],
                           [0.94545, 0.00000, 0.00000],
                           [1.00000, 0.00000, 0.00000],
                           [1.00000, 0.12500, 0.12500],
                           [1.00000, 0.25000, 0.25000],
                           [1.00000, 0.37500, 0.37500],
                           [1.00000, 0.50000, 0.50000],
                           [1.00000, 0.62500, 0.62500],
                           [1.00000, 0.75000, 0.75000],
                           [1.00000, 0.87500, 0.87500],
                           [1.00000, 1.00000, 1.00000]])

ANSWER_SIM = [4, 5, 0, 0, 10, 0, 0, 0.8, 0, ARB_MATRIX]
