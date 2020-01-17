# Standard imports
import cv2
import numpy as np;
 
# Read image
im = cv2.imread("blob.jpg", cv2.IMREAD_GRAYSCALE)
 
# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector()
 
# Detect blobs.
print("ok")
keypoints = detector.detect(im)
print("ka")
cv2.imshow("Im", im)
cv2.waitKey(0)