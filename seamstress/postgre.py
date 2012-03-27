from fabric.api import *
from fabric.contrib import files
from seamstress import core


def installation():
    core.package_repository("ppa:pitti/postgresql") 
    core.package("postgresql-9.1")


def user(name):
    with settings(hide("warnings"), warn_only=True):
        result = sudo('createuser -R -S -d {}'.format(name), user="postgres")
    if result.failed and 'role "{}" already exists'.format(name) not in result:
        abort(str(result))


def database(name):
    with settings(hide("stdout")):
        result = sudo("psql -l", user="postgres")
    if name not in result:
        sudo('createdb {}'.format(name), user="postgres")

