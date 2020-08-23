import cv2
import numpy as np

# read images
full_image = cv2.imread('puzzle_1.jpg')    
piece = cv2.imread('piece_1.png', cv2.IMREAD_UNCHANGED)

# convert piece to gray and threshold to binary
partial_image = cv2.cvtColor(piece,cv2.COLOR_BGR2GRAY)
partial_image = cv2.threshold(partial_image, 0, 255, cv2.THRESH_BINARY)[1]

# get largest contour from binary image
contours = cv2.findContours(partial_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
big_contour = max(contours, key=cv2.contourArea)

# draw the contour of the piece outline as the mask
mask = np.zeros((55, 55, 3), dtype=np.uint8)
cv2.drawContours(mask, [big_contour], 0, (255,255,255), 1)
hh, ww = mask.shape[:2]

# extract the template from the BGR (no alpha) piece 
template = piece[:,:,0:3]

correlation = cv2.matchTemplate(full_image, template, cv2.TM_CCORR_NORMED, mask=mask)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(correlation)
max_val_ncc = '{:.3f}'.format(max_val)
print("normalize_cross_correlation: " + max_val_ncc)
xx = max_loc[0]
yy = max_loc[1]

print('xmatchloc =',xx,'ymatchloc =',yy)

# draw template bounds and corner intersection in red onto img
result = full_image.copy()
cv2.rectangle(result, (xx, yy), (xx+ww, yy+hh), (0, 0, 255), 1)

# save results
cv2.imwrite('puzzle_template.png', template)
cv2.imwrite('puzzle_mask.png', mask)
cv2.imwrite('full_image_matches.jpg', result)

# show results
cv2.imshow('full_image', full_image)
cv2.imshow('piece', piece)
cv2.imshow('partial_image', partial_image)
cv2.imshow('mask', mask)
cv2.imshow('template', template)
cv2.imshow('result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()