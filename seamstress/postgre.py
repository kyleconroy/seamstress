from fabric.api import *
from seamstress import core


def installation():
    core.package_repository("ppa:pitti/postgresql") 
    core.package("postgresql-9.1")

