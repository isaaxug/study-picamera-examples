from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.object_detection import non_max_suppression
import imutils
import time
import numpy as np
import cv2
import sys

class FaceDetector(object):
    def __init__(self, flip = True):
        self.vs = PiVideoStream(resolution=(800, 608)).start()
        self.flip = flip
        time.sleep(2.0)

        self.argvs = sys.argv
        self.face_cascade = cv2.CascadeClassifier('camera/processor/model/haarcascades/haarcascade_frontalface_default.xml')
        if len(self.argvs) >= 2 and "eyes" in self.argvs:
            self.eye_cascade = cv2.CascadeClassifier('camera/processor/model/haarcascades/haarcascade_eye.xml')

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        frame = self.process_image(frame)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def process_image(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 3)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            if len(self.argvs) >= 2 and "eyes" in self.argvs:
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        return frame
