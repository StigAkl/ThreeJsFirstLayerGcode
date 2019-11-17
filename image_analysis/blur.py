import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('octo.PNG')
kernel = np.ones((5,5),np.float32)/25
dst = cv2.filter2D(img,-1,kernel)

ret, thresh = cv2.threshold(dst, 222, 255, cv2.THRESH_BINARY)

plt.subplot(131),plt.imshow(img),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(dst),plt.title('Averaging')
plt.xticks([]), plt.yticks([])
plt.show()

