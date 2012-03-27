from seamstress import core
from seamstress import mysql
from seamstress import nginx
from seamstress import postgre
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


def test_foreman_service():
    core.git_repository("responsive", "git://github.com/derferman/areyouresponsive.git")

    with cd("responsive"):
        core.foreman_service("areyouresponsive")

    sudo("test -f /etc/init/areyouresponsive.conf")


def test_nginx_install():
    nginx.installation()
    assert_in("1.0.14", run("nginx -v"))


def test_postgre_install():
    postgre.installation()
    assert_in("9.1", run("psql --version"))
