import json
import GetInfo
import csv
import time
import random
import loadjs
import deleteold
import initialdatabase as idb
import sys
from info_local import cookie_buff


def time_now():                                                         # 时间戳生成函数
    ticks_ = time.strftime('%Y_%m_%d_%H:%M:%S', time.localtime())
    return ticks_


def err_action():                                                       # 规定循环内出现错误后的行为函数
    time.sleep(120)                                                     # 爬取失败等待网络连接或远程主机关闭反爬虫机制
    tick = time_now()                                                   # 获取当前时间
    print(e.__class__.__name__)                                         # 打印错误名称
    with open('errlog.txt', 'a', encoding='utf-8') as fi:               # 将发生的错误写入日志文件
        fi.write('igxe:%s' % tick, e.__class__.__name__)


def times_sleep(MinS, MaxS):                             # 随机时长暂停函数
    SleepTime = random.randint(MinS, MaxS)
    time.sleep(SleepTime)


game = input("game:\n")                                                 # 选择需要爬取的市场
if game == "":
    game = "csgo"

# 反反爬虫
MinSleepTime = int(input("MinSleepTime（大于4以免反爬虫）:\n"))             # 两次爬取间的最小间隔时间
MaxSleepTime = int(input("MaxSleepTime:\n"))                            # 两次爬取间的最大间隔时间


while 0 < MaxSleepTime < MinSleepTime:                                  # 检测间隔时间是否合法
    print("MaxSleepTime must be larger than MinSleepTime,pls try again.")
    MinSleepTime = int(input("MinSleepTime（大于4以免反爬虫）:\n"))
    MaxSleepTime = int(input("MaxSleepTime:\n"))



# input("cookie:\n")
# 选择要爬取的类,类之间用英文逗号分隔
str_choose = input("choose a class:\n")
class_choose = str_choose.split(",")
if 0 == len(class_choose):
    print("没有选择任何类型，程序终止运行")
    sys.exit()
# 若选取的类中存在44码，则爬取所有数据
if '44' in class_choose:
    class_choose.remove('44')
    for ii in range(0,15):
        if str(ii) not in class_choose:
            class_choose.append(str(ii))
# 询问是否启用数据存储
enable_txt = input("save data as .txt file?(y/n)")
enable_csv = input("save data as .csv file?(y/n)")
enable_sql = input("save data to databases?(y/n)")
# 删除旧的数据
if enable_txt == 'y' or enable_csv == 'y' or enable_txt == 'Y' or enable_csv == 'Y':
    s = input("delete old data(text/csv)？")
    if s == 'y' or s == 'Y':
        deleteold.delete_old_file()
if enable_sql == 'y' or enable_sql == 'Y':
    s = input("delete old database(mysql)？")
    if s == 'y' or s == 'Y':
        idb.delete_all()
        idb.initial_all()

# 初始化两种数据存储文件
if enable_txt == 'y' or enable_txt == 'Y':
    file_buff = open("price_now\\HistoryPrice_buff.txt", 'a', encoding='utf-8')
    file_igxe = open("price_now\\HistoryPrice_igxe.txt", 'a', encoding='utf-8')
    file_max = open("price_now\\HistoryPrice_max.txt", 'a', encoding='utf-8')
    file_com = open("price_now\\HistoryPrice_com.txt", 'a', encoding='utf-8')
    file_wuhu = open("price_now\\wuhu.txt", 'a', encoding='utf-8')

if enable_csv =='Y' or enable_csv =='y':
    csvfile_buff = open('price_now\\HistoryPrice_buff.csv', 'a', newline='', encoding='utf-8')
    csv_writer_buff = csv.writer(csvfile_buff)
    csvfile_igxe = open('price_now\\HistoryPrice_igxe.csv', 'a', newline='', encoding='utf-8')
    csv_writer_igxe = csv.writer(csvfile_igxe)
    csvfile_max = open('price_now\\HistoryPrice_max.csv', 'a', newline='', encoding='utf-8')
    csv_writer_max = csv.writer(csvfile_max)
    csvfile_com = open('price_now\\HistoryPrice_com.csv', 'a', newline='', encoding='utf-8')
    csv_writer_com = csv.writer(csvfile_com)
    csvfile_wuhu = open('price_now\\wuhu.csv', 'a', newline='', encoding='utf-8')
    csv_writer_wuhu = csv.writer(csvfile_wuhu)

# 数据名称规范
# handler_box = {'buff': [file_buff, csvfile_buff, csv_writer_buff],
#                'max': [file_max, csvfile_max, csv_writer_max],
#                'igxe': [file_igxe, csvfile_igxe, csv_writer_igxe],
#                'com': [file_com, csvfile_com, csv_writer_com],
#                'wuhu': [file_wuhu, csvfile_wuhu, csv_writer_wuhu]}

# 获取回传的json数据
id_dict, name_list = loadjs.load()
# 打印时间戳
ticks = time_now()
print(ticks)
# 定义爬取失败标志
flag_un = 0

