#!/usr/bin/python

from time import sleep
import socket
import select
import threading


class Server(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.daemon = True
        self.port = port
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srvsock.bind(("", port))
        self.srvsock.listen(5)

        self.descriptors = [self.srvsock]
        print ('Server started on port %s' % port)

    def run(self):
        while 1:

            # Await an event on a readable socket descriptor
            (sread, swrite, sexc) = select.select(self.descriptors, [], [])

            # Iterate through the tagged read descriptors
            for sock in sread:

                # Received a connect to the server (listening) socket
                if sock == self.srvsock:
                    self.accept_new_connection()
                else:
                    try:
                        # Received something on a client socket
                        str = sock.recv(2000)
                        host, port = sock.getpeername()
                        # Check to see if the peer socket closed
                        if str == '' or str == 'q':
                            print('Client left {0}:{1}'.format(host, port))
                            sock.close()
                            self.descriptors.remove(sock)
                        else:
                            print('{0}:{1} says: "{2}"'.format(host, port, str))
                            sock.send("Hello from your test server!")

                    except socket.error:
                        host, port = sock.getpeername()
                        print('Socket Error - Client left {0}:{1}'.format(host, port))
                        sock.close()
                        self.descriptors.remove(sock)

    def accept_new_connection(self):
        newsock, (remhost, remport) = self.srvsock.accept()
        self.descriptors.append(newsock)
        print('Client joined {0}:{1}'.format(remhost, remport))


def main():
    myServer = Server(10000)
    myServer.start()
    try:
        while 1:
            # Do nothing...
            sleep(1.0)

    except KeyboardInterrupt:
        print ('Exiting...')


if __name__ == '__main__':
    main()
