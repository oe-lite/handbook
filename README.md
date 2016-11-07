# OE-lite handbook

This is the user's guide to the OE-lite build system. The most recent
official version can be read at
[readthedocs.io](http://oe-lite-handbook.readthedocs.io/en/master/).

## Building locally

It is also possible to clone this repository and build the
documentation locally. This requires the Python package Sphinx. On
Debian/Ubuntu system, this can be installed by running

```sh
$ sudo apt-get install make python-sphinx sphinx-rtd-theme-common
$ sudo apt-get install python-pip
$ sudo pip install sphinxcontrib-domaintools
```

You may then build the html version by running

```sh
$ make html
```

The output can be found in the `build/html` directory. Open the
`build/html/index.html` file.

## Using docker

If you are not running Debian/Ubuntu or cannot install the above
packages, you may instead create a docker image from the
[Dockerfile](https://github.com/oe-lite/docker/tree/master/handbook/ubuntu-16.04/Dockerfile)
found in the [OE-lite docker](https://github.com/oe-lite/docker) git
repository.

