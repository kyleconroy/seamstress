from fabric.api import *
from seamstress import core

def installation():
    core.package_repository("ppa:ubuntu-on-rails")
    core.package("ruby1.9.2")
    core.package("rubygems")
    gem("foreman")


def gem(name, version=None, state="installed"):
    with settings(warn_only=True):
        installed = sudo("gem list -i {}".format(name)) 

    if state == "uninstalled":
        if installed == "true":
            sudo("gem uninstall -a -I -x {}".format(name))
        return

    if version:
        vflag = "--version '{}'".format(version)
    else:
        vflag = ""

    with settings(warn_only=True):
        result = sudo("gem install {} {} --no-ri --no-rdoc".format(name, vflag))
        if result.failed and not result.return_code == -1:
            abort("The {} gem can't be found".format(name))


