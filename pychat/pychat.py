"""

A simple chat server using TCP/IP and the publisher-subscriber pattern.

@author Steven Briggs
@version 2015.05.25

"""

import sys
import argparse
import socket

DEFAULT_PORT = 8080
DEFAULT_BACKLOG = 5

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

    # Prepare the listening socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostname(), port))
    server_socket.listen(DEFAULT_BACKLOG)

    # Accept connections until the program is killed
    running = True
    while running:
        (client_socket, address) = server_socket.accept()
        client_socket.close()
        print("Got a client @ address {0}".format(address))

    server_socket.close()

if __name__ == "__main__":
    sys.exit(main())