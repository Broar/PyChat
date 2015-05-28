"""

A client that can connect to a PyChat server and send messages

@author Steven Briggs
@version 2015.05.26

"""

import sys
import argparse
import socket
import threading
import utils
from random import randint

def send_msgs(sock):
    """

    A thread function for reading messages from STDIN and sending them
    to the specified socket

    @param sock the socket to send messages to

    """
    while True:
        msg = sys.stdin.readline()
        sock.sendall("{0:04d}{1}".format(len(msg), msg))

def recv_msgs(sock):
    """

    A thread function for reading message from the specified socket and
    printing them to the console

    @param sock the socket to send messages to

    """
    while True:
        msg = utils.recv(sock)
        print(msg)

def get_args():
    """

    Parse and return the arguments given at the command line

    @returns the command line arguments

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("host", type=str, help="server to connect to")
    parser.add_argument("port", type=str, help="port to connect on")
    parser.add_argument("-n", "--name", type=str, help="display name for chat")
    return parser.parse_args()

def main():
    # Read any command line arguments
    args = get_args()
    address = (args.host, args.port)
    name = "user{0}".format(randint(0, 4096))

    # Set the display name if the user entered one
    if args.name:
        name = args.name

    sock = None

    # Connect to the chat server
    try:
        sock = socket.create_connection(address)
    except socket.error as e:
        exit("socket error({0}) : {1}".format(e.errno, e.strerror))

    # Spin up threads for sending/receiving messages
    try:
        sock.sendall("{0:04d}{1}".format(len(name), name))

        recv_thread = threading.Thread(target=recv_msgs, args=(sock,))
        send_thread = threading.Thread(target=send_msgs, args=(sock,))

        recv_thread.start()
        send_thread.start()

        recv_thread.join()
        send_thread.join()
    finally:
        sock.close()

if __name__ == "__main__":
    sys.exit(main())