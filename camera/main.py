from flask import Flask, render_template, Response
#from processor.simple_streamer import SimpleStreamer
# from processor.pedestrian_detector import PedestrianDetector
from processor.motion_detector import MotionDetector
import time
import threading

#video_camera = SimpleStreamer(flip=False)
# video_camera = PedestrianDetector(flip=False)
video_camera = MotionDetector(flip=False)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, threaded=True)
