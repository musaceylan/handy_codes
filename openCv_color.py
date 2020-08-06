import numpy as np
import cv2
 
#cap = cv2.VideoCapture(0)
im = cv2.imread("/home/otonom2/Documents/handy_codes/green.jpeg")

hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
v = hsv[:, :, 2]
height, width = v.shape

print(hsv.shape)
print(v.shape)


height_div3 = int((height - 6) / 3)

red_region = v[3:3 + height_div3, 3:width - 3]
yellow_region = v[3 + height_div3:3 + height_div3 * 2, 3:width - 3]
green_region = v[3 + height_div3 * 2:3 + height_div3 * 3, 3:width - 3]


sum_brightness_red = np.sum(red_region)
avg_brightness_red = sum_brightness_red / (height_div3 * width)
sum_brightness_yellow = np.sum(yellow_region)
avg_brightness_yellow = sum_brightness_yellow / (height_div3 * width)
sum_brightness_green = np.sum(green_region)
avg_brightness_green = sum_brightness_green / (height_div3 * width)

print(sum_brightness_red)
print(sum_brightness_yellow)
print(sum_brightness_green)

all_images = np.hstack((im,hsv))
all_regions = np.hstack((red_region,yellow_region,green_region))

cv2.imshow('all_images',all_images)
cv2.imshow('all_regions',all_regions)


cv2.waitKey(0)


'''
while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]
    height, width = v.shape

    height_div3 = int((height - 6) / 3)

    red_region = v[3:3 + height_div3, 3:width - 3]
    yellow_region = v[3 + height_div3:3 + height_div3 * 2, 3:width - 3]
    green_region = v[3 + height_div3 * 2:3 + height_div3 * 3, 3:width - 3]

    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    
    #cv2.imshow('image',im)
    #cv2.imshow('v',v)
    #cv2.imshow('red',red_region)
    #cv2.imshow('yellow',yellow_region)
    #cv2.imshow('green',green_region)

    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

'''