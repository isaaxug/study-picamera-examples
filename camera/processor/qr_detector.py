from imutils.video.pivideostream import PiVideoStream
import time
from datetime import datetime
import numpy as np
import cv2

from pyzbar import pyzbar

class QRDetector(object):
    def __init__(self, flip = False):
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
        decoded_objs = self.decode(frame)
        frame = self.draw(frame, decoded_objs)
        return frame

    def decode(self, frame):
        decoded_objs = pyzbar.decode(frame, scan_locations=True)
        for obj in decoded_objs:
            print(datetime.now().strftime('%H:%M:%S.%f'))
            print('Type: ', obj.type)
            print('Data: ', obj.data)
        return decoded_objs

    def draw(self, frame, decoded_objs):
        for obj in decoded_objs:
            left, top, width, height = obj.rect
            frame = cv2.rectangle(frame,
                                  (left, top),
                                  (left + width, height + top),
                                  (0, 0, 255), 2)
            data = obj.data.decode('utf-8')
            cv2.putText(frame,data,(left,top),cv2.FONT_HERSHEY_PLAIN, 2,(0, 0, 255))
        return frame
    

