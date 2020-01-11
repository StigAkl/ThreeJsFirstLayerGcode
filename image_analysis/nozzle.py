import numpy as np
import cv2

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

    print("Center x: {}".format(xd))
    print("Center y: {}".format(yd))

    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(original, (x, y), (x + w, y + h), (36,255,12), 2)

print("(x1, y1) = ({}, {})".format(minHorizontal, minVertical))
print("(x2, y2) = ({}, {})".format(maxHorizontal, minVertical))
print("(x3, y3) = ({}, {})".format(maxHorizontal, maxVertical))
print("(x4, y4) = ({}, {})".format(minHorizontal, maxVertical))

roi = original[minVertical:maxVertical, minHorizontal:maxHorizontal]

cv2.imshow("Cropped", roi)
cv2.imshow('mask', mask)
cv2.imshow('original', original)
cv2.waitKey(0)

#HSV nozzle: (140, 175, 176) to (160, 242, 231)
#HSV filament: (28, 46, 51) to (100,255,255)