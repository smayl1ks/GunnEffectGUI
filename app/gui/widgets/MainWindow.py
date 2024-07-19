#----------------------------------------------------------------------------
#Author : Roman Shchiptsov, email: schiptsov.roman@gmail.com
#File   : MainWindow.py
#Revise : 16-07-2024
#----------------------------------------------------------------------------

from PyQt5 import QtWidgets, QtCore

from .FFTWindow import FFTWindow
from .SetOpticWindow import SetOpticWindow

from .DynamicPlot import DynamicPlot
from .Slider import Slider
from .LinearRegion import LinearRegion

from app.utils import validate_float

import time

class MainWindow(QtWidgets.QWidget):
    changeFFTData = QtCore.pyqtSignal(object)
    def __init__(self, U0, shr_j, shr_E, shr_ne, shr_p, shr_Gi,
                 sleep_time, should_terminate):
        super().__init__()

        self.U = U0
        self.jt = shr_j

        # Максимальная длина массива
        self.jt_lenght = len(self.jt)
        self.jt_slice = 0

        self.E = shr_E
        self.ne = shr_ne
        self.p = shr_p
        self.Gi = shr_Gi

        self.sleep_time = sleep_time
        self.should_terminate = should_terminate
        self.fft_on = False

        self.resize(1290, 820)
        self.setWindowTitle("GunnEffectGUI")

        self.setLayoutManagement()
        self.createFigures()
        self.createGroupBoxSetting()
        self.createFiguresBox()

        self.timer_update = QtCore.QTimer()
        self.timer_update.setInterval(30)
        self.timer_update.timeout.connect(self.updatePlotData)

        self.optic_window = SetOpticWindow()
        self.optic_window.changeGi.connect(self.updateGi)

        self.fft_window = FFTWindow()
        self.changeFFTData.connect(self.fft_window.update_jt)

        self.LinearRegion = LinearRegion((self.jt_slice, self.jt_lenght))
        self.message_error = QtWidgets.QMessageBox()

    def setLayoutManagement(self):
        main_box = QtWidgets.QVBoxLayout(self)

        self.grid_plots_box = QtWidgets.QGridLayout()

        main_box.addLayout(self.grid_plots_box)

    def createFigures(self):
        self.graph_electrons = DynamicPlot(xlabel="x, мкм",
                                           ylabel="n(x,t), см<sup>-3</sup>",
                                           parent=self)

        self.graph_electrons.setYRange(0, 2E15)
        self.plot_data_electrons = self.graph_electrons.getDataPlot()

        self.graph_holes = DynamicPlot(xlabel="x, мкм",
                                       ylabel="p(x,t), см<sup>-3</sup>",
                                       parent=self)
        self.plot_data_holes = self.graph_holes.getDataPlot()

        self.graph_E = DynamicPlot(xlabel="x, мкм",
                                       ylabel="E(x,t), см<sup>-3</sup>с<sup>-1</sup>",
                                       parent=self)
        self.graph_E.setYRange(0, 80)
        self.plot_data_E = self.graph_E.getDataPlot()

        self.graph_jt = DynamicPlot(xlabel="t",
                                    ylabel="j(t)",
                                    parent=self)
        self.plot_data_jt = self.graph_jt.getDataPlot()

    def createGroupBoxSetting(self):
        self.form_setting = QtWidgets.QFormLayout()

        # ---------------
        # Напряжение
        # ---------------
        self.edit_U = QtWidgets.QLineEdit("250")
        self.edit_U.editingFinished.connect(self.updateParameters)

        self.form_setting.addRow("Напряжение U(В):", self.edit_U)

        # ---------------
        # Оптическое воздействие
        # ---------------
        self.box_optic = QtWidgets.QGroupBox()
        self.box_optic.setTitle("Оптическое воздействие")

        hbox_optic = QtWidgets.QHBoxLayout(self.box_optic)
        self.btn_on_optic = QtWidgets.QRadioButton("ВКЛ/ВЫКЛ")
        self.btn_on_optic.toggled.connect(self.lightOn)
        self.btn_optic_setting = QtWidgets.QPushButton("Настройки")
        self.btn_optic_setting.setDisabled(True)
        self.btn_optic_setting.clicked.connect(self.light_setting)

        hbox_optic.addWidget(self.btn_on_optic)
        hbox_optic.addWidget(self.btn_optic_setting)

        # ---------------
        # Преобразование Фурье
        # ---------------
        self.box_fft = QtWidgets.QGroupBox()
        self.box_fft.setTitle("Преобразование Фурье")

        hbox_fft = QtWidgets.QHBoxLayout(self.box_fft)
        self.btn_fft_choice = QtWidgets.QRadioButton("Режим выделения области")
        self.btn_fft_choice.toggled.connect(self.fft_choice)
        self.btn_fft_run = QtWidgets.QPushButton("Запуск")
        #self.btn_fft_run.setDisabled(True)
        self.btn_fft_run.clicked.connect(self.fft_run)

        hbox_fft.addWidget(self.btn_fft_choice)
        hbox_fft.addWidget(self.btn_fft_run)

        # ---------------
        # Sliders
        # ---------------
        form_sliders = QtWidgets.QFormLayout()
        self.slider_sleep = Slider()
        self.slider_sleep.setValue(0)
        self.slider_sleep.valueChanged.connect(self.update_time_sleep)

        self.slider_sleep_value = QtWidgets.QLabel(f'ЗАДЕРЖКА: {0} %')

        form_sliders.addRow(self.slider_sleep_value)
        form_sliders.addRow(self.slider_sleep)

        self.slider_lenght_jt = Slider()
        self.slider_lenght_jt.setRange(0, self.jt_lenght)
        self.slider_lenght_jt.setValue(self.jt_lenght)
        self.slider_lenght_jt.valueChanged.connect(self.update_lenght_jt)

        self.slider_lenght_value = QtWidgets.QLabel(f'Длина массива jt: {self.jt_lenght}')

        form_sliders.addRow(self.slider_lenght_value)
        form_sliders.addRow(self.slider_lenght_jt)

        # ---------------
        # START STOP RESET
        # ---------------
        hbox_start_stop = QtWidgets.QHBoxLayout()
        self.btn_start = QtWidgets.QPushButton("START")
        self.btn_start.clicked.connect(self.start)

        self.btn_stop = QtWidgets.QPushButton("STOP")
        self.btn_stop.setDisabled(True)
        self.btn_stop.clicked.connect(self.stop)

        self.btn_reset = QtWidgets.QPushButton("RESET")
        self.btn_reset.setDisabled(True)

        hbox_start_stop.addWidget(self.btn_start)
        hbox_start_stop.addWidget(self.btn_stop)
        hbox_start_stop.addWidget(self.btn_reset)
        # ---------------
        self.setting_container = QtWidgets.QVBoxLayout()

        self.setting_container.addLayout(self.form_setting)
        self.setting_container.addWidget(self.box_optic)
        self.setting_container.addWidget(self.box_fft)

        self.setting_container.addLayout(form_sliders)

        self.setting_container.addLayout(hbox_start_stop)
        self.setting_container.addStretch(1)

        self.setting_box = QtWidgets.QGroupBox()
        self.setting_box.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                       QtWidgets.QSizePolicy.Preferred)
        self.setting_box.setLayout(self.setting_container)
        self.setting_box.setContentsMargins(5, 5, 30, 5)

    def createFiguresBox(self):
        self.grid_plots_box.addWidget(self.setting_box, 0, 0)
        self.grid_plots_box.addWidget(self.graph_electrons, 0, 1)
        self.grid_plots_box.addWidget(self.graph_holes, 0, 2)
        self.grid_plots_box.addWidget(self.graph_jt, 1, 0, 1, 2)
        self.grid_plots_box.addWidget(self.graph_E, 1, 2)

    @QtCore.pyqtSlot()
    def updatePlotData(self):
        if self.fft_on:
            self.changeFFTData.emit(self.jt[self.jt_slice:])

        self.plot_data_E.setData(self.optic_window.x*1E6, self.E[:])
        self.plot_data_electrons.setData(self.optic_window.x*1E6, self.ne[:])
        self.plot_data_holes.setData(self.optic_window.x*1E6, self.p[:])
        self.plot_data_jt.setData(range(self.jt_lenght - self.jt_slice), self.jt[self.jt_slice:])


    @QtCore.pyqtSlot()
    def updateParameters(self):
        try:
            self.U.value = validate_float(self.edit_U.text(), 1)
        except ValueError as e:
            self.edit_U.setText(str(self.U.value))
            self.message_error.critical(self, "ERROR!", str(e))

    @QtCore.pyqtSlot()
    def start(self):
        self.sleep_time.value = 0
        self.btn_start.setDisabled(True)
        self.btn_start.setText("RUN")
        self.btn_stop.setDisabled(False)
        #self.btn_reset.setDisabled(False)
        self.slider_sleep.setValue(0)
        self.timer_update.start()

    @QtCore.pyqtSlot()
    def stop(self):
        self.sleep_time.value = 100 # 100 % задержка
        self.slider_sleep.setValue(self.sleep_time.value)
        self.btn_stop.setDisabled(True)
        self.btn_start.setDisabled(False)
        self.timer_update.stop()

    @QtCore.pyqtSlot()
    def reset(self):
        pass

    @QtCore.pyqtSlot()
    def lightOn(self):
        if self.btn_on_optic.isChecked():
            self.btn_optic_setting.setDisabled(False)
            self.optic_window.updateOpticRegion()
        else:
            self.btn_optic_setting.setDisabled(True)
            self.Gi[:] = [0] * len(self.Gi[:])

    @QtCore.pyqtSlot()
    def light_setting(self):
        self.optic_window.show()

    @QtCore.pyqtSlot(object)
    def updateGi(self, Gi):
        self.Gi[:] = Gi

    @QtCore.pyqtSlot(int)
    def update_time_sleep(self, value):
        self.slider_sleep_value.setText(f'ЗАДЕРЖКА: {value} %')
        self.sleep_time.value = value

    @QtCore.pyqtSlot(int)
    def update_lenght_jt(self, slc):
        self.jt_slice = self.jt_lenght - slc
        self.slider_lenght_value.setText(f'Длина массива jt: {slc}')
        self.updatePlotData()

    @QtCore.pyqtSlot()
    def fft_choice(self):
        x0 = (self.jt_lenght - self.jt_slice) // 4
        x1 = x0 + (self.jt_lenght - self.jt_slice) // 2

        self.LinearRegion.setRegion((x0, x1))
        if not self.btn_fft_choice.isChecked():
            self.graph_jt.removeItem(self.LinearRegion)
        else:
            self.graph_jt.addItem(self.LinearRegion)

    @QtCore.pyqtSlot()
    def fft_run(self):
        self.fft_on = True
        self.fft_window.show()
    # Закрытие основного окна
    def closeEvent(self, event):
        self.should_terminate.value = True
        self.sleep_time.value = 0

        self.optic_window.close()
        self.fft_window.close()
        self.hide()
        # Ждем завершения процесса core
        time.sleep(0.5)
        event.accept()