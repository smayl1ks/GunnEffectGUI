#----------------------------------------------------------------------------
#Author : Roman Shchiptsov, email: schiptsov.roman@gmail.com
#File   : figures.py
#Revise : 18-07-2024
#----------------------------------------------------------------------------

import pyqtgraph as pg

class LinearRegion(pg.LinearRegionItem):
    def __init__(self, values=(0, 1)):
        super().__init__(values=values)
        self.setMovable(True)

