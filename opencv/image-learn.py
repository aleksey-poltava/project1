import cv2
import numpy as np

img = cv2.imread('flower.jpg')

px = img[110,110]
print px

leaf = img[280:340, 330:390]
img[273:333, 100:160] = leaf


cv2.imshow('frame', img)
cv2.waitKey(0)
cv2.destroyAllWindows()