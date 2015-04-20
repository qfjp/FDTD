"""
The plot widget
"""
# pylint: disable=no-name-in-module, no-member
import matplotlib
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QSizePolicy

from matplotlib.backends.backend_qt5agg \
     import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')


class MainWindow(FigureCanvas):
    """
    Main window for fdtd simulator
    :param array: The array to draw using imshow
    :param extent: The extents to use for drawing the plot
                   (left, right, bottom, top)

    :param parent: The parent widget
    :param width: The width of the chart
    :param height: the height of the chart
    :param dpi: the resolution of the chart
    :type array: numpy.ndarray
    :type extent: list
    """
    def __init__(self, **kwargs):
        # Default kwargs to use:
        array = None
        extent = None
        parent = None
        width = 5
        height = 4
        dpi = 100
        try:
            array = kwargs['array']
            extent = kwargs['extent']
            parent = kwargs['parent']
            width = kwargs['width']
            height = kwargs['height']
            dpi = kwargs['dpi']
        except KeyError:
            pass
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

        # self.x = np.arange(0, 4 * np.pi, 0.1)
        # self.y = np.sin(self.x)

        self.array = array
        self.extent = extent

    def update_figure(self):
        """
        Update the matplotlib plot
        """
        # self.axes.plot(self.x, self.y)
        # self.y = np.roll(self.y, -1)
        self.axes.imshow(self.array, extent=self.extent)
        self.draw()
