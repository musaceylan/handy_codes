import glob
import cv2

label_path = "/media/otonom2/Extreme SSD/tl_ryg_off_bag/off/"
files = glob.glob(label_path + "*.txt")
#file_folder = "/media/otonom2/Extreme SSD/tl_ryg_off_bag/off/"

counter = 0

print("aaaa")
for file in files:
    # img_path = img_paths + file_folder[len(label_path):-3] + "jpg"
    
    
    img_path = file[:-3] + "jpg"
    txt_file = file[:-3] + "txt"
    print(img_path)
    print(txt_file)


    with open(txt_file) as f:
        lines = f.readlines()

    # print(file)
    img_mat = cv2.imread(img_path)
    height, width, channels = img_mat.shape
    # print(img_mat.shape)

    new_lines = []

    for i in range(len(lines)):
        values = lines[i].split(" ")
        if values[0] == 7:
            print("traffic light") 

        x_center = float(values[1]) * width
        y_center = float(values[2]) * height

        bbox_width = float(values[3]) * width
        bbox_heigh = float(values[4]) * height

        bbox_img = img_mat[int(y_center - bbox_heigh / 2):int(y_center + bbox_heigh / 2),
                   int(x_center - bbox_width / 2):int(x_center + bbox_width / 2)]

        # print("************")
        # print("Id : " + values[0])
        # print("bbox area : " + str(bbox_width * bbox_heigh))

        cv2.imshow("Input", bbox_img)
        cv2.waitKey(0)