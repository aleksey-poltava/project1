import numpy as np
import cv2

cap = cv2.VideoCapture(0)

winName = "img2"
cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)

# take first frame of the video
ret,frame = cap.read()

# setup initial location of window
# r,h,c,w - region of image
#           simply hardcoded the values
r,h,c,w = 200,20,300,20
track_window = (c,r,w,h)

# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((100.,  23., 117.)), np.array((152.,  54., 191.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by at least 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while(1):
    ret ,frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        # apply meanshift to get the new location
        ret, track_window = cv2.meanShift(dst, track_window, term_crit)

        # Draw it on image
        x,y,w,h = track_window
        cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        cv2.imshow('img2', frame)

        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break


    else:
        break

cv2.destroyAllWindows()
cap.release()