import glob
import cv2
import os

folders_path = "/media/otonom2/Extreme SSD/tl_ryg_off_bag/ryg/"


output_folder = "/media/otonom2/Extreme SSD/tl_ryg_off_bag/cropped_ryg/"

#for folder in os.listdir(folders_path):
#label_path = folders_path + folder +"/"
#print(label_path)

#files = glob.glob(label_path + "*.txt")
files = glob.glob(folders_path + "*.txt")
print(len(files))

    
counter = 0
for file in files:
    # img_path = img_paths + file_folder[len(label_path):-3] + "jpg"


    img_path = file[:-3] + "jpg"
    txt_file = file[:-3] + "txt"

    with open(txt_file) as f:
        lines = f.readlines()
    #print(txt_file)

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
            #cv2.imshow("Input", bbox_img)
        if int(values[0]) == 7:
            #cv2.imwrite(os.path.join(output_folder,  str(folder) + "_" + str(counter)+ ".jpg"),bbox_img)
            print(txt_file)
            cv2.imwrite(os.path.join(output_folder,  str(counter)+ ".jpg"),bbox_img)
            counter+=1
        
        print(counter)

        cv2.waitKey(0)

