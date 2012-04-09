from seamstress.core import directory, user
from nose.tools import assert_equals
from tail import assert_abort
from fabric.api import *

# Directory
@assert_abort
def test_directory_no_root():
    directory("/") 

@assert_abort
def test_directory_invalid_state():
    directory("/var/web/upickem", state="foobar")

def test_directory_create_mode():
    directory("/var/web/boom", mode=0666)
    assert_equals(sudo('stat -c "%a" /var/web/boom'), "666")

def test_directory_create():
    directory("/var/web/upickem")
    sudo("test -d /var/web/upickem")

def test_directory_context_manager():
    with directory("/var/web/upickem"):
        assert_equals("/var/web/upickem", sudo("pwd"))

def test_directory_delete():
    directory("/var/web/foobar", state="deleted")
    sudo("test ! -d /var/web/foobar")

def test_directory_owner_group():
    user("foo")
    directory("/var/web/foobar", group="foo", owner="foo")
    assert_equals(sudo('stat -c "%G" /var/web/foobar'), "foo")
    assert_equals(sudo('stat -c "%U" /var/web/foobar'), "foo")
    user("foo", state="deleted")

def test_directory_owner():
    user("foo")
    directory("/var/web/foobar", owner="foo")
    assert_equals(sudo('stat -c "%U" /var/web/foobar'), "foo")
    user("foo", state="deleted")

def test_directory_user():
    user("foo")
    directory("/var/web/foobar", group="foo")
    assert_equals(sudo('stat -c "%G" /var/web/foobar'), "foo")
    user("foo", state="deleted")


