from fabric.api import *
from fabric.contrib import files
from seamstress import core


def installation():
    core.package_repository("ppa:nginx/stable")
    core.package("nginx")
    if files.exists("/etc/nginx/sites-enabled/default"):
        sudo("rm /etc/nginx/sites-enabled/default")


def enabled_site(conf):
    basename = os.path.basename(conf)
    sudo("cp {} /etc/nginx/conf.d/{}".format(conf, basename))
    with settings(warn_only=True):
        result = sudo("nginx -s reload")
    if result.failed:
        sudo("nginx")


