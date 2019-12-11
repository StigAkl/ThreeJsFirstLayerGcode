import numpy as np
import cv2
from matplotlib import pyplot as plt

# def scale(image, scale):
#     height, width, depth = image.shape
#     imgScale = scale/width
#     newX,newY = image.shape[1]*imgScale, image.shape[0]*imgScale
#     return cv2.resize(image,(int(newX),int(newY)))    


# img = cv2.medianBlur(img,5)

# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ret,th1 = cv2.threshold(gray,105,255,cv2.THRESH_BINARY)
# ret,thresh1 = cv2.threshold(gray,120,200,cv2.THRESH_BINARY)

# cv2.imshow("img", gray)
# cv2.waitKey(0)

img = cv2.imread('octo_first_layer.PNG', 1)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

mask = cv2.inRange(hsv, (40, 40, 40), (90, 255,255))

imask = mask>0
green = np.zeros_like(img, np.uint8)
green[imask] = img[imask]
cv2.imshow('img', img)
cv2.imshow('green', green)
cv2.imshow('mask', mask)
cv2.waitKey(0)
#-----Splitting the LAB image to different channels-------------------------

# #-----Applying CLAHE to L-channel-------------------------------------------
# clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
# cl = clahe.apply(l)
# cv2.imshow('CLAHE output', cl)

# #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
# limg = cv2.merge((cl,a,b))
# cv2.imshow('limg', limg)

# #-----Converting image from LAB Color model to RGB model--------------------
# final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
# cv2.imshow('final', final)

# cv2.waitKey(0)
