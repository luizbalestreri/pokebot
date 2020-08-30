from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from Jogo import Jogo
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setFixedSize(300, 450)
        self.move(0, 10)
        self.setWindowTitle("LegadoBot")
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.initUI()
        self.thread = Jogo()
   
    
    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Escolher sempre cara ou coroa?")
        self.label.setGeometry(QtCore.QRect(20, 70, 185, 15)) # x, y, w, h

        self.btnStart = QtWidgets.QPushButton(self)
        self.btnStart.setText("Start")
        self.btnStart.clicked.connect(self.btnStartClicked)
        self.btnStart.move (220, 50)

        self.btnStop = QtWidgets.QPushButton(self)
        self.btnStop.setText("Stop")
        self.btnStop.clicked.connect(self.btnStopClicked)
        self.btnStop.move (220, 100)
        self.btnStop.setEnabled(False)
        
        self.rdCara = QtWidgets.QRadioButton(self)
        self.rdCara.setGeometry(QtCore.QRect(30, 90, 95, 20))
        self.rdCara.setChecked(True)
        self.rdCara.setObjectName("rdCara")
        self.rdCoroa = QtWidgets.QRadioButton(self)
        self.rdCoroa.setEnabled(True)
        self.rdCoroa.setGeometry(QtCore.QRect(130, 90, 95, 20))
        self.rdCoroa.setObjectName("rdCoroa")
        self.rdCara.setText("Cara")
        self.rdCoroa.setText("Coroa")

    def Controller(self):
        self.btnStart.setEnabled(False)
        self.thread.run()

    def btnStartClicked(self):
        self.btnStart.setEnabled(False)
        self.btnStop.setEnabled(True)
        isHeads = self.rdCara.isChecked()
        self.thread.render(isHeads)

    def btnStopClicked(self):
        self.btnStart.setEnabled(True)
        self.btnStop.setEnabled(False)
        self.thread.terminate()


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()