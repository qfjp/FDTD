# pylint: disable=no-member
"""
.. module:: fdtd.define_general_parameters
   :platform: Unix, Windows
   :synopsis: An attempt to translate the god awful madness that is
              the matlab fdtd toolkit. This should be a direct
              translation of definegeneralparameters.m

.. moduleauthor:: Daniel Pade <djpade@gmail.com>
"""
import numpy as np
import phys_util.units as u
import phys_util.constants as constants

# NOTE: as a translation guide:
#       answer[1] -> self.answers['max_gp']
#       answer[2] -> self.answers['eps']
#       answer[3] -> self.answers['mu']
#       answer[4] -> self.answers['x_dim']
#       answer[5] -> self.answers['y_dim']
#       answer[6] -> self.answers['timestep']
#       answer[7] -> self.answers['layers']
#       answer[8] -> self.answers['axis']


class Params:
    """
    Reworking define_general_parameters as a class
    """
    def __init__(self, answers):
        self.answers = answers
        self._x_arr = None   # x
        self._y_arr = None   # y
        self.del_x = 0       # dx
        self.del_y = 0       # dy
        self._x_grid = None  # X
        self._y_grid = None  # Y
        self.ep_v = None
        self.mu_v = None
        self.z_s = None
        self.alphadat = None

        self.axisimage = self.answers['axis']
        self.pmlwidth = self.answers['layers']
        self.set_from_user_input()

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

        :type beg: float
        :type end: float
        :type num: int
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

        :type beg: float
        :type end: float
        :type num: int
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

    def set_from_user_input(self):
        """
        The meat of define_general_parameters
        """
        micrometer = 1e-6 * u.meter
        x_dim = self.answers['x_dim'] / micrometer
        y_dim = self.answers['y_dim'] / micrometer
        max_gp = self.answers['max_gp']
        # if ANSWER[4] > ANSWER[5]:
        if x_dim > y_dim:
            self.set_x_arr(-x_dim / 2, x_dim / 2,
                           max_gp)
            self.set_y_col_notation(-y_dim / 2 - self.del_x,
                                    self.del_x,
                                    y_dim / 2 + self.del_x)
        else:
            self.set_y_arr(-y_dim / 2, y_dim / 2,
                           max_gp)
            self.set_x_col_notation(-x_dim / 2 - self.del_y,
                                    self.del_y,
                                    x_dim / 2 + self.del_y)

        self.set_grid()

        background_eps = constants.epsilon0 * self.answers['eps']
        background_mu = constants.mu0 * self.answers['mu']
        self.ep_v = background_eps * np.ones(self.get_grid()[0].shape)
        self.mu_v = background_mu * np.ones(self.get_grid()[0].shape)
        self.z_s = self.answers['timestep']

        self.alphadat = np.ones(self.get_grid()[0].shape)
