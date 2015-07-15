__author__ = 'robert'

class TestHelper:
    fail_count = 0

    def __init__(self):
        self.fail_count = 0

    def run_test(self, test):
        self.fail_count = 0
        test(self)
        name = test.func_name
        if self.fail_count != 0:
            self.FAIL(name)
        else:
            self.PASS(name)

    def should_be(self, actual, expected):
        if actual != expected:
            self.fail_count += 1
            print("Expected to get {0} but got {1}").format(expected, actual)

    def PASS(self, name):
        print("PASS - {0}").format(name)

    def FAIL(self, name):
        print("FAIL - {0}").format(name)
