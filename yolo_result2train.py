import re
from PIL import Image
import os



gt_path = '/home/otonom2/Downloads/darknet-master (1)/result.txt'
ds_path = '/home/otonom2/Downloads/darknet-master (1)/result'
myfile=open(gt_path,'r')
lines=myfile.readlines()
class_pattern= "traffic light"
image_name_pattern = '/media/otonom2/Extreme SSD/'

image_name_list = []
found_class = []

for line in lines:



    if re.search(image_name_pattern,line):
        img_path =line.split(":")[0]
        image_name_list.append(img_path)
        img = Image.open(img_path)
        width, height = img.size

    if re.search(class_pattern,line):
        
  
        Cord_Raw=line
            
        Cord=Cord_Raw.split("(")[1].split(")")[0].split("  ")
        print(Cord) 

        x_min = int(Cord_Raw.split("left_x:")[1].split("top_y")[0])
        x_max = x_min + int(Cord_Raw.split("width:")[1].split("height")[0])
        #x_max=x_min + int(Cord[5])
        y_min = int(Cord_Raw.split("top_y:")[1].split("width")[0])
        #y_min=int(Cord[3])
        y_max = y_min + int(Cord_Raw.split("height:")[1].split(")")[0])
        #y_max=y_min+ int(Cord[7])
        print(x_min,x_max,y_min,y_max)


        center_x = format(((x_max - x_min) / 2) / width, '.6f')
        center_y = format(((y_min - y_max) / 2) / height, '.6f')
        width_bbox = format((x_max - x_min) / height, '.6f')
        height_bbox = format((y_min - y_max) / height, '.6f')

        label_f.write("{} {} {} {} {}\n".format(7, center_x, center_y, width_bbox, height_bbox))


