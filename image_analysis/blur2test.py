import numpy as np
import cv2
from matplotlib import pyplot as plt
from shape_detector import ShapeDetector
import cv2


def has_same_contour(c1, cnts):
    for cnt in cnts:
        if np.array_equal(cnt[0], c1[0]):
            return True

    return False

def scale(image, scale):
    height, width, depth = image.shape
    imgScale = scale/width
    newX,newY = image.shape[1]*imgScale, image.shape[0]*imgScale
    return cv2.resize(image,(int(newX),int(newY)))    

image = scale(cv2.imread('octo.PNG'), 700)
image_fail = scale(cv2.imread('octo_fail.PNG'), 700)

ratio = image.shape[0] / image.shape[1]
kernel = np.ones((5,5),np.float32)/25

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 210 ,255, cv2.THRESH_BINARY_INV)[1]

blur_thresh = cv2.filter2D(thresh, -1, kernel)


cnts = cv2.findContours(blur_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]


circles = 0
squares = 0
pentagons = 0
rectangles = 0

circles_fail= 0
squares_fail = 0
pentagons_fail = 0
rectangles_fail = 0

ratio_fail = image_fail.shape[0] / image_fail.shape[1]
kernel_fail = np.ones((5,5),np.float32)/25

gray_fail = cv2.cvtColor(image_fail, cv2.COLOR_BGR2GRAY)
thresh_fail = cv2.threshold(gray_fail, 210 ,255, cv2.THRESH_BINARY_INV)[1]

blur_thresh_fail = cv2.filter2D(thresh_fail, -1, kernel_fail)


cnts_fail = cv2.findContours(blur_thresh_fail, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts_fail = cnts_fail[0] if len(cnts_fail) == 2 else cnts_fail[1]


largest_area = -1
largest_area_shape = "none"
largest_contour = None

# count = 0
# for c in cnts:
#     cv2.drawContours(image,[c], 0, (0,0,255), 1)
#     print(count)
#     cv2.imshow("image", image)
#     cv2.waitKey(0)
#     count += 1

# count = 0

# for c in cnts_fail:
#     cv2.drawContours(image_fail,[c], 0, (0,0,255), 1)
#     print(count)
#     cv2.imshow("image_fail", image_fail)
#     cv2.waitKey(0)
#     count += 1

#print(np.array_equal(cnts[76], cnts_fail[58]))

print(cnts[76][1])
print(cnts_fail[58][1])

print(has_same_contour(cnts[76], cnts_fail))

num_fails = 0
for c in cnts:
    if not has_same_contour(c, cnts_fail):
        cv2.drawContours(image_fail,[c], 0, (0,0,255), 1)
        num_fails+=1

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

for c in cnts_fail:
    detector = ShapeDetector()
    area = cv2.contourArea(c)
    #cv2.drawContours(image_fail,[c], 0, (0,0,255), 1)

    M = cv2.moments(c)

    shape = detector.detect(c)

    if shape == "circle":
        circles_fail+=1
    elif shape == "square":
        squares_fail+=1
    elif shape == "pentagon":
        pentagons_fail+=1
    elif shape == "rectangle":
        rectangles_fail+=1

print("Largest area: ", largest_area)
print("Largest area shape: ", largest_area_shape)

M = cv2.moments(largest_contour)
cx = int((M["m10"] / M["m00"]) * ratio)
cy = int((M["m01"] / M["m00"]) * ratio)

#cv2.putText(image, largest_area_shape, (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 1)

print("--------- STATISTICS ---------")
print("Squares:", abs(squares-squares_fail))
print("Circles:", abs(circles-circles_fail))
print("Rectangles: ", abs(rectangles-rectangles_fail))
print("Pentagons: ", abs(pentagons-pentagons_fail))

total = squares+circles+rectangles+pentagons
total_fail = squares_fail+circles_fail+rectangles_fail+pentagons_fail
diff = abs(total_fail-total)

print("Polygon error: " + str(round(diff / total * 100, 2)) + "%")
cv2.putText(image_fail, "Polygon error: " + str(round(diff / total * 100, 2)) + "%", (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 1)
cv2.imshow('image', image)
cv2.imshow('image_fail', image_fail)
#cv2.imshow('thresh', blur_thresh)
cv2.waitKey(0)