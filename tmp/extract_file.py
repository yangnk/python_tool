#! usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = ningkai.yang@tongdun.cn
import os

file_name = '/Users/yangnk_mac/PycharmProjects/python_tool/data/words_location_trans.txt'
file = open(file_name, 'r')
list = file.readlines()

dict = {}
for item in list:
    one = item.split();
    name = one[0];
    info = one[1:];
    info = map(int, info)
    dict.setdefault(name, []).append(info)
print(dict)
for key in dict:
    out = ''
    cnt = 0
    len_dict = len(dict[key])
    while cnt < len_dict :
        value_list = dict[key]
        one_info = value_list[cnt]
        out += key + ' '+' '.join(map(str,one_info)) + '\n'
        cnt += 1;
        print out
    path_out = os.path.join('/Users/yangnk_mac/PycharmProjects/python_tool/result', key)
    key_out = path_out[:-4] + '.txt'
    os.system('touch %s' % (key_out))
    file_out = open(key_out, 'w')
    file_out.write(out)
    file_out.flush()