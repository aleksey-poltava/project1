# Inspired by from https://github.com/mattwilliamson/Motion-Tracker/blob/master/track.py

import cv2.cv as cv
import time

class MotionDetectorContour:
    def __init__(self,ceil=15):
        self.ceil = ceil
        self.capture = cv.CaptureFromCAM(0)
        cv.NamedWindow("Target", 1)

    def run(self):
        # Capture first frame to get size
        frame = cv.QueryFrame(self.capture)
        frame_size = cv.GetSize(frame)

        width = frame.width
        height = frame.height

        surface = width * height #Surface area of the image
        cursurface = 0 #Hold the current surface that have changed

        grey_image = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
        moving_average = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_32F, 3)
        difference = None

        # draw net 75% of frame size
        second_line = int(width/2)
        first_line = int(second_line / 2)
        third_line = int(width) - first_line
        frame_center_height =  height/2
        interest_width = width * 0.75
        interest_hight = height * 0.75
        # define crossing time list
        marks_crossing_list = [0,0,0]

        while True:
            color_image = cv.QueryFrame(self.capture)

            # draw lines net
            # cv.Line(color_image, (int(frame_center_width), int(frame_center_height-interest_hight/2)),(int(frame_center_width), int(frame_center_height+interest_hight/2)),(0,255,255),1)
            # for i in range(0, 3):
            #    print i
            #    cv.Line(color_image, (int(frame_center_width-i*interest_width/5), int(frame_center_height-interest_hight/2)),(int(frame_center_width-i*interest_width/5),int(frame_center_height+interest_hight/2)),(0,255,255),1)
            #    cv.Line(color_image, (int(frame_center_width+i*interest_width/5), int(frame_center_height-interest_hight/2)),(int(frame_center_width+i*interest_width/5),int(frame_center_height+interest_hight/2)),(0,255,255),1)

            # cv.Line(color_image, (int(frame_center_width-interest_width/2+interest_width/10), int(frame_center_height-interest_hight/2)),(int(frame_center_width-interest_width/2+interest_width/10),int(frame_center_height+interest_hight/2)),(0,255,255),1)

            cv.Smooth(color_image, color_image, cv.CV_GAUSSIAN, 3, 0) #Remove false positives

            if not difference: #For the first time put values in difference, temp and moving_average
                difference = cv.CloneImage(color_image)
                temp = cv.CloneImage(color_image)
                cv.ConvertScale(color_image, moving_average, 1.0, 0.0)
            else:
                cv.RunningAvg(color_image, moving_average, 0.020, None) #Compute the average

            # Convert the scale of the moving average.
            cv.ConvertScale(moving_average, temp, 1.0, 0.0)

            # Minus the current frame from the moving average.
            cv.AbsDiff(color_image, temp, difference)

            #Convert the image so that it can be thresholded
            cv.CvtColor(difference, grey_image, cv.CV_RGB2GRAY)
            cv.Threshold(grey_image, grey_image, 70, 255, cv.CV_THRESH_BINARY)

            cv.Dilate(grey_image, grey_image, None, 18) # to get object blobs
            cv.Erode(grey_image, grey_image, None, 10)

            # Find contours
            storage = cv.CreateMemStorage(0)
            contours = cv.FindContours(grey_image, storage, cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_SIMPLE)

            backcontours = contours # Save contours

            # while contours: #For all contours compute the area
            # cursurface += cv.ContourArea(contours)
            # contours = contours.h_next()

            idx =0
            while contours: # For all contours draw rectangle
                idx += 1
                x,y,w,h = cv.BoundingRect(contours) # w - width, h - height
                cv.Circle(color_image,(x+w/2,y+h/2), 7, (0,255,0), -1) # draw circle in center of rectangle
                if (first_line - 15) < int(x+w/2) < (first_line + 15):
                    marks_crossing_list[0] = int(round(time.time() * 1000))
                    print "first"
                if (second_line - 15) < int(x+w/2) < (second_line + 15) and marks_crossing_list[0] != 0:
                    marks_crossing_list[1] = int(round(time.time() * 1000))
                    print "second"
                if (third_line - 15) < int(x+w/2) < (third_line + 15) and marks_crossing_list[0] != 0 and marks_crossing_list[1] != 0:
                    marks_crossing_list[2] = int(round(time.time() * 1000))
                    crossing_time_delta = marks_crossing_list[2] - marks_crossing_list[0]
                    print "third crossing delta: ", crossing_time_delta
                    marks_crossing_list = [0,0,0]
                    if 1000 < crossing_time_delta < 3000:
                        print "current time to write to DB ", time.strftime("%d:%m:%Y:%H:%M:%S")
                        print "crossing time milliseconds is must be bigger than 2s and smaller than 3s ", crossing_time_delta
                        print "all cleared"

                cv.Rectangle(color_image,(x,y),(x+w,y+h),(0,255,0),2)
                contours = contours.h_next() # Increment contour number

            # avg = (cursurface*100)/surface #Calculate the average of contour area on the total size
            # if avg > self.ceil:
            #    print "Something is moving !"
            #print avg,"%"
            cursurface = 0 #Put back the current surface to 0

            #Draw the contours on the image
            _red =  (0, 0, 255); #Red for external contours
            _green =  (0, 255, 0);# Gren internal contours
            levels=1 #1 contours drawn, 2 internal contours as well, 3 ...
            cv.DrawContours (color_image, backcontours,  _red, _green, levels, 2, cv.CV_FILLED)

            cv.ShowImage("Target", color_image)
            # Listen for ESC or ENTER key
            if cv.WaitKey(1) & 0xFF == ord('q'):
                break

if __name__=="__main__":
    t = MotionDetectorContour()
    t.run()