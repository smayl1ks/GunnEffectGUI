#----------------------------------------------------------------------------
#Author : Roman Shchiptsov, email: schiptsov.roman@gmail.com
#File   : SetOpticWindow.py
#Revise : 16-07-2024
#----------------------------------------------------------------------------

from PyQt5 import QtWidgets, QtCore, QtGui
from .DynamicPlot import DynamicPlot
from app.utils import read_data, create_Gi, validate_float
from app.settings import IMG_DICT, PROFILES_DICT

class SetOpticWindow(QtWidgets.QWidget):
    changeGi = QtCore.pyqtSignal(object)
    """
    Окно установки области оптического воздействия
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Оптическое воздействие")
        self.resize(1290, 440)

        self.createFigures()
        self.createGroupBoxOptic()
        self.setLayoutManagement()

        self.Gi = []
        self.x = read_data(nameFile=PROFILES_DICT["x.csv"], columns=1)
        self.message_error = QtWidgets.QMessageBox()

    def createFigures(self):
        self.graph_optic = DynamicPlot(xlabel="x, мкм",
                                       ylabel="G(x), см<sup>-3</sup>с<sup>-1</sup>",
                                       parent=self)
        self.plot_data_optic = self.graph_optic.getDataPlot()

    def createGroupBoxOptic(self):
        self.box_optic = QtWidgets.QGroupBox()
        self.box_optic.setTitle("Оптическое воздействие")

        self.gmax_optic = QtWidgets.QLineEdit("1E20")
        self.x0_optic = QtWidgets.QLineEdit("250")
        self.d_optic = QtWidgets.QLineEdit("90")

        self.is_updating = False  # функция updateOpticRegion вызывается несколько раз,
        # так как она подключена к сигналу editingFinished для каждого из трех полей ввода
        self.gmax_optic.editingFinished.connect(self.updateOpticRegion)
        self.x0_optic.editingFinished.connect(self.updateOpticRegion)
        self.d_optic.editingFinished.connect(self.updateOpticRegion)

        self.equationImg = QtWidgets.QLabel()
        self.equationImg.setPixmap(QtGui.QPixmap(IMG_DICT["optic_influence.jpg"]))

        form = QtWidgets.QFormLayout()
        form.addRow("G(x)max, см<sup>-3</sup>с<sup>-1</sup>, ", self.gmax_optic)
        form.addRow("x0, мкм:", self.x0_optic)
        form.addRow("d, мкм:", self.d_optic)

        self.grbox_optic = QtWidgets.QVBoxLayout(self.box_optic)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addLayout(form)
        hbox.addStretch(1)
        self.grbox_optic.addLayout(hbox)
        self.grbox_optic.addWidget(self.equationImg)
        self.grbox_optic.addStretch(1)

    def setLayoutManagement(self):
        self.main_box = QtWidgets.QHBoxLayout(self)
        self.main_box.addWidget(self.box_optic, stretch=1)
        self.main_box.addWidget(self.graph_optic, stretch=2)

    @QtCore.pyqtSlot()
    def updateOpticRegion(self):

        if self.is_updating:
            return
        self.is_updating = True

        try:
            x0 = validate_float(self.x0_optic.text(), 1E-6)
            d = validate_float(self.d_optic.text(), 1E-6)
            Gmax = validate_float(self.gmax_optic.text(), 1E-4)
        except ValueError as e:
            self.message_error.critical(self, "ERROR!", str(e))
            x0 = 0; d = 1; Gmax = 0

        try:
            self.dataIsCorrect(x0, d, Gmax)
        except ValueError:
            x0 = 0; d = 1; Gmax = 0

        self.Gi = create_Gi(x0, d, Gmax, self.x)
        self.plot_data_optic.setData(self.x * 1E6, self.Gi * 1E4)
        self.graph_optic.setYRange(0, Gmax * 1E4)
        self.changeGi.emit(self.Gi)

        self.is_updating = False

    def dataIsCorrect(self, x0, d, Gmax):
        if not (self.x[-1] >= x0 >= 0):
            self.message_error.critical(self, "ERROR!", f"Ошибка ввода\n"
                                                        f"x0 должен быть в диапазоне\n"
                                                        f"[0:{self.x[-1] * 1E6}]")
            raise ValueError

        if not (self.x[-1] >= d >= 0):
            self.message_error.critical(self, "ERROR!", f"Ошибка ввода\n"
                                                        f"d должен быть в диапазоне\n"
                                                        f"[0:{self.x[-1] * 1E6}]")
            raise ValueError

        if not (Gmax >= 0):
            self.message_error.critical(self, "ERROR!", f"Ошибка ввода\n"
                                                        f"Gmax должен быть положительным")
            raise ValueError