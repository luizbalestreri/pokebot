import numpy as np
import cv2
import time
import pyautogui
import StateMachine as sm
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from WindowCapture import WindowCapture
from PIL import ImageGrab
from Jogo import Jogo

playing = True
wincap = None
processed_img = None
pos = (0,0)
isHeads = False
tempoEspera = 30
exiting = False
wincap = WindowCapture('Pokemon Trading Card Game Online')
pos = WindowCapture.get_screen_position(wincap, pos)
pyautogui.FAILSAFE = True
tempImage = None
txtPeca = cv2.imread("img/txtPecaQueAMoeda.png")

def CannyIt(img):
    return cv2.Canny(img, threshold1=200, threshold2=300)

txtEnemyDecidindo = CannyIt(cv2.imread("img/txtEnemyDecidindo.png"))

def SearchImage(img):
    print()
while(True):
    ss = wincap.get_screenshot()
    sim = CannyIt(cv2.imread("img/btnSim.png"))
    cv2.imshow("", CannyIt(ss))
    cv2.imshow("sim", sim)
    cv2.waitKey(1)
    #cv2.imshow("teste", txtEnemyDecidindo)

