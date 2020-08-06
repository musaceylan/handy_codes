import glob
import cv2
import os

folders_path = "/home/otonom2/Desktop/ThermalDataset/yolo_format/"

counter = 0

for folder in os.listdir(folders_path):

    label_path = folders_path + folder +"/"
    print(label_path)
    files = glob.glob(label_path + "*.txt")
    print(len(files))
    #file_folder = "/home/otonom2/Pictures/bumpy_road/bisikletli/"   
    
    for file in files:
        # img_path = img_paths + file_folder[len(label_path):-3] + "jpg"

        img_path = file[:-3] + "jpg"
        txt_file = file[:-3] + "txt"

        with open(txt_file,"r+") as f:
            lines = f.readlines()
            for index, line in enumerate(lines):
                #if line.split(" ")[0] == "8" :
                #    del lines[index]    
                if line.split(" ")[0] == "1" :
                    #line = "0 "+line.split(" ")[1]+" "+line.split(" ")[2]+" "+line.split(" ")[3]+ " " +line.split(" ")[4]
                    #print(line)
                    #f.seek(0)
                    #f.truncate()
                    #f.writelines(line)
                    counter+=1
    print(counter)                
                    
