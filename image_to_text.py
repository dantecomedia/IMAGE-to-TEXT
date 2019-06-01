import cv2
import numpy as np
from PIL import Image
import tempfile
import pytesseract
import os
from tqdm import tqdm
img_size = 1800
threshold = 215


def process_image(file):
    temp = image_dpi(file)
    im_new = remove_noise_and_smooth(temp)
    return im_new


def image_dpi(file):
    im = Image.open(file)
    length_x, width_y = im.size
    factor = max(1, int(img_size / length_x))
    size = factor * length_x, factor * width_y
    # size = (1800, 1800)
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp = temp_file.name
    im_resized.save(temp, dpi=(300, 300))
    return temp


def smoothening(img):
    ret1, th1 = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3


def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image







#ENTER THE SINGLE IMAGE ADDRESS HERE
input_image="text2.png"
#ENTER THE DIR IMAGE ADDRESS HERE , UNCOMMNENT TO USE IT
#input_image_dir=""


####---------------DOING THE IMAGE PREPROCESSING----------------------------------
def single_image_text():
	image_address=input("Enter image address :")
	new_img=process_image(image_address)
	new_name=image_address[0:-4]+"_processed.png"
	cv2.imwrite(new_name, new_img)
	sentence = pytesseract.image_to_string(Image.open(new_name))
	address=image_address[0:-4]+"_text.txt"
	f=open(address,"w")
	f.write(str(sentence))
	f.close()


def multiple_image_text():
	image_address_dir=input("Enter image directory address:")
	'''if  not os.path.exists(image_address_dir+"/"+"Converted Text files") and os.path.exists(image_address_dir+"/"+"Processed Images"):
		os.mkdir(image_address_dir+"/"+"Converted Text files")
		os.mkdir(image_address_dir+"/"+"Processed Images")
	else:
		os.path.join(image_address_dir+"/"+"Converted Text files",image_address_dir+"/"+"Processed Images")'''
	os.mkdir(image_address_dir+"/"+"Converted Text files")
	os.mkdir(image_address_dir+"/"+"Processed Images")
	for i in tqdm(os.listdir(image_address_dir)):
		if i!="Converted Text files" and i!="Processed Images":
			image_address=image_address_dir+"/"+i
			#print(image_address)
			new_img=process_image(image_address)
			new_name=i[0:-4]+"_processed.png"
			new_address=image_address_dir+"/Processed Images/"+new_name
			#print(new_address)
			cv2.imwrite(new_address, new_img)
			sentence = pytesseract.image_to_string(Image.open(new_address))
			address=image_address_dir+"/"+"Converted Text files/"+i[0:-4]+"_text.txt"
			f=open(address,"w")
			f.write(str(sentence))
			f.close()


def main():
	print("\n")
	print("1.Single image to text\n")
	print("2.Multiple image to text\n")
	ch=int(input("ENTER CHOICE :"))
	if ch==1:
		single_image_text()
	elif ch==2:
		multiple_image_text()

if __name__=="__main__":
	main()