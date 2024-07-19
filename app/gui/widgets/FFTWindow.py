#----------------------------------------------------------------------------
#Author : Roman Shchiptsov, email: schiptsov.roman@gmail.com
#File   : FFTWindow.py
#Revise : 19-07-2024
#----------------------------------------------------------------------------

from PyQt5 import QtWidgets, QtCore
from app.core.fft import fftThread
from .DynamicPlot import DynamicPlot

class FFTWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.jt = []
        self.J = []
        self.f = []

        self.setWindowTitle("Преобразование Фурье")
        self.resize(540, 420)

        self.setLayoutManagement()
        self.createFigures()

        self.fftThread = fftThread(parent=self)
        self.fftThread.fJ.connect(self.update_fJ) # tuple(f, J)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot)

    def setLayoutManagement(self):
        self.main_box = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.main_box)

    def createFigures(self):
        self.fft_plot = DynamicPlot("f, МГц", "J")
        self.fft_plot.setXRange(0, 5000)
        self.plot_data_fft = self.fft_plot.getDataPlot()
        self.main_box.addWidget(self.fft_plot)

    @QtCore.pyqtSlot()
    def update_plot(self) -> None:
        self.fftThread.jarray[:] = self.jt
        self.fftThread.start()
        if len(self.J) != 0:
            self.plot_data_fft.setData(self.f, self.J)

    @QtCore.pyqtSlot(object, object)
    def update_fJ(self, f, J):
        self.f, self.J = f, J

    @QtCore.pyqtSlot(object)
    def update_jt(self, jt):
        self.jt[:] = jt

    def showEvent(self, event):
        self.timer.start()
        QtWidgets.QWidget.showEvent(self, event)

    def closeEvent(self, event):
        self.timer.stop()
        QtWidgets.QWidget.closeEvent(self, event)

