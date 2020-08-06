import glob
import cv2


def crop(image, x_left_top,y_left_top,x_right_bottom,y_right_bottom):
    
    x0 = int(x_left_top)
    y0 = int(y_left_top)
    width = int(x_right_bottom)
    height = int(y_right_bottom)
    return image[ y0:height,x0:width, :]


# file_folder = "/home/kaan/Desktop/new_detection_datasets/gtd_sign_dataset/images.txt"
file_folder = "/home/otonom2/Pictures/unlabelled_imgs/bisikletli/img_lst.txt"
f = open(file_folder, "r")
files = f.readlines()
f.close()
counter = 0
for file in files:
    # img_path = img_paths + file_folder[len(label_path):-3] + "jpg"

    img_path = file[:-1]
    txt_file = file[:-4] + "txt"

    print("txt file:")
    print(txt_file)
    print("img path")
    print(img_path)

    with open(txt_file) as f:
        lines = f.readlines()

    img_mat = cv2.imread(img_path)
    height, width, channels = img_mat.shape

    new_lines = []

    for i in range(len(lines)):
        values = lines[i].split(" ")

        x = float(values[1]) * width
        y = float(values[2]) * height

        w = float(values[3]) * width
        h = float(values[4]) * height

        x_center = x
        y_center = y


        x_left_top = int(x_center - (w / 2))
        y_left_top = int(y_center - (h / 2))
        x_right_bottom = int(x_center + (w / 2))
        y_right_bottom = int(y_center + (h / 2))
        cv2.rectangle(img_mat, (x_left_top, y_left_top), (x_right_bottom, y_right_bottom), (255, 0, 0), 2)
        cv2.putText(img_mat, str(values[0]), (x_left_top, y_left_top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    
    #cv2.imshow("cropped",crop(img_mat,x_left_top,y_left_top,x_right_bottom,y_right_bottom))
    cv2.imshow("Input", img_mat)
    cv2.waitKey(0)