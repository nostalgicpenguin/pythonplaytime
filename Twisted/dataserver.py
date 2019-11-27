from twisted.internet import protocol, reactor
from twisted.protocols.basic import LineReceiver


class Database(LineReceiver):

    def __init__(self, factory):
        self.factory = factory
        self.dispatcher = {'PUT': self.handle_put,
                           'GET': self.handle_get,
                           'DELETE': self.handle_delete}

    def connectionMade(self):
        print("Connection from remote client")

    def connectionLost(self, reason):
        print("Connection from remote client lost")

    def lineReceived(self, line):
        print("Data received from Client: {}".format(line))
        self.decode_request(line.decode('utf8'))

    def rawDataReceived(self, data):
        pass

    def decode_request(self, request):
        try:
            cmd_and_params = request.split(':')
            print('cmd: {}'.format(cmd_and_params[0]))

            if cmd_and_params == 0:
                self.handle_bad_cmd('FAIL:Malformed request')
                return

            cmd, params = cmd_and_params[0], (cmd_and_params[1:])
            print('{} {}'.format(cmd, params))
            self.dispatcher[cmd_and_params[0]](cmd_and_params[1:])

        except Exception as e:
            print('Unable to decode request {}'.format(e))
            self.send_response('FAIL:Malformed request')

    def handle_put(self, params):
        if len(params) != 2:
            self.handle_bad_cmd('FAIL:PUT:Malformed params')
            return

        key, value = params[0], params[1]
        self.factory.db[key] = value
        self.send_response('OK:PUT:{}:{}'.format(key, value))

    def handle_get(self, params):
        if len(params) != 1:
            self.handle_bad_cmd('FAIL:GET:Malformed params')
            return

        key = params[0]
        try:
            value = self.factory.db[key]
            self.send_response('OK:GET:{}:{}'.format(key, value))
        except KeyError:
            self.send_response('FAIL:GET:{}:Key not found!'.format(key))

    def handle_delete(self, params):
        if len(params) != 1:
            self.handle_bad_cmd('FAIL:DELETE:Malformed params')
            return

        key = params[0]
        try:
            del self.factory.db[key]
            self.send_response('OK:DELETE:{}'.format(key))
        except KeyError:
            self.send_response('FAIL:DELETE:{}:Key not found!'.format(key))

    def handle_bad_cmd(self, reason):
        self.send_response(reason)

    def send_response(self, response):
        self.transport.write('{}\r\n'
                             .format(response)
                             .encode('ascii', 'ignore'))


class DataFactory(protocol.Factory):

    def __init__(self):
        self.db = {}

    def buildProtocol(self, addr):
        return Database(self)


if __name__ == '__main__':
    reactor.listenTCP(8000, DataFactory())
    reactor.run()
