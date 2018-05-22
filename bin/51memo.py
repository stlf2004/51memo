#!/usr/bin/env python
# coding: utf-8
# 51memo.py
# 51备忘录
# author: lufei

import os
import sys
import re

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, basedir)

from core.user import MemoUser
from core.memo import MemoAdmin
from core.common import Color,cmdParser


def main(cmd):
    """主函数"""

    argsMap = {
        '-h': {'comment': '帮助', 'pattern': re.compile(r'-h\s*$')},
        '-u': {'comment': '用户名', 'pattern': re.compile(r'-u\s+(\S+)\s?')},
        '-y': {'comment': '年', 'pattern': re.compile(r'-y\s+(\d{4})\s?')},
        '-m': {'comment': '月', 'pattern': re.compile(r'-m\s+(\d{1,2})\s?')},
        'query': {'comment': '查询', 'pattern': re.compile(r'query\s+')},
        'mail': {'comment': '发送邮件', 'pattern': re.compile(r'mail\s+')},
    }

    if not cmd:
        print(Color.red('51备忘录'.center(30, '#')))
        try:
            MemoUser.run()
        except Exception as e:
            print('报错：', e)
    else:
        args = cmdParser(cmd, argsMap)
        for h in ('-h', '--help', 'help'):
            if h in args:
                print(args[h])
                return
        if 'query' in args:
            print(args)
            if '-u' in args and '-y' in args and '-m' in args:
                print(MemoAdmin.query(args['-u'], args['-y'], args['-m']))
                return
            else:
                print('Usage: query -u [用户名] -y [年份] -m [月份]')
                return
        if 'mail' in args:
            if '-u' in args and '-y' in args and '-m' in args:
                print(MemoAdmin.mail(args['-u'], args['-y'], args['-m']))
                return
            else:
                print('Usage: mail -u [用户名] -y [年份] -m [月份]')
                return
        else:
            print(args['-h'])
            return

if __name__ == '__main__':
    main(' '.join(sys.argv[1:]))
