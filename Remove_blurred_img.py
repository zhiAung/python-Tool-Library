
# coding: utf-8

# In[56]:


#-*-coding:utf-8-*-
"""python 2.x
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
"""
"""<= Python 3.3
import imp
imp.reload(sys)"""

#>=python 3.4
import sys
import importlib
importlib.reload(sys)
import os
import cv2
import shutil
from PIL import Image
in_file="E:/SF6压力表/"#原文件夹
out_file1='E:/SF6压力表11'#输出清晰图片的文件夹
out_file2='E:/SF6压力表22'#模糊图片文件夹
THRESHOLD=200#模糊度阈值，值越小越模糊
images=os.listdir(in_file)
clear_img_list = []
blurry_img_list= []
count=0
for img in images:
    img2 = Image.open(os.path.join(in_file, img))
    im = img2.resize((453, 255),Image.ANTIALIAS)
    box = (80, 25, 373, 235)
    crop = im.crop(box)
    img_arr = np.array(crop)
    gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    imageVar = cv2.Laplacian(gray, cv2.CV_64F).var()#方差
    count+=imageVar
    if imageVar > THRESHOLD:
        clear_img_list.append(img)
    else:
        blurry_img_list.append(img)
    #print("图片{}：值{}".format(img,imageVar))
for img in clear_img_list:
    shutil.copy2( os.path.join(in_file,img), os.path.join(out_file1,img))
for img in blurry_img_list:
    shutil.copy2( os.path.join(in_file,img), os.path.join(out_file2,img))
#print(count/len(images))    

