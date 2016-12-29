.. // This is part of the OE-lite Developers Handbook
.. // Copyright (C) 2013
.. //   Esben Haabendal <esben@haabendal.dk>

*************
Project Setup
*************

This chapter describes how to setup a new OE-lite project, ie. the
creation of a new :term:`OE-lite manifest` and setup of an
:term:`OE-lite repository` for it.

From Scratch
============

To create a new :term:`OE-lite manifest` from scratch, all you need to do is:

1. Create an empty directory.

2. Create a conf/bakery.conf file.

3. Run ``oe init``.

4. Convert :term:`layers <OE-lite layer>` to be of internal layer type.

Bakery.conf from scratch
------------------------

The bakery.conf follows the OE-lite metadata syntax, or rather a subset
of it. The primary purpose is to assign a value to the variable called
``OESTACK``, which defines the :term:`OE-lite stack`
.

An OE-lite stack is composed of a number of OE-lite layers, with each
layer typically being a seperate git repository.

A small OE-lite stack could look like this::

    # OE-lite/base
    OESTACK += "meta/base"
    OESTACK .= ";srcuri=git://oe-lite.org/oe-lite/base.git"
    OESTACK .= ";branch=master"

    # OE-lite/core
    OESTACK += "meta/core"
    OESTACK .= ";srcuri=git://oe-lite.org/oe-lite/core.git"
    OESTACK .= ";branch=master"

    OESTACK += "lib/fetching/fetching"
    OESTACK .= ";srcuri=git://oe-lite.org/python-fetching.git"
    OESTACK .= ";pythonpath=.."

    OESTACK += "lib/GitPython"
    OESTACK .= ";srcuri=git://oe-lite.org/gitpython/GitPython.git"
    OESTACK .= ";pythonpath="

    OESTACK += "lib/urlgrabber"
    OESTACK .= ";srcuri=git://oe-lite.org/urlgrabber.git"
    OESTACK .= ";pythonpath="

The example above uses the two OE-lite append assignment operators "+="
and ".=". The "+=" operator appends the a space and the value to the
variable. The ".=" just appends the value to the variable.

The resulting ``OESTACK`` variable is thus a space separated list of
layers. Each layer is specified by a path and a number of parameters,
separated by ";".

    **Note**

    Add reference to the OE-lite Bakery Manual for full documentation on
    the bakery.conf syntax here, when it is actually written…

After the ``oe init`` command is done, the my-bsp directory should be
populated with the following structure::

    ├── conf
    │   └── bakery.conf
    ├── lib
    │   ├── fetching
    │   ├── GitPython
    │   └── urlgrabber
    └── meta
        ├── base
        └── core

and all the layers should be cloned from their upstream origin.

Example (for the copy-and-paste hungry):

.. code:: sh

    mkdir my-bsp
    cd my-bsp
    mkdir conf
    emacs conf/bakery.conf
    oe init

At this point, you should create the initial git commit of your brand
new OE-lite manifest:

.. code:: sh

    git add conf/bakery.conf
    git commit -s -m "Initial commit"

You are now (almost) ready to build something. To try this, see
chapter `building` for how to build.

Of-course, you might want to add some more metadata layers, and probably
add your own machine and/or distro configurations and even some custom
recipes, fx. a recipe for building a custom rootfs image. But that is a
different story…

External Layers
---------------

Let’s say you are creating an OE-lite manifest for your embedded Linux
BSP project. You of-course need to use OE-lite/core, and the simplest
solution is to just add it to the STACK by adding the following to
bakery.conf::

    OESTACK += "meta/core"
    OESTACK .= ";srcuri=git://oe-lite.org/oe-lite/core.git"

With this, users of your manifest will get an OE-lite/core layer at
meta/core, using a clone from the git://oe-lite.org/oe-lite/core.git
repository.

While this is definitely a lean and simple approach, it does come with a
few drawbacks.

1. You will not be able to create any commits, tags or branches to the
   OE-lite/core layer.

2. When cloning the OE-lite repository, you depend on both the server
   hosting the manifest repository and the oe-lite.org server.

See also appendix `terminology` for definition of internal layer.

Internal Layers
---------------

For each layer you have added to the OE-lite stack as an external
layer, you should consider to convert it to be an internal layer to
address the problems with external layers described above. See
appendix `terminology` for definition of internal layer.

By converting all external layers to internal layers, and thus having a
manifest consisting of only embedded and internal layers, you will have
a number of advantages:

1. When creating a clone of the OE-lite repository, you will only have
   to fetch from your project OE-lite repository.

2. You will be able to create backup/redundant copies of your entire
   OE-lite repository using a single command.

3. You will be able to switch back and forth between different copies of
   your OE-lite repository without making any changes to the OE-lite
   manifest.

4. You will be able to make complete from local clones of your OE-lite
   repository, without depending on any remote repositories.

For each layer you want to convert from external layer to internal
layer, you have to do the following:

1. Remove the ``srcuri`` parameter for the layer in conf/bakery.conf

2. Change the url entry of the layer submodule in .gitmodules to the
   path relative to the containing git super project. Fx. the relative
   path of meta/core contained in the manifest repository is
   ./meta/core, and the relative path of lib/GitPython/git/ext/async
   contained in the lib/GitPython submodule is ./git/ext/async .

When done, run ``oe update`` and commit the changes in conf/bakery.conf
and .gitmodules files.

From Template
=============

TBD…

Repository Setup
================

This section describes how to setup an OE-lite repository, suitable for
hosting as a remote repository. Details on how to setup hosting is out
of scope of this section.

To setup an OE-lite repository of an existing OE-lite manifest, all you
need to do is to call::

    oe clone --bare <url> <path>

..

    **Note**

    OE-lite Bakery version 4.1 or newer is required for this.

This will create a new (bare) OE-lite repository clone of <url> at the
local directory <path>. The ``<url>`` argument can be any valid git URL
(see link:See git[git clone documentation] for more on this). This even
includes a local path to an OE-lite manifest repository, which is handy
for setting up the first OE-lite repository right after creation of a
new OE-lite manifest.

All internal layers will be cloned (recursively) together with the
manifest repository. Any other git submodules (ie. git submodules with
absolute url’s or relative paths different from the path relative to the
git super project) will not be cloned.
