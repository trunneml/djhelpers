import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "djhelpers",
    version = "0.0.1",
    author = "Michael Trunner",
    author_email = "michael@trunner.de",
    description = ("Some useful helpers for the django web framework"),
    license = "Apache License 2.0",
    keywords = "django helpers",
    url = "https://github.com/trunneml/djhelpers",
    packages=find_packages(exclude=['tests']),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Framework :: Django",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: Apache Software License",
    ],
)
