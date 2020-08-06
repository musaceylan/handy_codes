
import os, sys


file_path = "/home/otonom2/Downloads/test_images/Sola_Donulmez10/cropped/"

files = os.listdir(file_path)
counter = 672

for file in files:
    if file[-4:] == '.jpg':
        print(file)
        print("{0}.jpg".format(counter))
        os.rename(file_path+file, file_path+"{0}.jpg".format(counter))
        counter += 1