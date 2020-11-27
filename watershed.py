"""
This code shows a minimum working example to using the watershed detection
algorithm.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
import matplotlib.image as mpimg

from skimage.segmentation import watershed
from skimage.feature import peak_local_max

img = mpimg.imread('cropfigs/wg04sm_0009_blur2.tif')


# calculates the euclidean distance of a pixel from the background image
# The euclidean distance transform gives values of the euclidean distance:
#               n
# y_i = sqrt(sum (x[i]-b[i])**2)
#               i
# where b[i] is the background point (value 0) with the smallest Euclidean distance to input points x[i], and n is the number of dimensions. You can read more about this function here: https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.morphology.distance_transform_edt.html
distance = ndi.distance_transform_edt(img)

# find the local peaks for each fracture in the image
local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((3, 3)), labels=img)
# creates labels similar to the the label function in the hessian code.
# Here I only take the labels (the first item in the returned tuple).
# The second item is the number of features found. You can read more about this here: https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.label.html
markers = ndi.label(local_maxi)[0]

# applies the watershed algorithm to labeled image. You can read more about this here: https://scikit-image.org/docs/dev/api/skimage.segmentation.html#skimage.segmentation.watershed
labels = watershed(-distance, markers, mask=img)