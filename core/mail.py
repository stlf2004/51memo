#!/usr/bin/env python
# encoding: utf-8
# Author: Johnny Loo
# Email: johnnyloo1985@gmail.com

from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import re
import os


class Mail:
    """邮件类型"""
    def __init__(self, type, username):
        if type == 'register':
            self.mailType = 'html'
            self.subject = f'恭喜{username}注册成功'
            self.body = f"""
            <h3>
            尊敬的{username}:
            <h3>
            <p>
                欢迎您使用51备忘录！
            </p>
            """
        if type == 'login':
            self.mailType = 'html'
            self.subject = f'{username}登录成功'
            self.body = f"""
            <h3>
            尊敬的{username}:
            </h3>
            <p>
                您已成功登录51备忘录！
            </p>
            """





class MailError(Exception):
    """邮件异常报错"""
    pass


class MailSender:
    """书写并发送邮件"""
    PATTERN_EMAIL = re.compile(
        r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?")

    def __init__(self, smtpSvr, sender, password):
        """
        初始化
            - smtp服务器
            - 登录
        """
        if not MailSender.PATTERN_EMAIL.match(sender):
            raise MailError(f'{sender}不是有效的邮件地址。')
        self.smtp = SMTP_SSL(smtpSvr)
        # self.smtp.set_debuglevel(1)
        self.smtp.ehlo(smtpSvr)
        self.smtp.login(sender, password)
        self.sender = sender
        self.receivers = []
        self.msg = MIMEMultipart()
        self.msg['from'] = sender

    def addRecevicer(self, *receivers):
        """添加收件人"""
        for i in receivers:
            if not MailSender.PATTERN_EMAIL.match(i):
                raise MailError(f'{i}不是有效的邮件地址。')
            self.receivers.append(i)

    def write(self, mailType="plain", *, subject, body):
        """书写正文"""
        self.msg['subject'] = Header(subject, 'utf-8')
        if not self.receivers:
            self.addRecevicer()
        self.msg['to'] = ','.join(self.receivers)
        text = MIMEText(body, mailType, 'utf-8')
        self.msg.attach(text)

    def attach(self, attachment):
        """附加附件"""
        if not os.path.isfile(attachment):
            raise MailError(f'{attachment}文件不存在。')
        with open(attachment, 'rb') as f:
            mime = MIMEBase('text', 'plain', filename=attachment)
            mime.add_header('Content-Disposition', 'attachment', filename=attachment)
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            self.msg.attach(mime)

    def send(self):
        """发送邮件"""
        if not self.receivers:
            self.addRecevicer()
        try:
            self.smtp.sendmail(self.sender, self.receivers, self.msg.as_string())
        except Exception as e:
            print('报错：', e)
        finally:
            self.smtp.quit()


def main():
    body = """
        <h1>第8哥的邮件啊</h1>
        <h2>须有html格式, 比如写个表格</h2>
        <table border="1">
            <tr>
                <th>姓名</th>
                <th>城市</th>
            </tr>
            <tr>
                <td>第8哥</td>
                <td>北京</td>
            </tr>
        </table>
    """

    ms = MailSender()
    ms.addRecevicer('stlf_2003@163.com', '398372655@qq.com')
    ms.write('html', subject='这是标题', body=body)
    ms.attach('test.json')
    ms.send()


if __name__ == '__main__':
    main()
