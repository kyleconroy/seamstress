from fabric.api import * 

def installed(command):
    with settings(warn_only=True):
        result = sudo("hash {}".format(command))
        return result.succeeded
