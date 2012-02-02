from seamstress.ruby import gem 
from nose.tools import assert_equals
from tail import assert_abort
from fabric.api import *

# Gem
@assert_abort
def test_gem_install_nonexistent_package():
    gem("fooofoofoofooofoofoo")

def test_gem_version():
    gem("nokogiri", version="1.4.5")
    assert_equals(sudo('gem list -i nokogiri -v 1.4.5'), "true")

def test_gem():
    gem("nokogiri")
    assert_equals(sudo('gem list -i nokogiri'), "true")

def test_gem_remove():
    gem("nokogiri", state="uninstalled")
    with settings(warn_only=True):
        assert_equals(sudo('gem list -i nokogiri'), "false")


