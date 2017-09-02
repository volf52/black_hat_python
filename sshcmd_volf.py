#!/usr/bin/python
"""

@author : 'Muhammad Arslan <rslnrkmt2552@gmail.com>'

"""

import threading
import paramiko
import subprocess

host = raw_input("[*] Enter IP > ").strip()
user = raw_input("[*] Enter username > ").strip()
passwd = raw_input("[*] Enter password > ").strip()
com = raw_input("[*] Enter command > ").strip()

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024)
    return

ssh_command(host, user, passwd, com)