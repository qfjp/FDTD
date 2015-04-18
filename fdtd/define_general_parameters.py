# pylint: disable=invalid-name,no-member
"""
An attempt to translate the god awful madness that is fdtd.m
"""
import numpy
import fdtd.constants as constants

"""
These seem to be hardcoded in interactiveFDTD.m
"""
arb_matrix = numpy.matrix([[1.00000, 1.00000, 1.00000],
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
plotvar1 = 5
plotvar2 = 4
plotvar3 = 0
plotvar4 = 0
plotvar5 = 0.8
plotvar6 = 0
plotvar8 = 0
plotvar9 = arb_matrix
plotvar10 = 10

Anzeige = 0  # Display?!

# From definegeneralparameters.m
# Columns in answer are (in order):
#    i) Max number of gridpoints in 1-D
#   ii) \epsilon - Background
#  iii) \mu - Background
#   iv) Size x-dim [\mum]
#    v) Size y-dim [\mum]
#   vi) Num of time stepsa
#  vii) num of perfectly matched layers
# viii) axis equal
prompt = ['maximum number of Gridpoints in one Dimension',
          '\\epsilon - Background', '\\mu - Background',
          'Size x-Dimension [\\mum]', 'Size y-Dimension [\\mum]',
          'Number of timesteps', 'Number of Perfectly Matched Layers',
          'axis equal']
default_answer = ['300', '1', '1', '5', '5', '300000', '10', '0']
answer = [int(i) for i in default_answer]
pmlwidth = answer[6]

Anz = 0
if Anzeige == 0:
    Anz = pmlwidth + 1
else:
    Anz = 1

# PML Vorkehrungen (Precautions?)
# if answer[4] > answer[5]:
if answer[5] > answer[4]:
    # x=linspace(-str2num(answer{4})/2,str2num(answer{4})/2,str2num(answer{1}))
    # y=[-str2num(answer{5})/2-dx:dx:str2num(answer{5})/2+dx]
    x = numpy.linspace(-answer[3] / 2, answer[3] / 2, num=answer[0])
    dx = x[1] - x[0]

    j = -answer[4] / 2 - dx
    i = dx
    k = answer[4] / 2 + dx
    m = int((k - j) / i)
    # Want the list j, j+i, j+2i, + ... + j+m*i
    y_lst = [j + (mul) * dx for mul in range(m + 1)]
    y = numpy.array(y_lst)
else:
    y = numpy.linspace(-answer[4] / 2, answer[4] / 2, answer[0])
    dx = y[1] - y[0]

    j = -answer[4] / 2 - dx
    i = dx
    k = answer[4] / 2 + dx
    m = int((k - j) / i)
    # Want the list j, j+i, j+2i, + ... + j+m*i
    x_lst = [j + (mul) * dx for mul in range(m + 1)]
    x = numpy.array(x_lst)

X, Y = numpy.meshgrid(x, y)

backgroundeps = constants.epsilon0 * answer[1]
backgroundmu = constants.mu0 * answer[2]
epsilon = backgroundeps * numpy.ones(X.shape)
mu = backgroundmu * numpy.ones(X.shape)
ZS = answer[5]

alphadat = numpy.ones(X.shape)
usergeneralparameters = answer
