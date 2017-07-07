#! usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = ningkai.yang@tongdun.cn
from __future__ import division
import os

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

ign_list=[num for num in xrange(191,253)]

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

# 计算label和detect中相同字符的标注框匹配数目
# input：相同字符在label和detect中标注框list
# output：标注框匹配数目
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
    path = os.getcwd()
    path_l = os.path.join(path, "data/label_file")
    path_d = os.path.join(path, "data/detect_file")
    listdir_l = os.listdir(path_l)
    listdir_d = os.listdir(path_d)
    listdir_abs_l = [path_l + "/" + x for x in listdir_l]
    listdir_abs_d = [path_d + "/" + x for x in listdir_d]

    # 判定result文件是否存在，若否则新建
    if os.path.exists(os.path.join(os.getcwd(), "result/")) == False:
        os.mkdir(os.path.join(os.getcwd(), "result/"))
    if os.path.exists(os.path.join(os.getcwd(), "result/result.txt")) == True:
        os.remove(os.path.join(os.getcwd(), "result/result.txt"))

    # os.mknod(os.path.join(os.getcwd(), "result/result.txt")) //os.mknod()在mac下为什么失效？
    os.system("touch result/result.txt")
    os.system("chmod 770 result/result.txt")
    # file_result = open(path_result, "w+")
    return (listdir_abs_l, listdir_abs_d)

if __name__ == "__main__":
    (listdir_abs_l, listdir_abs_d) = init()
    name_result = os.path.join(os.getcwd(), "result/result.txt")
    file_result = open(name_result,"w+")
    cnt_valid = 0
    sum_recall = 0
    sum_precision = 0

    for path_abs_l in listdir_abs_l:
        name_l = path_abs_l.split('/')[-1]
        if name_l.split('.')[-1] != "txt":
            continue
        elif (name_l not in [x.split('/')[-1] for x in listdir_abs_d]) or (len(listdir_abs_d) == 0):
            print('none, %s' % (name_l))
            file_result.writelines("none" + ", ")
            file_result.writelines(name_l + "\n")
            continue
        else:
            file_l = open(path_abs_l)
            path_abs_d = os.getcwd() + "/data/detect_file/" + name_l
            file_d = open(path_abs_d)
            list_l = file_l.readlines()
            list_d = file_d.readlines()
            # 将一个label_file存到dict_l中，一个detect_file存到dict_l中
            dict_l = {}
            dict_d = {}
            for item in list_l:
                one = item.split()
                char = one[1]
                if char in ign_list:
                    continue
                info_0 = one[2:]
                info = map(int, info_0)
                dict_l.setdefault(char, []).append(info)
            for item in list_d:
                one = item.split()
                char = one[1]
                info_0 = one[2:]
                info = map(int, info_0)
                dict_d.setdefault(char, []).append(info)
            dict_len_l = multi_dict_len(dict_l)
            dict_len_d = multi_dict_len(dict_d)

            # 新增
            # ==计算recall：START==
            # cnt_bingo表示在dict_d中识别出来的字符数量
            cnt_bingo = 0
            # dict_new_l保存在dict_d中识别出来的字符
            dict_new_l = {}
            for dict_one in dict_l:
                if len(dict_l[dict_one]) == 1:
                    if dict_d.has_key(dict_one):
                        cnt_bingo += 1
                        dict_new_l[dict_one] = dict_l[dict_one]
                else:
                    if dict_d.has_key(dict_one):
                        dict_new_l[dict_one] = dict_l[dict_one]
                        cnt_bingo += len(dict_l[dict_one])
            if dict_len_l == 0:
                recall = 0
            else:
                recall = cnt_bingo / dict_len_l
            # ==计算recall：END==

            # ==计算precision:START==
            # cnt_pefect表示正确识别出字符的标注框是准确的，通过IOU>=0.8判定
            cnt_pefect = 0
            for dict_one in dict_new_l:
                cnt_pefect += match_num(dict_l[dict_one], dict_d[dict_one])
            if cnt_bingo == 0:
                precision = 0
            else:
                precision = cnt_pefect / cnt_bingo
            # ==计算precision:END==

            cnt_valid += 1
            sum_recall += recall
            sum_precision += precision

            result_recall = "recall=%.3f" % recall
            result_precision = "precision=%.3f" % precision
            result = "%s, %s, %s" % (result_recall, result_precision, name_l)
            print result
            file_result.writelines(result + "\n")
            file_result.flush()
            file_l.close()
            file_d.close()
    if(cnt_valid != 0):
        result_recall_average = "average recall=%.3f" % (sum_recall / cnt_valid)
        result_precision_average = "average precision=%.3f" % (sum_precision / cnt_valid)
        result_average = "\nvalid count=%s, %s, %s" % (cnt_valid ,result_recall_average, result_precision_average)
    else:
        result_average = 'none valid file.'
    print result_average
    file_result.writelines(result_average)
    file_result.flush()
    file_result.close()