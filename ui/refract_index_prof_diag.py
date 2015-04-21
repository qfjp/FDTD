"""
Translation of definerefractiveindexprofile.m
"""
# pylint: disable=no-member

# import PyQt5.QtCore as qtcore
import PyQt5.QtWidgets as qtwidg


class Diag(qtwidg.QWidget):
    """
    The initial dialog window
    """
    def __init__(self, parent=None):
        super(Diag, self).__init__(parent)

        self.responses = {'eps': '2.25',
                          'mu': '1',
                          'soft': '0',
                          'struct': '1'}

        # Input boxes

        self.input_boxes = {'eps': qtwidg.QLineEdit(),
                            'mu': qtwidg.QLineEdit(),
                            'soft': qtwidg.QLineEdit(),
                            'struct': qtwidg.QLineEdit()}

        layout = qtwidg.QVBoxLayout()

        self.add_input('ε - Structure',
                       self.input_boxes['eps'],
                       default=self.responses['eps'], layout=layout)

        self.add_input('μ - Structure',
                       self.input_boxes['mu'],
                       default=self.responses['mu'], layout=layout)

        self.add_input('Softened Structures',
                       self.input_boxes['soft'],
                       default=self.responses['soft'], layout=layout)

        self.add_input('Structure (0 pc, 1 square, 2 circ, 3 poly)',
                       self.input_boxes['struct'],
                       default=self.responses['struct'], layout=layout)

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
        self.setWindowTitle('Refractive Index Profile Params')

    def submit_clicked(self):
        # TODO
        pass

    def cancel_clicked(self):
        """
        Cancel button hook
        """
        self.hide()

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
