# 图像预处理小工具集合

### 运行环境
1. mac 10.12；
2. python 2.7;

###  工具说明
- `detection_evaluation.py`计算label_file和detect_file目录下所有文件的recall和precision。

1. 目录结构：./data/label_file/ 存放人工标注好的.txt文件，./data/detect_file/ 存放检测出来的.txt文件，./result/resut 存放检测结果；
2.  注意事项：label_file和detect_file请保存正确标注格式，否则无法正确运行；
3.  结果说明：每次输出一个文件的recall和precision，无效文件输出`none`，最后输出所有有效文件的average recall和average precision；

- `validate_file.py`效验file目录下所有文件是否符合格式。

1. 目录结构：./file 存放所有 .txt 文件；./valid_file 存放运行后有效的 .txt 文件；./invalid_file 存放运行后无效的 .txt 文件；
2. 有效.txt 格式说明： 对于一条记录`x0 x1 x2 x3 x4 x5`满足x0以 .jpg 结束字符串，x2, x3, x4, x5 为非负整数； 

- `replace_word_e2c.py` 将码表中编码转换为字符。
- `replace_word_C2E.py` 将字符转换码表中编码转换，为以上工具的逆过程。

### 处理流程
先用`validate_file.py`对file 进行有效性检查，valid_file／ 中生成有效file文件，再用`detection_evaluation.py`计算。

最后file 文件格式统一为：一条记录`x0 x1 x2 x3 x4 x5`满足x0以 .jpg 结束字符串，x1 为字符编码, x2, x3 为标注框左上角（x， y）, x4，x5 分别为标注框width，height； 

### TODO

### bug