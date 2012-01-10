from fabric.api import *
from fabric.colors import magenta
from seamstress import *
from mock import patch

def assert_abort(func):
    @patch("seamstress.abort")
    def actual_test(mock):
        mock.side_effect = KeyError
        try:
            func()
        except KeyError:
            return
        abort("%s should abort" % func.__name__) 

    actual_test.__name__ = func.__name__
    return actual_test

@assert_abort
def test_directory_no_root():
    directory("/") 

@assert_abort
def test_directory_invalid_state():
    directory("/var/web/upickem", state="foobar")

def test_directory_create():
    directory("/var/web/upickem")
    sudo("test -d /var/web/upickem")

def test_directory_delete():
    directory("/var/web/foobar",
        state="deleted")
    sudo("test ! -d /var/web/foobar")

@task
def seamstress_test():
    for (name, thing) in globals().iteritems():
        if name.startswith("test"):
            puts(magenta(name))
            thing()

