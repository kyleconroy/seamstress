from fabric.api import *
from nose.tools import assert_in
from seamstress.core import document
from seamstress import python

def test_requirements_file():
    document("requirements.txt", source="tests/files/requirements.txt")
    with python.virtualenv("_env"):
        python.packages("requirements.txt")
        for line in open("tests/files/requirements.txt"):
            assert_in(line.strip(), run("pip freeze"))


def test_virtualenv():
    python.virtualenv("_env")
    run("test -d _env")
    run("test -f _env/bin/activate")


def test_virtualenv_python():
    with python.virtualenv("_env"):
        assert_in("2.7", run("python --version"))


