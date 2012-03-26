import os
from fabric.api import * 
from fabric.utils import abort
from fabric.contrib import files
from seamstress import system
from fabric.contrib.project import rsync_project


__all__ = ["document", "directory", "user", "remote_file", "package",
           "git", "nginx_site", "jekyll", "ecosystem", "link"]

def states(*states):
    def func(f):
        def wrapper(*args, **kwargs):
            if "state" in kwargs and kwargs["state"] not in states:
                msg = "A {} can't be in state {}. ".format(f.__name__, kwargs["state"])
                msg += "Valid states are {}".format(', '.join(states))
                abort(msg)
            f(*args, **kwargs)
        return wrapper
    return func


def md5(path):
    return sudo("md5sum %s" % path).strip().split(" ")[0]


def sha1(path):
    return sudo("sha1sum %s" % path).strip().split(" ")[0]


def calc_checksum(path, checksum):
    if len(checksum) == 40:
        return sha1(path)
    else:
        return md5(path)


def verify(path, checksum):
    if len(checksum) == 40:
        return sha1(path) == checksum 
    else:
        return md5(path) == checksum


def nginx_site(conf, state="enabled"):
    basename = os.path.basename(conf)
    document("/etc/nginx/conf.d/{}".format(basename),
        source=conf)

    with settings(warn_only=True):
        if sudo("nginx -s reload").failed:
            sudo("nginx")

def ecosystem(lang, version=None):
    if lang == "python":
        package("python-software-properties")
        package_repository("ppa:fkrull/deadsnakes")
        package("python2.7")

        remote_file("/tmp/distribute_setup.py",
            source="http://python-distribute.org/distribute_setup.py",
            mode=0644)

        sudo("python2.7 /tmp/distribute_setup.py")
        sudo("easy_install-2.7 pip")
        sudo("pip-2.7 install virtualenv")
        return
    if lang == "ruby":
        package_repository("ppa:ubuntu-on-rails")
        package("ruby1.9.2")
        package("rubygems")
        sudo("gem install foreman --no-ri --no-rdoc")


def git(path, repository, branch="master", state="created"):
    pass


def jekyll(path, source=None):
    pass


def _file_attribs(location, mode=None, owner=None, group=None, recursive=False):
    """Updates the mode/owner/group for the remote file at the given
    location."""
    recursive = recursive and "-R " or ""
    if mode:
        sudo('chmod {} {:o} "{}"'.format(recursive, mode,  location))
    if owner:
        sudo('chown {} {} "{}"'.format(recursive, owner, location))
    if group:
        sudo('chgrp {} {} "{}"'.format(recursive, group, location))


@states("created", "deleted")
def document(path, source=None, state="created", mode=None, owner=None,
             group=None):
    if state == "deleted":
        sudo("rm -f %s" % path)
        return

    if source is None:
        sudo("touch %s" % path)
    else:
        if isinstance(source, basestring) and not os.path.exists(source):
            abort("No document exists at the local path %s" % source)

        if isinstance(source, basestring) and not os.path.isfile(source):
            abort("Specified path %s is a directory" % source)

        put(source, path, use_sudo=True, mode=mode)

    _file_attribs(path, mode=mode, owner=owner, group=group)


@states("created", "deleted")
def user(name, state="created", group=None, system=False):
    if state == "deleted":
        with settings(warn_only=True):
            result = sudo("userdel %s" % name)
            if result.failed and not result.return_code == 6:
                abort("Error when deleting user %s. `userdel` command "
                      "exited with status %s" % (name, result.return_code))
    else:
        with settings(warn_only=True):
            result = sudo("useradd %s" % name)
            if result.failed and not result.return_code == 9:
                abort("Error when creating user %s. `useradd` command "
                      "exited with status %s" % (name, result.return_code))


@states("created", "deleted")
def directory(path, state="created", owner=None, group=None, 
              mode=None, source=None):
    if path == "/":
        abort("Configuring / is considered harmful")

    if state not in ["created", "deleted"]:
        abort(("A directory can't be in state '%s'. "
               "Valid states are 'created' or 'deleted'") % state)

    if state == "deleted":
        sudo("rm -rf %s" % path)
        return

    sudo("mkdir -p %s" % path)

    _file_attribs(path, mode=mode, owner=owner, group=group)

    if source:
        if not source.endswith("/"):
            source += "/"
        rsync_project(path, local_dir=source, delete=True, exclude=[".*"])


@states("created", "deleted")
def link(source, destination, state="created",
         symbolic=True, mode=None, owner=None, group=None):
    """Creates a (symbolic) link between source and destination on the remote host,
    optionally setting its mode/owner/group."""
    if state == "deleted":
        sudo("rm -rf %s" % destination)
        return
    if symbolic:
        sudo('ln -sf "{}" "{}"'.format(source, destination))
    else:
        sudo('ln -f "{}" "{}"'.format(source, destination))
    _file_attribs(destination, mode, owner, group)


def remote_file(path, source=None, checksum=None, group=None, owner=None,
                mode=None):
    if not (checksum and files.exists(path) and verify(path, checksum)):
        with settings(hide('stdout')):
            sudo("wget -O %s %s" % (path, source))

    if checksum and not verify(path, checksum):
        abort("File downloaded from %s has signature '%s', expected '%s'" % \
              (source, calc_checksum(path, checksum), checksum))

    if owner or group:
        sudo("chown %s:%s %s" % (owner or "", group or "", path))

    if mode:
        sudo("chmod %o %s" % (mode, path))


def package_repository(repository):
    sudo("add-apt-repository " + repository)


def package_upgrade_apt():
    sudo("apt-get --yes upgrade")


def package_update_apt(package=None):
    if package == None:
        sudo("apt-get --yes update")
    else:
        if type(package) in (list, tuple):
            package = " ".join(package)
        sudo("apt-get --yes upgrade " + package)


def package_upgrade_apt(package=None):
    sudo("apt-get --yes upgrade")


def package_install_apt(package, update=False):
    if update:
        sudo("apt-get --yes update")
    if type(package) in (list, tuple):
        package = " ".join(package)
    sudo("apt-get --yes install %s" % (package))


def package_ensure_apt(package, update=False):
    status = run("dpkg-query -W -f='${Status}' %s ; true" % package)
    if status.find("not-installed") != -1 or status.find("installed") == -1:
        package_install_apt(package, update=update)
        return False
    else:
        if update:
            package_update_apt(package)
        return True


def package(name):
    package_ensure_apt(name, update=True)
