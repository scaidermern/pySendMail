#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import mimetypes
import os
import smtplib
import sys
import time
from email.message import EmailMessage

class pySendMail:
    def __init__(self):
        self.subject = 'pySendMail'
        self.content = 'Hello from pySendMail'
        self.file = None
        self.attach = None
        self.retry = False

        try:
            path = os.path.abspath(os.path.dirname(__file__))
            self.config = json.load(open(path + '/sendMailConfig.json', 'r'))
        except Exception as e:
            print('Could not parse config file: %s' % e)
            sys.exit(1)

    def send(self):
        while True:
            try:
                self.sendInternal()
                break
            except smtplib.SMTPAuthenticationError as e:
                print(e)
                # no retry in case of wrong credentials
                return
            except Exception as e:
                print(e)
                if not self.retry:
                    return
                time.sleep(1)

    def sendInternal(self):
        msg = EmailMessage()
        msg['From'] = self.config['mail']['from']
        msg['To'] = self.config['mail']['to']
        msg['Subject'] = self.subject

        if self.content:
            msg.set_content(self.content)
        elif self.file:
            if self.file == '-':
                # read from stdin
                msg.set_content(sys.stdin.read())
            else:
                # read from file
                with open(self.file) as f:
                    msg.set_content(f.read())

        if self.attach:
            for path in self.attach:
                ctype, encoding = mimetypes.guess_type(path)
                if ctype is None or encoding is not None:
                    # unknown type or compressed file
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)
                with open(path, 'rb') as fp:
                    msg.add_attachment(fp.read(),
                                       maintype=maintype,
                                       subtype=subtype,
                                       filename=os.path.basename(path))

        host = self.config['mail']['smtp']['server']
        port = self.config['mail']['smtp']['port']
        timeout = self.config['mail']['smtp']['timeout']
        if timeout == 0:
            timeout = None
        if self.config['mail']['smtp']['tls']:
            # use SSL/TLS
            server = smtplib.SMTP_SSL(host=host, port=port, timeout=timeout)
        else:
            # use STARTTLS
            server = smtplib.SMTP(host=host, port=port, timeout=timeout)
            server.starttls()
        server.login(self.config['mail']['smtp']['user'], self.config['mail']['smtp']['password'])
        server.send_message(msg)
        server.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send message via mail.')
    parser.add_argument('-s', '--subject', help='mail subject')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--content', help='mail content from string')
    group.add_argument('-f', '--file', help='mail content from file, specify - to read from stdin')
    parser.add_argument('-a', '--attach', action='append', help='attachment(s), can be specified multiple times')
    parser.add_argument('-r', '--retry', action='store_true', help='keep retrying until sending succeeds (except for failed logins)')
    args = parser.parse_args()

    mail = pySendMail()
    if args.subject:
        mail.subject = args.subject
    if args.content:
        mail.content = args.content
    if args.file:
        mail.file = args.file
    if args.attach:
        mail.attach = args.attach
    mail.retry = args.retry
    mail.send()
