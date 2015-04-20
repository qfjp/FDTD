"""
.. module:: ui.init_param_diag
   :platform: Unix, Windows
   :synopsis: A copy of the first dialog to define the initial paramaters
              Hooks into fdtd.define_general_parameters
.. moduleauthor:: Daniel Pade <djpade@gmail.com>
"""
# pylint: disable=no-member

# import PyQt5.QtCore as qtcore
import PyQt5.QtWidgets as qtwidg

import phys_util.units as u

import fdtd.define_general_parameters as dgp

import sys


class Diag(qtwidg.QWidget):
    """
    The initial dialog window
    """

    @staticmethod
    def add_input(label, text_box, default=None, layout=None):
        """
        Add an input box

        :param label: The label to use for the input box
        :type label: string
        """
        label_widg = qtwidg.QLabel(label)
        text_box.insert(default)
        layout.addWidget(label_widg)
        layout.addWidget(text_box)

    def __init__(self, parent=None):
        super(Diag, self).__init__(parent)

        self.responses = {'max_gp': '300',
                          'eps': '1',
                          'mu': '1',
                          'x_dim': '5 micrometer',
                          'y_dim': '5 micrometer',
                          'timestep': '300000',
                          'layers': '10',
                          'axis': '0'}

        # Input boxes

        self.input_boxes = {'max_gp': qtwidg.QLineEdit(),
                            'eps': qtwidg.QLineEdit(),
                            'mu': qtwidg.QLineEdit(),
                            'x_dim': qtwidg.QLineEdit(),
                            'y_dim': qtwidg.QLineEdit(),
                            'timestep': qtwidg.QLineEdit(),
                            'layers': qtwidg.QLineEdit(),
                            'axis': qtwidg.QLineEdit()}

        layout = qtwidg.QVBoxLayout()

        self.add_input('Max # of Gridpoints in 1D',
                       self.input_boxes['max_gp'],
                       default=self.responses['max_gp'], layout=layout)

        self.add_input('ε - Background (unitless):', self.input_boxes['eps'],
                       default=self.responses['eps'], layout=layout)

        self.add_input('μ - Background (unitless):', self.input_boxes['mu'],
                       default=self.responses['mu'], layout=layout)

        self.add_input('Size x-Dim [Default = μm]:', self.input_boxes['x_dim'],
                       default=self.responses['x_dim'], layout=layout)

        self.add_input('Size y-Dim [Default = μm]:', self.input_boxes['y_dim'],
                       default=self.responses['y_dim'], layout=layout)

        self.add_input('# of timesteps:', self.input_boxes['timestep'],
                       default=self.responses['timestep'], layout=layout)

        self.add_input('# of perfectly matched layers:',
                       self.input_boxes['layers'],
                       default=self.responses['layers'], layout=layout)

        # axis_label = qtwidg.QLabel('axis equal:')
        self.add_input('axis equal:', self.input_boxes['axis'],
                       default=self.responses['axis'], layout=layout)

        # Buttons
        self.submit_button = qtwidg.QPushButton('OK')
        self.cancel_button = qtwidg.QPushButton('Cancel')
        self.submit_button.clicked.connect(self.submit_clicked)
        self.cancel_button.clicked.connect(self.cancel_clicked)

        # Layouts
        self.button_layout = qtwidg.QGridLayout()
        self.button_layout.addWidget(self.submit_button, 0, 0)
        self.button_layout.addWidget(self.cancel_button, 0, 1)

        main_lay = qtwidg.QGridLayout()
        main_lay.addLayout(layout, 0, 1)
        main_lay.addLayout(self.button_layout, 1, 1)

        self.setLayout(main_lay)
        self.setWindowTitle('Define Initial Parameters')

    def _validate_input(self, param, func, message):
        """
        Try func(param) to see if there will be a ValueError.
        If not, return the result. Otherwise, show a MessageBox with
        the message
        """
        try:
            output = func(param)
        except ValueError:
            qtwidg.QMessageBox.information(self, 'Invalid Field', message)
            return False
        return output

    def _parse_results(self):
        """
        Used to convert the strings in the text boxes to the
        appropriate format
        :return: True if everything could be parsed, false if any field
                 was invalid
        """
        max_gp = self._validate_input(self.input_boxes['max_gp'].text(),
                                      int,
                                      'Gridpoints must be an integer')
        ep_v = self._validate_input(self.input_boxes['eps'].text(), float,
                                    'ε must be a real number')

        mu_v = self._validate_input(self.input_boxes['mu'].text(), float,
                                    'μ must be a real number')
        timestep = self._validate_input(self.input_boxes['timestep'].text(),
                                        int,
                                        'Timestep must be an integer')
        layers = self._validate_input(self.input_boxes['layers'].text(), int,
                                      'Number of layers must be an integer')
        axis = self._validate_input(self.input_boxes['axis'].text(), int,
                                    'Axis val must be an integer')

        res_list = [max_gp, ep_v, mu_v, timestep, layers, axis]
        for item in res_list:
            if isinstance(item, bool) and item is False:
                return

        x_dim = u.parse_dimensions(self.input_boxes['x_dim'].text())
        y_dim = u.parse_dimensions(self.input_boxes['y_dim'].text())

        if x_dim is None:
            qtwidg.QMessageBox.information(self, 'Invalid Field',
                                           'Invalid units in x dimension')
            return
        if y_dim is None:
            qtwidg.QMessageBox.information(self, 'Invalid Field',
                                           'Invalid units in y dimension')
            return
        self.responses = {'max_gp': max_gp,
                          'eps': ep_v,
                          'mu': mu_v,
                          'x_dim': x_dim,
                          'y_dim': y_dim,
                          'timestep': timestep,
                          'layers': layers,
                          'axis': axis}
        return True

    def submit_clicked(self):
        """
        OK button hook
        """
        if self._parse_results():
            for key in self.responses:
                print('{} : {}'.format(key, self.responses[key]))
            self.destroy()
            sys.exit(0)

    @staticmethod
    def cancel_clicked():
        """
        Cancel button hook
        """
        sys.exit(0)

if __name__ == '__main__':
    import sys

    APP = qtwidg.QApplication(sys.argv)

    SCREEN = Diag()
    SCREEN.show()

    sys.exit(APP.exec_())
