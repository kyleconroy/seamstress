from seamstress.core import remote_file, user
from nose.tools import assert_equals
from tail import assert_abort
from fabric.api import *


@assert_abort
def test_remote_file_sha1_wrong():
    remote_file("/tmp/nginx.tar.gz",
        source="http://nginx.org/download/nginx-1.0.11.tar.gz",
        checksum="c06144234144261358ccf785e99f751b8ca0a3bb")


@assert_abort
def test_remote_file_md5_wrong():
    remote_file("/tmp/nginx.tar.gz",
        source="http://nginx.org/download/nginx-1.0.11.tar.gz",
        checksum="a41a01d7cd46e53ea626d7c9ca283a95")
    

def test_remote_file_sha1():
    remote_file("/tmp/nginx.tar.gz",
        source="http://nginx.org/download/nginx-1.0.11.tar.gz",
        checksum="c06144214144b61358ccf785e99f751b8ca0a3bb")
    sudo("test -f /tmp/nginx.tar.gz")


def test_remote_file():
    remote_file("/tmp/nginx.tar.gz",
        source="http://nginx.org/download/nginx-1.0.11.tar.gz")
    sudo("test -f /tmp/nginx.tar.gz")


def test_remote_file_md5():
    remote_file("/tmp/nginx.tar.gz",
        source="http://nginx.org/download/nginx-1.0.11.tar.gz",
        checksum="a41a01d7cd46e13ea926d7c9ca283a95")
    sudo("test -f /tmp/nginx.tar.gz")


def test_remote_file_create_mode():
    remote_file("/tmp/nginx.tar.gz",
        source="http://nginx.org/download/nginx-1.0.11.tar.gz",
        checksum="a41a01d7cd46e13ea926d7c9ca283a95",
        mode=0600)
    assert_equals(sudo('stat -c "%a" /tmp/nginx.tar.gz'), "600")


def test_remote_file_owner_group():
    user("foo")
    remote_file("/tmp/nginx.tar.gz",
        source="http://nginx.org/download/nginx-1.0.11.tar.gz",
        checksum="a41a01d7cd46e13ea926d7c9ca283a95",
        group="foo",
        owner="foo")
    assert_equals(sudo('stat -c "%G" /tmp/nginx.tar.gz'), "foo")
    assert_equals(sudo('stat -c "%U" /tmp/nginx.tar.gz'), "foo")
    user("foo", state="deleted")


