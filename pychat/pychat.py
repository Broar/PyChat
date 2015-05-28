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
from channel import Channel

DEFAULT_PORT = 8080
DEFAULT_BACKLOG = 5

# A mapping of channel names to objects. A default 'main' channel always exists
channels = {"main" : Channel()}
lock = threading.Lock()
    
def list_channels():
    """

    Create a string of the available channels

    @returns a string of the available channels

    """
    lock.acquire()

    channel_list = []
    for key, val in channels.items():
        channel_list.append(key)

    lock.release()

    return "\n".join(channel_list)

def handle_client(client, channel):
    """

    Listen to messages from the client and broadcast them to a channel

    @param client the client who has joined the channel
    @param channel the channel to send/receive messages from

    """
    while True:
        msg = utils.recv(client[0]).strip("\r\n ")
        split_list = msg.split(None, 2)

        if split_list[0] == "whisper":
            if len(split_list) < 3:
                usage = "usage: whisper <user> <message>"
                client[0].sendall("{0:04d}{1}".format(len(usage), usage))
            else:
                channel.whisper(client, split_list[1], split_list[2])

        elif split_list[0] == "join":
            if len(split_list) < 2:
                usage = "usage: join <channel>"
                client[0].sendall("{0:04d}{1}".format(len(usage), usage))
            else:
                channel.leave(client)

                try:
                    channel = channels[split_list[1]]
                except KeyError:
                    channels[split_list[1]] = Channel()
                    channel = channels[split_list[1]]

                channel.join(client)

        elif split_list[0] == "leave":
            channel.leave(client)
            channel = channels["main"]
            channel.join(client)

        elif split_list[0] == "channels":
            response = list_channels()
            client[0].sendall("{0:04d}{1}".format(len(response), response))

        elif split_list[0] == "users":
            pass

        elif split_list[0] == "help":
            pass

        elif split_list[0] == "quit":
            channel.leave(client)
            break

        else:
            channel.say(client, msg)

    client[0].close()

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

    serversock = None

    # Prepare a socket to listen for connections
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        serversock.bind(("", port)) 
    except socket.error as e:
        serversock.close()
        exit("socket error({0}) : {1}".format(e.errno, e.strerror))

    serversock.listen(DEFAULT_BACKLOG)

    # Accept connections until the program is killed. 
    # All client join the main channel upon first connecting
    try:
        while True:
            (clientsock, address) = serversock.accept()
            name = utils.recv(clientsock).strip("\r\n ")

            # Clients are simple two-element lists containing a socket and name
            client = [clientsock, name]
            print(client)
            channel = channels["main"]
            channel.join(client)

            t = threading.Thread(target=handle_client, args=(client, channel,))
            t.setDaemon(True)
            t.start()
    finally:
        server_socket.close()

if __name__ == "__main__":
    sys.exit(main())