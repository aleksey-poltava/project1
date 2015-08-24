import cv2
import time

face_cascade = cv2.CascadeClassifier('cars-cascade-11-08-2015.xml')
vc = cv2.VideoCapture('road-08-08-2015.avi')

if vc.isOpened():
    rval , frame = vc.read()
else:
    rval = False

# init params
ncars = 0
roi_crossing_time = 0
roi_crossing_time_cur = 0
frame_counter_stop = 0
num_cars_cur = 0

while rval:
    rval, frame = vc.read()

    # car detection.
    cars = face_cascade.detectMultiScale(frame, 1.1, 2)

    for (x,y,w,h) in cars:
        cv2.rectangle(frame,(x, y),(x+w, y+h),(0,255,0),2)
        roi_crossing_time_cur = int(round(time.time() * 1000))
        if (120 < (x+w/2) < 300) and (420 < (y+h/2) < 480):
            if roi_crossing_time_cur - roi_crossing_time > 500:
                ncars += 1
                roi_crossing_time = roi_crossing_time_cur

    print("Number of cars = ", ncars)
    # show result
    cv2.imshow("Result",frame)
    cv2.waitKey(1);
vc.release()
