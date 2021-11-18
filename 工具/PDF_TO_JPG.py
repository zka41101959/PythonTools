import json
import shutil
import os
from pdf2image import convert_from_path


def pdf2image2(pdfPath, imagePath, thread_num, page_front, jpegopt, dpi):
    if not os.path.exists(imagePath):
        os.makedirs(imagePath)
    else:
        shutil.rmtree(imagePath)
        os.makedirs(imagePath)
    convert_from_path(pdfPath,
                      dpi=dpi,
                      output_folder=imagePath,
                      fmt="jpeg",
                      jpegopt=jpegopt,
                      output_file=page_front,
                      thread_count=thread_num,
                      transparent=True)


def get_pdf_list():
    L = []
    for root, dirs, files in os.walk("../"):
        for file in files:
            c = os.path.splitext(file)[1]
            if c == '.pdf':
                L.append(os.path.join(root, file))
        for i in range(len(L)):
            L[i] = L[i][2:]
        break
    return L


def get_file_name_dict(pdf_list, mark):
    old_name, new_name, files_name_dict = [], [], {}
    [old_name.append(pdf_name) for pdf_name in pdf_list]
    [
        new_name.append("%s%03d.pdf" % (mark, (i + 1)))
        for i in range(len(old_name))
    ]
    for j in range(len(old_name)):
        files_name_dict["file%03d" % (j + 1)] = [old_name[j], new_name[j]]
    return files_name_dict


def creat_dir1(path):
    if os.path.exists(path):
        print("目录 %s 已存在,将会删除其内部所有文件" % path)
        shutil.rmtree(path)
        os.makedirs(path)

    else:
        try:
            os.makedirs(path)
        except:
            print("创建目录: %s 失败" % path)


if __name__ == '__main__':
    # 运行前目录不要有中文
    dir = os.path.split(os.path.realpath(__file__))[0].replace("\\", "/")
    bak_dir = "pdf_backup"  # 备份文件夹目录
    mark = "book_"  # 输出文件夹前缀
    file_histoty_name = "file_name_list.txt"  # 备份文件对照表目录
    dpi = 400
    jpegopt = {
        "quality": 85,
        "optimize": True,
        "progressive": True
    }  # 输出jpeg的参数
    thread_num = 12  # 线程,仅针对单文件
    # 创建pdf列表对照
    pdf_list = get_pdf_list()
    file_name_dict = get_file_name_dict(pdf_list, mark)
    # 保存文件对照表至file_histoty_name
    with open(file_histoty_name, 'w', encoding='utf8') as oand:
        oand.write(str(file_name_dict))
    print(file_name_dict)
    print("输出图像DPI:%s ,Jpeg质量:%s" % (dpi, jpegopt.get("quality")))
    # 统一更名,并将旧文件移入备份文件夹
    creat_dir1(bak_dir)
    for j in range(len(file_name_dict.keys())):
        old_name = file_name_dict["file%03d" % (j + 1)][0]
        new_name = file_name_dict["file%03d" % (j + 1)][1]
        shutil.copy2(old_name, bak_dir)
        os.rename(old_name, new_name)
        imagePath = dir + "/" + new_name[:-4]
        page_front = "page_"  # 单页文件前缀
        page_front = new_name.rstrip(".pdf") + "_" + page_front
        pdf2image2(new_name, imagePath, thread_num, page_front, jpegopt, dpi)
        print("原文件名: %s \t新文件名: %s \n输出目录: %s" %
              (old_name, new_name, imagePath))
        os.rename(new_name, new_name[5:][:-4] + "_" + old_name)
    print("任务完成")
