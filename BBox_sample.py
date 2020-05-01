
import cv2
import numpy as np
import os

def crop(image, BBox):
    
    x0 = int(BBox[0])
    y0 = int(BBox[1])
    width = int(BBox[2])
    height = int(BBox[3])
    return image[ y0:height,x0:width, :]



window_name = 'image'
category = (2,6)

ext = ".jpg"

output_folder = str(category)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

BBox1 = ['1318', '865', '1345', '902']
BBox2 = ["1447", "866", "1475", "903"]

BBox = [BBox1,BBox2]
print(len(BBox))

img = cv2.imread('10071002120911120601800.png_3.jpg')

for i in range(len(BBox)):
    print(BBox[i])
    cropped_img = crop(img, BBox[i])
    
    cv2.imwrite(os.path.join(str(category[i])+"/"+"cropped_img_" + str(i) + ext),cropped_img)
    
#cropped_img = crop(img, BBox)

#cv2.imwrite(os.path.join(str(category)+"/"+"cropped_img.jpg"),cropped_img)

cv2.imshow(window_name,cropped_img)

while True:
    key = cv2.waitKey(1)
    if key == 27: #ESC key to break
        break

cv2.destroyAllWindows()




"""

import cv2
import numpy as np

# read and scale down image
# wget https://bigsnarf.files.wordpress.com/2017/05/hammer.png #black and white
# wget https://i1.wp.com/images.hgmsites.net/hug/2011-volvo-s60_100323431_h.jpg
img = cv2.pyrDown(cv2.imread('10071002120911120601800.png_3.jpg', cv2.IMREAD_UNCHANGED))

# threshold image
ret, threshed_img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
                127, 255, cv2.THRESH_BINARY)
# find contours and get the external one

contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#image, contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE,
#                cv2.CHAIN_APPROX_SIMPLE)

# with each contour, draw boundingRect in green
# a minAreaRect in red and
# a minEnclosingCircle in blue
for c in contours:
    # get the bounding rect
    x, y, w, h = cv2.boundingRect(c)
    # draw a green rectangle to visualize the bounding rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # get the min area rect
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    # convert all coordinates floating point values to int
    box = np.int0(box)
    # draw a red 'nghien' rectangle
    cv2.drawContours(img, [box], 0, (0, 0, 255))

    # finally, get the min enclosing circle
    (x, y), radius = cv2.minEnclosingCircle(c)
    # convert all values to int
    center = (int(x), int(y))
    radius = int(radius)
    # and draw the circle in blue
    img = cv2.circle(img, center, radius, (255, 0, 0), 2)

print(len(contours))
cv2.drawContours(img, contours, -1, (255, 255, 0), 1)

cv2.imshow("contours", img)

cv2.imshow("contours", img)

while True:
    key = cv2.waitKey(1)
    if key == 27: #ESC key to break
        break

cv2.destroyAllWindows()

"""