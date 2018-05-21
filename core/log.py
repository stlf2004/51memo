#!/usr/bin/env python
# encoding: utf-8
# Author: Johnny Loo
# Email: johnnyloo1985@gmail.com

import os
import logging
from logging.handlers import TimedRotatingFileHandler
from .config import MemoConfig


class MemoLog:
    """日志功能"""

    def __init__(self, logger_name):
        """初始化logger"""
        """
        - 读配置：用户名、日志级别、日志滚动方式
        - 初始化logger
        """
        mc = MemoConfig()
        logcfg = mc.get_logconf()  # 获取日志相关配置
        self.logger = logging.getLogger(logger_name)
        logswitch = logcfg.get('logswitch')
        if logswitch == 'off':
            logging.disable(logging.CRITICAL)
        else:
            level_dict = {
                'debug': logging.DEBUG,
                'info': logging.INFO,
                'warning': logging.WARNING,
                'error': logging.ERROR,
                'critical': logging.CRITICAL
            }
            self.logger.setLevel(level_dict.get(logcfg.get('loglevel')))
            basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            log_path = os.path.join(basedir, logcfg.get('logdir'), logcfg.get('logfile'))
            fh = TimedRotatingFileHandler(filename=log_path,
                                          when=logcfg.get('logrotateby'),
                                          interval=1,
                                          backupCount=logcfg.get('logretain'),
                                          encoding='utf-8')
            fh.suffix = '%Y%m%d_%H%M%S'
            formatter = logging.Formatter(
                '[T]%(asctime)s [N]%(name)s [M]%(module)s [F]%(funcName)s [L]%(levelname)s [MSG]%(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
