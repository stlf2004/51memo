#!/usr/bin/env python
# coding: utf-8
# 51memo.py
# 51备忘录
# author: lufei

import os
import sys

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, basedir)

from core.user import MemoUser
from core.memo import MemoAdmin
from core.common import Color


def main(*args):
    """主函数"""
    # print(args)
    if not args:
        print(Color.red('51备忘录'.center(30, '#')))
        try:
            MemoUser.run()
        except Exception as e:
            print('报错：', e)
    else:
        if args[0] in {'-h', '--help', 'help'}:
            print('Usage: \n-h or --help or help 查看帮助\nquery -u [用户名] -y [年] -m [月] 查询备忘录信息\nmail -u [用户名] -y [年] -m [月] 发送备忘录信息到用户的邮箱中')
        if args[0] == 'query':
            if args[1] == '-u' and args[3] == '-y' and args[5] == '-m':
                print(MemoAdmin.query(args[2], args[4], args[6]))
        if args[0] == 'mail':
            if args[1] == '-u' and args[3] == '-y' and args[5] == '-m':
                print(MemoAdmin.mail(args[2], args[4], args[6]))

if __name__ == '__main__':
    main(*sys.argv[1:])
