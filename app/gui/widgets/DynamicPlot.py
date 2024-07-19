#----------------------------------------------------------------------------
#Author : Roman Shchiptsov, email: schiptsov.roman@gmail.com
#File   : DynamicPlot.py
#Revise : 16-07-2024
#----------------------------------------------------------------------------

import pyqtgraph as pg

class DynamicPlot(pg.PlotWidget):
    """
    Widget for plotting Data
    """
    def __init__(self, xlabel = "x", ylabel = "y", parent=None):
        super().__init__(parent=parent)
        label_style = {'color': '#000000', 'font-size': '10pt'}

        self.setBackground("#f0f0f0")
        self.setLabel("bottom", xlabel, **label_style)
        self.setLabel("left", ylabel, **label_style)
        self.showGrid(x=True, y=True, alpha=1.0)


    def getDataPlot(self, pencolor="#000000"):
        """
        :param pencolor: color for pen
        :return: plot for updata data
        """

        self.pen = pg.mkPen(color=pencolor, width=2.8)
        return self.plot(x=[], y=[], pen=self.pen)