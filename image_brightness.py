import cv2
import skimage.exposure
from skimage.filters import threshold_yen
from skimage.exposure import rescale_intensity
import numpy as np

image = cv2.imread('/home/otonom2/Downloads/gamma-correction/frame0112.jpg')

alpha = 2 # Contrast control (1.0-3.0)
beta = 30 # Brightness control (0-100)

adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

out1 = skimage.exposure.rescale_intensity(image, in_range=(0,128), out_range=(0,255))
yen_threshold = threshold_yen(image)
bright = rescale_intensity(image, (0, yen_threshold), (0, 255))
hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

v = hsv[:, :, 2]
cv2.imshow('v', v)

cv2.imshow('Out1', out1)
cv2.imshow('bright', bright)

#cv2.imwrite("deneme.jpg",bright)
cv2.imshow('original', image)
cv2.imshow('adjusted', adjusted)

cv2.waitKey()