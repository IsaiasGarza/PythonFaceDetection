#!/usr/bin/python

import cv2
import cv2.cv as cv
import numpy as np
from PIL import Image, ImageOps

class ImageManipulation:
    def __init__(self, DEBUG=False):
        self.DEBUG = DEBUG
        print 'ImageManipulation : DEBUG is set to', self.DEBUG

    def getEqualized(self, img):
        return cv2.equalizeHist(img)

    def getGreyscale(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def saveImage(self, img, imgName='saved-image.png'):
        cv2.imwrite(imgName,img)

if __name__ == "__main__":
    DEBUG = True
