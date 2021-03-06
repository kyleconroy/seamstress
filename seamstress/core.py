import os
from fabric.api import * 
from fabric.utils import abort
from fabric.contrib import files
from seamstress import system
from fabric.contrib.project import rsync_project


__all__ = ["document", "directory", "user", "group", "remote_file", "package",
           "git_repository", "link", "service", "foreman_service", "copy"]

def states(*states):
    def func(f):
        def wrapper(*args, **kwargs):
            if "state" in kwargs and kwargs["state"] not in states:
                msg = "A {} can't be in state {}. ".format(f.__name__, kwargs["state"])
                msg += "Valid states are {}".format(', '.join(states))
                abort(msg)
            return f(*args, **kwargs)
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


def git_repository(path, repository, branch="master", **kwargs): 
    if not files.exists(path, use_sudo=True):
        sudo("git clone {} {}".format(repository, path))
    with cd(path):
        sudo("git checkout {}".format(branch))
        sudo("git pull origin {}".format(branch))
    return directory(path, **kwargs)


def jekyll(path, source=None):
    pass


def _file_attribs(location, mode=None, owner=None, group=None, recursive=False):
    """Updates the mode/owner/group for the remote file at the given
    location."""
    recursive = "-R " if recursive else ""
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


def copy(path, source):
    sudo("cp {} {}".format(source, path))


def group_create(name, gid=None):
	"""Creates a group with the given name, and optionally given gid."""
	options = []
	if gid:
		options.append("-g '%s'" % (gid))
	sudo("groupadd %s '%s'" % (" ".join(options), name))


def group_check(name):
	"""Checks if there is a group defined with the given name,
	returning its information as a
	'{"name":<str>,"gid":<str>,"members":<list[str]>}' or 'None' if
	the group does not exists."""
	group_data = run("cat /etc/group | egrep '^%s:' ; true" % (name))
	if group_data:
		name, _, gid, members = group_data.split(":", 4)
		return dict(name=name, gid=gid,
					members=tuple(m.strip() for m in members.split(",")))
	else:
		return None


def group(name, gid=None):
	"""Ensures that the group with the given name (and optional gid)
	exists."""
	d = group_check(name)
	if not d:
		group_create(name, gid)
	else:
		if gid != None and d.get("gid") != gid:
			sudo("groupmod -g %s '%s'" % (gid, name))


def group_user_check(group, user):
	"""Checks if the given user is a member of the given group. It
	will return 'False' if the group does not exist."""
	d = group_check(group)
	if d is None:
		return False
	else:
		return user in d["members"]


def group_user_add(group, user):
	"""Adds the given user/list of users to the given group/groups."""
	assert group_check(group), "Group does not exist: %s" % (group)
	if not group_user_check(group, user):
		sudo("usermod -a -G '%s' '%s'" % (group, user))


def group_user_ensure(group, user):
	"""Ensure that a given user is a member of a given group."""
	d = group_check(group)
	if user not in d["members"]:
		group_user_add(group, user)


@states("created", "deleted")
def user(name, state="created", group=None, system=False):
    if state == "deleted":
        with settings(warn_only=True):
            result = sudo("userdel %s" % name)
            if result.failed and not result.return_code == 6:
                abort("Error when deleting user %s. `userdel` command "
                      "exited with status %s" % (name, result.return_code))
        return

    with settings(warn_only=True):
        result = sudo("useradd %s" % name)
        if result.failed and not result.return_code == 9:
            abort("Error when creating user %s. `useradd` command "
                  "exited with status %s" % (name, result.return_code))


    if group:
        group_user_ensure(group, name)



@states("created", "deleted")
def directory(path, state="created", owner=None, group=None, 
              mode=None, source=None, recursive=False):
    if path == "/":
        abort("Configuring / is considered harmful")

    if state not in ["created", "deleted"]:
        abort(("A directory can't be in state '%s'. "
               "Valid states are 'created' or 'deleted'") % state)

    if state == "deleted":
        sudo("rm -rf %s" % path)
        return

    sudo("mkdir -p %s" % path)

    _file_attribs(path, mode=mode, owner=owner, group=group, 
                  recursive=recursive)

    if source:
        if not source.endswith("/"):
            source += "/"
        rsync_project(path, local_dir=source, delete=True, exclude=[".*"])

    return cd(path)


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


def service(name):
    with settings(warn_only=True):
        status = sudo("service {} status".format(name))
    if status.failed:
        sudo("service {} start".format(name))
    else:
        sudo("service {} restart".format(name))


def foreman_service(name, port=5000, user="ubuntu", env=None):
    with prefix('export PATH="/var/lib/gems/1.8/bin:$PATH"'):
        command = ("foreman export upstart /etc/init "
                   "--app {} --port {} --user {}")
        cmd = command.format(name, port, user)

        if env:
            cmd += " --env {}".format(env)

        sudo(cmd)
    with settings(warn_only=True):
        sudo("stop {}".format(name))
    sudo("start {}".format(name))
