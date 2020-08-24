import numpy as np
import cv2
import pyautogui
from windowcapture import WindowCapture
from PIL import ImageGrab

wincap = WindowCapture('Pokemon Trading Card Game Online')
jogar = cv2.imread('img/jogar.png',  cv2.IMREAD_UNCHANGED)
pyautogui.FAILSAFE = True
isHeads = 0
tempImage = None
imageNames = []
images = []
roi = (680, 523, 242, 83)

def SearchImage(img):
    ##partial_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ##partial_image= cv2.threshold(partial_image, 0, 255, cv2.THRESH_BINARY)[1]

    partial_image = img
    partial_image= cv2.threshold(partial_image, 0, 255, cv2.THRESH_BINARY)

    # get largest contour from binary image
    ##contours = cv2.findContours(partial_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ##contours = contours[0] if len(contours) == 2 else contours[1]
    ##big_contour = max(contours, key=cv2.contourArea)

    # draw the contour of the piece outline as the mask
    ##mask = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    ##cv2.drawContours(mask, [big_contour], 0, (255,255,255), 1)
    ##hh, ww = mask.shape[:2]

    # extract the template from the BGR (no alpha) piece 
    template = img[:,:]
    correlation = cv2.matchTemplate(processed_img, template, cv2.TM_CCORR_NORMED)
    ##correlation = cv2.matchTemplate(processed_img, template, cv2.TM_CCORR_NORMED, mask=mask)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(correlation)
    max_val_ncc = '{:.3f}'.format(max_val)
    #print("normalize_cross_correlation: " + max_val_ncc)
    xx = max_loc[0]
    yy = max_loc[1]
    #print(xx, yy)
        
    # draw template bounds and corner intersection in red onto img
    ##cv2.rectangle(screenshot, (xx, yy), (xx+ww, yy+hh), (0, 0, 255), 1)
    
    #return xx, yy
    return max_val_ncc
def Jogar():
    #Se deve jogar cara ou coroa
    HeadsOrTails()
    #   Escolhe $caraoucoroa
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

def HeadsOrTails():
    if isHeads:
        tempImage = cv2.imread("img/btnCara.png")
    else: tempImage = cv2.imread("img/btnCoroa.png")
    SearchImage(tempImage)
    pyautogui.moveTo()

def LoadImageNames():
    imageNames.append("img/btnCara.png") #0
    imageNames.append("img/btnCoroa.png") #1
    imageNames.append("img/btnFinalizar.png") #2
    imageNames.append("img/btnRender.png") #3
    imageNames.append("img/btnSim.png") #4 
    imageNames.append("img/btnJogar.png") #5
    imageNames.append("img/txtEnemyDecidindo.png") #6
    imageNames.append("img/txtDesejaJogarPrimeiro.png") #7
    imageNames.append("img/txtEscolhaUmPokemon.png") #8
    imageNames.append("img/txtPecaQueAMoeda.png") #9
    imageNames.append("img/txtVocePerdeuMoeda.png") #10
    imageNames.append("img/txtVoceVenceuMoeda.png") #11
    imageNames.append("img/wait1seg.png") #12

LoadImageNames()
for imn in imageNames:
    images.append(cv2.imread(imn))

def CannyIt(img):
    return cv2.Canny(img, threshold1=200, threshold2=300)

testess = cv2.imread("img/test.png")
testess = CannyIt(testess)

while(True):
    screenshot = wincap.get_screenshot()
    cv2.imshow('ROI',roi)
    processed_img = testess#CannyIt(screenshot)
    cv2.imshow("processada", processed_img)

    #cv2.imshow("screenshot", screenshot)
    img_np = np.array(screenshot)
    imgTemp = np.array(images[5])
    cv2.imshow("", CannyIt(images[7]))
    #cv2.imshow("2", testess)
    roi = screenshot[523:523+imgTemp.shape[0], 680:680+imgTemp.shape[1], :]
    for i in range(len(imageNames)):
        temp = SearchImage(CannyIt(images[int(i)]))
        #if (float(temp) > 0.7):
        print(imageNames[int(i)], temp)
    ##
    #print(corr)     
    #TODO: função botar jogar
    # if float(max_val) > 0.91:
    #     loc = (xx + 2, yy + 2)
    #     pyautogui.moveTo(loc)
    #     pyautogui.PAUSE = 1
         #pyautogui.click()
         


    key = cv2.waitKey(1)
    if key == 27:
        break    
cv2.destroyAllWindows()