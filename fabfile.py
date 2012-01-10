from fabric.api import *
from fabric.colors import magenta
from seamstress import *

def testcase(func):
    def inner_func(*args, **kwargs):
        puts(magenta("%s" % func.__name__))
        return func(*args, **kwargs)
    return inner_func

@testcase
def test_directory_create():
    directory("/var/web/upickem")
    sudo("test -d /var/web/upickem")

@testcase
def test_directory_delete():
    directory("/var/web/foobar",
        state="deleted")
    sudo("test ! -d /var/web/foobar")

@task
def test():
    test_directory_create()
    test_directory_delete()


