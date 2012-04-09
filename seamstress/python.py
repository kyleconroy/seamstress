from fabric.api import sudo, prefix
from fabric.contrib import files
from seamstress import core

def installation():
    core.package("python-software-properties")
    core.package("python-setuptools")
    core.package("python-dev")

    core.package_repository("ppa:fkrull/deadsnakes")
    core.package("python2.7")

    core.remote_file("/tmp/distribute_setup.py",
        source="http://python-distribute.org/distribute_setup.py",
        mode=0644)

    # Python 2.7
    sudo("python2.7 /tmp/distribute_setup.py")
    sudo("easy_install-2.7 pip")
    sudo("pip-2.7 install virtualenv")

    # Python 2.6
    sudo("easy_install-2.6 pip")
    sudo("pip-2.6 install virtualenv")


def virtualenv(name, python_version="2.6", system_packages=False):
    if not files.exists(name):
        sp = "--system-site-packages" if system_packages else ""
        sudo("virtualenv {} -p /usr/bin/python{} {}".format(
            name, python_version, sp))
    return prefix("source {}/bin/activate".format(name))


def packages(requirements_file, upgrade=False):
    upgrade = "--upgrade " if upgrade else "" 
    sudo("pip install {} -r {}".format(upgrade, requirements_file))


def package(name, version=None, upgrade=False):
    upgrade = "--upgrade " if upgrade else "" 
    version = "=={}".format(version) if version else ""
    sudo("pip install {} {}{}".format(upgrade, name, version))



