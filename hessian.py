"""
This code shows a minimum working example for performing a hessian filter on
the 2d tomography scans.

I use pcolormesh instead of imshow because it's typically faster for plotting
but it doesn't preserve the dimensions of the pixels without some coercion.

I have commented out the image plotting since it takes a while and you know how to make images
"""

from skimage.filters import hessian
from skimage.measure import label, regionprops, regionprops_table
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd

# import a single scan
img = mpimg.imread('cropfigs/wg04sm_0009_blur2.tif')

# calculate the hessian filter
# documentation  can be found here: https://scikit-image.org/docs/dev/api/skimage.filters.html#skimage.filters.hessian
# the sigmas represent the scale of the filter that is
# they are the standard deviation of the assumed gaussian kernel
# that is used to differentiate the fractures from the 
# homogeneous rock. Essentially what these end up being is the 
# thickness of the border that is eventually deleted later.
# to learn more about hessian filters read this link: https://link.springer.com/chapter/10.1007%2F978-3-319-16811-1_40
result = hessian(img, sigmas=[2,2])

# creates a figure of the raw hessian filter output
# fig, ax = plt.subplots(1, 2, figsize=(14,8), sharex=True, sharey=True)

# ax[0].pcolormesh(img, cmap='Blues')
# ax[1].pcolormesh(result, cmap='cool_r')

# ax[0].set_title('image')
# ax[1].set_title('Hessian Noise Filter')
# fig.savefig('hessian.png', bbox_inches='tight')

# label is an automated function that labels all of the spaces found
# in the image. This works for basically any image filter that returns
# a matrix of zeros and ones afaik. It replaces the ones with the label
# number of the unique fracture that is found.
lab = label(result)

# this line removes the borders and replaces them with the same label
# as the homogenous rock.
lab[lab == 0] = 1
# fig, ax = plt.subplots(1, 2, figsize=(14,8), sharex=True, sharey=True)

# ax[0].pcolormesh(img, cmap='Blues')
# cbar = ax[1].pcolormesh(lab, cmap='nipy_spectral_r')

# ax[0].set_title('image')
# ax[1].set_title('labeled')
# fig.savefig('labeled_hessian.png', bbox_inches='tight')

# to create the data set for the fractures we can use regionprops_table. It
# is an automated function that creates a pandas dataframe from the labeled
# fractures. There are more properties that can be calculated than found
# here. To learn more about this function read here: https://scikit-image.org/docs/dev/api/skimage.measure.html#skimage.measure.regionprops_table
# to create data set for all slices one would need to import all of the images
# and perform the same steps as before for each image:
# df = pd.DataFrame()
# for img in images:
#     h = hessian(img)
#     l = label(h)
#     l[l == 0] = 1
#     rp = regionprops_table(l)
#     df = pd.concat([df, rp])
fracprops = pd.DataFrame(regionprops_table(lab, properties=['label', 'bbox', 'bbox_area', 'convex_area', 'eccentricity', 'filled_area', 'major_axis_length', 'minor_axis_length']))