"""

A collection of useful utility functions for sending and receiving messages
between sockets. 

@author Steven Briggs
@version 2015.05.26

"""

import socket

MSG_LEN_SIZE = 4
MSG_BUFFER_SIZE = 2048

def recv_len(sock):
    """

    Read in the length of an incoming message from the specified socket.
    Messages are to prefixed with MSG_LEN_SIZE numerical characters.

    @param sock the socket to read from
    @returns the length of an incoming message

    """
    chunks = []
    n = 0

    while n < MSG_LEN_SIZE:
        chunk = sock.recv(min(MSG_LEN_SIZE - n, MSG_LEN_SIZE))
        if chunk == "":
            raise RuntimeError("socket connection broken")
        chunks.append(chunk)
        n += len(chunk)

    return int("".join(chunks))

def recv_msg(sock, size):
    """

    Read in a message of length size from the specified socket

    @param sock the socket to read from
    @param size the length of the message to read
    @returns the message from the socket

    """
    chunks = []
    n = 0

    while n < size:
        chunk = sock.recv(MSG_BUFFER_SIZE)
        if chunk == "":
            raise RuntimeError("socket connection broken")
        n += len(chunk)

    return "".join(chunk)

def recv(sock):
    """

    Read in a message from the specified socket

    @param socket the socket to read from
    @returns the message from the socket

    """
    return recv_msg(sock, recv_len(sock))