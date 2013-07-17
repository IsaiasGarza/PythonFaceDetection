#!/usr/bin/python

import cv2
import cv2.cv as cv
import numpy as np
from pyfaces.pyfaces import PyFaces

class FaceRecon:
    def __init__(self, DEBUG=False):
        self.DEBUG = DEBUG
        if DEBUG:
            print 'FaceRecon : DEBUG set to', self.DEBUG

    def train(self):
        print 'Im training'
    
    def recognize(self,img, directory, faces, thresh, resize, show=None):
        if show is None:
            show = self.DEBUG
        faceRecon = PyFaces(img, directory, faces, thresh, resize)
        if show:
            distance, match = faceRecon.show()
        else:
            distance, match = faceRecon.match()
        return distance,match

    def confFile(self):
        print 'Im conf file'

