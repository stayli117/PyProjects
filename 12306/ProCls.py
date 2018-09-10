# -*- coding: UTF-8 -*
import threading
from ProApi import *
from colorama import init, Fore, Back, Style

threadLock = threading.Lock()
init(autoreset=False)
class Colored(object):
    #  前景色:红色  背景色:默认
    def red(self, s):
        return Fore.LIGHTRED_EX + s + Fore.RESET
    #  前景色:绿色  背景色:默认
    def green(self, s):
        return Fore.LIGHTGREEN_EX + s + Fore.RESET
    def yellow(self, s):
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET
    def white(self,s):
        return Fore.LIGHTWHITE_EX + s + Fore.RESET
    def blue(self,s):
        return Fore.LIGHTBLUE_EX + s + Fore.RESET

class myThread (threading.Thread):
    def __init__(self, threadID, threadName, train_no, from_station_no, to_station_no, seat_types, date,pricesDic):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName
        self.train_no = train_no
        self.from_station_no = from_station_no
        self.to_station_no = to_station_no
        self.seat_types = seat_types
        self.date = date
        self.pricesDic = pricesDic
    def run(self):
        #print ("开始线程：" + self.threadName)
        # 获取锁，用于线程同步
        threadLock.acquire()
        getPrice(self.threadName, self.train_no, self.from_station_no, self.to_station_no, self.seat_types, self.date, self.pricesDic)
        # 释放锁，开启下一个线程
        threadLock.release()
        #print ("退出线程：" + self.threadName)

def getPrice(threadName, train_no, from_station_no, to_station_no, seat_types, date,pricesDic):
    while 1:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            moneyUrl = "https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no={}&from_station_no={}&to_station_no={}&seat_types={}&train_date={}".format(
                train_no, from_station_no, to_station_no, seat_types, date)
            req = urllib.request.Request(url=moneyUrl, headers=headers)
            r_price = urllib.request.urlopen(req).read().decode('utf-8')
            if r_price.startswith(u'\ufeff'):
                r_price = r_price.encode('utf8')[3:].decode('utf-8')
                # print(r_price)
            r_price = json.loads(r_price)
            break
        except:
            continue
    price = r_price['data']
    price = dict(price)
    A = ('A9' in price.keys())
    if A == False:
        A = ('P' in price.keys())
        if A == False:
            A = ''
        else:
            A = price['P']
    else:
        A = price['A9']

    B = ('M' in price.keys())
    if B == False:
        B = ''
    else:
        B = price['M']
    C = ('O' in price.keys())
    if C == False:
        C = ''
    else:
        C = price['O']
    D = ('A6' in price.keys())
    if D == False:
        D = ''
    else:
        D = price['A6']
    E = ('A4' in price.keys())
    if E == False:
        E = ''
    else:
        E = price['A4']
    F = ('F' in price.keys())
    if F == False:
        F = ''
    else:
        F = price['F']
    G = ('A3' in price.keys())
    if G == False:
        G = ''
    else:
        G = price['A3']

    H = ('A2' in price.keys())
    if H == False:
        H = ''
    else:
        H = price['A2']
        # print("软座："+H)
    I = ('A1' in price.keys())
    if I == False:
        I = ''
    else:
        I = price['A1']

    J = ('WZ' in price.keys())
    if J == False:
        J = ''
    else:
        J = price['WZ']
    pricesDic['A'] = A
    pricesDic['B'] = B
    pricesDic['C'] = C
    pricesDic['D'] = D
    pricesDic['E'] = E
    pricesDic['F'] = F
    pricesDic['G'] = G
    pricesDic['H'] = H
    pricesDic['I'] = I
    pricesDic['J'] = J

