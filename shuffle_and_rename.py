import os 
from PIL import Image
import shutil

import os


def rename(files,path):
	for folder in os.listdir(path):
		
		for index, file in enumerate(os.listdir(os.path.join(path+"/"+folder))):
			
			os.rename(os.path.join(folder, file), os.path.join(folder, ''.join([str(index), '.png'])))

def add_zeros(number_ofdigits, path, files, extensions):
	for item in files:
		if item.endswith(extensions):
			name = item.split(".")
			zeros = number_ofdigits-len(name[0])
			newname = str(zeros*"0")+name[0]+"."+name[1]
			shutil.move(path+"/"+item, path+"/"+newname)
	
		
# Function to rename multiple files 
def main(): 
	number_ofdigits = 5
	path = "Train"
	files = os.listdir(path)
	extensions = (".jpg", ".jpeg","png")

	#rename(files,path)
	for folder in os.listdir(path):
		
		for index, file in enumerate(os.listdir(os.path.join(path+"/"+folder))):
			
			os.rename(os.path.join(folder, file), os.path.join(folder, ''.join([str(index), '.png'])))

	#add_zeros(number_ofdigits, path, files, extensions)

	#mogrify -format png test_tr/*.jpg 		
	#cd 
	#rm *.jpg
   		
  	
# Driver Code 
if __name__ == '__main__': 
      
    # Calling main() function 
    main() 
