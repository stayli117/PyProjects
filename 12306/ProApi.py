# -*- coding: UTF-8 -*
import re, urllib, urllib, http, json, datetime, time
from stationsInfo import stationLists, stations2CN, stations2CODE
from prettytable import PrettyTable
from datetime import timedelta, date
from Resources import *
from ProCls import Colored
from ProCls import myThread, threadLock

K = []
D = []
G = []
Z = []
T = []

"""获取数据"""


def getData(url):
    data = ''
    while 1:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            req = urllib.request.Request(url=url, headers=headers)
            data = urllib.request.urlopen(req).read().decode('utf-8')
            # print(url)
            # print(data)
            # if data['status'] == False:
            #     break
            if data.startswith(u'\ufeff'):
                data = data.encode('utf8')[3:].decode('utf-8')
            break
        except:
            continue
    return data


"""解析响应数据"""


def resolveData(from_station, to_station, date):
    # 拼接出查询链接
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, stations2CODE[from_station], stations2CODE[to_station])
    # 获取数据
    while 1:
        try:
            data = getData(url)
            lists = json.loads(data)["data"]["result"]
            # if data['status'] == False:
            #     print('获取失败！请检查网络')
            #     break
            break
        except:
            continue
    cont = []
    color = Colored()
    i = 0
    for items in lists:
        data = {
            "station_train_code": '',
            "from_station_name": '',
            "to_station_name": '',
            'start_time': '',
            'end': '',
            "lishi": '',
            "swz_num": '',
            "zy_num": '',
            "ze_num": '',
            "dw_num": '',
            "gr_num": '',
            "rw_num": '',
            "yw_num": '',
            "rz_num": '',
            "yz_num": '',
            "wz_num": '',
            "qt_num": '',
            "note_num": ''
        }
        item = items.split('|')
        data['station_train_code'] = item[3]

        if re.match(r'^K', item[3]):
            K.append(i)
        if re.match(r'^D', item[3]):
            D.append(i)
        if re.match(r'^G', item[3]):
            G.append(i)
        if re.match(r'^Z', item[3]):
            Z.append(i)
        if re.match(r'^T', item[3]):
            T.append(i)
        i = i + 1
        data['from_station_name'] = item[6]
        data['to_station_name'] = item[7]
        data['start_time'] = item[8]
        data['arrive_time'] = item[9]
        data['lishi'] = item[10]
        data['swz_num'] = item[32] or item[25]  # 商务座在32或25位置
        data['zy_num'] = item[31]
        data['ze_num'] = item[30]
        data['gr_num'] = item[21]
        data['rw_num'] = item[23]
        data['dw_num'] = item[27]
        data['yw_num'] = item[28]
        data['rz_num'] = item[24]
        data['yz_num'] = item[29]
        data['wz_num'] = item[26]
        data['qt_num'] = item[22]
        if item[0] == 'null':
            data['note_num'] = item[1]
        else:
            data['note_num'] = color.white(item[1])
        train_no = item[2]
        from_station_no = item[16]
        to_station_no = item[17]
        types = item[35]
        getPriceThread = myThread(1, "Thread-1", train_no, from_station_no, to_station_no, types, date, pricesDic)
        getPriceThread.start()  # 开启查询车票的线程
        for pos in name:
            if data[pos] == '':
                data[pos] = '-'
        threadLock.acquire()
        for pos in priceName:
            if pos == 'swz_num':
                data['swz_num'] = data['swz_num'] + '\n' + color.blue(pricesDic['A'])
            if pos == 'zy_num':
                data['zy_num'] = data['zy_num'] + '\n' + color.blue(pricesDic['B'])
            if pos == 'ze_num':
                data['ze_num'] = data['ze_num'] + '\n' + color.blue(pricesDic['C'])
            if pos == 'gr_num':
                data['gr_num'] = data['gr_num'] + '\n' + color.blue(pricesDic['D'])
            if pos == 'rw_num':
                data['rw_num'] = data['rw_num'] + '\n' + color.blue(pricesDic['E'])
            if pos == 'dw_num':
                data['dw_num'] = data['dw_num'] + '\n' + color.blue(pricesDic['F'])
            if pos == 'yw_num':
                data['yw_num'] = data['yw_num'] + '\n' + color.blue(pricesDic['G'])
            if pos == 'rz_num':
                data['rz_num'] = data['rz_num'] + '\n' + color.blue(pricesDic['H'])
            if pos == 'yz_num':
                data['yz_num'] = data['yz_num'] + '\n' + color.blue(pricesDic['I'])
            if pos == 'wz_num':
                data['wz_num'] = data['wz_num'] + '\n' + color.blue(pricesDic['J'])
        threadLock.release()
        cont.append(data)
    color = Colored()
    tickets = []
    for x in cont:
        tmp = []
        for y in name:
            if y == "from_station_name":
                s = color.green(stations2CN[x[y]]) + '\n' + color.red(stations2CN[x["to_station_name"]])
                tmp.append(s)
            elif y == "start_time":
                s = color.green(x[y]) + '\n' + color.red(x["arrive_time"])
                tmp.append(s)
            elif y == "station_train_code":
                s = color.yellow(x[y])
                tmp.append(s)
            else:
                tmp.append(x[y])
        tickets.append(tmp)
    return tickets


