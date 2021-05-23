# -*- coding: utf-8 -*-
"""
Created on Fri May 21 09:26:01 2021

@author: Ricky
"""

import cv2
import numpy as np
from numpy import random
from numpy.random import randint
from matplotlib import pyplot as plt
import math

height,width= 299,299                                                       # Required size of the masks

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

def generate_masks(n, imsize, seed=0):
    im_centre = (int(width/2), int(height/2))
    x_bounds =  (int(0.1*width), int(width-0.1*width))                      # Bounds for the valid region of mask centres.
    y_bounds =  (int(0.1*height), int(height - 0.1*height))
    
    random.seed(seed)   # Set seed for repeatability

    centre_pts = sample_centre_pts(n, imsize, x_bounds, y_bounds)           # Get a random sample for the mask centres.
    
    startAngle = 0.0
    endAngle = 360.0
        
    for pt in centre_pts:
        size = abs(int(random.normal(50, 10)))                              # Random mask size.
        ratio = 2*random.random(1) + 1                                      # Ratio between length and width.
        
        centrex = int(pt[0])
        centrey = int(pt[1])
        
        angle = find_angle(im_centre, (centrex, centrey))                   # Get the angle between the centre of the image and the mask centre.
        angle = int(angle + random.normal(0.0, 5.0))                        # Base the angle of rotation on the above angle.
        
        mask = np.zeros((height,width), np.uint8)                           # Create blank canvas for the mask.

        mask = cv2.ellipse(mask, (centrex,centrey), (size, int(size*ratio)), 
                           angle, startAngle, endAngle, 
                           color=255, thickness=-1)                         # Insert a ellipse with the parameters defined above.
        
        # plt.imshow(mask, cmap='Greys_r')
        # plt.show()

generate_masks(100, (width,height))