# TODO documentation

import socket
import threading
import binascii
import select

from fprime.gds.models.serialize import u32_type


# Constants for public use
GUI_TAG = "GUI"
FSW_TAG = "FSW"

class ThreadedTCPSocketClient(object):
    '''Threaded TCP client that connects to teh socket server which serves packets from the helecopter'''

    def __init__(self, sock=None):
        """
        Threaded client socket constructor

        Keyword Arguments:
                sock {Socket} -- A socket for the client to use. Created own if
                                 None (default: {None})
        """

        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

        # NOTE can't do this b/c EINPROGRESS: self.sock.setblocking(0)

        self.__distributors = []
        self.__select_timeout = 1
        self.__data_recv_thread = threading.Thread(target=self.recv)
        self.stop_event = threading.Event()


    def register_distributor(self, distributor):
        """Registers a fprime.gds.distributor object with this socket

        Arguments:
                fprime.gds.distributor {Distributor} -- Distributor must implement data_callback
        """

        self.__distributors.append(distributor)


    def register_to_server(self, register_as):
        '''
        Registers the caller to the server as type register_as

        This function assumes the socket connects to an fprime TCP server

        Args:
            register_as (string): How to identify this process to the TCP server
                                  Can be either "FSW" or "GUI"
        '''
        data = "Register %s\n"%register_as

        self.sock.send(data)


    def connect(self, host, port):
        """Connect to host at given port and start the threaded recv method.

        Arguments:
                host {string} -- IP of the host server
                port {int} -- Port of the host server
        """
        try:
            self.sock.connect((host, port))
            self.__data_recv_thread.start()
        except:
            print("There was a problem connecting to the TCP Server")
            exit(-1)


    def disconnect(self):
        """Disconnect the socket client from the server and stop the internal thread.
        """
        self.stop_event.set()
        self.__data_recv_thread.join()
        self.sock.close()


    def send(self, data, dest):
        """
        Send data to the server

        All necessary headers are added in this function.

        Arguments:
            data {binary} -- The data to send (What you want the destination
                             to receive)
            dest {String} -- Where to send the data to. Either "FSW" or "GUI"
        """
        self.sock.send("A5A5 %s %s"%(dest, data))


    def recv(self):
        """Method run constantly by the enclosing thread. Looks for data from the server.
            """

        while not self.stop_event.is_set():
            #print "Running fprime.gds.distributor client recv..."
            ready = select.select([self.sock], [], [], self.__select_timeout)
            if ready[0]:
                chunk = self.sock.recv(1024)
                for d in self.__distributors:
                    d.on_recv(chunk)

