from twisted.internet import reactor, protocol


class QuoteProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.send_quote()

    def get_quote(self):
        return self.factory.quote.encode('ascii','ignore')

    def send_quote(self):
        self.transport.write(self.get_quote())

    def dataReceived(self, data):
        print("Received quote: {}".format(data))
        self.transport.loseConnection()


class QuoteClientFactory(protocol.ClientFactory):

    def __init__(self, quote):
        self.quote = quote

    def buildProtocol(self, addr):
        return QuoteProtocol(self)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed: {}'.format(reason.getErrorMessage()))
        maybe_stop_reactor()

    def clientConnectionLost(self, connector, reason):
        print('Connection lost: {}'.format(reason.getErrorMessage()))
        maybe_stop_reactor()


def maybe_stop_reactor():

    global quote_counter
    quote_counter -= 1

    if not quote_counter:
        reactor.stop()


if __name__ == "__main__":

    quotes = [
        'You snooze you lose',
        'The early bird gets the worm',
        'Carpe diem'
    ]

    quote_counter = len(quotes)

    for q in quotes:
        reactor.connectTCP('localhost', 8000, QuoteClientFactory(q))

    reactor.run()
