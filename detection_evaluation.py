#! usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import division
import os
import math

# 计算一键多值dict记录数
# input：一键多值dict
# output：一键多值dict记录数
def multi_dict_len(dict):
    cnt = 0
    for x in dict:
        cnt += len(dict[x])
    return cnt

# 计算两个矩形重叠面积
# input：矩形a，矩形b
# output：两个矩形框是否匹配, 两个矩形IOU = a ∩ b/a ∪ b
def calcu_IOU(a, b):
    xa1 = a[0]
    ya1 = a[1]
    xa2 = a[0] + a[2]
    ya2 = a[1] + a[3]

    xb1 = b[0]
    yb1 = b[1]
    xb2 = b[0] + b[2]
    yb2 = b[1] + b[3]

    xac = (xa1 + xa2)/2
    yac = (ya1 + ya2)/2
    xbc = (xb1 + xb2)/2
    ybc = (yb1 + yb2)/2

    # dist = math.sqrt((xac - xbc)*(xac - xbc) + (yac - ybc)*(yac - ybc))
    # 判定矩形是否重叠，否则返回0
    if (abs(xbc - xac) <= (abs(xa1 - xa2)/2 + abs(xb1 - xb2)/2) and abs(ybc - yac) <= (abs(ya1 - ya2)/2 + abs(yb1 - yb2)/2)) == False:
        return False, 0

    # 计算重叠矩形面积
    xo1 = max(xa1, xb1)
    yo1 = max(ya1, yb1)
    xo2 = min(xa2, xb2)
    yo2 = min(ya2, yb2)
    area_o = (xo2 - xo1) * (yo2 - yo1)
    area_a = (xa2 - xa1) * (ya2 - ya1)
    area_b = (xb2 - xb1) * (yb2 - yb1)
    IOU = area_o/(area_a + area_b - area_o)

    # 判定两个标注框是否匹配
    if IOU >= 0.8:
        is_match = True
    else:
        is_match = False
    return is_match, IOU

# 计算label和detect中相同字符的标注框匹配数
# input：相同字符在label和detect中标注框
# output：标注框匹配数
def match_num(list1, list2):
    num = 0
    for x in list1:
        for y in list2:
            if calcu_IOU(x, y)[0] == True:
                num += 1
                continue
    if(num > len(list2)):
        num = len(list2)
    return num

def init():
    pass

if __name__ == "__main__":
    init()
    path_l = os.path.join(os.getcwd(), "data/3_l.txt")
    path_d = os.path.join(os.getcwd(), "data/3_d.txt")
    path_result = os.path.join(os.getcwd(), "result/result.txt")
    file_l = open(path_l);
    file_d = open(path_d);
    list_l = file_l.readlines();
    list_d = file_d.readlines();

    # 判定result文件是否存在，若否则新建
    if os.path.exists(os.path.join(os.getcwd(), "result/")) == False:
        os.mkdir(os.path.join(os.getcwd(), "result/"))
    if os.path.exists(os.path.join(os.getcwd(), "result/result.txt")) == False:
        os.system("touch result/result.txt")
        os.system("chmod 770 result/result.txt")
    file_result = open(path_result, "w+")

    dict_l = {};
    dict_d = {};
    for item in list_l:
        x = item.split();
        char = x[1];
        info_0 = x[2:];
        info = map(int, info_0)
        #dict_l[char] = info
        # dict_l.setdefault(,)
        dict_l.setdefault(char, []).append(info)
    for item in list_d:
        x = item.split();
        char = x[1];
        info_0 = x[2:];
        info = map(int, info_0)
        # dict_d[char] = info;
        dict_d.setdefault(char, []).append(info)

    dict_len_l = multi_dict_len(dict_l)
    dict_len_d = multi_dict_len(dict_d)

    # 计算recall
    cnt_bingo = 0
    for x in dict_l:
        if dict_d.has_key(x):
            cnt_bingo += 1
        #    if dict_d.has_key(x) == True:
        #        cnt += match_num(dict_l[x], dict_d[x])
        #        # cnt += 1
        # # else:
        #     if dict_d.has_key(x) == False:
        #         continue
        #     else:
        #         # multi_len = len(dict_l[x])
        #         cnt += match_num(dict_l[x], dict_d[x])

    # cnt_d = 0;
    # cnt_l = dict_len_l
    # for x in dict_l:
    #     if x in dict_d:
    #         cnt_d = cnt_d + 1;
    recall = cnt_bingo / dict_len_l

    # 计算precision
    # 判定被正确标注的数量，通过判定label中字符是否在detect出现，分字符只出现一次和出现多次两类处理
    cnt_pefect = 0
    for x in dict_l:
        # if len(dict_l[x]) == 1:
        if dict_d.has_key(x) == False:
            continue
        else:
            cnt_pefect += match_num(dict_l[x], dict_d[x])
    precision = cnt_pefect / cnt_bingo

    result_recall = "recall=%.3f" % recall
    result_precision = "precision=%.3f" % precision
    print result_recall
    print result_precision
    file_result.writelines(result_recall)
    file_result.writelines(result_precision)
    file_result.flush()
    file_l.close()
    file_d.close()
    file_result.close()