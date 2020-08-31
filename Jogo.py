import numpy as np
import time, random, cv2
import pyautogui
from PyQt5.QtCore import *
from WindowCapture import WindowCapture



class Jogo(QThread):
    
    playing = True
    wincap = None
    processed_img = None
    pos = (0,0)
    isHeads = 0
    tempoEspera = 60
    sendMsg = False
    #constants
    pathImg = "img/"
    pathImg1280 = "img1280/"
    resolutionsEnum = ( 1, 0.85, 1.2)
    resolutionIndex = 0

    def __init__(self, parent= None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.wincap = WindowCapture('Pokemon Trading Card Game Online')
        self.pos = WindowCapture.get_screen_position(self.wincap, self.pos)
        pyautogui.FAILSAFE = True
        self.tempImage = None

    def Concat(self, str):
        if (self.resolutionIndex == 0):
            return ("img/" + str)
        elif (self.resolutionIndex == 1):
            return ("img1280/" + str)

    def run(self):
        print(self.isHeads)
        self.Jogar()

    def render(self, isHeads, resolution, waitTime, sendMsg):
        self.isHeads = isHeads
        self.resolutionIndex = resolution
        self.tempoEspera = waitTime
        self.sendMsg = sendMsg
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
        return xx + self.pos[0] + ww/2, yy + self.pos[1] + hh/2, max_val_ncc

    def BelaJogada(self):
        sizeXY = (self.wincap.get_screenshot().shape[1], self.wincap.get_screenshot().shape[0])
        pyautogui.moveTo((sizeXY[0] + self.pos[0]) - 20, (sizeXY[1] + self.pos[1]) - 20)
        pyautogui.click()
        msgBox = cv2.imread(self.Concat("msgBox.png"))
        xxx, yyy, confidence = self.SearchImage(msgBox)
        pyautogui.moveTo(xxx, yyy - int(msgBox.shape[0]/4.5))
        pyautogui.click()
        
    def Jogar(self):
        self.NovaPartida()

    def NovaPartida(self):
        btnJogar = cv2.imread(self.Concat("btnJogar.png"))
        while(True):
            self.x, self.y, self.confidenceValue = self.SearchImage(btnJogar)
            if (float(self.confidenceValue) > 0.85):
                pyautogui.moveTo(self.x, self.y)
                pyautogui.click()
                break
            self.TestarFinalizar()       
        self.WhoWon()

    def TestarFinalizar(self):
        btnFinalizar = cv2.imread(self.Concat("btnFinalizar.png"))
        print("testando finalizar")
        x, y, confidenceValue = self.SearchImage(btnFinalizar)
        print(confidenceValue)
        if float(confidenceValue) > 0.8:
            pyautogui.moveTo(x,y)
            pyautogui.click()
            self.NovaPartida()

    def WhoWon(self):
        txtPeca = cv2.imread(self.Concat("btnCoroa.png"))
        txtVocePerdeu = cv2.imread(self.Concat("txtVocePerdeuMoeda.png"))
        txtVoceVenceu = cv2.imread(self.Concat("txtVoceVenceuMoeda.png"))
        while(True):
            print("testando quem joga a moeda")
            x, y, confidenceValue = self.SearchImage(txtPeca)
            if (float(confidenceValue) > 0.8):
                self.HeadsOrTails() 
            x, y, confidenceValue = self.SearchImage(txtVocePerdeu)
            if (float(confidenceValue) > 0.8):
                print("eu perdi")
                if(self.sendMsg):
                    self.BelaJogada()
                self.PlayerLose()
                break
            x, y, confidenceValue = self.SearchImage(txtVoceVenceu)
            if (float(confidenceValue) > 0.8):
                print("eu venci")
                if(self.sendMsg):
                    self.BelaJogada()
                self.PlayerWon()
                break
    
    def PlayerWon(self): 
        btnFinalizar = cv2.imread(self.Concat("/btnFinalizar.png"))
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
        btnSettings = cv2.imread(self.Concat("btnSettings.png"))
        btnRender = cv2.imread(self.Concat("btnRender.png"))
        btnSim = cv2.imread(self.Concat("btnSim.png"))
        btnFinalizar = cv2.imread(self.Concat("btnFinalizar.png"))    
        while(True):
            print("desistindo")
            x, y, confidenceValue = self.SearchImage(btnSettings)
            print(confidenceValue)
            if float(confidenceValue) > 0.8:
                pyautogui.moveTo(x,y)
                pyautogui.click()
                break
            self.TestarFinalizar()
        while(True):
            print("clicando botao render-se")
            x, y, confidenceValue = self.SearchImage(btnRender)
            print(confidenceValue)
            if float(confidenceValue) > 0.8:
                pyautogui.moveTo(x,y)
                pyautogui.click()
                break
            self.TestarFinalizar()
        while(True):
            print("clicando botao sim")
            x, y, confidenceValue = self.SearchImage(btnSim)
            print(confidenceValue)
            if float(confidenceValue) > 0.8:
                pyautogui.moveTo(x,y)
                pyautogui.click()
                break
            self.TestarFinalizar()
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
        if self.isHeads == 0:
            tempImage = cv2.imread(self.Concat("btnCara.png"))
        elif self.isHeads == 1: tempImage = cv2.imread(self.Concat("btnCoroa.png"))
        else: 
            if random.randrange(1) == 1:
                tempImage = cv2.imread(self.Concat("btnCara.png"))
            else: tempImage = cv2.imread(self.Concat("btnCoroa.png"))
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