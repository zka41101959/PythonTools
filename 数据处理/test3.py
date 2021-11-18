import docx
from docx import Document

file = docx.Document("全试题.docx")
with open("全试题.txt",'w',encoding='utf-8') as f:
    for para in file.paragraphs:
        f.write(para.text)



