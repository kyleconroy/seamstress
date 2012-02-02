import random
from fabric.api import *
from fabric.colors import magenta
from tests.test_ruby import *
from tests.test_package import *
from tests.test_remote_file import *
from tests.test_user import *
from tests.test_directory import *
from tests.test_document import *


def functional():
    tests = [f for f in globals().iteritems() if f[0].startswith("test")]
    random.shuffle(tests)

    for (name, thing) in tests: 
        puts(magenta(name))
        with settings(warn_only=True):
            thing()

