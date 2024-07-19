from PyQt5 import QtCore
from app.settings import WRITE_FREQUENCY
from app.core.algorithm import t
from numpy import fft, linspace, sort, copy

class fftThread(QtCore.QThread):
    fJ = QtCore.pyqtSignal(object, object)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.jarray = []

    def FFT(self):
        if len(self.jarray) != 0:
            self.fy = abs(fft.rfft(self.jarray) / (len(self.jarray) / 2))
            self.fn = 1 / (2 * t * WRITE_FREQUENCY)
            self.fx = list(linspace(0, self.fn * 1E-6, len(self.fy)))

            self.fy[0] = self.fy[0] / 2
            self.fJ.emit(self.fx, self.fy)

    def run(self):
        self.FFT()