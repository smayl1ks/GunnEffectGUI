#----------------------------------------------------------------------------
#Author : Roman Shchiptsov, email: schiptsov.roman@gmail.com
#File   : run_gui.py
#Revise : 17-07-2024
#----------------------------------------------------------------------------
from PyQt5 import QtWidgets, QtGui
from app.settings import IMG_DICT
from app.gui.widgets import MainWindow, SplashScreen

import sys

def run_gui(U0, shr_j, shr_E, shr_ne, shr_p, shr_Gi,
                  sleep_time, should_terminate):
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(U0, shr_j, shr_E, shr_ne, shr_p, shr_Gi,
                  sleep_time, should_terminate)

    # Preparing the core for computation
    # User should not be using the GUI
    splashScreen = SplashScreen()
    splashScreen.loadInitialization(window, QtGui.QMovie(IMG_DICT["loading.gif"]))
    # Forced event handling
    QtWidgets.QApplication.instance().processEvents()

    window.show()
    sys.exit(app.exec_())