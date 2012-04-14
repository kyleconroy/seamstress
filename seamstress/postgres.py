from fabric.api import *
from fabric.contrib import files
from seamstress import core


def installation():
    core.package_repository("ppa:pitti/postgresql") 
    core.package("postgresql-9.1")
    core.package("libpq-dev")


def user(name, password):
    cmd = ('psql -c "CREATE USER {} WITH NOCREATEDB NOCREATEUSER '
           'ENCRYPTED PASSWORD E\'{}\'"')
    with settings(hide("running", "warnings"), warn_only=True):
        result = sudo(cmd.format(name, password), user='postgres')
    if result.failed and 'role "{}" already exists'.format(name) not in result:
        abort(str(result))


def database(name):
    with settings(hide("running", "warnings"), warn_only=True):
        result = sudo('psql -c "CREATE DATABASE {}"'.format(name), user='postgres')
    if result.failed and 'database "{}" already exists'.format(name) not in result:
        abort(str(result))


def privilege(name, user=None, database=None):
    if not user or not database:
        abort("name and database required")
    cmd = 'psql -c "GRANT ALL PRIVILEGES ON DATABASE {} TO {}"'
    sudo(cmd.format(database, user), user='postgres')
