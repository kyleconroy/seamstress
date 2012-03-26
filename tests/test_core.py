from seamstress import core
from nose.tools import assert_equals, assert_in
from tail import assert_abort
from fabric.api import *

def test_python():
    core.ecosystem("python")
    assert_in("2.7", run("python2.7 --version"))

def test_ruby():
    core.ecosystem("ruby")
    assert_in("1.9", run("ruby1.9.2 --version"))

def test_ruby_gems():
    core.ecosystem("ruby")
    assert_in("1.3.7", run("gem -v"))

def test_git_repo():
    core.package("git-core")
    core.git_repository("seamstress", "git://github.com/derferman/seamstress.git")
    with cd("seamstress"):
        assert_in("master", run("git branch"))
