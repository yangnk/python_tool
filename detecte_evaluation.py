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
def match_num(dict_label, dict_detect):
    num = 0
    for key1_detect in dict_detect:
        for key1_label in dict_label:
            if (dict_detect[key1_detect] == dict_label[key1_label]) == False:
                continue
            list1 = map(int,key1_detect[1:])
            list2 = map(int, key1_label[1:])
            (my_bool, my_iou)=calcu_IOU(list1, list2)
            if my_bool == False:
                continue
            num += 1
            break
    return num

def init():
    label_path = os.path.join(os.getcwd(), 'label_file.txt')
    detect_path = os.path.join(os.getcwd(), 'detect_file.txt')
    try:
        label_file = open(label_path, 'r')
    except IOError:
        print('no label_file.txt！')
    try:
        detect_file = open(detect_path, 'r')
    except IOError:
        print('no detect_file.txt！')

    name_result = os.path.join(os.getcwd(), "result.txt")
    # 判定result文件是否存在，若否则新建
    if os.path.exists(os.path.join(os.getcwd(), "result/")) == False:
        os.mkdir(os.path.join(os.getcwd(), "result/"))
    if os.path.exists(os.path.join(os.getcwd(), "result/result.txt")) == True:
        os.remove(os.path.join(os.getcwd(), "result/result.txt"))
    os.system("touch result/result.txt")
    os.system("chmod 770 result/result.txt")
    file_result = open(name_result,"w+")
    return (label_file, detect_file, file_result)

# 将words_all.txt 转换为dict
# input:null
# output:words_dict
def gen_words_dict():
    try:
        words_file = open(os.path.join(os.getcwd(), 'words_all.txt'), 'r')
    except IOError:
        print('no words_all.txt！')
    words_list = words_file.readlines()
    words_dict = {}
    for words_item in words_list:
        words_item_list = words_item.split(" ")
        words_encoding = int(words_item_list[0])
        word_char = words_item_list[1]
        words_dict[words_encoding] = word_char
    words_file.close()
    return words_dict

# 判断编码是否在编码表特定区间
# input: 编码bbox_encode，string类型
# output:在区间为TRUE, 不在区间为FALSE
def is_ign(bbox_encode):
    ign_list = [encode for encode in xrange(191, 253)]
    return int(bbox_encode) in ign_list

# 将file_list 转为file_dict
# input:file_list
# output:file_dict
def gen_dict(file_all_list):
    words_all_dict = gen_words_dict()
    file_dict = {}
    item_dict = {}
    pre_file_name = ''
    for item in file_all_list:
        item_list = item.split(" ")
        file_name = item_list[0]
        bbox_encode = item_list[1]
        bbox_info = item_list[2:]
        # 判定是否跳转下一张img
        if file_name != pre_file_name:
            file_dict[pre_file_name] = item_dict
            item_dict = {}
            # item_dict.clear()
        item_dict_key = map(str, bbox_info)
        item_dict_key.insert(0, words_all_dict[int(bbox_encode)])
        if is_ign(bbox_encode):
            pass
        else:
            item_dict[tuple(item_dict_key)] = bbox_encode
        pre_file_name = file_name
    file_dict[file_name] = item_dict
    del file_dict['']
    return file_dict

if __name__ == "__main__":
    # (listdir_abs_l, listdir_abs_d) = init() # 重写init（），output：lable_file 和 detect_file 路径名
    # 将label_file 和 detect_file 读入dict中
    (label_file, detect_file, file_result) = init()
    label_list = label_file.readlines()
    detect_list = detect_file.readlines()
    label_dict = gen_dict(label_list)
    detect_dict = gen_dict(detect_list)
    cnt_valid = 0
    sum_recall = 0
    sum_precision = 0
    # 计算正确match的bounding box
    for detect_item in detect_dict:
        # label中没有detect中file
        if label_dict.has_key(detect_item) ==False:
            result = "none %s" % (detect_item)
        else:
            cnt_right_bbox = match_num(label_dict[detect_item], detect_dict[detect_item])
            # 计算recall
            cnt_label_bbox = len(label_dict[detect_item])
            recall = cnt_right_bbox / cnt_label_bbox
            sum_recall += recall
            # 计算precision
            cnt_detect_bbox = len(detect_dict[detect_item])
            precision = cnt_right_bbox / cnt_detect_bbox
            sum_precision += precision
            cnt_valid += 1
            result_recall = "recall=%.3f" % recall
            result_precision = "precision=%.3f" % precision
            result = "%s, %s, %s" % (result_recall, result_precision, detect_item)
        print result
        file_result.writelines(result + "\n")
        file_result.flush()
        label_file.close()
        detect_file.close()
        result_recall_average = "average recall=%.3f" % (sum_recall / cnt_valid)
        result_precision_average = "average precision=%.3f" % (sum_precision / cnt_valid)
        result_average = "\nvalid count=%s, %s, %s" % (cnt_valid ,result_recall_average, result_precision_average)
    print result_average
    file_result.writelines(result_average)
    file_result.flush()
    file_result.close()