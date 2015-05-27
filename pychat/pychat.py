"""

A simple chat server using TCP/IP

@author Steven Briggs
@version 2015.05.25

"""

import sys
import argparse
import socket
import threading
import utils

DEFAULT_PORT = 8080
DEFAULT_BACKLOG = 5

# A dictonary mapping channel names to objects
channels = {}

def handle_client():
    pass

def get_args():
    """

    Parse and return the arguments given at the command line

    @returns the command line arguments

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=DEFAULT_PORT, type=int, help="port number for the server")
    return parser.parse_args()

def main():
    args = get_args()
    port = args.port

    server_socket = None

    # Prepare a socket to listen for connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind(("", port)) 
    except socket.error as e:
        server_socket.close()
        exit("socket error({0}) : {1}".format(e.errno, e.strerror))

    server_socket.listen(DEFAULT_BACKLOG)

    # Accept connections until the program is killed
    try:
        running = True
        while running:
            (client_socket, address) = server_socket.accept()
            print(utils.recv(client_socket))
    finally:
        server_socket.close()

if __name__ == "__main__":
    sys.exit(main())