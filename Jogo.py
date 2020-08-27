import numpy as np
import cv2
import time
import pyautogui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from WindowCapture import WindowCapture
from PIL import ImageGrab



class Jogo(QThread):
    
    playing = True
    wincap = None
    processed_img = None
    pos = (0,0)
    isHeads = False
    tempoEspera = 60

    def __init__(self, parent= None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.wincap = WindowCapture('Pokemon Trading Card Game Online')
        self.pos = WindowCapture.get_screen_position(self.wincap, self.pos)
        pyautogui.FAILSAFE = True
        self.tempImage = None


    def run(self):
        print(self.isHeads)
        self.Jogar()

    def render(self, isHeads):
        self.isHeads = isHeads
        self.start()
   
    def SearchImage(self, img):
        self.screenshot = self.wincap.get_screenshot()
        self.processed_img = self.CannyIt(self.screenshot)
        self.img_np = np.array(self.screenshot)
        img = self.CannyIt(img)
        hh, ww = img.shape[:2]
        template = img[:,:]
        correlation = cv2.matchTemplate(self.processed_img, template, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(correlation)
        max_val_ncc = '{:.3f}'.format(max_val)
        xx = max_loc[0]
        yy = max_loc[1]
        return xx + self.pos[0] + 4, yy + self.pos[1] + 4, max_val_ncc

    def Jogar(self):
        self.NovaPartida()

    def NovaPartida(self):
        btnJogar = cv2.imread("img/btnJogar.png")
        while(True):
            self.x, self.y, self.confidenceValue = self.SearchImage(btnJogar)
            if (float(self.confidenceValue) > 0.9):
                pyautogui.moveTo(self.x, self.y)
                pyautogui.click()
                break       
        self.WhoWon()

    def WhoWon(self):
        txtPeca = cv2.imread("img/txtPecaQueAMoeda.png")
        txtVocePerdeu = cv2.imread("img/txtVocePerdeuMoeda.png")
        txtVoceVenceu = cv2.imread("img/txtVoceVenceuMoeda.png")
        while(True):
            print("testando quem joga a moeda")
            x, y, confidenceValue = self.SearchImage(txtPeca)
            if (float(confidenceValue) > 0.8):
                self.HeadsOrTails() 
            x, y, confidenceValue = self.SearchImage(txtVocePerdeu)
            if (float(confidenceValue) > 0.8):
                print("eu perdi")
                self.PlayerLose()
                break
            x, y, confidenceValue = self.SearchImage(txtVoceVenceu)
            if (float(confidenceValue) > 0.8):
                print("eu venci")
                self.PlayerWon()
                break
    
    def PlayerWon(self): 
        btnFinalizar = cv2.imread("img/btnFinalizar.png")
        StartTime = time.time()
        while(time.time() - StartTime < self.tempoEspera):
            print("esperando tempo")
            print (time.time() - StartTime)
            x, y, confidenceValue = self.SearchImage(btnFinalizar)
            print(confidenceValue)
            if float(confidenceValue) > 0.8:
                pyautogui.moveTo(self.x, self.y)
                pyautogui.click()
                break
        self.Desistir()

    def PlayerLose(self):
        self.Desistir()

    def Desistir(self):
        btnSettings = cv2.imread("img/btnSettings.png")
        btnRender = cv2.imread("img/btnRender.png")
        btnSim = cv2.imread("img/btnSim.png")
        btnFinalizar = cv2.imread("img/btnFinalizar.png")    
        while(True):
            print("desistindo")
            x, y, confidenceValue = self.SearchImage(btnSettings)
            print(confidenceValue)
            if float(confidenceValue) > 0.8:
                pyautogui.moveTo(x,y)
                pyautogui.click()
                break
            print("testando finalizar")
            x, y, confidenceValue = self.SearchImage(btnFinalizar)
            print(confidenceValue)
            if float(confidenceValue) > 0.8:
                pyautogui.moveTo(x,y)
                pyautogui.click()
                self.NovaPartida()
        while(True):
            print("clicando botao render-se")
            x, y, confidenceValue = self.SearchImage(btnRender)
            print(confidenceValue)
            if float(confidenceValue) > 0.8:
                pyautogui.moveTo(x,y)
                pyautogui.click()
                break
            print("testando finalizar")
            x, y, confidenceValue = self.SearchImage(btnFinalizar)
            print(confidenceValue)
            if float(confidenceValue) > 0.8:
                pyautogui.moveTo(x,y)
                pyautogui.click()
                self.NovaPartida()
        while(True):
            print("clicando botao sim")
            x, y, confidenceValue = self.SearchImage(btnSim)
            print(confidenceValue)
            if float(confidenceValue) > 0.8:
                pyautogui.moveTo(x,y)
                pyautogui.click()
                break
            print("testando finalizar")
            x, y, confidenceValue = self.SearchImage(btnFinalizar)
            print(confidenceValue)
            if float(confidenceValue) > 0.8:
                pyautogui.moveTo(x,y)
                pyautogui.click()
                self.NovaPartida()
        while(True):
            print("clicando finalizar")
            x, y, confidenceValue = self.SearchImage(btnFinalizar)
            print(confidenceValue)
            if float(confidenceValue) > 0.8:
                pyautogui.moveTo(x,y)
                pyautogui.click()
                break
        self.NovaPartida()

    def HeadsOrTails(self):
        if self.isHeads:
            tempImage = cv2.imread("img/btnCara.png")
        else: tempImage = cv2.imread("img/btnCoroa.png")
        while(True):
            x, y, confidence = self.SearchImage(tempImage)
            if (float(confidence) > 0.8): 
                pyautogui.moveTo(x, y)
                pyautogui.click()
                self.WhoWon()
                break

    def CannyIt(self, img):
        return cv2.Canny(img, threshold1=200, threshold2=300)
            


"""legado

    def WhoChooseCoin(self):
        txtPeca = cv2.imread("img/txtPecaQueAMoeda.png")
        txtEnemyDecidindo = cv2.imread("img/txtEnemyDecidindo.png")
        while(True):
            x, y, confidenceValue = self.SearchImage(txtPeca)
            print("eu:" + confidenceValue)
            if (float(confidenceValue) > 0.8):
                print("eu jogo a moeda")
                pyautogui.moveTo(x, y)
                return True
            print("inimigo:" + confidenceValue)
            if (float(confidenceValue) > 0.8):
                print("inimigo joga a moeda")
                return False

"""


        #       Se ganhou
        #           Envia bela jogada
        #           Espera 25 segundos
        #           Desiste ou Espera
        #       Se perdeu
        #           Desiste
        #           Começa de novo
        #Se deve esperar
        #   Se ganhou
        #       Envia bela jogada
        #       Espera 25 segundos
        #       Desiste ou Espera
        #   Se perdeu
        #       Desiste
        #       Começa de novo