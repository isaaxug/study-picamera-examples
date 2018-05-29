from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np
import cv2

class FaceDetector(object):
    def __init__(self, flip = True):
        self.vs = PiVideoStream(resolution=(800, 608)).start()
        self.flip = flip
        time.sleep(2.0)

        #opencvの顔分類器(CascadeClassifier)をインスタンス化する

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
        #opencvでframe(カラー画像)をグレースケールに変換
        #上記でグレースケールに変換したものをインスタンス化した顔分類器のdetectMultiScaleで処理し、顔の部分だけを切り出す
        #切り出した顔の座標配列をcv2.rectangleを使ってframe上に描画する

        #frameを返却する
