import cv2
import numpy as np
from numpy import random
from numpy.random import randint
from matplotlib import pyplot as plt
import math

def find_angle(pos1, pos2, ret_type = 'deg'):
    # Find the angle between two pixel points, pos1 and pos2.
    angle_rads = math.atan2(pos2[1] - pos1[1], pos2[0] - pos1[1])
    
    if ret_type == 'rads':
        return angle_rads
    elif ret_type == 'deg':
        return math.degrees(angle_rads)                                     # Convert from radians to degrees.


def sample_centre_pts(n, imsize, xlimits=(50,250), ylimits=(50,250)):
    # Function to generate random sample of points for the centres of the elliptical masks.
    pts = np.empty((n,2))                                                   # Empty array to hold the final points
    
    count=0
    while count < n:
        sample = randint(0, imsize[0], (n,2))[0]                            # Assumes im_size is symmetric

        # Check the point is in the valid region.
        is_valid = (sample[0] < xlimits[0]) | (sample[0] > xlimits[1]) |     \
                (sample[1] < ylimits[0]) | (sample[1] > ylimits[1])
        
        if is_valid:                                                        # Only take the point if it's within the valid region.
            pts[count] = sample
            count += 1

    return pts

def generate_ellipse_mask(imsize, mask_size, seed=None):
    im_centre = (int(imsize[0]/2), int(imsize[1]/2))
    x_bounds =  (int(0.1*imsize[0]), int(imsize[0] - 0.1*imsize[0]))        # Bounds for the valid region of mask centres.
    y_bounds =  (int(0.1*imsize[1]), int(imsize[1] - 0.1*imsize[1]))
    
    if seed is not None:
      random.seed(seed)   # Set seed for repeatability

    n = 1 + random.binomial(1, 0.3)                                         # The number of masks per image either 1 (70% of the time) or 2 (30% of the time) 
    centre_pts = sample_centre_pts(n, imsize, x_bounds, y_bounds)           # Get a random sample for the mask centres.
    
    startAngle = 0.0
    endAngle = 360.0                                                        # Draw full ellipses (although part may fall outside the image)
        
    mask = np.zeros((imsize[0], imsize[1], 1), np.float32)                  # Create blank canvas for the mask.

    for pt in centre_pts:
        size = abs(int(random.normal(mask_size, mask_size/5.0)))            # Randomness introduced in the mask size. 
        ratio = 2*random.random(1) + 1                                      # Ratio between length and width. Sample from Unif(1,3).
        
        centrex = int(pt[0])
        centrey = int(pt[1])
        
        angle = find_angle(im_centre, (centrex, centrey))                   # Get the angle between the centre of the image and the mask centre.
        angle = int(angle + random.normal(0.0, 5.0))                        # Base the angle of rotation on the above angle.
        
        mask = cv2.ellipse(mask, (centrex,centrey), (size, int(size*ratio)), 
                           angle, startAngle, endAngle, 
                           color=1, thickness=-1)                         # Insert a ellipse with the parameters defined above.

    mask = np.minimum(mask, 1.0)                                          # This may be redundant.
    mask = np.transpose(mask, [2, 0, 1])                                  # bring the 'channel' axis to the first axis.
    mask = np.expand_dims(mask, 0)                                        # Add in extra axis at axis=0 - resulting shape (1, 1, )

    return mask


test_mask = generate_ellipse_mask(imsize = (224,224), mask_size = 40)
from matplotlib import pyplot as plt
plt.imshow(test_mask[0][0], cmap='Greys_r')
plt.show()