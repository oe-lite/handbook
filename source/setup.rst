.. // This is part of the OE-lite Developers Handbook
.. // Copyright (C) 2013
.. //   Esben Haabendal <esben@haabendal.dk>

**********
Host Setup
**********

This chapter describes how to setup a host machine (your development PC,
server or whatever) for working with OE-lite development.

Requirements
============

The only officially supported host OS is Linux, but at least one
developer is also using Mac OS X with some luck.

Install Bakery
==============

To do any kind of OE-lite development, you need to have the OE-lite
Bakery tool installed. OE-lite Bakery depends on Python (2.6 or 2.7) and
git.

There are several ways of installing OE-lite Bakery on your host
machine.

1. Install from source.

2. Run from source.

3. Install from Ubuntu PPA (Ubuntu based distributions only).

4. Install on Exherbo Linux.

If installing or running from source, you need to install additional
required host software tools manually. If installing from a host OS
package, the package should pull in the required software automatically.

Install Additional Tools
------------------------

In order to run OE-lite Bakery, you need a few additional software
packages which you might not have installed. This is currently limited
to Git and PLY.

Git
~~~

OE-lite Bakery uses the git command when fetching OE-lite manifests.

The easiest way is most likely to simply install the git command
provided by your host OS.

**Debian GNU/Linux, Ubuntu Linux, …**

.. code:: sh

    sudo apt-get install -y git

PLY (Python Lex-Yacc)
~~~~~~~~~~~~~~~~~~~~~

OE-lite Bakery uses PLY for parsing configuration files.

The easiest way is most likely to simply install the PLY version
provided by your host OS.

**Debian GNU/Linux, Ubuntu Linux, …**

.. code:: sh

    sudo apt-get install -y python-ply

Install from source
-------------------

To install OE-lite Bakery, you need to have Python setuptools installed.

To install Python setuptools on Debian GNU/Linux, Ubuntu Linux and so
on, use

.. code:: sh

    sudo apt-get install -y python-setuptools

After that, you should be able to install it with the following command:

.. code:: sh

    wget -qO- http://oe-lite.org/download/bakery/oe-lite-bakery-4.0.2.tar.gz \
            | tar -xz \
            && sudo oe-lite-bakery-4.0.2/setup.py install

Run from source
---------------

OE-lite Bakery also supports running directly from source distribution.

Download and extract the latest release from
http://oe-lite.org/download/bakery/

.. code:: sh

    wget -qO- http://oe-lite.org/download/bakery/oe-lite-bakery-4.0.2.tar.gz \
            | tar -xz

or clone the bakery repository with

.. code:: sh

    git clone git://oe-lite.org/oe-lite/bakery.git

You can use the oebakery/oe.py script directly, but you should probably
symlink it to "oe" somewhere in your $PATH or setup a shell alias so you
can just type "oe" when using bakery.

Something like

.. code:: sh

    ln -s ../src/bakery/oebakery/oe.py $HOME/bin/oe 

(assuming you have the bakery source distribution in $HOME/src/bakery
and have $HOME/bin in your $PATH)

Install from Ubuntu PPA
-----------------------

This method is only for use on Ubuntu Linux or distributions compatible
with Ubuntu Linux (like Mint).

To install bakery from the PPA, you can use the following commands:

.. code:: sh

    sudo apt-get install -y python-software-properties
    sudo add-apt-repository ppa:esben-haabendal/oe-lite
    sudo apt-get update
    sudo apt-get install -y oe-lite

Install on Exherbo Linux
------------------------

Since Exherbo is a source based distribution, most dependencies are
installed already. The rest is pulled in by the oe-bakery package.

.. code:: sh

    sudo cave resolve oe-bakery

Install Manifest Dependencies
=============================

Depending on the :term:`OE-lite manifest(s) <OE-lite manifest>` you
will be working with, and what you will build with it, you will
require some additional host tools. If you installed bakery from PPA,
you most likely already have all you need, and you can skip this
section.

If you installed bakery in another way, you might want to install some
additional development tools.

Installing additional development tools in Fedora 16 (and possibly other
RPM based distributions):

.. code:: sh

    sudo yum install python-magic python-ply python-pycurl \
    python-sqlite2 python-devel fakeroot libstdc++-static glibc-static \
    gettext-devel ncurses-devel libtool texinfo flex bison coreutils \
    sed git-core cvs subversion mercurial quilt gawk texinfo automake \
    autoconf curl texi2html openjade groff make gcc-c++ gcc binutils bc \
    unzip lzma gtk-doc docbook-utils xml2 xmlto help2man glib2-devel gperf

Install additional development tools in Debian GNU/Linux, Ubuntu Linux
and so on, something like:

.. code:: sh

    sudo apt-get install python python-support python-magic python-ply \
    python-pycurl python-pysqlite2 python-pkg-resources python-dev \
    coreutils sed git-core cvs subversion mercurial quilt gawk texinfo \
    automake autoconf autopoint libtool curl texi2html diffstat \
    openjade groff mtd-utils build-essential make gcc g++ binutils \
    bison flex bc ncurses-dev unzip lzma gtk-doc-tools docbook-utils \
    libxml2-utils xmlto help2man libglib2.0-dev lzop gperf python-svn

Install additional development tools in RHEL 6.2, something like:

.. code:: sh

    sudo yum install python-magic python-ply python-pycurl python-devel \
    fakeroot gettext-devel ncurses-devel libtool texinfo flex bison \
    coreutils sed git-core cvs subversion mercurial quilt gawk texinfo \
    automake autoconf curl openjade groff make gcc-c++ gcc binutils bc \
    unzip gtk-doc docbook-utils xmlto glib2-devel intltool glibc-static \
    gperf

Goodbye dash
============

On some systems (fx. Ubuntu Linux), ``/bin/sh`` is a symlink to dash,
which not all software packages are fully compatible with. To work with
OE-lite, you therefore have to make sure that ``/bin/sh`` is actually
``/bin/bash``.

You can do this the brute force way

.. code:: sh

    sudo ln -sf bash /bin/sh

Or on Ubuntu Linux, you can do this more nicely with

.. code:: sh

    sudo dpkg-reconfigure dash

and answer "No" to the "Use dash as the default system shell (/bin/sh)?"
question.
