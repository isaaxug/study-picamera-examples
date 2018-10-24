from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np
import cv2

import os
import sys
import requests


try:
    SLACK_URL = os.environ['SLACK_URL']
    SLACK_TOKEN = os.environ['SLACK_TOKEN']
    SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
except KeyError as e:
    sys.exit('Couldn\'t find env: {}'.format(e))

net = cv2.dnn.readNetFromCaffe('/home/pi/models/MobileNetSSD_deploy.prototxt',
        '/home/pi/models/MobileNetSSD_deploy.caffemodel')
        

def upload():
    image = { 'file': open('hello.jpg', 'rb') }
    payload = {
        'filename': 'hello.jpg',
        'token': SLACK_TOKEN,
        'channels': [SLACK_CHANNEL],
    }
    requests.post(SLACK_URL, params=payload, files=image)


class PersonDetector(object):
    def __init__(self, flip = True):
        self.last_upload = time.time()
        self.vs = PiVideoStream(resolution=(800, 608)).start()
        self.flip = flip
        time.sleep(2.0)
        
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
        frame = imutils.resize(frame, width=300)
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        count = 0
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence < 0.2:
                continue

            idx = int(detections[0, 0, i, 1])
            if idx != 15:
                continue

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype('int')
            label = '{}: {:.2f}%'.format('Person', confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            count += 1
        
        if count > 0:
            print('Count: {}'.format(count))
            elapsed = time.time() - self.last_upload
            if elapsed > 60:
                cv2.imwrite('hello.jpg', frame)
                upload()
                self.last_upload = time.time()
                
        return frame
