from seamstress.core import link, document
from nose.tools import assert_equals
from tail import assert_abort
from fabric.api import *

@assert_abort
def test_link_invalid_state():
    link("/var/web/upickem", "/foo", state="foobar")

def test_link_create():
    document("foobar")
    link("foobar", "bar")
    run("test -L bar")

def test_link_delete():
    link("foobar", "bar", state="deleted")
    run("test ! -L foobar")
