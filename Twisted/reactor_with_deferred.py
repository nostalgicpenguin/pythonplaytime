import functools

from twisted.internet import reactor, defer


def wrapper(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        print('Starting {}'.format(func.__name__))
        ret = func(*args, **kwargs)
        print('Ending {}'.format(func.__name__))
        return ret
    return wrap


class HeadlineRetriever(object):

    @wrapper
    def processHeadline(self, headline):
        if len(headline) > 50:
            self.d.errback(Exception("The headline '{}' is too long!".format(headline)))
        else:
            self.d.callback(headline)

    @wrapper
    def _toHTML(self, result):
        return "<h1>{}</h1>".format(result)

    @wrapper
    def getHeadlines(self, input):
        self.d = defer.Deferred()
        # Wait before calling
        reactor.callLater(1, self.processHeadline, input)
        self.d.addCallback(self._toHTML)
        return self.d


# Invoked by callback
@wrapper
def printData(result):
    print(result)

# Invoked by errBack
@wrapper
def printError(failure):
    print(failure.value)


@wrapper
def finish():
    reactor.stop()


if __name__ == '__main__':

    h = HeadlineRetriever()
    # This will cause printData to be invoked
    d = h.getHeadlines("Breaking News: Twisted Takes us to the Moon!")
    d.addCallbacks(printData, printError)

    h = HeadlineRetriever()
    # This will cause printError to be invoked
    d = h.getHeadlines("1234567890" * 6)
    d.addCallbacks(printData, printError)

    reactor.callLater(2, finish)
    reactor.run()
