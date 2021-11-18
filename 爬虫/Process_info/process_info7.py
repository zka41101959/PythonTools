import os
from bs4 import BeautifulSoup
from cv2 import cv2
from dataserver import Mysqldb

def get_s(ppp):
    ft = "." + ppp.split("/")[-1].split(".")[-1]
    return ft


dbinfo = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': 'root',
    'port': 3306,
    'db': 'sizheng',
    'charset': 'utf8',
    'use_unicode': True
}



def get_frame_from_video(video_name, frame_time, img_dir, img_name):
    vidcap = cv2.VideoCapture(video_name)
    vidcap.set(cv2.CAP_PROP_POS_MSEC, frame_time - 1)
    success, image = vidcap.read()
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    if success:
        cv2.imwrite(img_dir + os.sep + img_name, image)




def get_file_list_from_path(path, suffix_list, exclude=None):
    allfiles = []
    for root, dirs, files in os.walk(path):
        [allfiles.append(os.path.join(root, file))
         for file in files if os.path.splitext(file)[1] in suffix_list]
    if exclude and exclude != []:
        [[allfiles.remove(i) for ex in exclude if i[len(i.split("\\")) - 1] in ex] for i in allfiles]
    return allfiles


def get_path_info(path):
    (fp, tfn) = os.path.split(path)
    (fn0, es) = os.path.splitext(tfn)
    return fp, tfn, fn0, es

if __name__ == '__main__':
    img_dir = r"D:\phpstudy_pro\WWW\sizheng\uploads\static\video\img"
    for i,v in enumerate(get_file_list_from_path(r"D:\phpstudy_pro\WWW\sizheng\uploads\static\video",[".mp4"])):
        fp, tfn, fn0, es = get_path_info(v)
        get_frame_from_video(v,1200,img_dir,fn0+".jpg")
        # break



# db = Mysqldb(dbinfo)
# all_i = db.select("select * from ey_article_content")
# for (id, aid, content, add_time, update_time, title) in all_i:
#     # soup = BeautifulSoup(content, "html.parser")
#     # video_soup_list = soup.find_all("video")
#     # new_fin = content.replace("flv", "mp4")
#     print(content)
#
#     us = f"UPDATE ey_article_content SET content='{new_fin}' WHERE aid={aid}"
#     db.execute(us)