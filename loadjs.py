import os
import json
# 此函数用以加载物品id


def load():
    _files_ = os.listdir('allid')                   # 存储json文件名称
    _list_ = []                                     # 存储id列表
    for _file_ in _files_:                          # 遍历路径下文件进行数据读取
        if _file_[-5:] == '.json':                  # 判断是否为合法文件
            with open('allid\\'+str(_file_), 'rb') as fi:# 读取文件内容
                _list_.append(json.load(fi))
    return _list_, _files_
