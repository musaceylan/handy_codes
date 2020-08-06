
# to create and slit the

import os
import random
import shutil
import torch
from torch.utils import data


train_folder = "Train"
val_folder = "Validation"


#if not os.path.isdir(val_folder):
    #print(val_folder + ' not found, making a validation set')
    #os.mkdir(val_folder)
for dirs in os.listdir(train_folder):
    os.mkdir(val_folder + '/' + dirs)
    subfolder_dir = os.listdir(train_folder + '/' + dirs)  # dir is your directory path
    number_files = len(subfolder_dir)
    print(number_files)

    sample = random.sample([f for f in subfolder_dir],int(number_files*0.1))
    for i in sample:
        #shutil.copy(train_folder + '/' + dirs + '/' + i,val_folder + '/' + dirs )
	    shutil.move(train_folder + '/' + dirs + '/' + i,val_folder + '/' + dirs )
    #for f in os.listdir(train_folder + '/' + dirs):


        #index = random.randrange(0, len(f)*0.1)
        #if f.endswith('00000') or f.endswith('00001') or f.endswith('00002'):
            # move file to validation folder
        #shutil.copyfile(train_folder + '/' + dirs + '/' + f, val_folder + '/' + dirs + '/' + f)
"""


for folderName, subfolders, files in os.walk(train_folder):

    for subfolder in subfolders:
        subfolder_dir = os.listdir(train_folder + '/' + subfolder)
        number_files = len(subfolder_dir)

    sampling = random.sample(files, int(number_files*0.1))
    print(subfolder)
    print(sampling)
        #idx = list(range(number_files))
        #selected_idx = random.sample(idx,int(len(idx)*0.1))
        #selected_file = random.sample(filenames, number_files * 0.1)


"""
