#----------------------------------------------------------------------------
#Author : Roman Shchiptsov, email: schiptsov.roman@gmail.com
#File   : SplashScreen.py
#Revise : 16-07-2024
#----------------------------------------------------------------------------

from PyQt5 import QtWidgets, QtGui, QtCore
import time

class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self, parent=None):
        super().__init__(parent, flags=QtCore.Qt.WindowType.WindowStaysOnTopHint)

    def loadInitialization(self, parent: QtWidgets.QWidget, movie: QtGui.QMovie):
        movie.start()
        self.setPixmap(movie.currentPixmap())
        self.show()
        for i in range(500):
            time.sleep(0.01)
            self.setPixmap(movie.currentPixmap())
            QtWidgets.QApplication.instance().processEvents()

        self.finish(parent)

    def mousePressEvent(self, event):
        return