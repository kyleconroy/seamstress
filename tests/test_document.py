from seamstress.core import document, user
from nose.tools import assert_equals
from tail import assert_abort
from fabric.api import *

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


