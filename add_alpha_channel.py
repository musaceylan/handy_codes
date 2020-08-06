import cv2 
import os,random
import numpy as np

def get_random_crop(image, crop_height, crop_width):

    max_x = image.shape[1] - crop_width
    max_y = image.shape[0] - crop_height

    x = np.random.randint(0, max_x)
    y = np.random.randint(0, max_y)

    crop = image[y: y + crop_height, x: x + crop_width]

    return crop

def overlay_transparent(background_img, img_to_overlay_t, x, y, overlay_size=None):
	"""
	@brief      Overlays a transparant PNG onto another image using CV2
	
	@param      background_img    The background image
	@param      img_to_overlay_t  The transparent image to overlay (has alpha channel)
	@param      x                 x location to place the top-left corner of our overlay
	@param      y                 y location to place the top-left corner of our overlay
	@param      overlay_size      The size to scale our overlay to (tuple), no scaling if None
	
	@return     Background image with overlay on top
	"""
	
	bg_img = background_img.copy()
	
	if overlay_size is not None:
		img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

	# Extract the alpha mask of the RGBA image, convert to RGB 
	b,g,r,a = cv2.split(img_to_overlay_t)
	overlay_color = cv2.merge((b,g,r))
	
	# Apply some simple filtering to remove edge noise
	mask = cv2.medianBlur(a,5)

	h, w, _ = overlay_color.shape
	roi = bg_img[y:y+h, x:x+w]

	# Black-out the area behind the logo in our original ROI
	img1_bg = cv2.bitwise_and(roi.copy(),roi.copy(),mask = cv2.bitwise_not(mask))
	
	# Mask out the logo from the logo image.
	img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = mask)

	# Update the original image with our new ROI
	bg_img[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)

	return bg_img

alpha_folder = "/home/otonom2/Desktop/alpha/"
folders_path = "/home/otonom2/Desktop/dfg_to_german/"

for folder in os.listdir(folders_path):
    
    new_directory = folders_path+"0"+folder + "_alpha/"
    print(folder)
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)
    counter = 0 
 
    for file in os.listdir(folders_path+folder+"/"):
        print(file)
        img = cv2.imread(folders_path+folder+"/"+file,-1)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        shape = img.shape
        #b_channel, g_channel, r_channel = cv2.split(img)
        #mask = np.zeros(img.shape[:2], np.uint8)


        background = cv2.imread(alpha_folder+random.choice(os.listdir(alpha_folder)))
        #alpha_img = cv2.cvtColor(alpha_img, cv2.COLOR_BGR2RGB)
        background = get_random_crop(background, shape[0],shape[1])
        #background = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)

        img_BGRA = overlay_transparent(background,img,0,0)

        #th, alpha = cv2.threshold(np.array(rgb),0,255, cv2.THRESH_BINARY)
        #alpha = cv2.GaussianBlur(alpha, (7,7),0)
        #alpha = alpha.astype(float)/255


        #img = cv2.multiply(alpha, img)
        #background = cv2.multiply(1.0 - alpha, background)


        #rgba_alpha = cv2.cvtColor(alpha_crop, cv2.COLOR_RGB2RGBA)
        
        #alpha_channel = rgba_alpha[:, :, 3]
        #alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50 #creating a dummy alpha channel image.
        
        #img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
        #img_BGRA = cv2.addWeighted(alpha_channel,0.4,img,0.1,0)
        #img_BGRA =cv2.add(img, background)


        #cv2.imshow("alpha",background)
        #cv2.imshow("[winname]", img_BGRA)
        cv2.imwrite(os.path.join(new_directory, str(counter) + ".jpg"),img_BGRA )
        counter +=1
        cv2.waitKey(0)