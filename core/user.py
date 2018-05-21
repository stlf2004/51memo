#!/usr/bin/env python
# encoding: utf-8
# Author: Johnny Loo
# Email: johnnyloo1985@gmail.com

import os
import pickle
from .config import MemoConfig
from .log import MemoLog
from .memo import MemoAdmin
from .mail import Mail, MailSender
from .common import *


# 将用户管理功能所有函数整合为一个类 MemoUser
# 初始化当前登录用户变量为None,其他方法可修改该变量
# 备忘录主程序管理模块创建MemoUser对象，执行run方法，run方法是MemoUser的主程序


class MemoUser:
    """用户管理模块"""

    def __init__(self):
        """初始化当前登录用户"""
        self.current_user = None  # 初始化当前登录用户为None
        # 初始化日志logger
        self.ml = MemoLog('UserModule')

    def chk_empty(self):
        """检查当前配置文件中是否没有任何用户的信息"""
        mc = MemoConfig()
        return bool(mc.cfg.sections())

    def setup(self):
        """设置"""
        while True:
            setup_menu = {
                "L": "日志",
                "M": "邮件",
                "U": "返回上一级菜单"
            }
            print('-' * 30)
            for key, text in setup_menu.items():
                print(Color.green(f'     按"{key}"键：{text}'.ljust(30)))
            print('-' * 30)
            choose = checkInput('请选择：', 'l', 'm', 'u')
            if choose == 'l':
                self.setup_log()  # 日志配置
                continue
            elif choose == 'm':
                self.setupMail()  # 设置邮件相关配置
                continue
            else:
                break

    def setupMail(self):
        """设置邮件相关配置"""
        print('当前配置：')
        mailCfg = self.loadMailCfg()  # 加载邮件相关配置信息
        print('-' * 30)
        for opt, val in mailCfg.items():
            print(Color.green(f'{opt}: {val}'))
        print('-' * 30)
        choose = checkInput('是否保持当前配置？', 'y', 'n')
        if choose == 'n':
            mailCfg['SMTP服务器'] = input('SMTP服务器：')
            mailCfg['发件人'] = checkMail('发件人：')  # 检查邮件地址合法性
            self.saveMailAuth(mailCfg['发件人授权文件'])  # 保存密码为验证文件
            self.saveMailCfg(mailCfg)  # 保存邮件配置
            print(Color.green('邮件配置完成'))
        else:
            return

    def saveMailAuth(self, senderAuth):
        """保存密码为验证文件"""
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        senderAuthPath = os.path.join(basedir, 'cfg', senderAuth)
        password = checkPassword('密码：')
        with open(senderAuthPath, 'wb') as f:
            pickle.dump(password, f)


    def saveMailCfg(self, mailCfg):
        """保存邮件配置"""
        mc = MemoConfig()
        mc.cfg.set(mc.cfg.default_section, 'smtpserver', mailCfg.get('SMTP服务器')),
        mc.cfg.set(mc.cfg.default_section, 'sender', mailCfg.get('发件人')),
        mc.cfg.set(mc.cfg.default_section, 'senderAuth', mailCfg.get('发件人授权文件')),
        mc.save()


    def loadMailCfg(self):
        """加载邮件相关配置信息"""
        mc = MemoConfig()
        mailCfg = {
            'SMTP服务器': mc.cfg.get(mc.cfg.default_section, 'smtpserver'),
            '发件人': mc.cfg.get(mc.cfg.default_section, 'sender'),
            '发件人授权文件': mc.cfg.get(mc.cfg.default_section, 'senderAuth')
        }
        return mailCfg


    def setup_log(self):
        """配置日志相关选项"""
        print('当前配置：')
        logcfg = self.load_logcfg()  # 加载日志配置信息
        print('-' * 30)
        for opt, val in logcfg.items():
            print(Color.green(f'{opt}: {val}'))
        print('-' * 30)
        choose = checkInput('是否保持当前配置？', 'y', 'n')
        if choose == 'n':
            log_on = checkInput('是否打开日志功能？', 'y', 'n')
            if log_on == 'y':
                logcfg['日志开关'] = 'on'
                logcfg['日志等级'] = checkInput('日志等级：', 'debug', 'info', 'warning', 'error', 'critical')
                logcfg['日志滚动粒度'] = checkInput('日志滚动粒度(d:天,h:小时,m:分钟,s:秒)：', 'd', 'h', 'm', 's')
                logcfg['日志保留时长'] = self.chk_num('日志保留时长（输入数字）：')
            if log_on == 'n':
                logcfg['日志开关'] = 'off'
            self.save_logcfg(logcfg)  # 保存日志配置
            print(Color.green('日志配置完成'))
        else:
            return

    def chk_num(self, text):
        """处理数字输入"""
        while True:
            num = input(text).strip()
            if num.isdecimal():
                return num
            else:
                print('非法输入，请重新输入。')

    def load_logcfg(self):
        """从主配置文件中加载日志配置"""
        mc = MemoConfig()
        logcfg = {
            '日志开关': mc.cfg.get(mc.cfg.default_section, 'logswitch'),
            '日志等级': mc.cfg.get(mc.cfg.default_section, 'loglevel'),
            '日志滚动粒度': mc.cfg.get(mc.cfg.default_section, 'logrotateby'),
            '日志保留时长': mc.cfg.getint(mc.cfg.default_section, 'logretain')
        }
        return logcfg

    def save_logcfg(self, logcfg):
        """保存日志配置"""
        mc = MemoConfig()
        mc.cfg.set(mc.cfg.default_section, 'logswitch', logcfg.get('日志开关')),
        mc.cfg.set(mc.cfg.default_section, 'loglevel', logcfg.get('日志等级')),
        mc.cfg.set(mc.cfg.default_section, 'logrotateby', logcfg.get('日志滚动粒度')),
        mc.cfg.set(mc.cfg.default_section, 'logretain', str(logcfg.get('日志保留时长')))
        mc.save()

    def login(self):
        """用户登录"""
        while True:
            username = input('用户名：'.rjust(14)).strip().lower()
            password = input('密码：'.rjust(15))
            is_exist = self.user_exist(username)
            if is_exist:
                pass
            else:
                print('当前用户不存在，请重新输入。')
                self.ml.logger.error(f'User "{username}" login fail.')
                continue
            auth_result = self.user_auth(
                username, password)
            if auth_result:
                self.current_user = username
                self.ml.logger.info(f'User "{self.current_user}" login successful.')
                self.sendMail('login', username)
                print(Color.green('登录成功邮件已发送到您的邮箱中，请查收。'))
                return apiReturn()
            else:
                print(apiReturn(1,f'User "{username}" login fail.'))
                print('验证失败，请重新输入。')
                self.ml.logger.error(f'User "{username}" login fail.')

    def register(self):
        """用户注册"""
        while True:
            username = input('用户名：'.rjust(14)).strip().lower()
            password = input('密码：'.rjust(15))
            password_again = input('再次输入密码：'.rjust(11))
            if username and password and password == password_again:
                # 检查用户名是否已存在的结果，True or False
                is_exist = self.user_exist(username)
                if not is_exist:
                    break
                else:
                    print(f'{username}已被使用，请换个用户名试试。')
                    continue
            else:
                print('存在空输入，或两次输入的密码不一致，请重新输入。')

        # 输入邮件地址，用来给用户发送邮件
        email = checkMail('Email：'.rjust(15))


        # 将用户名密码写入配置
        try:
            mc = MemoConfig()
            mc.add_user(username, password, email)  # 添加用户
            print(f'{username} 注册成功！')
            self.ml.logger.info(f'User "{username}" register successful.')
            self.sendMail('register', username)  # 发送注册成功邮件
            print(Color.green('注册成功邮件已发送到您的邮箱中，请查收。'))
            self.current_user = username
            self.ml.logger.info(f'User "{self.current_user}" login successful.')
            return apiReturn()
        except Exception as e:
            self.ml.logger.error(f'User "{username}" register fail, ', e)
            return apiReturn(1, f'User "{username}" register fail')

    def sendMail(self, type, username):
        """根据用途发送邮件"""
        mailCfg = MemoConfig().getMailcfg(username)  # 获取邮件配置信息
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        senderAuthPath = os.path.join(basedir, 'cfg', mailCfg['senderAuth'])
        with open(senderAuthPath, 'rb') as f:
            password = pickle.load(f)
        ms = MailSender(mailCfg['smtpSvr'], mailCfg['sender'], password)
        ms.addRecevicer(mailCfg['recevicer'])
        m = Mail(type, username)
        ms.write(m.mailType, subject=m.subject, body=m.body)
        ms.send()



    def quit(self):
        """用户未登录状态时的退出"""
        self.ml.logger.info('quit')
        self.current_user = None
        self.end = True

    def user_auth(self, username, password):
        """验证用户名密码"""
        # 1. 从备忘录主配置文件中读取用户配置信息，获得存放用户名密码的数据文件的路径
        # 2. 加载用户名密码文件数据，获得用户名密码
        # 3. 检查输入的用户名密码与文件读取的是否一致，一致则返回True ，否则返回False
        auth_db = self.get_authdb(username)  # 根据username查找并加载验证文件，并获得验证数据
        if username == auth_db['username'] and password == auth_db['password']:
            self.ml.logger.debug(f'User "{username}" authenticate successfully.')
            return True
        else:
            self.ml.logger.debug(f'User "{username}" authenticate fail.')
            return False

    def user_exist(self, username) -> bool:
        """验证用户是否已在配置文件中"""
        # 1. 从备忘录主配置文件中读取配置
        # 2. 检查username是否在配置对象的section中，在则返回True ，不在则返回False
        mc = MemoConfig()
        result = mc.cfg.has_section(username)
        if result:
            self.ml.logger.debug(f'User "{username}" is in the config.')
        else:
            self.ml.logger.debug(f'User "{username}" is not in the config.')
        return result

    def get_authdb(self, username) -> dict:
        """获得用户验证文件中的数据"""
        # 1. 从主配置文件中读取用户验证文件的路径
        # 2. 加载用户验证文件，读取内容，返回验证数据，验证数据: {'username': 'xxx', 'password': '111'}
        try:
            mc = MemoConfig()
            cfgdir = mc.cfg.get(username, 'cfgdir')
            authdir = mc.cfg.get(username, 'authdir')
            authfile = mc.cfg.get(username, 'authfile')
            root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            auth_path = os.path.join(root_path, cfgdir, authdir, authfile)
            with open(auth_path, 'rb') as f:
                authdb = pickle.load(f)
            self.ml.logger.debug(f'Acquiring user "{username}"\'s authinfo successfully.')
            return authdb
        except Exception as e:
            self.ml.logger.debug(f'Acquiring user "{username}"\'s authinfo failed, ', e)

    @classmethod
    def run(cls):
        """主程序"""
        mu = cls()
        while True:
            if mu.current_user is None:
                is_empty = not mu.chk_empty()  # 检查是否第一次使用，没有任何已注册的用户
                if is_empty:
                    mu.ml.logger.debug('New user checking is true.')
                    while True:
                        sure = checkInput('您是第一位用户，是否注册？', 'y', 'n')
                        if sure == 'y':
                            mu.register()
                            break
                        else:
                            mu.quit()
                            break
                else:
                    mu.ml.logger.debug('New user checking is false.')
                    u_menu = {
                        "L": "登录",
                        "R": "注册",
                        "S": "设置",
                        "Q": "退出"
                    }
                    print('-' * 30)
                    for key, text in u_menu.items():
                        print(Color.green(f'按"{key}"键： {text}'.center(30)))
                    print('-' * 30)
                    choose = checkInput('请选择：', 'l', 'r', 's', 'q')
                    if choose == 'l':
                        mu.login()
                    elif choose == 'r':
                        mu.register()
                    elif choose == 's':
                        mu.setup()
                        mu.end = False
                    else:
                        mu.quit()
                if mu.current_user is None and mu.end:
                    print('Bye!')
                    break
            if mu.current_user is not None:  # 注册用户后直接让用户登录，标记当前用户非None
                ma = MemoAdmin(mu.current_user)
                ma.run()
                if ma.is_logout:
                    mu.current_user = None
