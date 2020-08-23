import numpy as np
import cv2
import pyautogui
from windowcapture import WindowCapture

from PIL import ImageGrab


wincap = WindowCapture('Pokemon Trading Card Game Online')

fourcc = cv2.VideoWriter_fourcc('X','V','I','D') #you can use other codecs as well.
vid = cv2.VideoWriter('record.avi', fourcc, 8, (1440,900))

jogar = cv2.imread('img/jogar.png',  cv2.IMREAD_UNCHANGED)

pyautogui.FAILSAFE = True

def SearchImage(img):
    partial_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    partial_image= cv2.threshold(partial_image, 0, 125, cv2.THRESH_BINARY)[1]

    # get largest contour from binary image
    contours = cv2.findContours(partial_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    big_contour = max(contours, key=cv2.contourArea)

    # draw the contour of the piece outline as the mask
    mask = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    cv2.drawContours(mask, [big_contour], 0, (255,255,255), 1)
    hh, ww = mask.shape[:2]

    # extract the template from the BGR (no alpha) piece 
    template = img[:,:,0:3]
    correlation = cv2.matchTemplate(img_np, template, cv2.TM_CCORR_NORMED, mask=mask)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(correlation)
    max_val_ncc = '{:.3f}'.format(max_val)
    print("normalize_cross_correlation: " + max_val_ncc)
    xx = max_loc[0]
    yy = max_loc[1]
    print(xx, yy)
        
    # draw template bounds and corner intersection in red onto img
    result = full_image.copy()
    cv2.rectangle(result, (xx, yy), (xx+ww, yy+hh), (0, 0, 255), 1)
    
    return correlation 


while(True):
    ss = wincap.get_screenshot()
    cv2.imshow("", ss)
    ''' legacy code:
    #img = ImageGrab.grab(bbox=(0, 0, 1000, 1000)) #x, y, w, h
    #img_np = np.array(img)
    #img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    #vid.write(img_np)
    ''' 
    img = ss
    img_np = np.array(img)
    full_image = img_np
    corr = SearchImage(jogar)
     ##
    #print(corr)     
    #if float(max_val) > 0.91:
    #     loc = (xx + 2, yy + 2)
    #     pyautogui.moveTo(loc)
    #     pyautogui.PAUSE = 1
         #pyautogui.click()
         


    key = cv2.waitKey(1)
    if key == 27:
        break    
vid.release()
cv2.destroyAllWindows()