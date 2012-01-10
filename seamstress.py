__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)

from fabric.api import abort, sudo

def directory(path, state="created", owner=None, group=None):
    if path == "/":
        abort("Configuring / is considered harmful")

    if state == "created":
        sudo("mkdir -p %s" % path)
        return 

    if state == "deleted":
        sudo("rm -rf %s" % path)
        return

    abort(("A directory can't be in state '%s'. "
           "Valid states are 'created' or 'deleted'") % state)

