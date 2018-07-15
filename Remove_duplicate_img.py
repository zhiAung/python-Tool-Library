
# coding: utf-8

# In[9]:


# -*- coding:utf-8 -*-

"""
用dhash判断是否相同照片
基于渐变比较的hash
hash可以省略(本文省略)
By Guanpx
"""
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import tarfile
from IPython.display import display, Image
from PIL import Image, ImageFilter
from os import listdir

def picPostfix():  # 图片后缀的集合
    postFix = set()
    postFix.update(['JPEG','bmp', 'jpg', 'png', 'tiff', 'gif', 'pcx', 'tga', 'exif',
                    'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf', 'ufo', 'eps', 'JPG', 'raw', 'jpeg'])
    return postFix

def getDiff(crop_high,width, high, image):  # 将要裁剪成w*h的image照片 得到渐变序列
    diff = []
    im = image.resize((width, high),Image.ANTIALIAS)
    box = (0, crop_high, width, high)
    crop = im.crop(box)
    out = crop.resize((width,high),Image.ANTIALIAS)
    imgray = out.convert('L')  # 转换为灰度图片 便于处理
    pixels = list(imgray.getdata())  # 得到像素数据 灰度0-255

    for row in range(high):
        rowStart = row * width  # 起始位置行号
        for index in range(width - 1):
            leftIndex = rowStart + index  # 当前位置号
            rightIndex = leftIndex + 1
            diff.append(pixels[leftIndex] > pixels[rightIndex])

    return diff


def getHamming(diff=[], diff2=[]):
    # print len(diff)
    hamming_distance = 0
    for i in range(len(diff)):
        if diff[i] != diff2[i]:
            hamming_distance += 1
    return hamming_distance

if __name__ == '__main__':

    width = 32
    high = 32
    crop_high=3
    dirName = "E:\SF6压力表"  # 相册路径
    allDiff = []
    postFix = picPostfix()
    dirList = listdir(dirName)
    for i in dirList:
        if str(i).split('.')[-1] in postFix:  # 判断后缀是不是照片格式
            im = Image.open(dirName+'/'+i)
            diff = getDiff(crop_high,width, high, im)
            allDiff.append((str(i), diff,[1]))
    for i in range(len(allDiff)):
        if allDiff[i][2][0]==0:
            continue
        for j in range(i + 1, len(allDiff)):
            if i != j:
                if  allDiff[j][2][0]==0:
                    continue 
                ans = getHamming(allDiff[i][1], allDiff[j][1])
                #print(ans)
                if ans <= 150:
                    print (allDiff[i][0], "and", allDiff[j][0], "maybe same photo...")
                    #print("删除图片{}".format(allDiff[j][0]))
                    allDiff[j][2][0]=0
                    if os.path.exists(dirName+'/'+allDiff[j][0]):
                        os.remove(dirName+'/'+allDiff[j][0])

