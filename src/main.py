#!/usr/bin/python

import cv2
import cv2.cv as cv
import numpy as np

from faceDetect import FaceDetect
from faceRecon import FaceRecon
from imageManipulation import ImageManipulation

from sys import argv

DEBUG = False
SHOW = False

try:
    image = argv[1]
    directory = argv[2]
except IndexError:
    exit('Wrong options')
faces = None
threshold = 0.5
resize = True

fR = FaceRecon(DEBUG)
dist, match = fR.recognize(image, directory,faces, threshold,resize)

if match is not None:
    f = open('index.dat')
    for line in f:
        if match in line:
            l = line.split()
            name = l[1]
            break
    f.close()
    print 'Known person:', name
    #print 'The image "%s" matches "%s" with a distance of "%s"' % (image, match, dist)
else:
    print 'Unknown person'

exit()

########################################################
#
# Despues de esto iba la implementacion en opencv
#
########################################################


fD = FaceDetect(DEBUG)
fR = FaceRecon(DEBUG)
iM = ImageManipulation(DEBUG)
options = '\n--------------------\n' + \
    '1 : Training\n' + \
    '2 : Detect and Recon\n' + \
    'q : quit' + \
    '\n--------------------\n'

action = str(raw_input(options))
exit('Wrong option') if action not in '12qQ' else None
exit() if action == 'q' else None

i = 0
while(True):
    frame = fD.getFrame()
    rectangle = fD.detectFaces(frame)
    if rectangle is not None: # When a face is detected

        rectangle = rectangle.tolist()[0]

        # Crop face from frame, convert to greyscale and normalize
        cropped = fD.cropRectangle( (rectangle[2],rectangle[3]),(rectangle[0],rectangle[1]), frame )
        cropped = iM.getGreyscale(cropped)
        cropped = iM.getEqualized(cropped)

        # Draw green rectangle around face
        color = (0, 255, 0)
        cv2.rectangle(frame, (rectangle[0],rectangle[1]), (rectangle[2],rectangle[3]), color, 5)

        if action == '1': #Training
            # Collect many frames of the face (20, 50, 100, 2000, etc). The more the better
            # Standarize frames size
            # Save frames to a directory
            # Update the file that maps the images with a name, something like
            #    1 Juan media/Juan/Juan_1.png
            #    1 Juan media/Juan/Juan_2.png
            #    2 Raul media/Raul/Raul_1.png
            #    2 Raul media/Raul/Raul_2.png
            # Train the program, try with createEigenFaceRecognizer
            # Also consider using LBPH
            pass
        elif action == '2': #Recognize
            pass

        if DEBUG:
            print 'BLUE',(rectangle[0],rectangle[1])
            cv2.circle(frame,(rectangle[0],rectangle[1]),5,(255,0,0),-1)
            print 'RED',(rectangle[2],rectangle[3])
            cv2.circle(frame,(rectangle[2],rectangle[3]),5,(0,0,255),-1)
            if SHOW:
                cv2.imshow("Face", cropped)
        i+=1 # closes if rectangle is not None

    if SHOW:
        cv2.imshow('FaceDetection', frame)

    if cv2.waitKey(5) == 27:
        try:
            print type(frame), frame.shape, len(frame), len(frame[0])
            cv2.imwrite('lastFrame.png', frame)
            cv2.imwrite('lastFace.png', cropped)
        except NameError: print 'No faces detected'
        break
cv2.destroyAllWindows()

