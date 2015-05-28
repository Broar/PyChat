"""

A channel is a chat room in PyChat that contains clients. Channels manage 
sending messages to/from any subscribers; however, they do not receive
messages.

@author Steven Briggs
@version 2015.05.27

"""

import socket
import threading
import utils

class Channel(object):
    def __init__(self):
        """

        Create a new Channel object

        """
        self.clients = []
        self.lock = threading.Lock()

    def say(self, sender, msg):
        """

        Send a message to all subscribers

        @param sender the client who sent the message
        @param msg the message to be broadcasted

        """
        complete_msg = "<{0}> says: {1}".format(sender[1], msg)

        self.lock.acquire()

        # Send the complete message to all other subscribers
        for c in self.clients:
            if c != sender:
                c[0].sendall("{0:04d}{1}".format(len(complete_msg), complete_msg))

        self.lock.release()

    def whisper(self, sender, receiver_name, msg):
        """

        Send a private message from sender to receiver

        @param sender_name the client who is sending the message
        @param receiver_name the name of the client who is receiving message
        @param msg the private message to be sent

        """
        complete_msg = "<{0}> whispers: {1}".format(sender[1], msg)

        self.lock.acquire()

        for c in self.clients:
            if c[1] == receiver_name:
                c[0].sendall("{0:04d}{1}".format(len(complete_msg), complete_msg))
                break
        else:
            failure_msg = "error: <{0}> does not exist on this channel".format(receiver_name)
            sender[0].sendall("{0:04d}{1}".format(len(failure_msg), failure_msg))

        self.lock.release()

    def join(self, client):
        """

        Add a new subscriber to the channel

        @param client the client that is joining tbe channel

        """
        self.lock.acquire()

        self.clients.append(client)
        msg = "<{0}> joined the channel".format(client[1])

        for c in self.clients:
            if c != client:
                c[0].sendall("{0:04d}{1}".format(len(msg), msg))

        self.lock.release()

    def leave(self, client):
        """

        Remove a subscriber from the channel

        @param client the client that is leaving the channel

        """
        self.lock.acquire()

        self.clients.remove(client)
        msg = "<{0}> left the channel".format(client[1])

        for c in self.clients:
            if c != client:
                c[0].sendall("{0:04d}{1}".format(len(msg), msg))

        self.lock.release()