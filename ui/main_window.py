import matplotlib
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, \
                            QSizePolicy, QMessageBox, QWidget

import numpy as np
from matplotlib.backends.backend_qt5agg \
     import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')


class MainWindow(FigureCanvas):
    """
    Main window for fdtd simulator
    """
    def __init__(self, array=None, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # Clear the axes every time plot() is called
        self.axes.hold(False)

        super(MainWindow, self).__init__(fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        timer = QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(50)

        self.x = np.arange(0, 4 * np.pi, 0.1)
        self.y = np.sin(self.x)

        self.array = array

    def update_figure(self):
        # self.axes.plot(self.x, self.y)
        # self.y = np.roll(self.y, -1)
        self.axes.imshow(self.array)
        self.draw()
