class Algo(object):
    def handle_test_event(self):
        print("test event handled")

    def handle_x_changed(self, x):
        print("new {x}".format(x=x))


class XPosition(object):
    def __init__(self):
        self._handlers1 = []
        self._handlers2 = []

    def register_test_event(self, f):
        self._handlers1.append(f)

    def raise_test_event(self):
        handlers = self._handlers1
        if handlers:
            for h in handlers:
                h()

    def register_x_changed(self, f):
        self._handlers2.append(f)

    def raise_x_changed(self, x):
        handlers = self._handlers2
        if handlers:
            for h in handlers:
                h(x)


if __name__ == '__main__':
    a = Algo()
    x = XPosition()

    x.register_test_event(a.handle_test_event)
    x.register_test_event(lambda: print("hello from lambda method"))
    x.raise_test_event()

    x.register_x_changed(a.handle_x_changed)
    x.register_x_changed(lambda new_x: print("lambda method with x: '{}'".format(new_x)))
    x.raise_x_changed(27)
