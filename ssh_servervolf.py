#!/usr/bin/env python
"""

@author : 'Muhammad Arslan <rslnrkmt2552@gmail.com>'

"""
#TODO add a graceful exit

import socket
import paramiko
import threading
import sys

host_key = paramiko.RSAKey(filename='test_rsa.key')

class Server(paramiko.ServerInterface):
    '''
    Custom SSH Server - volf
    '''
    def __init__(self):
        self.event = threading.Event()


    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


    def check_auth_password(self, username, password):
        if (username == "volf") and (password == "volf"):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED


server = sys.argv[1]
ssh_port = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print "[*] Listening for connections ..."
    client, addr = sock.accept()
except Exception, e:
    print "[-] Listen failed: %s" + str(e)
    sys.exit(0)

print "[+] Got a connection!"

try:
    vsession = paramiko.Transport(client)
    vsession.add_server_key(host_key)
    server = Server()
    try:
        vsession.start_server(server=server)
    except paramiko.SSHException, x:
        print "[-] SSH negotiation failed."

    chan = vsession.accept(20)
    print "[+] Authenticated!"
    print chan.recv(1024)
    chan.send("Welcome to ssh_volf !!!")
    while True:
        try:
            command = raw_input("Enter command #> ")
            if command != 'exit':
                chan.send(command)
                print chan.recv(1024) + '\n'
            else:
                chan.send('exit')
                print "Exiting..."
                vsession.close()
                raise Exception('exit')
        except KeyboardInterrupt:
            vsession.close()

except Exception, e:
    print "[-] Caught exception: %s" % str(e)
    try:
        vsession.close()
    except:
        pass

    sys.exit(1)

