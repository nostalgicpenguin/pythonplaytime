from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

# Simple chat server to handle registrations from multiple clients over telnet
# and message sharing (broadcast to all clients)
#
# Clients connect with telnet localhost 8123


class ChatProtocol(LineReceiver):

    def __init__(self, factory):
        self.factory = factory
        self.name = None
        self.state = "REGISTER"

    def connectionMade(self):
        self.send_message("What's your name?")

    def connectionLost(self, reason):
        if self.name in self.factory.users:
            del self.factory.users[self.name]
            self.broadcast_message("{} has left the channel."
                                   .format(self.name))

    def lineReceived(self, line):
        if self.state == "REGISTER":
            self.handle_REGISTER(line)
        else:
            self.handle_CHAT(line)

    def rawDataReceived(self, data):
        pass

    def handle_REGISTER(self, name):
        if name in self.factory.users:
            self.send_message("Name taken, please choose another.")
            return

        self.send_message("Welcome, {}!".format(name))
        self.broadcast_message("{} has joined the channel.".format(name))
        self.name = name
        self.factory.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = "<{}> {}".format(self.name, message)
        self.broadcast_message(message)

    def send_message(self, message):
        self.sendLine(message.encode('ascii', 'ignore'))

    def broadcast_message(self, message):
        for name, protocol in self.factory.users.items():
            if protocol != self:
                protocol.sendLine(message.encode('ascii', 'ignore'))


class ChatFactory(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)


if __name__ == '__main__':
    reactor.listenTCP(8123, ChatFactory())
    reactor.run()
