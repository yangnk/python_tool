#! usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = ningkai.yang@tongdun.cn
import os
import shutil

def init():
    path = os.path.join(os.getcwd(), "file")
    file_list = os.listdir(path)
    file_list_name = [path + "/" + x for x in file_list]

    # 判定valid_file文件夹是否存在，若否则新建
    if os.path.exists(os.path.join(os.getcwd(), "valid_file")) == False:
        os.mkdir(os.path.join(os.getcwd(), "valid_file"))
    if os.path.exists(os.path.join(os.getcwd(), "invalid_file")) == False:
        os.mkdir(os.path.join(os.getcwd(), "invalid_file"))
    # if os.path.exists(os.path.join(os.getcwd(), "result_valid_file.txt")) == True:
    #     os.remove(os.path.join(os.getcwd(), "result_valid_file.txt"))
    os.system("touch result_valid_file.txt")
    os.system("chmod 770 result_valid_file.txt")
    return file_list_name

# 判定该条记录是否有效
# input: 标注文件中一条记录
# output：该条记录有效：True，该条记录无效：False
def is_valid(info_str):
    info_str_list = info_str.split(" ")
    # info_str_list = map(int, info_str_list[2,])
    info_str_list_4 = map(int, info_str_list[2:])
    if len(info_str_list) != 6:
        return False
    elif info_str_list[0].split(".")[-1] != "jpg":
        return False
    elif (info_str_list_4[0] >= 0 and info_str_list_4[1] >= 0 and info_str_list_4[2] > 0 and info_str_list_4[3] > 0) == False:
        return False
    return True

if __name__ == "__main__":
    file_list_name = init()
    path_abs = os.getcwd()
    path_file = os.path.join(os.getcwd(), "file")
    path_valid = os.path.join(os.getcwd(), "valid_file")
    path_invalid = os.path.join(os.getcwd(), "invalid_file")
    # print "ok"
    # 判定file中格式是否有效
    for name_file in file_list_name:
        file = open(name_file, "r")
        info_list = file.readlines()
        cnt = 0
        for info_str in info_list:
            info_len = len(info_list)
            cnt += 1
            if is_valid(info_str) == False:
                # name_file.split("\\")[-1]
                shutil.copyfile(os.path.join(path_file, name_file.split("/")[-1]), os.path.join(path_invalid, name_file.split("/")[-1]))
                break
            if cnt == info_len:
                shutil.copyfile(os.path.join(path_file, name_file.split("/")[-1]), os.path.join(path_valid, name_file.split("/")[-1]))
    print "ok"



