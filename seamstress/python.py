from fabric.api import sudo, prefix
from seamstress.core import *

def virtualenv(name):
    sudo("virtualenv {}".format(name))
    return prefix("source {}/bin/activate".format(name))

def packages(requirements_file, upgrade=False):
    upgrade = "--upgrade " if upgrade else "" 
    sudo("pip install {} -r {}".format(upgrade, requirements_file))


