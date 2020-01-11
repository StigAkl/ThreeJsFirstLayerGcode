import numpy as np
import cv2
from matplotlib import pyplot as plt

# def scale(image, scale):
#     height, width, depth = image.shape
#     imgScale = scale/width
#     newX,newY = image.shape[1]*imgScale, image.shape[0]*imgScale
#     return cv2.resize(image,(int(newX),int(newY)))    


img = cv2.imread('octo_first_layer.PNG', 1)

height, width, channels = img.shape

# img = cv2.medianBlur(img,5)

# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ret,thresh1 = cv2.threshold(gray,105,255,cv2.THRESH_BINARY)
# ret,thresh2 = cv2.threshold(gray,120,255,cv2.THRESH_BINARY)


# cv2.imshow("Thresh1", thresh1)
# cv2.imshow("Thresh2", thresh2)
# cv2.waitKey(0)

# cv2.imwrite("bin1.png", thresh1)
# cv2.imwrite("bin2.png", thresh# 2)
# cv2.imshow("img", gray)
# cv2.waitKey(0)



hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.imshow("HSV", hsv)

mask = cv2.inRange(hsv, (40, 40, 40), (200, 255,255))

imask = mask>0

green = np.zeros_like(img, np.uint8)
green[imask] = img[imask]

cv2.imshow("Green", green)
gray_image = cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)

res = cv2.bitwise_and(img,green,mask = mask)

cv2.imwrite("res.jpg", res)

res_read = cv2.imread("res.jpg", cv2.IMREAD_GRAYSCALE)

cv2.imshow("Resread", res_read)
# Apply cv2.threshold() to get a binary image
kernel = np.ones((5,5),np.float32)/25
thresh = cv2.threshold(res, 20 ,255, cv2.THRESH_BINARY_INV)[1]

#Add blur
blur_thresh = cv2.filter2D(thresh, -1, kernel)

# Find contours:
cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]


#Create blank image
blank_image = np.zeros((height,width,3), np.uint8)
blank_image[0:height, 0:width] = 255

valid_cnts = []
i = 1
while i < len(cnts):
    c = cnts[i]
    area = cv2.contourArea(c)

    if area > 25:
        cv2.drawContours(blank_image,[c], 0, (255,0,0), 1)
        valid_cnts.append(c)
    i += 1

print(thresh)
cv2.imshow("Mask", mask)
cv2.imshow("Img", blank_image)

cv2.waitKey(0)
