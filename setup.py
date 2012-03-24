from seamstress import __version__
from setuptools import setup, find_packages

setup(
    name = "seamstress",
    version = __version__,
    description = "Simple configuration management built on Fabric",
    author = "Kyle Conroy",
    author_email = "kyle@twilio.com",
    url = "http://github.com/derferman/seamstress",
    keywords = ["configuration management"],
    install_requires = ["fabric == 1.4"],
    packages = find_packages(),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        ],
    )
