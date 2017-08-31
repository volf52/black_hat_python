#!/usr/bin/python
'''
 @author : "Muhammad Arslan<rslnrkmt2552@gmail.com>"
'''

import sys
import socket
import getopt
import threading
import subprocess

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def usage():
    print "NetVolf Tool\n"
    print "Usage: netvolf.py -t target_host -p port"
    print "-l --listen                  = listen on [host] for incoming connections"
    print "-e --execute=file_to_run     = execute the given file upon recieving conn"
    print "-c --commandshell            =initialize a command shell"
    print "-u --upload=destination      = upon recieving a conn, upload to [destination]\n\n"

    print "Examples:"
    print "netvolf.py -t 192.168.0.1 -p 5555 -l -c"
    print "netvolf.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "netvolf.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./netvolf.py -t 192.168.11.12 -p 135"
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read() # send CTRL + D if not sending input to stdin, as it will block otherwise

        client_sender(buffer)

    if listen:
        server_loop()


main()