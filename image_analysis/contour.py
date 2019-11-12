from shape_detector import ShapeDetector
import argparse
import imutils
import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])
resized = imutils.resize(img, width=300)
ratio = img.shape[0] / float(resized.shape[0])

gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5),2)
thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]

circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
output = img.copy()
if circles is not None:
    print("Not none")

    circles = np.round(circles[0, :]).astype("int")

    num_circles = 0
    for(x,y,r) in circles: 
        num_circles+=1
        cv2.circle(output, (x,y), r, (0, 255,0), 4)
        cv2.rectangle(output,(x - 5, y-5), (x+5, y+5), (0, 128, 255), -1)

        cv2.imshow("output", np.hstack([img, output]))
        cv2.waitKey(0)

print("Circles: ", num_circles)
# cv2.imshow("Image", blurred)
# cv2.waitKey(0)

# cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)

# detector = ShapeDetector()


# for c in cnts: 
#     M = cv2.moments(c)
#     cx = int((M["m10"] / M["m00"]) * ratio)
#     cy = int((M["m01"] / M["m00"]) * ratio)
#     shape = detector.detect(c)
#     c = c.astype("float")
#     c *= ratio
    
#     print(shape)
#     c = c.astype("int")
#     cv2.drawContours(img, [c], -1, (0,255,0),2)
#     cv2.putText(img, shape, (cx,cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
#     cv2.imshow("Image", img)
#     cv2.waitKey(0)