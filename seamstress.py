__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)

import os
from fabric.api import * 
from fabric.utils import abort
from fabric.contrib import files

__all__ = ["document", "directory", "user", "remote_file", "package"]

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


def document(path, source=None, state="created", mode=None, owner=None,
             group=None):
    if state not in ["created", "deleted"]:
        abort(("A document can't be in state '%s'. "
               "Valid states are 'created' or 'deleted'") % state)

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

    if owner or group:
        sudo("chown %s:%s %s" % (owner or "", group or "", path))

    if mode:
        sudo("chmod %o %s" % (mode, path))


def user(name, state="created", group=None, system=False):
    if state not in ["created", "deleted"]:
        abort(("A user can't be in state '%s'. "
               "Valid states are 'created' or 'deleted'") % state)

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


def directory(path, state="created", owner=None, group=None, mode=None):
    if path == "/":
        abort("Configuring / is considered harmful")

    if state not in ["created", "deleted"]:
        abort(("A directory can't be in state '%s'. "
               "Valid states are 'created' or 'deleted'") % state)

    if state == "deleted":
        sudo("rm -rf %s" % path)
        return

    sudo("mkdir -p %s" % path)

    if owner or group:
        sudo("chown %s:%s %s" % (owner or "", group or "", path))

    if mode:
        sudo("chmod %o %s" % (mode, path))

def remote_file(path, source=None, checksum=None):
    if checksum and files.exists(path) and verify(path, checksum):
        return

    with settings(hide('stdout')):
        sudo("wget -O %s %s" % (path, source))

    if checksum and not verify(path, checksum):
        abort("File downloaded from %s has signature '%s', expected '%s'" % \
              (source, calc_checksum(path, checksum), checksum))

def package(name, state=None, version=None):
    with settings(hide('stdout')):
        sudo("apt-get update")

    if version:
        name = name + "=" + version

    sudo("apt-get install %s" % name)

