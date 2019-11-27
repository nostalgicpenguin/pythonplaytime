from twisted.internet import protocol, reactor


class Echo(protocol.Protocol):

    def connectionMade(self):
        print("Connection from Client")

    def dataReceived(self, data):
        print("Data received from Client: {}".format(data))
        self.transport.write(data)


class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()


if __name__ == "__main__":
    reactor.listenTCP(8000, EchoFactory())
    reactor.run()
