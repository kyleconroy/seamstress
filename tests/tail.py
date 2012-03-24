from fabric.api import *

def assert_abort(func):

    def actual_test():
        with settings(warn_only=True):
            result = func()
        if not result.failed:
            abort("%s should abort" % func.__name__) 
        return result

    actual_test.__name__ = func.__name__
    return actual_test
