#!/usr/bin/python

import cv2
import cv2.cv as cv
import numpy as np

HAAR_FRONTAL_FACE = "./src/haarcascade_frontalface_alt.xml"
VIDEO_FILE = "/media/sdb1/Dropbox/FIME/8voSemestre/VisionComputacional/project/media/base1.avi"

class FaceDetect:
    def __init__(self):
        # Constructor for the videocapture, 0 because there is only one webcam connected
        # instead of 0, a video file could be passed as parameter
        self.vidCap = cv2.VideoCapture(0)
        #self.vidCap = cv2.VideoCapture(VIDEO_FILE)

    def getFrame(self):
        _,frame = self.vidCap.read() # tuple contains a return value and image
        return frame

    def detectFaces(self,img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # image to grayscale
        img = cv2.equalizeHist(img) # image equalized

        # cascade classifier for object detectio
        # HAAR_FRONTAL_FACE is the path to the file from which the classifier is loaded
        casClassif = cv2.CascadeClassifier(HAAR_FRONTAL_FACE)
        rectangles = casClassif.detectMultiScale( img, scaleFactor=1.3,
                                                  minNeighbors=4, minSize=(30, 30),
                                                  flags = cv.CV_HAAR_SCALE_IMAGE )
        if len(rectangles) == 0:
            return

        if len(rectangles) > 1:
            for i in range(0, len(rectangles)):
                re = rectangles[i]
                print re
                re[:,:2] += re[:,2]
                rectangles[i] = re
        else:
            rectangles[:,:2] += rectangles[:,2]
        return rectangles

    def cropRectangle(self, (x1,y1), (x2,y2), original):
        width = x2-x1
        height = y2-y1
        size = (width, height)

        print "W:", width, "H:", height
        cropped = cv.CreateImage(( size ), 8, 3) #  CreateImage( CvSize size, int depth, int channels  )
        src_region = cv.GetSubRect(cv.fromarray(original), (x1, y1, width, height) ) # GetSubRect( img, (pos_left, pos_top, width, height) )
        cv.Copy(src_region, cropped)
        cropped = np.asarray(cropped[:,:])
        return cropped

if __name__ == "__main__":
    fD = FaceDetect()
    storage = cv.CreateMemStorage()
    i = 0
    while(1):
        frame =fD.getFrame()
        rectangle = fD.detectFaces(frame)
        if rectangle is not None:

            print "\nPossible face at", rectangle.tolist()
            rectangle = rectangle.tolist()[0]

            cropped = fD.cropRectangle( (rectangle[2],rectangle[3]),(rectangle[0],rectangle[1]), frame )
            cv2.imshow("Face", cropped)
            i+=1

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
