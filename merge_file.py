#! usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = ningkai.yang@tongdun.cn
import os

if __name__ == "__main__":
    path_file = os.path.join(os.getcwd(), "file")
    result_name = os.path.join(os.getcwd(), 'label_file.txt')
    file_result_name = open(result_name, "a")
    path_file_list = os.listdir(path_file)

    for name_file in path_file_list:
        if name_file.split(".")[-1] != 'txt':
            continue
        abs_name_file = os.path.join(path_file,name_file)
        total_resutl_list = []
        file = open(abs_name_file, "r")
        info_list = file.readlines()
        file_result_name.writelines(info_list)
        file_result_name.flush()
        file.close()
    file_result_name.close()
    print "ok"



