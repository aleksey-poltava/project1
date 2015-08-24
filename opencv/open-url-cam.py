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
                    color_image = cv.cv.CreateImageHeader((frame.shape[1], frame.shape[0]), cv.IPL_DEPTH_8U, 3)
                    cv.cv.SetData(color_image, frame.tostring(), frame.dtype.itemsize * 3 * frame.shape[1])
                    cv.cv.Smooth(color_image, color_image, cv.cv.CV_GAUSSIAN, 3, 0) #Remove false positives
                    if not difference: #For the first time put values in difference, temp and moving_average
                        difference = cv.cv.CloneImage(color_image)
                        temp = cv.cv.CloneImage(color_image)
                        cv.cv.ConvertScale(color_image, moving_average, 1.0, 0.0)
                    else:
                        cv.cv.RunningAvg(color_image, moving_average, 0.020, None) #Compute the average

                    # Convert the scale of the moving average.
                    cv.cv.ConvertScale(moving_average, temp, 1.0, 0.0)

                    # Minus the current frame from the moving average.
                    cv.cv.AbsDiff(color_image, temp, difference)

                    #Convert the image so that it can be thresholded
                    cv.cv.CvtColor(difference, grey_image, cv.cv.CV_RGB2GRAY)
                    cv.cv.Threshold(grey_image, grey_image, 120, 255, cv.cv.CV_THRESH_BINARY)

                    cv.cv.Dilate(grey_image, grey_image, None, 18) # to get object blobs
                    cv.cv.Erode(grey_image, grey_image, None, 10)

                    # Find contours
                    storage = cv.cv.CreateMemStorage(0)
                    contours = cv.cv.FindContours(grey_image, storage, cv.cv.CV_RETR_EXTERNAL, cv.cv.CV_CHAIN_APPROX_SIMPLE)

                    # Save contours
                    backcontours = contours

                    idx =0
                    while contours: # For all contours draw rectangle
                        idx += 1
                        x,y,w,h = cv.cv.BoundingRect(contours) # w - width, h - height
                        cv.cv.Circle(color_image, (x+w/2,y+h/2), 7, (0,255,0), -1) # draw circle in center of rectangle
                        if (120 < (x+w) < 200) and\
                                (420 < y < 440):
                            marks_crossing_list[0] = int(round(time.time() * 1000))
                            print "first time: ", marks_crossing_list[0]
                        cv.cv.Rectangle(color_image,(x,y),(x+w,y+h),(0,255,0),2)
                        contours = contours.h_next() # Increment contour number

                    _red = (0, 0, 255) #Red for external contours
                    _green = (0, 255, 0) # Gren internal contours
                    levels = 1 #1 contours drawn, 2 internal contours as well, 3 ...
                    cv.cv.DrawContours(color_image, backcontours,  _red, _green, levels, 2, cv.cv.CV_FILLED)

                    cv.imshow('Target', np.asarray(color_image[:,:]))
                    if cv.cv.WaitKey(1) & 0xFF == ord('q'):
                        break

if __name__=="__main__":
    t = MotionDetectorContour()
    t.run()