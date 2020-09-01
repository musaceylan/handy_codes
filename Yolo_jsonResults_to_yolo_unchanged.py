import json
import sys
import os

output_path_label = "/media/otonom2/Extreme SSD/tl_ryg_off_bag/results"

imagepaths = []

value_change = {0: "0", 1: "5", 2: "2", 3: "6", 5: "3", 7: "4", 9: "7"}

with open('/home/otonom2/Downloads/darknet-master (1)/result.json', 'r') as json_file:
    data = json.load(json_file)
    for idImage, d in enumerate(data):
        imagepaths.append(d["filename"])
        print(d)
        a = str(d["filename"].split("/")[6])

        filename = str(a.split(".")[0])
        print(filename)
        img_label_path = os.path.join(output_path_label, filename + ".txt")
        label_f = open(img_label_path, "a+")
        for idObject, object in enumerate(d["objects"]):

            id = object["class_id"]
            if id != 9:
                continue
            class_id = value_change[object["class_id"]]

            center_x = object["relative_coordinates"]["center_x"]
            center_y = object["relative_coordinates"]["center_y"]
            width_bbox = object["relative_coordinates"]["width"]
            height_bbox = object["relative_coordinates"]["height"]
            label_f.write("{} {} {} {} {}\n".format(class_id, center_x, center_y, width_bbox, height_bbox))
        label_f.close()
