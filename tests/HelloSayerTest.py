import unittest
from prenNetworkConnection.HelloSayer import HelloSayer


class HelloSayerTest(unittest.TestCase):
    def test_say_hello(self):
        self.assertEqual('hello Freddy', HelloSayer('Freddy').create_hello_message())


if __name__ == '__main__':
    unittest.main()
