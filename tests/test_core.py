from seamstress import core
from seamstress import mysql
from seamstress import nginx
from seamstress import postgres
from seamstress import ruby, python
from nose.tools import assert_equals, assert_in
from tail import assert_abort
from fabric.api import *

def test_python():
    python.installation()
    assert_in("2.7", run("python2.7 --version"))

def test_ruby():
    ruby.installation()
    assert_in("1.9", run("ruby1.9.2 --version"))

def test_ruby_gems():
    ruby.installation()
    assert_in("1.3.7", run("gem -v"))

def test_git_repo():
    core.package("git-core")
    core.git_repository("seamstress", "git://github.com/kyleconroy/seamstress.git")
    with cd("seamstress"):
        assert_in("master", run("git branch"))


def test_foreman_service():
    core.git_repository("responsive", "git://github.com/kyleconroy/areyouresponsive.git")

    with cd("responsive"):
        core.foreman_service("areyouresponsive")

    sudo("test -f /etc/init/areyouresponsive.conf")


def test_nginx_install():
    nginx.installation()
    assert_in("1.0.14", run("nginx -v"))


def test_postgres_database():
    postgres.installation()
    postgres.database("foobar")
    assert_in("foobar", sudo("psql -l", user="postgres"))

def test_postgres_user():
    postgres.installation()
    postgres.user("boo", "foo")
    assert_in("boo", sudo('psql -c "\\du"', user="postgres"))

def test_postgres_privilege():
    postgres.installation()
    postgres.database("foobar")
    postgres.user("boo", "foo")
    postgres.privilege("all",
            user="boo",
            database="foobar")
