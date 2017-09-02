#!/usr/bin/python
"""

@author : 'Muhammad Arslan <rslnrkmt2552@gmail.com>'

"""

import sys
import socket
import threading


def server_loop(lhost, lport, rhost, rport, recv_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((lhost, lport))
    except:
        print "[!!] Failed to listen on %s:%d" % (lhost, lport)
        print "[!!] Check for other listening sockets or correct permissions."
        sys.exit(0)

    print "[*]Server started\n. [*] Listening on %s:%d..." % (lhost, lport)

    server.listen(5)

    while True:

        client_sock, addr = server.accept()

        print "[==>] Recieved incoming connection from %s:%d" % (addr[0], addr[1])
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_sock, rhost, rport, recv_first))
        proxy_thread.start()


def hexdump(src, length=16):
    '''
    :param src: http://code.activestate.com/recipes/142812-hex-dumper/

    '''
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
        s = src[i:i + length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b"%04X %-*s %s" % (i, length * (digits + 1), hexa, text))
        print b'\n'.join(result)


def recieve_from(conn):
    buffer = ""
    conn.settimeout(2)

    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass

    return buffer


def request_handler(buff):
    # modify packets if you want, mortal
    return buff


def response_handler(buff):
    # same thing as request handler, but for response :D
    return buff


def proxy_handler(client_sock, rhost, rport, recv_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        remote_socket.connect((rhost, rport))
    except:
        print "[!!] Failed to connect to remote host. Exiting..."
        sys.exit(0)

    if recv_first:
        remote_buffer = recieve_from(remote_socket)
        hexdump(remote_buffer)
        remote_buffer = response_handler(remote_buffer)  #our response handler

        # send data to local client if there is some...
        if len(remote_buffer):
            print "[<==] Sending %d bytes to localhost." % len(remote_buffer)
            client_sock.send(remote_buffer)

    while True:
        local_buffer = recieve_from(client_sock)
        if len(local_buffer):
            print "[==>] Recieved %d bytes from localhost." % len(local_buffer)
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)

            remote_socket.send(local_buffer)
            print "[==>] Send to remote."

        remote_buffer = recieve_from(remote_socket)
        if len(remote_buffer):
            print "[<==] Recieved %d bytes from remote." % len(remote_buffer)
            hexdump(remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            client_sock.send(remote_buffer)
            print "[<==] Sent to localhost."

        if not len(local_buffer) and not len(remote_buffer):
            client_sock.close()
            remote_socket.close()
            print "[*] No more data. Closing connections..."
            break


def main():
    if len(sys.argv[1:]) != 5:
        print "Usage: ./proxyvolf.py [localhost] [localport] [remotehost] [remoteport] [recieve_first]"
        print "Example: ./proxyvolf.py 127.0.0.1 1313 10.12.132.1 9000 True"
        print "Example: ./proxyvolf.py 127.0.0.1 21 ftp.hq.nasa.gov 21 True"

    lhost, lport, rhost, rport, recv_first = sys.argv[1:]

    if "True" in recv_first:
        recv_first = True
    else:
        recv_first = False

    server_loop(lhost, int(lport), rhost, int(rport), recv_first)


if __name__ == "__main__":
    main()
