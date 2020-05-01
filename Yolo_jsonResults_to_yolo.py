import json 
import sys
import os


output_path_label = "/home/otonom2/Documents/handy_codes/labels"

imagepaths = []

value_change = {0:"0",1:"5",2:"2",3:"6",5:"3",7:"4",9:"7"}

with open('result_gtsdb.json', 'r') as json_file:
    data = json.load(json_file) 
    for idImage, d in enumerate(data):
        imagepaths.append(d["filename"])
        
        a = str(d["filename"].split("/")[6])
        print(idImage)
        filename = str(a.split(".")[0])
        img_label_path = os.path.join(output_path_label, filename + ".txt")
        label_f = open(img_label_path, "a+")
        for idObject ,object in  enumerate(d["objects"]):
            
            

            id = object["class_id"]
            if id != 0 and id != 1 and id != 2 and id != 3 and id != 5 and id != 7 and id != 9:
                continue
            class_id = value_change[object["class_id"]]

            center_x = object["relative_coordinates"]["center_x"]
            center_y = object["relative_coordinates"]["center_y"]
            width_bbox = object["relative_coordinates"]["width"]
            height_bbox = object["relative_coordinates"]["height"]
            label_f.write("{} {} {} {} {}\n".format(class_id, center_x, center_y, width_bbox, height_bbox))
        label_f.close()   


