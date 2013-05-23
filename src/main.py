#!/usr/bin/python

import cv2
import cv2.cv as cv
import numpy as np
from faceDetect import FaceDetect
from faceRecon import FaceRecon

fD = FaceDetect()
while(True):
    frame = fD.getFrame()
    rectangle = fD.detectFaces(frame)
    if rectangle is not None:

        print "\nPossible face at", rectangle.tolist()
        rectangle = rectangle.tolist()[0]

        cropped = fD.cropRectangle( (rectangle[2],rectangle[3]),(rectangle[0],rectangle[1]), frame )
        cv2.imshow("Face", cropped)

        cv2.rectangle(frame, (rectangle[0],rectangle[1]), (rectangle[2],rectangle[3]), (0,255,0), 5)

        print "BLUE",(rectangle[0],rectangle[1])
        cv2.circle(frame,(rectangle[0],rectangle[1]),5,(255,0,0),-1)

        print "RED",(rectangle[2],rectangle[3])
        cv2.circle(frame,(rectangle[2],rectangle[3]),5,(0,0,255),-1)

    cv2.imshow("FaceDetection", frame)

    if cv2.waitKey(5) == 27:
        cv2.imwrite("lastFrame.png", frame)
        cv2.imwrite("lastFace.png", cropped)
        break
cv2.destroyAllWindows()

