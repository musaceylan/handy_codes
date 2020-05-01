import json 
import sys
import os
import cv2




def crop(image, BBox):
    
    x0 = int(BBox[0])
    y0 = int(BBox[1])
    width = int(BBox[2])
    height = int(BBox[3])
    return image[ y0:height,x0:width, :]


output_folder = ""
imagepaths = []
path = "TL_train_data/Train/"
ext = ".jpg"

categories = set()
with open('TL_train.json', 'r') as json_file:
    data = json.load(json_file) 
    for idImage, d in enumerate(data):
        imagepaths.append(d["Path"])
        image = cv2.imread(os.path.join( path +  d["Path"]))
        print(idImage, image.shape)
        for idObject ,object in  enumerate(d["Objects"]):
            #print(idObject , object)
            #print(idObject, object["Category"],object["BBox"])
            cropped_img = crop(image, object["BBox"])
            cv2.imwrite(os.path.join(str(object["Category"])+"/"+ str(d["Path"])+ "cropped_img_" +  str(idObject) + ext),cropped_img)

               
   

print("---------------------------------------")

print(categories) 
print(len(imagepaths)) 
print(imagepaths[0])
print(imagepaths.index(imagepaths[-1]))



for c in categories:
    output_folder = str(c)    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

            
                