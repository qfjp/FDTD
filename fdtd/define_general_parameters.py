# pylint: disable=no-member
"""
An attempt to translate the god awful madness that is fdtd.m
"""
import numpy as np
import phys_util.constants as constants


class Params:
    """
    Reworking define_general_parameters as a class
    """
    def __init__(self):
        self._x_arr = None   # x
        self._y_arr = None   # y
        self.del_x = 0       # dx
        self.del_y = 0       # dy
        self._x_grid = None  # X
        self._y_grid = None  # Y
        self.epsilon = None
        self.mu = None
        self.z_s = None
        self.alphadat = None

    def set_grid(self):
        """
        Set the grid?
        """
        self._x_grid, self._y_grid = np.meshgrid(self._x_arr, self._y_arr)

    def get_grid(self):
        """
        Returns the grid?
        """
        return (self._x_grid, self._y_grid)

    def set_x_arr(self, beg, end, num):
        """
        Set the value of the x array as an evenly spaced array
        over the specified interval

        :param beg: The start of the interval
        :param end: The end of the interval
        :param num: The number of points over the interval

        :param beg: real
        :param end: real
        :param num: int
        """
        self._x_arr = np.linspace(beg, end, num=num)
        self.del_x = self._x_arr[1] - self._x_arr[0]

    def set_y_arr(self, beg, end, num):
        """
        Set the value of the x array as an evenly spaced array
        over the specified interval

        :param beg: The start of the interval
        :param end: The end of the interval
        :param num: The number of points over the interval

        :param beg: real
        :param end: real
        :param num: int
        """
        self._y_arr = np.linspace(beg, end, num=num)
        self.del_y = self._y_arr[1] - self._y_arr[0]

    def set_y_col_notation(self, j, i, k):
        """
        Set the y array using matlab colon notation
        """
        step = int((k - j) / i)
        y_lst = [j + (mul) * i for mul in range(step + 1)]
        self._y_arr = np.array(y_lst)

    def set_x_col_notation(self, j, i, k):
        """
        Set the x array using matlab colon notation
        """
        step = int((k - j) / i)
        x_lst = [j + (mul) * i for mul in range(step + 1)]
        self._x_arr = np.array(x_lst)

    def get_x_arr(self):
        """
        getter for the x array
        :return: The x numpy.ndarray
        """
        return self._x_arr

    def get_y_arr(self):
        """
        getter for the y array
        :return: The y numpy.ndarray
        """
        return self._y_arr


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
PROMPT = ['maximum number of Gridpoints in one Dimension',
          '\\epsilon - Background', '\\mu - Background',
          'Size x-Dimension [\\mum]', 'Size y-Dimension [\\mum]',
          'Number of timesteps', 'Number of Perfectly Matched Layers',
          'axis equal']

# TODO: What do these mean?
DEFAULT_ANSWER = ['300', '1', '1', '5', '5', '300000', '10', '0']
# options...
ANSWER = [int(i) for i in DEFAULT_ANSWER]
AXISIMAGE = ANSWER[7]
PMLWIDTH = ANSWER[6]

PARAMS = Params()

# if ANSWER[4] > ANSWER[5]:
if ANSWER[5] > ANSWER[4]:
    # x=linspace(-str2num(ANSWER{4})/2,str2num(ANSWER{4})/2,str2num(ANSWER{1}))
    # y=[-str2num(ANSWER{5})/2-dx:dx:str2num(ANSWER{5})/2+dx]
    PARAMS.set_x_arr(-ANSWER[3] / 2, ANSWER[3] / 2, ANSWER[0])
    PARAMS.set_y_col_notation(-ANSWER[4] / 2 - PARAMS.del_x,
                              PARAMS.del_x,
                              ANSWER[4] / 2 + PARAMS.del_x)
    # x = np.linspace(-ANSWER[3] / 2, ANSWER[3] / 2, num=ANSWER[0])
    # dx = x[1] - x[0]

    # j = -ANSWER[4] / 2 - dx
    # i = dx
    # k = ANSWER[4] / 2 + dx
    # m = int((k - j) / i)
    # # Want the list j, j+i, j+2i, + ... + j+m*i
    # y_lst = [j + (mul) * dx for mul in range(m + 1)]
    # y = np.array(y_lst)
else:
    # y = np.linspace(-ANSWER[4] / 2, ANSWER[4] / 2, ANSWER[0])
    PARAMS.set_y_arr(-ANSWER[4] / 2, ANSWER[4] / 2, ANSWER[0])
    PARAMS.set_x_col_notation(ANSWER[3] / 2 - PARAMS.del_y,
                              PARAMS.del_y,
                              ANSWER[3] / 2 + PARAMS.del_y)
    # dx = y[1] - y[0]

    # j = -ANSWER[4] / 2 - dx
    # i = dx
    # k = ANSWER[4] / 2 + dx
    # m = int((k - j) / i)
    # # Want the list j, j+i, j+2i, + ... + j+m*i
    # x_lst = [j + (mul) * dx for mul in range(m + 1)]
    # x = np.array(x_lst)

# X, Y = np.meshgrid(PARAMS.get_x_arr(), PARAMS.get_y_arr())
PARAMS.set_grid()

BACKGROUNDEPS = constants.epsilon0 * ANSWER[1]
BACKGROUNDMU = constants.mu0 * ANSWER[2]
PARAMS.epsilon = BACKGROUNDEPS * np.ones(PARAMS.get_grid()[0].shape)
PARAMS.mu = BACKGROUNDMU * np.ones(PARAMS.get_grid()[0].shape)
PARAMS.z_s = ANSWER[5]

PARAMS.alphadat = np.ones(PARAMS.get_grid()[0].shape)
USERGENERALPARAMATERS = ANSWER
