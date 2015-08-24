import numpy as np
import cv2

# Create a black image
img = np.zeros((512,512,3), np.uint8)

# Draw a diagonal blue line with thickness of 5 px
cv2.line(img,(0,0),(511,511),(51,199,14),5)
cv2.line(img,(0,511),(511,0),(51,199,14),5)
cv2.circle(img,(255,255), 63, (0,0,255), -1)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'OpenCV',(200,500), font, 1,(255,255,255),2)

# save image to file
# cv2.imwrite('houghlines3.jpg', (img))

cv2.imshow('Super Frame', img)
cv2.waitKey(0)
cv2.destroyAllWindows()