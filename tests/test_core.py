from seamstress.core import ecosystem
from nose.tools import assert_equals, assert_in
from tail import assert_abort
from fabric.api import *

def test_python():
    ecosystem("python")
    assert_in("2.7", run("python2.7 --version"))

def test_ruby():
    ecosystem("ruby")
    assert_in("1.9", run("ruby1.9.2 --version"))

def test_ruby_gems():
    ecosystem("ruby")
    assert_in("1.3.7", run("gem -v"))

