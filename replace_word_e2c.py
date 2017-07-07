#! usr/bin/env python
# -*- coding:utf-8 -*-
import os

# 编码表转字符工具
words_name = os.path.join(os.getcwd(), "words_all.txt")
label_filedir = os.listdir(os.path.join(os.getcwd(), "file"))
new_filedir = os.listdir(os.path.join(os.getcwd(), "result"))

file1 = open(words_name)
allword = file1.readlines()
for label_file in label_filedir:
    # 排除macos配置文件
    if label_file.split('.')[-1] != 'txt':
        continue
    new_path = os.path.join(os.getcwd(), "result")
    origin_path = os.path.join(os.getcwd(), "file")
    new_label = os.path.join(new_path, label_file)
    origin_label = os.path.join(origin_path, label_file)
    os.system("touch %s" % (new_label))
    file2 = open(origin_label)
    label_txt = file2.readlines()
    # 将words_all转化为dict
    dict_word = {}
    index = 0
    for x in allword:
        word = x.split()
        dict_word[index] = word[1]
        index += 1
    # 将label_txt 中编码替换为对应字符
    label_new_txt = list()
    new_txt = ""
    for x in label_txt:
        x1 = x.split()
        char = int(x1[1])
        replace = dict_word[char - 1]
        x1[1] = replace
        x_str = " ".join(x1)
        new_txt = new_txt + x_str + '\n'
        # 将new_txt 写入新文件中
    file_new_label = open(new_label, 'w')
    file_new_label.writelines(new_txt)
    file1.close()
    file_new_label.close()
print('ok')