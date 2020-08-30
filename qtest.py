from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from Jogo import Jogo
import sys

class Ui_MainWindow(object):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.thread = Jogo()
    
    def initUi(self, MainWindow):
        MainWindow.move(0, 10)
        MainWindow.setWindowTitle("LegadoBot")
        MainWindow.setFixedSize(270, 450)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupCoin = QtWidgets.QGroupBox(self.centralwidget)
        self.groupCoin.setGeometry(QtCore.QRect(10, 100, 181, 81))
        self.groupCoin.setObjectName("groupCoin")
        self.rdCara = QtWidgets.QRadioButton(self.groupCoin)
        self.rdCara.setGeometry(QtCore.QRect(10, 20, 95, 20))
        self.rdCara.setChecked(True)
        self.rdCara.setObjectName("rdCara")
        self.rdCoroa = QtWidgets.QRadioButton(self.groupCoin)
        self.rdCoroa.setGeometry(QtCore.QRect(10, 40, 95, 20))
        self.rdCoroa.setObjectName("rdCoroa")
        self.rdRandom = QtWidgets.QRadioButton(self.groupCoin)
        self.rdRandom.setGeometry(QtCore.QRect(10, 60, 95, 20))
        self.rdRandom.setObjectName("rdRandom")
        self.groupResolution = QtWidgets.QGroupBox(self.centralwidget)
        self.groupResolution.setGeometry(QtCore.QRect(10, 10, 191, 91))
        self.groupResolution.setObjectName("groupResolution")
        self.rd1280 = QtWidgets.QRadioButton(self.groupResolution)
        self.rd1280.setGeometry(QtCore.QRect(10, 30, 95, 20))
        self.rd1280.setObjectName("rd1280")
        self.rd1600 = QtWidgets.QRadioButton(self.groupResolution)
        self.rd1600.setGeometry(QtCore.QRect(10, 50, 181, 20))
        self.rd1600.setChecked(True)
        self.rd1600.setObjectName("rd1600")
        self.rd1980 = QtWidgets.QRadioButton(self.groupResolution)
        self.rd1980.setGeometry(QtCore.QRect(10, 70, 95, 20))
        self.rd1980.setObjectName("rd1980")
        self.checkBoxBelaJogada = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxBelaJogada.setGeometry(QtCore.QRect(20, 200, 411, 20))
        self.checkBoxBelaJogada.setChecked(True)
        self.checkBoxBelaJogada.setObjectName("checkBoxBelaJogada")
        self.txtBoxTime = QtWidgets.QLineEdit(self.centralwidget)
        self.txtBoxTime.setGeometry(QtCore.QRect(20, 290, 51, 22))
        self.txtBoxTime.setObjectName("txtBoxTime")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 230, 241, 61))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(80, 290, 55, 16))
        self.label_2.setObjectName("label_2")
        self.btnStart = QtWidgets.QPushButton(self.centralwidget)
        self.btnStart.setGeometry(QtCore.QRect(30, 340, 93, 28))
        self.btnStart.setObjectName("btnStart")
        self.btnStop = QtWidgets.QPushButton(self.centralwidget)
        self.btnStop.setGeometry(QtCore.QRect(150, 340, 93, 28))
        self.btnStop.setObjectName("btnStop")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 266, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.btnStop.clicked.connect(self.btnStopClicked)
        self.btnStart.clicked.connect(self.btnStartClicked)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.groupCoin.setTitle(_translate("MainWindow", "Como deseja jogar a moeda?"))
        self.rdCara.setText(_translate("MainWindow", "Cara"))
        self.rdCoroa.setText(_translate("MainWindow", "Coroa"))
        self.rdRandom.setText(_translate("MainWindow", "Aleatório"))
        self.groupResolution.setTitle(_translate("MainWindow", "Resolução do PTCGO"))
        self.rd1280.setText(_translate("MainWindow", "1024 x 720"))
        self.rd1600.setText(_translate("MainWindow", "1600 x 900 (recomendada)"))
        self.rd1980.setText(_translate("MainWindow", "1920 x 1080"))
        self.checkBoxBelaJogada.setText(_translate("MainWindow", "Enviar \"bela jogada\""))
        self.txtBoxTime.setText(_translate("MainWindow", "60"))
        self.label.setText(_translate("MainWindow", "Quando ganhar a partida, esperar quanto\n"
" tempo antes de desistir? (Caso o outro\n"
" jogador não desisita)"))
        self.label_2.setText(_translate("MainWindow", "segundos"))
        self.btnStart.setText(_translate("MainWindow", "Iniciar"))
        self.btnStop.setText(_translate("MainWindow", "Parar"))
        MainWindow.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
        self.btnStop.setEnabled(False)

    def Controller(self):
        self.btnStart.setEnabled(False)
        self.thread.run()

    def btnStartClicked(self):
        self.btnStart.setEnabled(False)
        self.btnStop.setEnabled(True)
        numtxtbox = int(self.txtBoxTime.text())
        self.thread.render(self.isHeadsCheck(), self.resolutionCheck(), numtxtbox, self.checkBoxBelaJogada.isChecked())

    def btnStopClicked(self):
        self.btnStart.setEnabled(True)
        self.btnStop.setEnabled(False)
        self.thread.terminate()
    
    def resolutionCheck(self):
        if self.rd1280.isChecked():
            return 1
        elif self.rd1600.isChecked():
            return 0
        else:
            return 2

    def isHeadsCheck(self):
        if self.rdCara.isChecked():
            return 0
        elif self.rdCoroa.isChecked():
            return 1
        else:
            return 2

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.initUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

