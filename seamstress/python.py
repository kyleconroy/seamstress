from fabric.api import sudo, prefix
from fabric.contrib import files
from seamstress.core import *

def virtualenv(name):
    if not files.exists(name):
        sudo("virtualenv {}".format(name))
    return prefix("source {}/bin/activate".format(name))

def packages(requirements_file, upgrade=False):
    upgrade = "--upgrade " if upgrade else "" 
    sudo("pip install {} -r {}".format(upgrade, requirements_file))


