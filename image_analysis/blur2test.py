import numpy as np
import cv2
from matplotlib import pyplot as plt
from shape_detector import ShapeDetector
import cv2

image = cv2.imread('octo.PNG')
ratio = image.shape[0] / image.shape[1]
kernel = np.ones((5,5),np.float32)/25

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 199 ,255, cv2.THRESH_BINARY_INV)[1]

blur_thresh = cv2.filter2D(thresh, -1, kernel)


cnts = cv2.findContours(blur_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]


circles = 0
squares = 0
pentagons = 0
rectangles = 0

largest_area = -1
largest_area_shape = "none"
largest_contour = None
for c in cnts:
    detector = ShapeDetector()
    area = cv2.contourArea(c)
    #cv2.drawContours(image,[c], 0, (0,0,255), 1)


    M = cv2.moments(c)

    shape = detector.detect(c)
    
    if shape == "circle":
        circles+=1
    elif shape == "square":
        squares+=1
    elif shape == "pentagon":
        pentagons+=1
    elif shape == "rectangle":
        rectangles+=1

    if area > largest_area:
        largest_area = area
        largest_area_shape=shape
        largest_contour = c

    #print(area, shape)

cv2.drawContours(image,[largest_contour], 0, (0,255,0), 1)
print("Largest area: ", largest_area)
print("Largest area shape: ", largest_area_shape)

M = cv2.moments(largest_contour)
cx = int((M["m10"] / M["m00"]) * ratio)
cy = int((M["m01"] / M["m00"]) * ratio)

cv2.putText(image, largest_area_shape, (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 1)

print("--------- STATISTICS ---------")
print("Squares:", squares)
print("Circles:", circles)
print("Rectangles: ", rectangles)
print("Pentagons: ", pentagons)

cv2.imshow('image', image)
cv2.imshow('thresh', blur_thresh)
cv2.waitKey(0)