from PIL import Image
import os
import cv2

gt_path = "/media/kaan/Sata/Datasets/Robotaksi/GermanTrafficSignDetectionBenchmark/gt.txt"
ds_path = "/media/kaan/Sata/Datasets/Robotaksi/GermanTrafficSignDetectionBenchmark/"

output_path_img = "/home/kaan/Desktop/german_yolo/img/"
output_path_label = "/home/kaan/Desktop/german_yolo/label/"

f = open(gt_path, "r")
lines = f.readlines()

for line in lines:
    splited_line = line.split(";")

    img_path = os.path.join(ds_path, splited_line[0])
    new_img_path = os.path.join(output_path_img, splited_line[0][:-3] + "png")
    img_label_path = os.path.join(output_path_label, splited_line[0][:-3] + "txt")

    label_f = open(img_label_path, "a+")

    img = Image.open(img_path)
    width, height = img.size
    img.save(new_img_path)

    left_top_x = int(splited_line[1])
    left_top_y = int(splited_line[2])
    right_bottom_x = int(splited_line[3])
    right_bottom_y = int(splited_line[4])

    center_x = format(((right_bottom_x - left_top_x) / 2) / width, '.6f')
    center_y = format(((right_bottom_y - left_top_y) / 2) / height, '.6f')
    width_bbox = format((right_bottom_x - left_top_x) / height, '.6f')
    height_bbox = format((right_bottom_y - left_top_y) / height, '.6f')

    # label_f.write("%s %.6f %.6f %.6f %.6f")

    # print("%d %.6f %.6f %.6f %.6f",
    #       8, center_x / width , center_y / height, width_bbox / width, height_bbox / height)
    print("{} {} {} {} {}".format(8, center_x, center_y, width_bbox, height_bbox))
    label_f.write("{} {} {} {} {}\n".format(8, center_x, center_y, width_bbox, height_bbox))

    # cv_img = cv2.imread(new_img_path)
    # x_center = center_x
    # y_center = center_y
    #
    # w = width_bbox
    # h = height_bbox
    #
    # x_left_top = left_top_x
    # y_left_top = left_top_y
    # x_right_bottom = right_bottom_x
    # y_right_bottom = right_bottom_y
    # cv2.rectangle(cv_img, (x_left_top, y_left_top), (x_right_bottom, y_right_bottom), (255, 0, 0), 2)
    # cv2.putText(cv_img, "traffic sign", (x_left_top, y_left_top - 10),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    #
    # cv2.imshow("aaaaa", cv_img)
    # cv2.waitKey(0)
    label_f.close()

f.close()