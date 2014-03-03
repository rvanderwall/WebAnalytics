__author__ = 'robert'

class TestHelper:
    count = 0

    def __init__(self):
        self.count = 0

    def should_be(self, actual, expected):
        if actual != expected:
            print("Expected to get {0} but got {1}").format(expected, actual)


    def PASS(self, name):
        print("PASS - {0}").format(name)
        self.count += 1