def filter(tickets, arguments):
    temp = []
    if arguments['-d']:
        for i in D:
            temp.append(tickets[i])
    if arguments['-k']:
        for i in K:
            temp.append(tickets[i])
    if arguments['-z']:
        for i in Z:
            temp.append(tickets[i])
    if arguments['-t']:
        for i in T:
            temp.append(tickets[i])
    if arguments['-g']:
        for i in G:
            temp.append(tickets[i])
    if arguments['-d'] == False and arguments['-k'] == False and arguments['-z'] == False and arguments[
        '-g'] == False and arguments['-t'] == False:
        return tickets

    return temp


# 检查输入信息from_station, to_station, d
def inputArgs(from_station, to_station, d):
    # 输入车站信息
    # from_station = input("请输入出发站：\n")
    # to_station = input("请输入目的地:\n")
    # d = input("请输入出发日期(格式：年-月-日)：\n")
    now_time = datetime.datetime.now()  # 当前日期
    # 校验
    flag1 = False
    flag2 = False
    flag3 = False

    while flag1 == False or flag2 == False or flag3 == False:
        from_index = stationLists.count(from_station)
        to_index = stationLists.count(to_station)
        # 始发站在车站列表中，并且始发站和终点站不同
        if from_index > 0 and to_station != from_station:
            flag1 = True
        # 终点站在车站列表中，并且始发站和终点站不同
        if to_index > 0 and to_station != from_station:
            flag2 = True
        rdate = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', d)
        if rdate:
            from_date = datetime.datetime.strptime(d, '%Y-%m-%d')
            sub_day = (from_date - now_time).days
            if -1 <= sub_day < 15:
                flag3 = True
        if not flag1:
            print("始发站不合法！")
            from_station = input("请输入出发站(年-月-日)：\n")
        if not flag2:
            print("终点站不合法！")
            to_station = input("请输入目的地:\n")
        if not flag3:
            print("出发日期不合法！")
            d = input("请输入出发日期(格式：年-月-日)：\n")
            from_date = datetime.datetime.strptime(d, '%Y-%m-%d')
            sub_day = (from_date - now_time).days
    info['from_station'] = from_station
    info['to_station'] = to_station
    info['from_date'] = d
    return info


# 菜单
def Menu():
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    print()
    print('          ________________________欢迎使用火车票查询系统____________________________           ')
    print('                                  您可以查询15天内的车票                                       ')
    print()
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    print()


# 显示查询结果
def display(tickets):
    ptable = PrettyTable('车次 出发/到达站 出发/到达时间 历时 商务座 一等座 二等座 高级软卧 软卧 动卧 硬卧 软座 硬座 无座 其他 备注'.split(' '))
    for ticket in tickets:
        ptable.add_row(ticket)
    print(ptable)


#
def operate(arguments):
    Menu()
    color = Colored()
    today = date.today()
    lastday = today + timedelta(days=15)
    info = inputArgs(arguments['<from>'], arguments['<to>'], arguments['<date>'])
    #info = inputArgs('xian', 'ganzhou', '2018-04-17')
    from_station = info['from_station']
    to_station = info['to_station']
    from_date = info['from_date']
    mdate = date(int(from_date[:4]), int(from_date[5:7]), int(from_date[8:]))
    for i in range(int(arguments['--n'])):
        # 执行查询
        ndate = mdate + timedelta(days=i)
        if today <= ndate and ndate <= lastday:
            print('--------------------------------------------------------------' + color.yellow(
                ndate.strftime('%Y-%m-%d')) + ' ------------------------------------------------------------------')
            print('请稍等...')
            tickets = resolveData(from_station, to_station, ndate)
            tickets = filter(tickets, arguments)
            display(tickets)
        else:
            print('--------------------------------------------------------------' + color.red(
                ndate.strftime('%Y-%m-%d') + '后不可查询') + ' ------------------------------------------------------')
            break

# def operate(counts):
#     Menu()
#     color = Colored()
#     today = date.today()
#     lastday = today + timedelta(days=15)
#     info = inputArgs()
#     from_station = info['from_station']
#     to_station = info['to_station']
#     from_date = info['from_date']
#     mdate = date(int(from_date[:4]), int(from_date[5:7]), int(from_date[8:]))
#     for i in range(counts):
#         # 执行查询
#         ndate = mdate + timedelta(days=i)
#         if today <= ndate and ndate <= lastday:
#             print('--------------------------------------------------------------' + color.yellow(
#                 ndate.strftime('%Y-%m-%d')) + ' ------------------------------------------------------------------')
#             print('请稍等...')
#             tickets = resolveData(from_station, to_station, ndate)
#             # tickets = filter(tickets, arguments)
#             display(tickets)
#         else:
#             print('--------------------------------------------------------------' + color.red(
#                 ndate.strftime('%Y-%m-%d') + '后不可查询') + ' ------------------------------------------------------')
#             break
