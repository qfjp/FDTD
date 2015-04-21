"""
The plot widget
"""
# pylint: disable=no-name-in-module, no-member
import matplotlib

import PyQt5.QtWidgets as qtwidg
import PyQt5.QtCore as qtcore

import numpy as np

from ui.plot_widget import PlotWidget

matplotlib.use('Qt5Agg')


class MainButtons(qtwidg.QWidget):
    """
    The buttons on the main window
    """
    def __init__(self, parent=None):
        super(MainButtons, self).__init__(parent)

        layout = qtwidg.QGridLayout()
        self.define_ref_button = \
            qtwidg.QPushButton('Define Refractive-Index Profile')
        self.change_ref_button = \
            qtwidg.QPushButton('Change Refractive-Index Profile')
        self.new_source_button = \
            qtwidg.QPushButton('New Source-Structure')
        self.change_src_button = \
            qtwidg.QPushButton('Change Source-Structure')
        self.start_sim_button = \
            qtwidg.QPushButton('Start Simulation')
        self.change_geom_button = \
            qtwidg.QPushButton('Change Basic Geometry Details')

        layout.addWidget(self.define_ref_button, 0, 0)
        layout.addWidget(self.change_ref_button, 0, 1)
        layout.addWidget(self.new_source_button, 0, 2)
        layout.addWidget(self.change_src_button, 1, 0)
        layout.addWidget(self.start_sim_button, 1, 1)
        layout.addWidget(self.change_geom_button, 1, 2)

        self.setLayout(layout)


class ApplicationWindow(qtwidg.QMainWindow):
    """
    The window where the magic happens
    """
    def __init__(self, array=None, extent=None):
        qtwidg.QMainWindow.__init__(self)
        self.setAttribute(qtcore.Qt.WA_DeleteOnClose)
        self.setWindowTitle('Application Main Window')

        self.file_menu = qtwidg.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 qtcore.Qt.CTRL + qtcore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = qtwidg.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = qtwidg.QWidget(self)

        plot_win = PlotWidget(array=array, extent=extent, parent=self)
        layout = qtwidg.QVBoxLayout(self.main_widget)
        layout.addWidget(plot_win)

        layout.addWidget(MainButtons())

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage('Status Message', 20000)

    # pylint: disable=invalid-name
    def fileQuit(self):
        """
        Quit the program
        """
        self.close()

    # pylint: disable=unused-argument
    def closeEvent(self, ce):
        """
        Quit the program
        """
        self.fileQuit()
    # pylint: enable=unused-argument

    def about(self):
        """
        Bring up the about window
        """
        qtwidg.QMessageBox.about(self, 'About', 'Unfinished')
    # pylint: enable=invalid-name

if __name__ == '__main__':
    import sys
    APP = qtwidg.QApplication(sys.argv)
    ARRAY = np.ones((300, 300))
    EXTENT = [-2.5167224080267561, 2.5000000000000631, -2.5167224080267561,
              2.5000000000000631]
    AW = ApplicationWindow(array=ARRAY, extent=EXTENT)
    AW.show()
    APP.exec_()
