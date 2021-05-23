import csv
from tqdm import tqdm
from os.path import join as oj
import os
import json
from PIL import Image
from imageio import imwrite
with open('config.json') as json_file:
    data = json.load(json_file)

data_path = data["data_folder"]
img_path = oj(data_path, "raw")
processed_path = oj(data_path, "processed")
segmentation_path = oj(data_path, "segmentation")
benign_path = oj(processed_path, "no_cancer_256")
malignant_path = oj(processed_path, "cancer_256")

os.makedirs(processed_path,exist_ok = True)
os.makedirs(benign_path,exist_ok = True)
os.makedirs(segmentation_path,exist_ok = True)
os.makedirs(malignant_path,exist_ok = True)

#%% Read in the metadata as a list of lists.
list_of_meta = []
with open(oj(data_path, "meta.csv"), newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader)   # Skip the header.
    for row in spamreader:
        list_of_meta.append(row)    
        
#%%  Get lists of file names for the benign images & malignant images.
list_benign_files = []
for line in list_of_meta:
    if len(line) > 0 and line[3] == 'benign':
        list_benign_files.append(line[0] + ".jpg")
list_mal_files = []
for line in list_of_meta:
    if len(line) > 0 and line[3] == 'malignant':
        list_mal_files.append(line[0] + ".jpg")
        
#%% Resize the images to 299x299 and save benign & malignant separately.

def resize_and_save(my_list, my_folder):
    for i,file_name in tqdm(enumerate(my_list)):
        try:
            img = Image.open(oj(img_path, file_name))
            # test = np.asarray(img)
            img_resized = img.resize((256, 256))
            imwrite(oj(my_folder, file_name), img_resized)
        except:
            print(file_name)
            
resize_and_save(list_mal_files, malignant_path)
resize_and_save(list_benign_files, benign_path)