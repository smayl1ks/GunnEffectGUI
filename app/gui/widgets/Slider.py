#----------------------------------------------------------------------------
#Author : Roman Shchiptsov, email: schiptsov.roman@gmail.com
#File   : Slider.py
#Revise : 16-07-2024
#----------------------------------------------------------------------------

from PyQt5 import QtWidgets, QtCore

class Slider(QtWidgets.QSlider):
    def __init__(self, orient=QtCore.Qt.Orientation.Horizontal):
        super().__init__(orientation=orient)
        self.setRange(0, 100)
        self.setSingleStep(5)
        self.setPageStep(5)

        styleSheetSlider = """
            QSlider:horizontal {
                min-height: 30px;
            }
            QSlider::groove:horizontal {
                height: 3px;
                background: black; 
            }
            QSlider::handle:horizontal {
                width: 20px;
                margin-top: -10px;
                margin-bottom: -10px;
                border-radius: 14px;
                background: black;
            }
        """
        self.setStyleSheet(styleSheetSlider)