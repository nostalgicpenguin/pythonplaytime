from twisted.internet import reactor, protocol


class DataClient(protocol.Protocol):

    def __init__(self):
        self.cmds = [
            (self.put, ['a', 'AAAA']),
            (self.get, ['a']),
            (self.get, ['b']),
            (self.put, ['b', 'BBBB']),
            (self.get, ['b']),
            (self.delete, ['a']),
            (self.get, ['a']),
        ]

    def connectionMade(self):
        cmd, params = self.cmds.pop(0)
        print('{} {}'.format(cmd, params))
        cmd(params)

    def dataReceived(self, data):
        self._process_response(data.decode('utf8'))

        # Run next cmd
        if self.cmds:
            (cmd, params) = self.cmds.pop(0)
            cmd(params)

    def put(self, params):
        if len(params) != 2:
            raise ValueError

        self._send('PUT:{}:{}'.format(params[0], params[1]))

    def get(self, params):
        if len(params) != 1:
            raise ValueError

        self._send('GET:{}'.format(params[0]))

    def delete(self, params):
        if len(params) != 1:
            raise ValueError

        self._send('DELETE:{}'.format(params[0]))

    def _send(self, request):
        print('[REQUEST] {}'.format(request))
        self.transport.write('{}\r\n'.format(request)
                             .encode('ascii', 'ignore'))

    def _process_response(self, response):
        tokens = response.strip('\r\n').split(':')

        if len(tokens) > 0:
            if tokens[0] == 'OK':
                self._handle_response_success(tokens[1:])
                return
            elif tokens[0] == 'FAIL':
                self._handle_response_fail(tokens[1:])
                return

        print('ERROR: Unable to decode response: {}'.format(response))

    def _handle_response_success(self, tokens):
        try:
            cmd = tokens[0]
            if cmd == 'PUT' or cmd == 'GET':
                print('[RESPONSE OK] {} {}={}'
                      .format(cmd, tokens[1], tokens[2]))
            elif cmd == 'DELETE':
                print('[RESPONSE OK] {} {}'.format(cmd, tokens[1]))
            else:
                print('Unrecognised response {}'.format(cmd))
        except ValueError as e:
            print('Unrecognised response {} ({})'.format(tokens, e))

    def _handle_response_fail(self, tokens):
        try:
            cmd = tokens[0]
            if cmd == 'PUT' or cmd == 'GET' or cmd == 'DELETE':
                print('[RESPONSE FAIL] {} {} ({})'
                      .format(cmd, tokens[1], tokens[2]))
            else:
                print('Unrecognised response {}'.format(cmd))
        except ValueError as e:
            print('Unrecognised response {} ({})'.format(tokens, e))


class DataFactory(protocol.ClientFactory):

    def buildProtocol(self, addr):
        return DataClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection to Server failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection to Server lost, reason: {}"
              .format(reason.getErrorMessage()))
        reactor.stop()


# Some tests in a class
class TestDataClient:
    def test_put(self):
        pass


if __name__ == '__main__':
    reactor.connectTCP('localhost', 8000, DataFactory())
    reactor.run()
