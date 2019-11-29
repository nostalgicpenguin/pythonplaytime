from twisted.internet.defer import Deferred


def add_bold(result):
    return "<b>{}</b>".format(result)


def add_italic(result):
    return "<i>{}</i>".format(result)


def print_html(result):
    print(result)


if __name__ == '__main__':
    d = Deferred()
    d.addCallback(add_bold)
    d.addCallback(add_italic)
    d.addCallback(print_html)
    d.callback('Hello World')