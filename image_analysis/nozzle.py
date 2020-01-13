import numpy as np
import cv2
import time
import math 

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
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
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
    
    contours = cv2.findContours(mask_blurred, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    cv2.imshow("Original Image", orig_roi)
    mask_blurred = cv2.cvtColor(mask_blurred, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(blank_image,contours, -1, (255,0,0), 1)
    cv2.drawContours(mask_blurred,contours, -1, (0,0,255),1)

    cv2.imshow("Blurred contour", mask_blurred)
    cv2.imshow("Contour", blank_image)

    #Calculate bounding rectangle for the contour
    x, y, w, h = cv2.boundingRect(contours[0])
    # draw a green rectangle to visualize the bounding rect
    cv2.rectangle(orig_roi, (x, y-2), (x+w, y+h), (0, 255, 0), 1)

    cv2.imshow("Bounding Box Visualization", orig_roi)

    return y
    

def calculateDistance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist  

# ---- MAIN ----- 
image = scale(cv2.imread('ref.png'), 1100)
original = image.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower = np.array([140, 175, 176], dtype="uint8")
upper = np.array([160, 242, 231], dtype="uint8")

mask = cv2.inRange(image, lower, upper)

kernel = np.ones((5,5),np.float32)/25
mask = cv2.filter2D(mask, -1, kernel)

cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

maxVertical = -1
maxHorizontal = -1
minVertical = 9999
minHorizontal = 9999


# Get center of nozzle
c2 = cnts[2]
x_center_nozzle, y_center_nozzle = get_center(c2)

#Calculate ROI points
for c in cnts:
    xd,yd = get_center(c)
    minHorizontal = min([minHorizontal, xd])
    minVertical = min([minVertical, yd])
    maxVertical = max([maxVertical, yd])
    maxHorizontal = max([maxHorizontal, xd])    
    #cv2.circle(original, (xd,yd), 10, (255,0,0), 2)
    #x,y,w,h = cv2.boundingRect(c)
    #cv2.rectangle(original, (x, y), (x + w, y + h), (36,255,12), 2)

roi = original[minVertical:maxVertical, minHorizontal:maxHorizontal]

cv2.imshow("Before contrast", roi)
roi_contrast = inc_contrast(roi)
cv2.imshow("After contrast", roi_contrast)
cv2.imwrite("contrast.jpg", roi_contrast)

fy = detect_filament_from_roi(roi_contrast)

print("Nozzle filament distance: ", abs(fy-minVertical))

p_nozzle = (x_center_nozzle, y_center_nozzle)
p_filament = (x_center_nozzle, minVertical+fy)

cv2.line(original, p_filament, p_nozzle, (0,255,0), 1)

cDist = str(calculateDistance(p_nozzle[0], p_nozzle[1], p_filament[0], p_filament[1]))
original = cv2.putText(original, "Distance: " + cDist, (x_center_nozzle+20, int((minVertical+fy+y_center_nozzle+30)/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 1, cv2.LINE_AA)

cv2.imshow("Line", original)
#cv2.imshow("Cropped", roi)/
# cv2.imshow('mask', mask)
# cv2.imshow('original', image)
#cv2.imshow('Contrast', roi_contrast)
cv2.waitKey(0)

#HSV nozzle: (140, 175, 176) to (160, 242, 231)
#HSV filament: (28, 46, 51) to (100,255,255)

#21-8 (filament to nozzle)