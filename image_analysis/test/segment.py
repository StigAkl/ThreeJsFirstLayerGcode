# import the necessary packages
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io
import matplotlib.pyplot as plt
import argparse
 
# construct the argument parser and parse the arguments

 
# load the image and convert it to a floating point data type
image = img_as_float(io.imread("IMG_20191117_154602.jpg"))

# loop over the number of segments

for numSegments in (10,100,200):

	segments = slic(image, n_segments = numSegments, sigma = 5)
 
	# show the output of SLIC
	fig = plt.figure("Superpixels -- %d segments" % (numSegments))
	ax = fig.add_subplot(1, 1, 1)
	ax.imshow(mark_boundaries(image, segments))
	plt.axis("off")
 
# show the plots
plt.show()