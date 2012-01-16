import random
from fabric.api import *
from fabric.colors import magenta
from seamstress import *
from mock import patch
from nose.tools import assert_equals, assert_in, assert_not_in, with_setup

def add_user():
    user("foo")

def del_user():
    user("foo", state="deleted")

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

# Users
@assert_abort
def test_user_invalid_state():
    user("alice", state="foobar")

def test_user_deletion():
    user("alice", state="deleted")
    users = sudo("cat /etc/passwd | awk -F: '{ print $1 }'")
    assert_not_in("alice", [u for u in users.split("\r\n")])

def test_user_creation():
    user("alice")
    users = sudo("cat /etc/passwd | awk -F: '{ print $1 }'")
    assert_in("alice", [u for u in users.split("\r\n")])

# Files
@assert_abort
def test_document_invalid_state():
    document("foobar", state="foobar")

@assert_abort
def test_document_directory():
    document("foobar", source="tests")

@assert_abort
def test_document_invalid_path():
    document("foobar", source="foo/bar/man.txt")

def test_document_create_file():
    document("foobar", source=open("tests/hello.txt"))
    contents = sudo("cat foobar")
    assert_equals(contents, "Hello World")

def test_document_create_contents():
    document("foobar", source="tests/hello.txt")
    contents = sudo("cat foobar")
    assert_equals(contents, "Hello World")

def test_document_create_mode():
    document("foobar", mode=0600)
    assert_equals(sudo('stat -c "%a" foobar'), "600")

def test_document_create():
    document("foobar")
    sudo("test -f foobar")

def test_document_delete():
    document("foobar", state="deleted")
    sudo("test ! -f foobar")

def test_document_owner_group():
    user("foo")
    document("foobar", group="foo", owner="foo")
    assert_equals(sudo('stat -c "%G" foobar'), "foo")
    assert_equals(sudo('stat -c "%U" foobar'), "foo")
    user("foo", state="deleted")

def test_document_owner():
    user("foo")
    document("foobar", owner="foo")
    assert_equals(sudo('stat -c "%U" foobar'), "foo")
    user("foo", state="deleted")

def test_document_user():
    user("foo")
    document("bat", group="foo")
    assert_equals(sudo('stat -c "%G" bat'), "foo")
    user("foo", state="deleted")

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

@task
def seamstress_test():
    # setup
    # sudo("adduser foo")

    tests = [f for f in globals().iteritems() if f[0].startswith("test")]
    random.shuffle(tests)

    for (name, thing) in tests: 
        puts(magenta(name))
        thing()

