#!/usr/bin/env python
# encoding: utf-8
# Author: Johnny Loo
# Email: johnnyloo1985@gmail.com

import os
import configparser
import pickle


class MemoConfig:
    """备忘录程序的配置管理"""
    # 1. 初始化配置：
    # 1.1 如果是首次打开该程序，则创建主配置文件，配置文件路径为cfg/memo.conf
    # 默认section ： DEFAULT 选项：
    # dbdir 存放所有用户备忘录数据的目录名，只是目录的basename, 放到程序root路径下 默认命名为db
    # authdir 存放用户验证数据的目录，放在cfg目录下，默认命名为auth
    # 1.2 如果使用过该程序，则主配置文件默认信息必然存在，读取配置
    # 1.3 不管是新创建的配置还是读取的配置，都传给self.cfg属性，这是一个configparser对象
    # 2. 一个用户是一个section，以username命名
    # authfile 配置文件名称，默认是 username.auth
    # dbfile 数据文件名称，默认是 username.db

    """
    增加日志功能：
    - 初始化相关配置
        - 日志开关
        - 日志存放目录，日志文件名
        - 日志级别
        - 日志滚动单位、滚动周期、保留日志文件数量
    """

    def __init__(self):
        """加载配置"""
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dbdir = 'db'
        logdir = 'log'  # 新增
        logfile = '51memo.log'  # 新增
        cfgdir = 'cfg'
        authdir = 'auth'
        cfgfile = 'memo.conf'
        cfg_path = os.path.join(root_path, cfgdir, cfgfile)
        auth_dir_path = os.path.join(root_path, cfgdir, authdir)
        smtpSvr = 'smtp.qq.com'
        sender = '398372655@qq.com'
        senderPass = 'ixirtgicbgkpbjjd'
        senderAuth = 'sender.auth'
        senderAuthPath = os.path.join(root_path, cfgdir, senderAuth)

        if os.path.isfile(cfg_path):
            # 配置文件存在，则从文件提取配置
            self.load(cfg_path)
        else:  # 如没有配置文件，则表示是首次打开程序，应创建配置相关目录文件
            os.makedirs(auth_dir_path)
            self.cfg = configparser.ConfigParser()
            self.cfg.setdefault(self.cfg.default_section)
            self.cfg[self.cfg.default_section] = {
                'dbdir': dbdir,
                'cfgdir': cfgdir,
                'authdir': authdir,
                'logswitch': 'on',
                'logdir': logdir,
                'logfile': logfile,
                'loglevel': 'info',
                'logrotateby': 'd',
                'logretain': '7',
                'smtpserver': smtpSvr,
                'sender': sender,
                'senderAuth': senderAuth
            }
            self.save()
            self.makeSenderAuth(senderPass, senderAuthPath)  # 将发件人邮件密码写入sender.auth文件中


    def makeSenderAuth(self, senderPass, senderAuthPath):
        """将发件人邮件密码写入sender.auth文件中"""
        with open(senderAuthPath, 'wb') as f:
            pickle.dump(senderPass, f)

    def getMailcfg(self, username):
        """获取邮件相关配置"""
        smtpSvr = self.cfg.get(self.cfg.default_section, 'smtpserver')
        sender = self.cfg.get(self.cfg.default_section, 'sender')
        senderAuth = self.cfg.get(self.cfg.default_section, 'senderAuth')
        recevicer = self.cfg.get(username, 'email')

        mailCfg = {
            'smtpSvr': smtpSvr,
            'sender': sender,
            'senderAuth': senderAuth,
            'recevicer': recevicer
        }
        return mailCfg


    def get_logconf(self):
        """获取日志配置"""
        logdir = self.cfg.get(self.cfg.default_section, 'logdir')
        logfile = self.cfg.get(self.cfg.default_section, 'logfile')
        logswitch = self.cfg.get(self.cfg.default_section, 'logswitch')
        loglevel = self.cfg.get(self.cfg.default_section, 'loglevel')
        logrotateby = self.cfg.get(self.cfg.default_section, 'logrotateby')
        logretain = self.cfg.getint(self.cfg.default_section, 'logretain')

        logcfg = {
            'logdir': logdir,
            'logfile': logfile,
            'logswitch': logswitch,
            'loglevel': loglevel,
            'logrotateby': logrotateby,
            'logretain': logretain
        }
        return logcfg

    def load(self, cfg_path):
        """加载配置"""
        self.cfg = configparser.ConfigParser()
        with open(cfg_path, 'r', encoding='utf-8') as f:
            self.cfg.read_file(f)

    def get_memopath(self, username):
        """获取备忘录数据文件路径"""
        dbdir = self.cfg.get(username, 'dbdir')
        dbfile = self.cfg.get(username, 'dbfile')
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(root_path, dbdir, dbfile)

    def add_user(self, username, password, email):
        """增加一个用户的配置，用于注册"""
        self.cfg.add_section(username)
        self.cfg[username] = {
            'authfile': username + '.auth',
            'dbfile': username + '.db',
            'email': email
        }
        self.save()
        auth_db = {
            'username': username,
            'password': password
        }
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        auth_path = os.path.join(root_path, 'cfg', 'auth', username + '.auth')
        with open(auth_path, 'wb') as f:
            pickle.dump(auth_db, f)

    def save(self):
        """保存配置"""
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cfgdir = 'cfg'
        cfgfile = 'memo.conf'
        cfg_path = os.path.join(root_path, cfgdir, cfgfile)
        with open(cfg_path, 'w', encoding='utf-8') as f:
            self.cfg.write(f)
