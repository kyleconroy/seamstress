from seamstress import core

def installation():
    core.package_repository("ppa:chris-lea/node.js")
    core.package("nodejs")
