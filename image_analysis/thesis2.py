import numpy as np
import cv2


lower_color_bounds = cv2.Scalar(100, 0, 0)
upper_color_bounds = cv2.Scalar(225,80,80)

frame = cv2.imread('octo_first_layer.PNG', 1)

gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
mask = cv2.inRange(frame,lower_color_bounds,upper_color_bounds)
mask_rgb = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
frame = frame & mask_rgb
cv2.imshow('Frame',frame)
cv2.waitKey(0)