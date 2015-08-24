import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 30, 200)

    # ret,thresh = cv2.threshold(gray,127,255,0)
    ret, thresh = cv2.threshold(gray,127,255, cv2.THRESH_BINARY_INV)
    # Display the resulting frame
    # cv2.imshow('frame',thresh)
    # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)

    # moments = cv2.moments(cnt)
    # if moments['m00'] != 0.0:
#        cx = int(moments['m10']/moments['m00'])
#        cy = int(moments['m01']/moments['m00'])
#        print 'cx ', cx, 'cy ', cy
#        cv2.rectangle(frame, (cy, cx), (cy+10, cx+10), (0,255,0), 3)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()