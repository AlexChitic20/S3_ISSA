from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import rsa_library
import _pickle as cPickle
import os
import threading
import sys, time

HOST = 'localhost'
PORT = 12346

stop_thread = False

flag = 1
flag_low = 0

unlockCar = 0xfd02


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        global server
        global public_key
        global private_key
        global server_created_flag
        server_created_flag = False
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(600, 500)
        MainWindow.setWindowTitle('Server')
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.centralwidget.setStyleSheet("background-color:white;")

        # Start server button
        self.server_start = QtWidgets.QPushButton(MainWindow)
        self.server_start.setText("Start server")
        self.server_start.setStyleSheet("font: bold; font-size: 15px;")
        self.server_start.setGeometry(QtCore.QRect(200, 170, 200, 41))
        self.server_start.clicked.connect(self.start_server)

        # Start server label
        self.server_label = QtWidgets.QLabel(self.centralwidget)
        self.server_label.setGeometry(QtCore.QRect(200, 210, 200, 40))
        self.server_label.setStyleSheet("font:bold;font-size: 15px;qproperty-alignment: AlignCenter;")

        # Key button
        self.key = QtWidgets.QPushButton(self.centralwidget)
        self.key.setGeometry(QtCore.QRect(225, 270, 150, 150))
        keyImage = QtGui.QIcon('./key.png')
        self.key.setIcon(keyImage)
        self.key.setIconSize(QtCore.QSize(80, 80))
        self.key.clicked.connect(self.send_key_data)
        self.key.setEnabled(False)

        # Unlock
        self.unlock = QtWidgets.QLabel(self.centralwidget)
        self.unlock.setGeometry(QtCore.QRect(225, 430, 150, 20))
        self.unlock.setText("Unlock the car!")
        self.unlock.setStyleSheet("font:bold;font-size: 15px;qproperty-alignment: AlignCenter;")

        # Dashboard image
        self.dashboard_label = QtWidgets.QLabel(self.centralwidget)
        self.dashboard_label.setGeometry(QtCore.QRect(120, 280, 360, 180))
        dashboard = QtGui.QImage(QtGui.QImageReader('./dashboard.png').read())
        self.dashboard_label.setPixmap(QtGui.QPixmap(dashboard))
        self.dashboard_label.setVisible(False)

        # Airgab image label
        self.airbag_label = QtWidgets.QLabel(self.centralwidget)
        self.airbag_label.setGeometry(QtCore.QRect(290, 365, 30, 30))
        airbag_image = QtGui.QPixmap("./airbag.png")
        airbag_image = airbag_image.scaled(30, 30, QtCore.Qt.KeepAspectRatio)
        self.airbag_label.setPixmap(QtGui.QPixmap(airbag_image))
        self.airbag_label.setVisible(False)

        # Ecu defect label
        self.ecu_defect_label = QtWidgets.QLabel(self.centralwidget)
        self.ecu_defect_label.setGeometry(QtCore.QRect(280, 365, 40, 30))
        self.ecu_defect_label.setStyleSheet("font:bold;font-size:12px;color:red")
        self.ecu_defect_label.setVisible(False)

        # Continental image
        self.conti_label = QtWidgets.QLabel(self.centralwidget)
        self.conti_label.setGeometry(QtCore.QRect(110, 30, 400, 100))
        continental = QtGui.QImage(QtGui.QImageReader('./rsz_conti.png').read())
        self.conti_label.setPixmap(QtGui.QPixmap(continental))

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.show()

    def start_server(self):
        self.key.setEnabled(True)
        self.airbag_label.setVisible(False)
        self.ecu_defect_label.clear()
        self.dashboard_label.setVisible(False)
        self.key.setVisible(True)
        self.unlock.setVisible(True)
        self.images()

        global server, public_key, private_key, server_created_flag

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(1)

        self.server_label.setText("Waiting for client...")
        QtWidgets.QApplication.processEvents()

        self.conn, addr = server.accept()
        server_created_flag = True
        self.server_label.setText("Client connected!")

        public_key, private_key = rsa_library.generate_keypair(277, 239)

        keys_data = cPickle.dumps((public_key, private_key))
        self.conn.sendall(keys_data)

        self.recv_messages()

    def send_key_data(self):
        global public_key
        encrypted_unlock = rsa_library.encrypt(public_key, unlockCar)
        data = cPickle.dumps(encrypted_unlock)
        self.conn.sendall(data)

        # Uncomment the following 3 lines after this exercise is completed

        self.dashboard_label.setVisible(True)
        self.unlock.setVisible(False)
        self.key.setVisible(False)

    def recv_messages(self):
        self.stop_event = threading.Event()
        self.c_thread = threading.Thread(target=self.recv_messages_handler, args=(self.stop_event,))
        self.c_thread.start()

    def recv_messages_handler(self, stop_event):
        global server_created_flag
        global stop_thread
        global flag, flag_low, private_key

        while server_created_flag and not stop_event.isSet() and stop_thread == False:
            try:
                self.conn.settimeout(1)
                data = self.conn.recv(4096)
            except socket.timeout:
                continue
            except OSError:
                break

            if not data:
                break

            try:
                encrypted_msg = cPickle.loads(data)
                decrypted_msg = rsa_library.decrypt(private_key, encrypted_msg)
            except Exception:
                continue

            flag_low = rsa_library.low_check(decrypted_msg)
            flag = rsa_library.number_check(decrypted_msg)

            if not flag_low:
                response = "Low Corruption"
            elif not flag:
                response = "High Corruption"
            else:
                response = "Airbag ON"

            try:
                self.conn.sendall(cPickle.dumps(response))
            except OSError:
                break

    ##############################################################
    def images(self):
        self.c_thread1 = threading.Thread(name='images', target=self.images_handler)
        self.c_thread1.start()

    def images_handler(self):
        global flag
        global flag_low
        global stop_thread

        while stop_thread == False:
            if flag_low == True and flag == True:
                self.ecu_defect_label.setVisible(False)
                self.airbag_label.setVisible(True)
            elif flag_low == True and flag == False:
                self.airbag_label.setVisible(False)
                self.ecu_defect_label.setVisible(True)
                self.ecu_defect_label.setText('  ECU\nDefect')
            elif flag_low == False and flag == False:
                self.airbag_label.setVisible(False)
                self.ecu_defect_label.setVisible(True)
                self.ecu_defect_label.setText('  ECU\nDefect')


class MyWindow(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        global stop_thread
        result = QtWidgets.QMessageBox.question(self,
                                                "Confirm Exit",
                                                "Are you sure you want to exit ?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if result == QtWidgets.QMessageBox.Yes:
            stop_thread = True
            event.accept()
        elif result == QtWidgets.QMessageBox.No:
            event.ignore()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


def kill_proc_tree(pid, including_parent=True):
    import psutil
    parent = psutil.Process(pid)
    if including_parent:
        parent.kill()


def main():
    global server_created_flag
    import sys
    global app
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.center()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()