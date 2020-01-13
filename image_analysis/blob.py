# Standard imports
import cv2
import numpy as np;
 
# Read image
im = cv2.imread("contrast.jpg", cv2.IMREAD_GRAYSCALE)
 
 # Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()
 

params.filterByColor = True
params.blobColor = 226

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create(params)
 
# Detect blobs.
keypoints = detector.detect(im)
 
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)