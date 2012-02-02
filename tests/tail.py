from mock import patch
from fabric.api import *

def assert_abort(func):
    @patch("seamstress.core.abort")
    def actual_test(mock):
        mock.side_effect = KeyError
        try:
            func()
        except KeyError:
            return
        abort("%s should abort" % func.__name__) 

    actual_test.__name__ = func.__name__
    return actual_test


