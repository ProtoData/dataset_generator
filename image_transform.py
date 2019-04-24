import os
import cv2
import random
import numpy as np


def resize(image, width, height):
    """
        Image resize function.
    :param image: input image
    :param width: image output width
    :param height: image output height
    """

    image = cv2.resize(image, (width, height))

    return image

def rotate(image, angle):
    """
        Function for overlay rotate.
    :param image: input overlay
    :param angle: angle for image rotate
    :return: result image
    """
   
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    image = cv2.warpAffine(image, M, (nW, nH))    

    return image

def perspective(image, src, dst, w, h):
    """
        Image percpective transform function.
    :param image: input image
    :param src: original image corners points array
    :param dst: output image corners points array
    :param w: image width
    :param h: image height
    :return: result image
    """
    M = cv2.getPerspectiveTransform(src, dst)

    image = cv2.warpPerspective(image, M, (w,h))

    return image

def increase_brightness(image, value=30):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    return image

def sp_noise(image, prob):
    '''
        Add salt and pepper noise to image
    :param image: input image
    :param prob: probability of the noise
    '''
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]

    return output
