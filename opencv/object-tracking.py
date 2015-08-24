import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_green = np.array([47,100,100])
    upper_green = np.array([78,225,215])

    lower_red = np.array([0,110,150])
    upper_red = np.array([10,254,254])

    lower_color = np.array([10, 9, 150])
    upper_color = np.array([40, 85, 248])

    # Threshold the HSV image to get only blue colors
    # mask = cv2.inRange(hsv, lower_green, upper_green)
    #  mask2 = cv2.inRange(hsv, lower_red, upper_red)
    mask3 = cv2.inRange(hsv, lower_color, upper_color)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask3)

#    cv2.imshow('frame',frame)
#    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()