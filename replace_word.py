#! usr/bin/env python
# -*- coding:utf-8 -*-
import os

file_name = "/Users/yangnk_mac/work/pretreatment/labelReplace/words_all.txt";
label_file = "/Users/yangnk_mac/work/pretreatment/labelReplace/label_file/3.txt";
new_file = "/Users/yangnk_mac/work/pretreatment/labelReplace/label_file/tmp.txt"

file1 = open(file_name);
file2 = open(label_file);
allword = file1.readlines();
label_txt = file2.readlines();
# 将words_all转化为dict
dict_word = {};
index = 0;
for x in allword:
    word = x.split();
    dict_word[index] = word[1];
    index += 1;
# 将label_txt 中编码替换为对应字符
label_new_txt = list();
new_txt = "";
for x in label_txt:
    x1 = x.split();
    char = int(x1[1]);
    replace = dict_word[char - 1];
    x1[1] = replace;
    x_str = " ".join(x1);
    new_txt = new_txt + x_str +'\n' ;

# 将new_txt 写入新文件中
#os.mknod(new_file);
#fp = open(new_file,w);
os.system("touch /Users/yangnk_mac/work/pretreatment/labelReplace/tmp.txt") # 绝对路径，之后修改成相对路径
# f = open("/Users/yangnk_mac/work/pretreatment/labelReplace/tmp.txt", w);
# f.write(new_txt);

file1.close();
print dict_word;
print label_txt;
print new_txt;
