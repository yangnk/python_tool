# -*- coding:utf-8 -*-
import os
import os.path
import shutil
# __author__ = kai.yu@tongdun.cn

input = os.walk( 'image')#输入图片目录
input2 = os.walk('label_file')#输入label目录
if os.path.exists( 'unlabel') is False:
    os.makedirs('unlabel')
outdir = 'unlabel'#检测是否存在unlabel目录，不存在则创建unlabel目录

for path,d,file in input2:
    name_list = [ name[:-4] for name in file]#取出label目录中所有文件名前缀

for path ,d , file in input:
    for pics in file:
        pic_name = pics[:-4]
        if pic_name not in name_list:
            print pic_name
            shutil.copy(os.path.join(path,pics),outdir)#取出图片目录中所有文件名字判断是否与label目录下中文件同名。否，则将其拷贝到unlabel目录下