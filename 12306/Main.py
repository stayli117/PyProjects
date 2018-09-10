# coding: utf-8
# -*- coding: UTF-8 -*
"""Train tickets query via command-line.
Usage:
    tickets [-gdtkz] <from> <to> <date> [--n=1]

Options:
    -h,--help        显示帮助菜单
    -g               高铁
    -d               动车
    -t               特快
    -k               快速
    -z               直达
    --n=<kn>         连续查询天数[default:1]

Example:
    tickets 南京 北京 2016-07-01
    tickets -dg 南京 北京 2016-07-01 -n=2
"""
from docopt import docopt
from ProApi import *
from Resources import info

def cli():
    """command-line interface"""
    arguments = {'<from>':'xian','<to>':'ganzhou', '<date>':'2018-04-17', '--n':5}
    # print(arguments)
    operate(arguments)



if __name__ == "__main__":#main方法
    # Menu()
    # isContionue = 'Y'
    # while isContionue == 'Y' or isContionue == 'y':
    #     counts = input('输入查询天数：\n')
    #     operate(int(counts))
    #     isContionue = input('是否继续查询？Y/N\n')
    # input('按任意键退出...')
    cli()