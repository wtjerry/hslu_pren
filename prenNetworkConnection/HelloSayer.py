class HelloSayer(object):
    def __init__(self, name):
        self.name = name

    def create_hello_message(self):
        return 'hello {name}'.format(name=self.name)

    def say_hello(self):
        print(self.create_hello_message())


if __name__ == '__main__':
    e = HelloSayer('Heiri')
    e.say_hello()
