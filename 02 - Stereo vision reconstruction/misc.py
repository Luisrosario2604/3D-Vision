
__author__ = "PMN"

import numpy as np
from numpy import linalg as la
from scipy import ndimage
import matplotlib.pyplot as ppl
#import re
#import pdb

from mpl_toolkits.mplot3d import Axes3D


def skew(v):
    """Compute the skew-symmetric matrix of a vector."""
    A = np.array([ [0, -v.item(2), v.item(1)], 
                [v.item(2), 0, -v.item(0)],
                [-v.item(1), v.item(0), 0] ])
    return A
    

def plot3D(x, y, z, *args):    
    fig = ppl.gcf()
    ax = Axes3D(fig)
    ax.plot3D(x, y, z, *args)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    scaling = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz']);    
    ax.auto_scale_xyz(*[[np.min(scaling), np.max(scaling)]]*3)
    ppl.draw()
    return ax
    
def plothom(points, *args, **kwargs):
    """Plot a set of points given in homogeneous coordinates."""
    p = points / points[2,:]
    return ppl.plot(p[0,:], p[1,:], *args, **kwargs)


def askpoints(image1, image2):
    """Ask for a list of point correspondences between two images."""
    
    points1 = []
    points2 = []
    
    # Prepare the two images.
    fig = ppl.gcf()
    fig.clf()
    ax1 = fig.add_subplot(121)
    ax1.imshow(image1)
    ax1.axis('image')
    ax2 = fig.add_subplot(122)
    ax2.imshow(image2)
    ax2.axis('image')
    ppl.draw()
    
    ax1.set_xlabel("Choose a point in left image (or right click to end)")
    p1 = ppl.ginput(1, timeout=-1, show_clicks=False, mouse_pop=2, mouse_stop=3)
    while len(p1) != 0:
        p1 = p1[0]
        ax1.plot(p1[0], p1[1], '.r')
        ax1.set_xlabel('')
        ax2.set_xlabel("Choose the matching point in right image")
        
        p2 = ppl.ginput(1, timeout=-1, show_clicks=False, mouse_pop=2, mouse_stop=3)
        if len(p2) == 0:
            break
        p2 = p2[0]
        ax2.plot(p2[0], p2[1], '.r')
        
        points1.append(p1)
        points2.append(p2)
        
        ax2.set_xlabel('')
        ax1.set_xlabel("Choose a point in left image (or right click to end)")
        p1 = ppl.ginput(1, timeout=-1, show_clicks=False, mouse_pop=2, mouse_stop=3)
    
    ax1.set_xlabel('')
    ax2.set_xlabel('')
    ppl.draw()
    
    # pdb.set_trace()

    # swap point co-ordinates
    
    num_points = len(points1)
    points1 = np.vstack((np.array(points1).T[:,:],np.ones(num_points)))
    points2 = np.vstack((np.array(points2).T[:,:],np.ones(num_points)))
    return points1, points2


