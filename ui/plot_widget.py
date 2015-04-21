"""
The widget to interface with matplotlib (for charts n stuff)
"""
# pylint: disable=no-name-in-module, no-member
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QSizePolicy

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg \
     import FigureCanvasQTAgg as FigureCanvas

import numpy as np


class PlotWidget(FigureCanvas):
    """
    Plot widget for fdtd simulator
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

        super(PlotWidget, self).__init__(fig)
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
        self.axes.set_xlabel(r'$\mu$m')
        self.axes.set_ylabel(r'$\mu$m')

        # set the x & y ticks
        low_x = np.floor(self.extent[0])
        low_y = np.floor(self.extent[2])
        hih_x = np.ceil(self.extent[1])
        hih_y = np.ceil(self.extent[3])
        self.axes.set_xlim([low_x, hih_x])
        self.axes.set_ylim([low_y, hih_y])
        # low_x = self.extent[0]
        # hih_x = self.extent[1]
        # low_y = self.extent[2]
        # hih_y = self.extent[3]
        self.axes.set_xticks(np.arange(low_x, hih_x, (hih_x - low_x) / 10))
        self.axes.set_yticks(np.arange(low_y, hih_y, (hih_y - low_y) / 10))

        self.axes.set_title('Refractive Index')
        self.axes.grid()
        self.draw()
