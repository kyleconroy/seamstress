import os
from fabric.api import settings, hide

def fabcontext(f):
    def wrapped(*args, **kwargs):
        with settings(hide('aborts', 'warnings', 'running', 'stdout', 'stderr'),
                      host_string="ec2-174-129-111-67.compute-1.amazonaws.com",
                      user="ubuntu",
                      key_filename=os.path.expanduser("~/.ssh/work.pem")):
                f(*args, **kwargs)
    wrapped.__name__ = f.__name__
    return wrapped
