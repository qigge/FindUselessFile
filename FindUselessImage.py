#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os,shutil
import re

xcodeproj_path = ''

def find_last(string,str):
    last_position=-1
    while True:
        position=string.find(str,last_position+1)
        if position==-1:
            return last_position
        last_position=position

def find_all_images(file_dir):
    print('******正在查找所有图片文件（png,jpg,jpeg)*****')
    fileType = ['.png','.jpg','.jpeg']
    image_list = []
    for root, dirs, files in os.walk(file_dir):
        # 找到工程目录

        # 忽略文件夹
        if (root.find('/Pods') != -1 or   #忽略 Pods文件夹
        root.find('.xcodeproj') != -1 or  #忽略 工程文件夹
        root.find('.xcworkspace') != -1 or #忽略 Pods工程文件夹
        root.find('.bundle') != -1 or  #忽略 bundle包
        root.find('.git') != -1):      #忽略 git文件夹
            continue
        
        # xcassets 的图片
        xcassetsIndex = root.find('.xcassets/')
        if xcassetsIndex != -1: 
            imagesetIndex = root.find('.imageset')
            if imagesetIndex != -1 :
                image_list.append((root[find_last(root,'/')+1:imagesetIndex],root))
        else:
            # 其他图片
            for file in files:
                file_info = os.path.splitext(file)
                if file_info[1] in fileType:
                    find_index = file_info[0].find('@')
                    if find_index > -1:
                        image_list.append((file_info[0][:find_index],os.path.join(root, file)))
                    else:
                        image_list.append((file_info[0],os.path.join(root, file)))
    
    find_useless_image_list(image_list)
        
def find_useless_image_list(image_list):
    print('******正在从文件（.h,.m,.mm,.xib,.storyboard）中查找没有用到的*****')
    fileType = ['.h', '.m','.mm','.xib','.storyboard']

    for root, dirs, files in os.walk(file_dir):
        # 忽略文件夹
        if (root.find('/Pods') != -1 or 
        root.find('.bundle') != -1 or  
        root.find('.xcodeproj') != -1 or 
        root.find('.xcworkspace') != -1 or 
        root.find('.git') != -1 or 
        root.find('.xcassets/') != -1):
            continue

        for file in files:
            if os.path.splitext(file)[1] in fileType:
                with open(os.path.join(root, file),'r') as f:
                    content = f.read()
                    image_list = [(filename, path) for filename, path in image_list 
                    if content.find('"%s.'%(filename)) == -1 
                    and content.find('"%s@'%(filename)) == -1
                    and content.find('"%s"'%(filename)) == -1]
    print(image_list)
    print(len(image_list))

    remove_image(image_list)

def remove_image(file_list):
    print('******正在将无用图片删除*****')
    # 创建无用文件文件夹
    useless_file_dir = file_dir+'/UselessImage'
    os.mkdir(useless_file_dir)

    for filename, path in file_list:
        print(path)
        try:
            shutil.move(path, useless_file_dir)
        except :
            print('已存在')
        # if os.path.isfile(path):
        #     os.remove(path)
        # else:
        #     delete_dir(path)

# 删除目录
def delete_dir(file_dir):
     for i in os.listdir(file_dir):
         path_file = os.path.join(file_dir,i)  # 取文件绝对路径
         if os.path.isfile(path_file):
            os.remove(path_file)
         else:
            delete_dir(path_file)

print('******请输入要清理的工程目录*****')
print('******或者将工程目录拖入即可*****')
file_dir = input()



find_all_images(file_dir)

print('完成')