# 遍历每一个类的id数据库进行爬取
for _i_ in class_choose:
    _i_ = int(_i_)                                                      # 将已选择的id数据库编号转换为整型
    class_name = name_list[_i_]
    for name, _id_ in id_dict[_i_].items():
        info_price_igxe = -1
        info_price_buff = -1
        info_price_max = -1
        print('#'*80)                                                   # 输出分割号
        com_price = {}
        while True:
            try:
                #################################### 爬取buff信息 ###############################################################################################################
                if _id_['buff'] != 0:
                    InfoJson_buff = GetInfo.getinfo(game, _id_['buff'], cookie_buff)    # 进行数据爬取
                    info_buff = json.loads(InfoJson_buff)                               # 转换数据格式
                    info_data_buff = info_buff['data']                                  # 提取物品数据
                    info_items_buff = info_data_buff['items']                           # 提取单个物品数据
                    if len(info_items_buff) != 0:                                       # 该类别存在在售饰品则进行下一步
                        info_item_buff = info_items_buff[0]                             # 最低价在售饰品数据
                        info_price_buff = info_item_buff['price']                       # 该饰品价格
                        goods_name_buff = info_data_buff['goods_infos'][str(_id_['buff'])]['name']# 该饰品名称
                        # 写入字典以便后续比较
                        com_price[info_price_buff] = goods_name_buff + 'buff'
                        # buff数据输出
                        if enable_txt == 'y' or enable_txt == 'Y':
                            file_buff.write("%s %s\n" % (info_price_buff, goods_name_buff))
                            file_buff.flush()                                               # 写入txt文件
                        if enable_csv == 'Y' or enable_csv == 'y':
                            csv_writer_buff.writerow([info_price_buff, goods_name_buff])
                            csvfile_buff.flush()                                            # 写入csv文件
                        if enable_sql == 'y' or enable_sql == 'Y':
                            idb.add_all_value('BUFF', [{'goods_name_buff': '"' + goods_name_buff + '"',
                                                        'info_price_buff': info_price_buff}])# 写入数据库
                        print("Done.", 'id:%10d' % _id_['buff'], 'price:%10f' % float(info_price_buff), 'name:' + goods_name_buff, 'buff')# 输出信息至运行窗口
                        flag_un = 0                                                     # 确定信息成功爬取
                    else:
                        print('null')                                                   # 若无在售饰品，显示为null
                        flag_un = 0
            except Exception as e:                                                      # 爬取失败后行为
                if flag_un==5:                                                          # 若同循环中接连出现五次错误，则终止程序
                    break
                else:
                    err_action()                                                        # 若错误出现不超过五次，则进行错误记录
                    flag_un = flag_un + 1
                continue
            else:
                break
        times_sleep(MinSleepTime, MaxSleepTime)                                          # 对同一网站每两次爬取间隔12-15s

        while True:
            try:
                #################################### 爬取igxe信息 ###############################################################################################################
                if _id_['igxe'] != 0:
                    InfoJson_igxe = GetInfo.getinfo_igxe(game, _id_['igxe'])            # 爬取数据
                    info_igxe = json.loads(InfoJson_igxe)                               # 转换数据格式
                    info_dlist_igxe = info_igxe['d_list']
                    if len(info_dlist_igxe) != 0:
                        info_item_igxe = info_dlist_igxe[0]                             # 饰品数据
                        info_price_igxe = info_item_igxe['unit_price']                  # 饰品价格
                        goods_name_igxe = info_item_igxe['product_name'] + ' (' + info_item_igxe['exterior_name'] + ')'# 饰品名称
                        # 写入字典以便后续比较
                        com_price[info_price_igxe] = goods_name_igxe + 'igxe'
                        # igxe数据输出
                        if enable_txt == 'y' or enable_txt == 'Y':
                            file_igxe.write("%s %s\n" % (info_price_igxe, goods_name_igxe))
                            file_igxe.flush()                                               # 写入txt文件
                        if enable_csv == 'Y' or enable_csv == 'y':
                            csv_writer_igxe.writerow([info_price_igxe, goods_name_igxe])
                            csvfile_igxe.flush()                                            # 写入csv文件
                        if enable_sql == 'y' or enable_sql == 'Y':
                            idb.add_all_value('IGXE', [{'goods_name_igxe': '"' + goods_name_igxe + '"',
                                                        'info_price_igxe': info_price_igxe}])# 写入数据库

                        print("Done.", 'id:%10d' % _id_['igxe'], 'price:%10f' % float(info_price_igxe), 'name:' + goods_name_igxe, 'igxe')# 输出信息
                    else:
                        print("null")
            except Exception as e:                                                      # 爬取失败后行为
                if flag_un == 5:                                                        # 若同循环中接连出现五次错误，则终止程序
                    break
                else:
                    err_action()                                                        # 若错误出现不超过五次，则认为可能是网络错误，进行错误记录
                    flag_un = flag_un + 1
                continue
            else:                                                                       # 程序正常运行则跳出循环进行下一次
                break
        times_sleep(MinSleepTime, MaxSleepTime)                                          # 对同一网站每两次爬取间隔12-15s

        while True:
            try:
                #################################### 爬取max信息 ###############################################################################################################
                if _id_['max'] != 0:
                    InfoJson_max = GetInfo.getinfo_max(game, _id_['max'])               # 爬取数据
                    info_max = json.loads(InfoJson_max)                                 # 转换数据格式
                    info_data_max = info_max['result']                                  # 饰品数据
                    goods_name_max = info_data_max['name']                              # 饰品名称
                    info_price_max = info_data_max['quick_price']                       # 饰品价格
                    # max数据处理与输出
                    if enable_txt == 'y' or enable_txt == 'Y':
                        file_max.write("%s %s\n" % (info_price_max, goods_name_max))
                        file_max.flush()                                                    # 写入txt文件
                    if enable_csv == 'Y' or enable_csv == 'y':
                        csv_writer_max.writerow([info_price_max, goods_name_max])
                        csvfile_max.flush()                                                 # 写入csv文件
                    if enable_sql == 'y' or enable_sql == 'Y':
                        idb.add_all_value('`MAX`', [{'goods_name_max': '"' + goods_name_max + '"',
                                                     'info_price_max': info_price_max}])    # 写入数据库
                    print("Done.", 'id:%10d' % _id_['max'], 'price:%10f' % float(info_price_max), 'name:' + goods_name_max, 'max')# 终端输出信息
                    # 写入字典以便后续比较
                    com_price[info_price_max] = goods_name_max + 'max'

            except Exception as e:                                                      # 爬取失败后行为
                if flag_un == 5:                                                        # 若同循环中接连出现五次错误，则终止程序
                    break
                else:
                    err_action()                                                        # 若错误出现不超过五次，则认为可能是网络错误，进行错误记录
                    flag_un = flag_un + 1
                continue
            else:
                break
        times_sleep(MinSleepTime, MaxSleepTime)  # 对同一网站每两次爬取间隔12-15s

        #################################### 对比差价 ###############################################################################################################
        max_price = max(com_price)                                                      # 找出最高价
        min_price = min(com_price)                                                      # 找出最低价
        diff_price = float(max_price) - float(min_price)                                # 计算差价
        # 输出至文件
        if enable_txt == 'y' or enable_txt == 'Y':
            file_com.write("%s %s %s %s %.3f\n" % (com_price[max_price], max_price, com_price[min_price], min_price, diff_price))
            file_com.flush()                                                                # 写入txt文件
        if enable_csv == 'Y' or enable_csv == 'y':
            csv_writer_com.writerow([com_price[max_price], max_price, com_price[min_price], min_price, diff_price])
            csvfile_com.flush()                                                             # 写入csv文件
        if enable_sql == 'y' or enable_sql == 'Y':
            idb.add_all_value('comp', [{'name_of_max_price': '"' + com_price[max_price] + '"',
                                        'max_price': max_price,
                                        'name_of_min_price': '"' + com_price[min_price] + '"',
                                        'min_price': min_price,
                                        'diff': diff_price}])                               # 写入数据库
        print("name:"+com_price[max_price], max_price, "name"+com_price[min_price], min_price, 'diff_price:%.3f' % diff_price)# 输出信息
        #################################### 对比buff ###############################################################################################################
        com2buff = {}
        k = 0
        if info_price_buff != -1:                                                       # 判断buff上是否有该饰品在售
            bupr = float(info_price_buff)                                               # 转换数据
            igpr = float(info_price_igxe)                                               # 转换数据
            mapr = float(info_price_max)                                                # 转换数据
            # 提取差价信息
            if info_price_max != -1:
                op = bupr - mapr
                if op > 0:
                    com2buff[op] = goods_name_max + 'max'
                    k = 1
            if info_price_igxe != -1:
                op = bupr - igpr
                if op > 0:
                    com2buff[op] = goods_name_igxe + 'igxe'
                    k = 1
            if k == 1:
                cheap = max(com2buff)
                print(cheap, com2buff[cheap])
                # 写差价信息
                if enable_txt == 'y' or enable_txt == 'Y':
                    file_wuhu.write("%s %s\n" % (cheap, com2buff[cheap]))
                    file_max.flush()                                                        # 写入txt文件
                if enable_csv == 'Y' or enable_csv == 'y':
                    csv_writer_wuhu.writerow([cheap, com2buff[cheap]])
                    csvfile_max.flush()                                                     # 写入csv文件
                if enable_sql == 'y' or enable_sql == 'Y':
                    idb.add_all_value('cheap', [{'cheap_price': cheap,
                                                 'cheap_name': '"' + com2buff[cheap] + '"'}])# 写入数据库

