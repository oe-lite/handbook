.. // This is part of the OE-lite Developers Handbook
.. // Copyright (C) 2013
.. //   Esben Haabendal <esben@haabendal.dk>

********
Building
********

This chapter describes how to build something with OE-lite, fx. how to
build a specific OE-lite recipe, a Linux kernel image, a JFFS2 root
filesystem image, an SDK toolchain image, and so on.

Building is done with the OE-lite Bakery sub-command called "bake".

Before building you need to setup the build configuration in the file
``conf/local.conf``.

A very minimal example configuration purely to test that building
works::

    DISTRO = "base"
    MACHINE_CPU = "arm-926ejs"
    PROVIDED = "all"
    SDK_CPU = "i686"
    SDK_OS = "linux-gnu"
    RMWORK = "0"

The ``DISTRO`` variable selects the :term:`OE-lite distribution`. Here
we choose a simple distribution called base to be able to build
something. Next we set the cpu we want to cross compile for using
``MACHINE_CPU``. It is also possible to set ``MACHINE`` to target a
specific board e.g. pandaboard or rpi (raspberry-pi).

    **Note**

    To set ``MACHINE="rpi"`` you will need the raspberry-pi manifest
    from git.oe-lite.org.

The ``PROVIDED`` variable is used to inform the bake command what
dependencies can be assumed to be provided on the host system. See
``conf/provided/all.conf`` in the core metadata layer. The ``SDK``
variables are used to specify what architecture the :term:`OE-lite
SDK` should be build for. ``RMWORK`` currently need to be set to 0
since automatic removal of temporary build files is not
implemented. Optionally you may want to set ``PARALLEL_MAKE = "-j X"``
where X is the number of CPUs available on your host system + 1, to
speed up the build.

Now it is possible to choose something to build with the bake command.
In OE-lite all :term:`recipes <OE-lite recipe>` can be build. A recipe
is a file with the ``.oe`` file extension, take a look at what recipes
you have in your current manifest using::

    find . -name '*.oe'

The primary goal of the building process in OE-lite is to produce
deployable images, so for this example we will build an image. In the
base metadata layer a rootfs image recipe is located in:
``recipes/images`` which we can try building::

    oe bake base-rootfs

``oe`` will resolve the list of dependencies, present you with a list of
what needs to be built and ask for confirmation before continuing. The
build process takes a while, but in the end you should see that
base-rootfs was build and the elapsed build time. The deployable images
are now located in ``tmp/images``
