import glob
import cv2

label_path = "/home/otonom2/Documents/handy_codes/test/label/"
files = glob.glob(label_path + "*.txt")
print(files)
file_folder = "/home/otonom2/Documents/handy_codes/test/image/"

counter = 0
for file in files:
    # img_path = img_paths + file_folder[len(label_path):-3] + "jpg"

    img_path = file[:-3] + "jpg"
    txt_file = file[:-3] + "txt"

    with open(txt_file) as f:
        lines = f.readlines()

    # print(file)
    img_mat = cv2.imread(img_path)
    height, width, channels = img_mat.shape
    # print(img_mat.shape)

    new_lines = []

    for i in range(len(lines)):
        values = lines[i].split(" ")

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