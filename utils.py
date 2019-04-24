import random
import numpy as np
from image_transform import (rotate, resize, perspective, sp_noise)


# example function - how you can use it
def prepare_overlay(overlay):
    """
        Function for random transform overlay
    :param overlay: input overlay image
    :return: random transformed overlay image
    """
    # random resize image
    oh,ow,_ = overlay.shape # get original width and height
    op = oh / ow
    h = random.randint(75, int(oh/4)) # new height
    w = int(h / op) # new width
    overlay = resize(overlay, w, h)

    # add random noise
    prob = random.randint(0,1) / 100
    overlay = sp_noise(overlay, prob)

    # random perspective transform and width resize
    d = random.randint(0, int(h/4))
    d1 = random.randint(0, int(h/4))
    s = random.randint(0,1)
    src = np.float32([[0,0],[w,0],[0,h],[w,h]])
    if s == 0:        
        dst = np.float32([[0,d1],[w,0],[0,h-d],[w,h]]) 
    elif s == 1:    
        dst = np.float32([[0,0],[w,d1],[0,h],[w,h-d]]) 
    overlay = perspective(overlay, src, dst, w, h)
    overlay = resize(overlay, w-d*2, h)

    # random rotate
    angle = random.randint(-15, 15)
    overlay = rotate(overlay, angle)

    return overlay

def set_overlay(background, overlay, pos=(0,0)):
    """
        Function to overlay a transparent image on background.
    :param background: input color background image
    :param overlay: input transparent image (BGRA)
    :param pos:  position where the image to be set.
    :return: result image
    """
    
    h,w,_ = overlay.shape
    rows,cols,_ = background.shape
    y,x = pos[0],pos[1]
    
    for i in range(h):
        for j in range(w):
            if x+i >= rows or y+j >= cols:
                continue
            alpha = float(overlay[i][j][3]/255.0)
            background[x+i][y+j] = alpha*overlay[i][j][:3]+(1-alpha)*background[x+i][y+j]

    return background