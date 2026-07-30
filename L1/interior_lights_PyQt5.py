from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal

import time
import threading

interiorLed = False
progress_bar_value = 0

KL_list = ['no_KL', 'KL_s', 'KL_15', 'KL_50', 'KL_75']
KL_position = 0

brightness_left_door = 0
brightness_right_door = 0

flag_left_door = 0
flag_right_door = 0

warning = False

leftWarningVar = False
rightWarningVar = False

carL = False


############################### EXERCISE 2 ################################
class MyThread_sweep(QThread):
    sweepLedsSignal = pyqtSignal(int)

    def run(self):
        for i in range(4):
            self.sweepLedsSignal.emit(i)
            time.sleep(0.3)


############################### EXERCISE 5 #################################
class MyThread_warning(QThread):
    warningLightsSignal = pyqtSignal(int)

    def run(self):
        state = 0
        while warning:
            self.warningLightsSignal.emit(state)
            state = 1 - state
            time.sleep(0.5)


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(900, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        MainWindow.setCentralWidget(self.centralwidget)

        # Set background application color
        self.centralwidget.setStyleSheet("background-color: white;")

        # Continental image
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(5, 350, 350, 120))
        pixmap = QPixmap("conti.png")
        pixmap = pixmap.scaled(350, 120, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)

        # Car image
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(300, 170, 331, 161))
        pixmap1 = QPixmap("car.jpg")
        pixmap1 = pixmap1.scaled(331, 161, QtCore.Qt.KeepAspectRatio)
        self.label_1.setPixmap(pixmap1)

        # Left door button
        self.left_door = QtWidgets.QPushButton(MainWindow)
        self.left_door.setText("Left Door")
        self.left_door.setStyleSheet("font: bold;")
        self.left_door.setGeometry(QtCore.QRect(380, 50, 211, 41))
        self.left_door.clicked.connect(self.fade_door_left)

        # Left door slider
        self.left_door_slider = QtWidgets.QSlider(self.centralwidget)
        self.left_door_slider.setGeometry(QtCore.QRect(410, 100, 160, 26))
        self.left_door_slider.setOrientation(QtCore.Qt.Horizontal)
        self.left_door_slider.setRange(0, 100)
        self.left_door_slider.setValue(0)
        self.left_door_slider.valueChanged.connect(self.valuechange_left_slider)

        # Left door spinbox
        self.spinBox_left = QtWidgets.QSpinBox(MainWindow)
        self.spinBox_left.setGeometry(QtCore.QRect(300, 50, 75, 41))
        self.spinBox_left.setKeyboardTracking(False)
        self.spinBox_left.setRange(0, 100)
        self.spinBox_left.valueChanged.connect(self.valuechange)

        # Right door
        self.right_door = QtWidgets.QPushButton(MainWindow)
        self.right_door.setText("Right door")
        self.right_door.setStyleSheet("font: bold;")
        self.right_door.setGeometry(QtCore.QRect(380, 400, 211, 41))
        self.right_door.clicked.connect(self.fade_door_right)

        # Right door slider
        self.right_door_slider = QtWidgets.QSlider(self.centralwidget)
        self.right_door_slider.setGeometry(QtCore.QRect(410, 360, 160, 26))
        self.right_door_slider.setOrientation(QtCore.Qt.Horizontal)
        self.right_door_slider.setRange(0, 100)
        self.right_door_slider.setValue(0)
        self.right_door_slider.valueChanged.connect(self.valuechange_right_slider)

        # Right door spinbox
        self.spinBox_right = QtWidgets.QSpinBox(MainWindow)
        self.spinBox_right.setGeometry(QtCore.QRect(300, 400, 75, 41))
        self.spinBox_right.setKeyboardTracking(False)
        self.spinBox_right.setRange(0, 100)
        self.spinBox_right.valueChanged.connect(self.valuechange)

        # Current kl label
        self.current_kl_label = QtWidgets.QLabel(self.centralwidget)
        self.current_kl_label.setGeometry(QtCore.QRect(680, 80, 151, 31))
        self.current_kl_label.setStyleSheet("font: bold;")
        self.current_kl_label.setText("Current KL: no_KL")

        # Previous kl button
        self.prev_kl = QtWidgets.QPushButton(MainWindow)
        self.prev_kl.setText("Previous KL")
        self.prev_kl.setStyleSheet("font: bold;")
        self.prev_kl.setGeometry(QtCore.QRect(670, 40, 101, 31))
        self.prev_kl.clicked.connect(self.prev_kl_function)
        self.prev_kl.setEnabled(False)

        # Prev kl label
        self.prev_kl_label = QtWidgets.QLabel(self.centralwidget)
        self.prev_kl_label.setGeometry(QtCore.QRect(780, 40, 92, 31))
        self.prev_kl_label.setStyleSheet("font: bold;")

        # Next kl button
        self.next_kl = QtWidgets.QPushButton(MainWindow)
        self.next_kl.setText("Next KL")
        self.next_kl.setStyleSheet("font: bold;")
        self.next_kl.setGeometry(QtCore.QRect(670, 120, 101, 31))
        self.next_kl.clicked.connect(self.next_kl_function)

        # Next kl label
        self.next_kl_label = QtWidgets.QLabel(self.centralwidget)
        self.next_kl_label.setGeometry(QtCore.QRect(780, 120, 81, 31))
        self.next_kl_label.setStyleSheet("font: bold;")
        self.next_kl_label.setText("KL_s")

        # warning Lights Button
        self.warning = QtWidgets.QPushButton(MainWindow)
        self.warning.setText("Warning Lights")
        self.warning.setStyleSheet("font: bold;")
        self.warning.setGeometry(QtCore.QRect(650, 370, 160, 60))
        self.warning.clicked.connect(self.warningLightsButton)

        # Warning Lights
        self.warningLight1 = QtWidgets.QLabel(self.centralwidget)
        self.warningLight1.setGeometry(QtCore.QRect(260, 190, 20, 20))

        self.warningLight2 = QtWidgets.QLabel(self.centralwidget)
        self.warningLight2.setGeometry(QtCore.QRect(260, 293, 20, 20))

        self.warningLight3 = QtWidgets.QLabel(self.centralwidget)
        self.warningLight3.setGeometry(QtCore.QRect(650, 190, 20, 20))

        self.warningLight4 = QtWidgets.QLabel(self.centralwidget)
        self.warningLight4.setGeometry(QtCore.QRect(650, 293, 20, 20))

        # 4 leds for sweep
        self.led1_sweep = QtWidgets.QLabel(self.centralwidget)
        self.led1_sweep.setGeometry(QtCore.QRect(220, 210, 20, 20))
        self.led1_sweep_label = QtWidgets.QLabel(self.centralwidget)
        self.led1_sweep_label.setGeometry(QtCore.QRect(225, 230, 20, 20))
        self.led1_sweep_label.setStyleSheet("font: bold;")
        self.led1_sweep_label.setText("0")

        self.led2_sweep = QtWidgets.QLabel(self.centralwidget)
        self.led2_sweep.setGeometry(QtCore.QRect(240, 210, 20, 20))
        self.led2_sweep_label = QtWidgets.QLabel(self.centralwidget)
        self.led2_sweep_label.setGeometry(QtCore.QRect(245, 230, 20, 20))
        self.led2_sweep_label.setStyleSheet("font: bold;")
        self.led2_sweep_label.setText("1")

        self.led3_sweep = QtWidgets.QLabel(self.centralwidget)
        self.led3_sweep.setGeometry(QtCore.QRect(260, 210, 20, 20))
        self.led3_sweep_label = QtWidgets.QLabel(self.centralwidget)
        self.led3_sweep_label.setGeometry(QtCore.QRect(265, 230, 20, 20))
        self.led3_sweep_label.setStyleSheet("font: bold;")
        self.led3_sweep_label.setText("2")

        self.led4_sweep = QtWidgets.QLabel(self.centralwidget)
        self.led4_sweep.setGeometry(QtCore.QRect(280, 210, 20, 20))
        self.led4_sweep_label = QtWidgets.QLabel(self.centralwidget)
        self.led4_sweep_label.setGeometry(QtCore.QRect(283, 230, 20, 20))
        self.led4_sweep_label.setStyleSheet("font: bold;")
        self.led4_sweep_label.setText("3")

        # KL_s led
        self.KL_S = QtWidgets.QLabel(self.centralwidget)
        self.KL_S.setGeometry(QtCore.QRect(700, 175, 20, 20))
        self.KL_S_label = QtWidgets.QLabel(self.centralwidget)
        self.KL_S_label.setGeometry(QtCore.QRect(730, 175, 50, 20))
        self.KL_S_label.setStyleSheet("font: bold;")
        self.KL_S_label.setText("KL_s")

        # KL_15 label
        self.KL_15 = QtWidgets.QLabel(self.centralwidget)
        self.KL_15.setGeometry(QtCore.QRect(700, 200, 20, 20))
        self.KL_15_label = QtWidgets.QLabel(self.centralwidget)
        self.KL_15_label.setGeometry(QtCore.QRect(730, 200, 50, 20))
        self.KL_15_label.setStyleSheet("font: bold;")
        self.KL_15_label.setText("KL_15")

        # KL_50 led
        self.KL_50 = QtWidgets.QLabel(self.centralwidget)
        self.KL_50.setGeometry(QtCore.QRect(700, 225, 20, 20))
        self.KL_50_label = QtWidgets.QLabel(self.centralwidget)
        self.KL_50_label.setGeometry(QtCore.QRect(730, 225, 50, 20))
        self.KL_50_label.setStyleSheet("font: bold;")
        self.KL_50_label.setText("KL_50")

        # KL_75 label
        self.KL_75 = QtWidgets.QLabel(self.centralwidget)
        self.KL_75.setGeometry(QtCore.QRect(700, 250, 20, 20))
        self.KL_75_label = QtWidgets.QLabel(self.centralwidget)
        self.KL_75_label.setGeometry(QtCore.QRect(730, 250, 50, 20))
        self.KL_75_label.setStyleSheet("font: bold;")
        self.KL_75_label.setText("KL_75")

        # Close all leds button
        self.close_all = QtWidgets.QPushButton(MainWindow)
        self.close_all.setText("Close all leds")
        self.close_all.setStyleSheet("font: bold;color: red")
        self.close_all.setGeometry(QtCore.QRect(50, 50, 120, 35))
        self.close_all.clicked.connect(self.close_all_leds)

        # 1 Led inside
        self.interior_lights = QtWidgets.QPushButton(MainWindow)
        self.interior_lights.setText("Interior lights")
        self.interior_lights.setStyleSheet("font: bold;")
        self.interior_lights.setGeometry(QtCore.QRect(50, 150, 160, 41))
        self.interior_lights.clicked.connect(self.set_interior_lights)

        # green led for interior lights
        self.interiorLightsLabel = QtWidgets.QLabel(self.centralwidget)
        self.interiorLightsLabel.setGeometry(QtCore.QRect(220, 160, 20, 20))

        # Led brightness percentage label
        self.percentage_label = QtWidgets.QLabel(self.centralwidget)
        self.percentage_label.setGeometry(QtCore.QRect(50, 260, 90, 40))
        self.percentage_label.setStyleSheet("font: bold;")
        self.percentage_label.setText("Percentage")

        # Led brightness progress bar
        self.progress_bar = QtWidgets.QProgressBar(MainWindow)
        self.progress_bar.setGeometry(50, 310, 200, 21)
        self.progress_bar.setRange(0, 100)

        # Led brightness spinbox
        self.spinBox = QtWidgets.QSpinBox(MainWindow)
        self.spinBox.setGeometry(QtCore.QRect(150, 260, 75, 41))
        self.spinBox.setKeyboardTracking(False)
        self.spinBox.setRange(0, 100)
        self.spinBox.valueChanged.connect(self.valuechange)

        # Sweep button
        self.sweep = QtWidgets.QPushButton(MainWindow)
        self.sweep.setText("Sweep")
        self.sweep.setStyleSheet("font: bold;")
        self.sweep.setGeometry(QtCore.QRect(50, 200, 160, 41))
        self.sweep.clicked.connect(self.sweep_threads)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.show()

    ############################### EXERCISE 1 ###############################
    # Clear all leds and widgtets when the Close all leds is pressed
    def close_all_leds(self):
        global interiorLed
        interiorLed = False
        self.interior_light_led("none")

    # Open one led when interior lights is pressed
    def interior_light_led(self, b1):
        self.interiorLightsLabel.setStyleSheet("background-color:" + str(b1) + ";border-radius:5px;")

    # Function called from button handler
    def set_interior_lights(self):
        global interiorLed
        interiorLed = not interiorLed
        if interiorLed:
            self.interior_light_led("green")
        else:
            self.interior_light_led("none")

    ############################### EXERCISE 2 ###############################
    # Sweep Leds thread
    def sweep_threads(self):
        self.thread = MyThread_sweep()
        self.thread.sweepLedsSignal.connect(self.sweep_leds)
        self.thread.start()

    # Sweep Leds function
    def sweep_leds(self, val):
        colors = ["none", "none", "none", "none"]
        colors[val] = "green"
        self.set4leds(colors[0], colors[1], colors[2], colors[3])

    # Sweep Leds
    def set4leds(self, led1, led2, led3, led4):
        self.led1_sweep.setStyleSheet("background-color:" + str(led1) + ";border-radius:5px;")
        self.led2_sweep.setStyleSheet("background-color:" + str(led2) + ";border-radius:5px;")
        self.led3_sweep.setStyleSheet("background-color:" + str(led3) + ";border-radius:5px;")
        self.led4_sweep.setStyleSheet("background-color:" + str(led4) + ";border-radius:5px;")

    ############################### EXERCISE 3 ###############################
    # Change progress bar value when spinbox value is changed
    def valuechange(self):
        global progress_bar_value
        target = self.spinBox.value()
        if target > progress_bar_value:
            self.change_pb_up_value(target)
        elif target < progress_bar_value:
            self.change_pb_down_value(target)

    # Change led brightness down when the spinbox value (representing led brightness percentage) is less than progress bar value
    def change_pb_down_value(self, value):
        global progress_bar_value
        while progress_bar_value > value:
            progress_bar_value -= 1
            self.progress_bar.setValue(progress_bar_value)
            QtWidgets.QApplication.processEvents()
            time.sleep(0.01)

    # Change led brightness up when the spinbox value (representing led brightness percentage) is bigger than progress bar value
    def change_pb_up_value(self, value):
        global progress_bar_value
        while progress_bar_value < value:
            progress_bar_value += 1
            self.progress_bar.setValue(progress_bar_value)
            QtWidgets.QApplication.processEvents()
            time.sleep(0.01)

    ############################### EXERCISE 4 ###############################
    # Succesice KL led turn
    def KL_lights(self, KL):
        index = KL_list.index(KL)
        colors = ["grey", "green", "red", "blue"]
        l1 = colors[0] if index >= 1 else "none"
        l2 = colors[1] if index >= 2 else "none"
        l3 = colors[2] if index >= 3 else "none"
        l4 = colors[3] if index >= 4 else "none"
        self.set_bg_colors(l1, l2, l3, l4)

    # Set previous value for KL when previous KL button is pressed
    def prev_kl_function(self):
        global KL_position
        if KL_position > 0:
            KL_position -= 1
            self.current_kl_label.setText(f"Current KL: {KL_list[KL_position]}")
            self.KL_lights(KL_list[KL_position])
            self.set_enable()

    # Set next value for KL when next KL button is pressed
    def next_kl_function(self):
        global KL_position
        if KL_position < len(KL_list) - 1:
            KL_position += 1
            self.current_kl_label.setText(f"Current KL: {KL_list[KL_position]}")
            self.KL_lights(KL_list[KL_position])
            self.set_enable()

    # Set enable KL buttons
    def set_enable(self):
        self.prev_kl.setEnabled(KL_position != 0)
        self.next_kl.setEnabled(KL_position != len(KL_list) - 1)

    # Set KL leds colors
    def set_bg_colors(self, l1, l2, l3, l4):
        self.KL_S.setStyleSheet("background-color:" + str(l1) + ";border-radius:5px;")
        self.KL_15.setStyleSheet("background-color:" + str(l2) + ";border-radius:5px;")
        self.KL_50.setStyleSheet("background-color:" + str(l3) + ";border-radius:5px;")
        self.KL_75.setStyleSheet("background-color:" + str(l4) + ";border-radius:5px;")

    #########################################################################
    ############################### USED FUNCTION ###########################
    def setWarningLights(self, warningLight1, warningLight2, warningLight3, warningLight4):
        self.warningLight1.setStyleSheet("background-color:" + str(warningLight1) + ";border-radius:5px;")
        self.warningLight2.setStyleSheet("background-color:" + str(warningLight2) + ";border-radius:5px;")
        self.warningLight3.setStyleSheet("background-color:" + str(warningLight3) + ";border-radius:5px;")
        self.warningLight4.setStyleSheet("background-color:" + str(warningLight4) + ";border-radius:5px;")

    #########################################################################
    ############################### EXERCISE 5 ##############################
    # Warning lights thread
    def warningLightsButton(self):
        global warning
        warning = not warning
        if warning:
            self.thread_warning = MyThread_warning()
            self.thread_warning.warningLightsSignal.connect(self.whileLights)
            self.thread_warning.start()
        else:
            self.setWarningLights("none", "none", "none", "none")

    # Warning Lights function
    def whileLights(self, val):
        if val == 1:
            self.setWarningLights("orange", "orange", "orange", "orange")
        else:
            self.setWarningLights("none", "none", "none", "none")

    ############################### EXERCISE 6 ##############################
    ################################ BONUS ################################
    # Open left door untill the obstacle is detected
    def fade_door_left(self):
        global brightness_left_door
        obstacle = self.spinBox_left.value()
        self.left_door_slider.setStyleSheet("")
        while brightness_left_door < obstacle:
            brightness_left_door += 1
            self.left_door_slider.setValue(brightness_left_door)
            QtWidgets.QApplication.processEvents()
            time.sleep(0.02)
        self.left_door_slider.setStyleSheet(
            "QSlider::handle:horizontal {background: red; border-radius: 5px;}"
        )

    # Fade out left door led brightness when slider is moving under obstacle value
    def valuechange_left_slider(self):
        global brightness_left_door
        self.left_door_slider.setStyleSheet("")
        brightness_left_door = self.left_door_slider.value()

    # Open right door untill the obstacle is detected
    def fade_door_right(self):
        global brightness_right_door
        obstacle = self.spinBox_right.value()
        self.right_door_slider.setStyleSheet("")
        while brightness_right_door < obstacle:
            brightness_right_door += 1
            self.right_door_slider.setValue(brightness_right_door)
            QtWidgets.QApplication.processEvents()
            time.sleep(0.02)
        self.right_door_slider.setStyleSheet(
            "QSlider::handle:horizontal {background: red; border-radius: 5px;}"
        )

    # Fade out right door led brightness when slider is moving under obstacle value
    def valuechange_right_slider(self):
        global brightness_right_door
        self.right_door_slider.setStyleSheet("")
        brightness_right_door = self.right_door_slider.value()


class MyWindow(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.question(self,
                                                "Confirm Exit",
                                                "Are you sure you want to exit ?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if result == QtWidgets.QMessageBox.Yes:
            event.accept()

        elif result == QtWidgets.QMessageBox.No:
            event.ignore()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.center()
    sys.exit(app.exec_())