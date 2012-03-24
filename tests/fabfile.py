import random
from fabric.api import *
from fabric import colors
#from tests.test_ruby import *
from tests.test_package import *
from tests.test_remote_file import *
from tests.test_user import *
from tests.test_directory import *
from tests.test_document import *
from tests.test_core import *
from tests.test_link import *


def functional():
    tests = [f for f in globals().iteritems() if f[0].startswith("test")]
    random.shuffle(tests)
    total = 0
    failed = 0
    success = 0

    for (name, thing) in tests: 

   
        with settings(hide("status", "running", "warnings",
                           "aborts", "stdout", "stderr")):
            try:
                total += 1
                execute(thing)
                puts(colors.green(name))
                success += 1
            except Exception as e:
                puts(colors.red(name))
                failed += 1
            except SystemExit as e:
                puts(colors.red(name))
                failed += 1

    puts(colors.yellow("Ran {} tests".format(total)))

    if failed:
        puts(colors.yellow("FAILED: (failures={})".format(failed)))
    else:
        puts(colors.yellow("SUCCESS"))


