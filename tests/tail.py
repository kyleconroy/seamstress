from fabric.api import *

def assert_abort(func):

    def actual_test():
        try:
            func()
            abort("%s should abort" % func.__name__) 
        except SystemExit:
            return

    actual_test.__name__ = func.__name__
    return actual_test
