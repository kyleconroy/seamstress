__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)

import os
from fabric.api import sudo, settings, hide, put
from fabric.utils import abort

def document(path, source=None, state="created", mode=None):
    if state not in ["created", "deleted"]:
        abort(("A document can't be in state '%s'. "
               "Valid states are 'created' or 'deleted'") % state)

    if state == "deleted":
        sudo("rm -f %s" % path)
        return

    if source is None:
        sudo("touch %s" % path)
        return

    if isinstance(source, basestring) and not os.path.exists(source):
        abort("No document exists at the local path %s" % source)

    if isinstance(source, basestring) and not os.path.isfile(source):
        abort("Specified path %s is a directory" % source)

    put(source, path, use_sudo=True, mode=mode)


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
        sudo("chmod %s %s" % (mode, path))


