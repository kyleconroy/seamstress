from seamstress.core import user
from nose.tools import assert_equals, assert_not_in, assert_in
from tail import assert_abort
from fabric.api import *

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
