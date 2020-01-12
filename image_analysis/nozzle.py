import numpy as np
import cv2
import time

def scale(image, scale):
    height, width, depth = image.shape
    imgScale = scale/width
    newX,newY = image.shape[1]*imgScale, image.shape[0]*imgScale
    return cv2.resize(image,(int(newX),int(newY)))   


def get_segment_crop(img,tol=0, mask=None):
    if mask is None:
        mask = img > tol
    return img[np.ix_(mask.any(1), mask.any(0))]

def get_center(cnt):
    M = cv2.moments(cnt)
    x = round(M['m10'] / M['m00'])
    y = round(M['m01'] / M['m00'])

    return x,y

def inc_contrast(img):
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    #cv2.imshow("lab",lab)

    #-----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)
    #cv2.imshow('l_channel', l)
    #cv2.imshow('a_channel', a)
    #cv2.imshow('b_channel', b)

    #-----Applying CLAHE to L-channel-------------------------------------------
    #Contrast Limited Adaptive Histogram Equalization
    clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    #cv2.imshow('CLAHE output', cl)

    #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv2.merge((cl,a,b))
    #cv2.imshow('limg', limg)

    #-----Converting image from LAB Color model to RGB model--------------------
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    return final

def detect_filament_from_roi(reg):

    height, width, channels = reg.shape

    blank_image = np.zeros((height,width,3), np.uint8)
    blank_image[0:height, 0:width] = 255
    orig_roi = reg.copy()

    reg = cv2.cvtColor(reg, cv2.COLOR_BGR2HSV)

    lower_filament = np.array([83, 27, 195], dtype="uint8")
    upper_filament = np.array([95,71,255], dtype="uint8")

    mask = cv2.inRange(reg, lower_filament, upper_filament)

    kernel = np.ones((1,30),np.float32)/25
    mask_blurred = cv2.filter2D(mask, -1, kernel)

    cv2.imshow("Binary Mask", mask_blurred)
    
    contours = cv2.findContours(mask_blurred, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    print(len(contours))

    cv2.imshow("Original Image", orig_roi)
    cv2.drawContours(blank_image,contours, -1, (255,0,0), 1)
    cv2.imshow("Contour", blank_image)

    #Calculate bounding rectangle for the contour
    x, y, w, h = cv2.boundingRect(contours[0])
    # draw a green rectangle to visualize the bounding rect
    cv2.rectangle(orig_roi, (x, y), (x+w, y+h), (0, 255, 0), 1)

    cv2.imshow("Bounding Box Visualization", orig_roi)

    

# ---- MAIN ----- 
image = scale(cv2.imread('ref.png'), 1100)
original = image.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([140, 175, 176], dtype="uint8")
upper = np.array([160, 242, 231], dtype="uint8")

mask = cv2.inRange(image, lower, upper)

cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cnts = cnts[0] if len(cnts) == 2 else cnts[1]

maxVertical = -1
maxHorizontal = -1
minVertical = 9999
minHorizontal = 9999

for c in cnts:
    xd,yd = get_center(c)
    minHorizontal = min([minHorizontal, xd])
    minVertical = min([minVertical, yd])
    maxVertical = max([maxVertical, yd])
    maxHorizontal = max([maxHorizontal, xd])

    #x,y,w,h = cv2.boundingRect(c)
    #cv2.rectangle(original, (x, y), (x + w, y + h), (36,255,12), 2)

roi = original[minVertical:maxVertical, minHorizontal:maxHorizontal]

roi_contrast = inc_contrast(roi)
cv2.imwrite("contrast.jpg", roi_contrast)

detect_filament_from_roi(roi_contrast)
#cv2.imshow("Cropped", roi)
# cv2.imshow('mask', mask)
# cv2.imshow('original', image)
#cv2.imshow('Contrast', roi_contrast)
cv2.waitKey(0)

#HSV nozzle: (140, 175, 176) to (160, 242, 231)
#HSV filament: (28, 46, 51) to (100,255,255)