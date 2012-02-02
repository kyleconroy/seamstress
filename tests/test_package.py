from seamstress.core import package
from nose.tools import assert_in
from fabric.api import *

# Package
def test_install_nginx():
    package("nginx")
    assert_in("0.7.65", sudo("nginx -v"))


