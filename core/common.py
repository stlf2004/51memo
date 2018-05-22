#!/usr/bin/env python
# encoding: utf-8
# Author: Johnny Loo
# Email: johnnyloo1985@gmail.com

# import functools
import re


# API返回成功、失败
SUCCESS = 'success'
FAILURE = 'failure'

def apiReturn(status=0, message=SUCCESS, data={}):
    return {
        'status': status,
        'message': message,
        'data': data
    }




# 打印颜色

class Color:
    RED = '\33[31m'
    GREEN = '\33[32m'
    YELLOW = '\33[33m'
    BLUE = '\33[34m'
    PURPLE = '\33[35m'
    DARKGREEN = '\33[36m'
    BLINK = '\33[5m'
    CLOSE = '\33[0m'

    @staticmethod
    def red(s):
        return Color.RED + s + Color.CLOSE

    @staticmethod
    def green(s):
        return Color.GREEN + s + Color.CLOSE

    @staticmethod
    def yellow(s):
        return Color.YELLOW + s + Color.CLOSE

    @staticmethod
    def blue(s):
        return Color.BLUE + s + Color.CLOSE

    @staticmethod
    def purple(s):
        return Color.PURPLE + s + Color.CLOSE

    @staticmethod
    def darkGreen(s):
        return Color.DARKGREEN + s + Color.CLOSE

    @staticmethod
    def blink(s):
        return Color.BLINK + s + Color.CLOSE



# 检查输入合法性
def checkInput(text, *options):
    """检查输入合法性"""
    optText = '(' + '/'.join(options) + ')'
    while True:
        choose = input(text + optText).strip().lower()
        if choose in options:
            return choose
        else:
            print(Color.red('非法输入，请重新输入。'))
            continue



# 检查输入数字是否在指定的范围内
def checkNumRange(text, *ran):
    while True:
        n = checkNum(text)
        if n in ran:
            return n
        else:
            print(Color.red('输入超出范围，请重新输入。'))
            continue



# 检查输入是否为数字
def checkNum(text):
    """处理数字输入"""
    while True:
        num = input(text).strip()
        if num.isdecimal():
            return int(num)
        else:
            print(Color.red('非法输入，请重新输入。'))


def checkMail(text):
    """处理邮件地址的输入"""
    while True:
        mail = input(text).strip()
        patternMail = re.compile(
            r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?")
        if patternMail.match(mail):
            return mail
        else:
            print(Color.red('email地址不合法，请重新输入。'))

def checkPassword(text):
    """检查密码输入是否为空"""
    while True:
        password = input(text)
        if password:
            return password
        else:
            print(Color.red('密码不能为空，请重新输入。'))



def cmdParser(cmd, argsMap):
    """命令行传参分析程序"""
    data = {}
    for k,v in argsMap.items():
        result = v['pattern'].search(cmd)
        if result:
            try:
                value = result.group(1)
                # print(value)
                data.update({k: value})
            except IndexError:
                if k in {'-h','--help','help','?'}:
                    value = 'Usage:\n'
                    for opt,val in argsMap.items():
                        value += opt+'\t'+val['comment']+'\n'
                    data.update({k: value})
                    return data
                else:
                    value = None
                    data.update({k: value})
    return data


def main():
    argsMap = {
        '-h': {'comment': '帮助', 'pattern': re.compile(r'-h\s*$')},
        '-u': {'comment': '用户名', 'pattern': re.compile(r'-u\s+(\S+)\s?')},
        '-p': {'comment': '密码', 'pattern': re.compile(r'-p\s+(\S+)\s?')}
    }
    print(cmdParser('command -u lufei -p 123', argsMap))
    # print(cmdParser('command -u lufei -p 123 ', argsMap))
    # cmdParser('command -u lufei -p 123 -a', argsMap)
    # print(cmdParser('command -h', argsMap))
    # cmdParser('command -h ', argsMap)


    # api = apiReturn()
    # api['data'].update({'user': 'lufei'})
    # print(api)

    # choose = checkInput('请选择：', 'y', 'n')
    # print(choose)

    # n = checkNum('请输入：')
    # print(n)

    # m = checkNumRange('请输入：', *range(10))
    # print(m)



    # print(Color.red('hello'))
    # print(Color.green('hello'))
    # print(Color.yellow('hello'))
    # print(Color.blue('hello'))
    # print(Color.purple('hello'))
    # print(Color.darkGreen('hello'))
    # print(Color.blink('hello'))

if __name__ == '__main__':
    main()