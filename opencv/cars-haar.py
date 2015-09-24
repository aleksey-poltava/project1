import cv2 as cv
import urllib
import numpy as np
import time
from PIL import Image


class MotionDetectorContour:
    def __init__(self, ceil=15):
        self.ceil = ceil
        cv.cv.NamedWindow("Target", 1)

    def run(self):
        # Capture first frame to get size
        face_cascade = cv.CascadeClassifier('cars-cascade-11-08-2015.xml')
        stream = urllib.urlopen('http://213.221.150.136/mjpg/video.mjpg')
        count = 0
        height = 0
        width = 0
        bytes = ''
        frame = None
        while count <= 1:
            bytes += stream.read(16384)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b+2]
                bytes = bytes[b+2:]
                frame = cv.imdecode(np.fromstring(jpg, dtype=np.uint8), cv.CV_LOAD_IMAGE_COLOR)
                height, width, channels = frame.shape
                count += 1

        print height, width

        cursurface = 0 #Hold the current surface that have changed

        grey_image = cv.cv.CreateImage([width, height], cv.cv.IPL_DEPTH_8U, 1)
        moving_average = cv.cv.CreateImage([width, height], cv.cv.IPL_DEPTH_32F, 3)
        difference = None

        # draw net 75% of frame size
        second_line = int(width/2)
        first_line = 10
        third_line = width
        # define crossing time list
        marks_crossing_list = [0,0,0]
        bytes=''
        while True:
            bytes += stream.read(16384)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b+2]
                bytes = bytes[b+2:]
                frame = cv.imdecode(np.fromstring(jpg, dtype=np.uint8), cv.CV_LOAD_IMAGE_COLOR)
                if frame is not None:
                    cars = face_cascade.detectMultiScale(frame, 1.1, 2)
                    ncars = 0
                    for (x,y,w,h) in cars:
                        cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                        ncars = ncars + 1
                    print(ncars)
                    cv.imshow('Target', np.asarray(frame[:,:]))
                    if cv.cv.WaitKey(1) & 0xFF == ord('q'):
                        break

if __name__=="__main__":
    t = MotionDetectorContour()
    t.run()
