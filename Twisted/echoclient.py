from twisted.internet import reactor, protocol


class EchoClient(protocol.Protocol):

    def connectionMade(self):
        response = "Hello, world!"
        self.transport.write(response.encode('ascii', 'ignore'))

    def dataReceived(self, data):
        print("Data received from Server: {}".format(data))
        self.transport.loseConnection()


class EchoFactory(protocol.ClientFactory):

    def buildProtocol(self, addr):
        return EchoClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection to Server failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection to Server lost, reason: {}"
              .format(reason.getErrorMessage()))
        reactor.stop()


reactor.connectTCP('localhost', 8000, EchoFactory())
reactor.run()
