import cv2
import numpy as np

img = cv2.imread('/home/alex/PycharmProjects/opencv/img/box.jpg',0)
ret,thresh = cv2.threshold(img,127,255,0)
contours,hierarchy = cv2.findContours(thresh, 1, 2)

cnt = contours[0]
M = cv2.moments(cnt)
print M

approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)

print 'coordinates of contour:', approx

cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
print 'Centoid:'
print cx, '     ', cy

area = cv2.contourArea(cnt)
print 'contour area is:', area

print 'contour area from m00:', M['m00']

# Create a black image
img = np.zeros((512,512,3), np.uint8)

# Draw a diagonal blue line with thickness of 5 px
img = cv2.line(img,(0,0),(511,511),(255,0,0),5)