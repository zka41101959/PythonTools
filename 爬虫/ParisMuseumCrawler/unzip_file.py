import os
import random
import shutil
import zipfile

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files

path = "./zip_file"

all_file_list = file_name(path)
image_list = []
for filename in all_file_list:
    print(filename)
    zip_file_path = path+"/"+filename
    zip_file = zipfile.ZipFile(zip_file_path)
    file_list = zip_file.namelist()
    jpg_list = []
    for file in file_list:
        if file[-4:]==".jpg":
            jpg_list.append(file)
    out_image_name = zip_file_path[:-4]+".jpg"
    for jpg in jpg_list:
        try:
            image_path = path + "/" + jpg
            zip_file.extract(jpg, path)
            if len(jpg_list) > 1:
                out_name = zip_file_path[:-4] + str(random.randint(0, 5000)) + ".jpg"
                os.rename(image_path, out_name)
            else:
                os.rename(image_path, out_image_name)
        except Exception as e:
            print("error: %s\tfile: %s"%(e,filename))
            outerrorfilter = path+"/"+"error"
            if not os.path.exists(outerrorfilter):
                print("error文件夹不存在,已新建")
                os.makedirs(outerrorfilter)
            shutil.copy2(zip_file_path,outerrorfilter)
    # break
