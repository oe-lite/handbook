.. // This is part of the OE-lite Developers Handbook
.. // Copyright (C) 2016
.. //   Rasmus Villemoes <ravi@prevas.dk>

*******************
Examples of recipes
*******************

Trigonometric utilities
=======================

Instead of showing a small *working* recipe, we'll start small and
show what fails at each step and explain how to fix it.

Suppose we wish to have utilities ``sin``, ``cos`` and ``tan`` that
will compute these trigonometric functions. To keep the number of
files small, we just use a single source file and some preprocessor
magic. So we create this directory tree::

  recipes/trig/
              ├── files
              │   └── trig.c
              └── trig_0.1.oe

  
The file ``trig.c`` is simply:
  
.. literalinclude:: examples/trig/trig.c
   :language: c
   :caption: recipes/trig/files/trig.c
	      
Our first attempt at describing how to build this to OE-lite is this:

.. literalinclude:: examples/trig/trig_0.1.oe
   :language: oe
   :caption: recipes/trig/trig_0.1.oe

The ``DESCRIPTION`` and ``LICENSE`` variables are self-explanatory -
neither are mandatory, but both are highly recommended. When possible,
it is recommended to use `SPDX identifiers
<https://spdx.org/licenses/>`_ in the ``LICENSE`` fields.

The ``RECIPE_TYPES`` variable should be a space-separated list of the
targets this recipe is applicable to. The default is ``machine``, but
since there's nothing machine-specific about this small utility, we
also include the ``native`` target. That allows us to say ``oe bake
native:trig`` to have OE-lite build the recipe for our host machine,
in turn allowing us to test the programs without transferring to the
target.

The ``inherit c`` is an example of the use of a `class <OE-lite
class>`. Even the simplest recipes will usually inherit a few
classes. The ``c`` class ensures that a suitable (cross-)compiler gets
`staged <staging>` and that variables such as ``CC`` get appropriate
values. This would be very tedious to set up manually, especially if
one wants the same recipe to work for multiple target architectures.

Next, we need to tell OE-lite the source files needed. In our case,
there is just one. Local files (as indicated by the ``file://``
prefix) are searched for in a number of subdirectories of the
directory containing the recipe file: First, ``${PN}-${PV}``, then
``${PN}`` and finally ``files``. This scheme allows sharing (and
non-sharing) files between different recipes and versions of the same
recipe. In our case, that's not important, so we just put the file in
the ``files`` subdirectory.

Finally, we need to tell OE-lite how to actually compile our
programs. We do this by defining a shell function called
``do_compile``. In a larger project, we would most likely have created
a Makefile or used autotools, but here a simple shell loop is
sufficient.

Let's try this:

.. code-block:: console

   $ oe bake trig -y
   machine:trig_0.1:do_stage started
   machine:trig_0.1:do_stage finished - 0.521 s
   machine:trig_0.1:do_fstage started
   machine:trig_0.1:do_fstage finished - 0.001 s
   machine:trig_0.1:do_fetch started
   machine:trig_0.1:do_fetch finished - 0.000 s
   machine:trig_0.1:do_unpack started
   machine:trig_0.1:do_unpack finished - 0.001 s
   machine:trig_0.1:do_patch started
   machine:trig_0.1:do_patch finished - 0.001 s
   machine:trig_0.1:do_configure started
   machine:trig_0.1:do_configure finished - 0.078 s
   machine:trig_0.1:do_compile started
   waiting for machine:trig_0.1:do_compile (started 0.020 seconds ago) to finish
   ERROR: machine:trig_0.1:do_compile failed - 0.023 s
   Build: 0.674 seconds
   
   ERROR: machine:trig_0.1:do_compile failed  /mnt/xfs/devel/oe-lite/tmp/work/machine/arm-926ejs-linux-gnueabi/trig-0.1/tmp/do_compile.20161102082713.log
   > LC_ALL=C /mnt/xfs/devel/oe-lite/tmp/work/machine/arm-926ejs-linux-gnueabi/trig-0.1/tmp/do_compile.20161102082713.run
   + cd /mnt/xfs/devel/oe-lite/tmp/work/machine/arm-926ejs-linux-gnueabi/trig-0.1/src/trig-0.1
   + do_compile
   + for f in sin cos tan
   + arm-926ejs-linux-gnueabi-gcc -o sin -DFUNC=sin -O2 trig.c
   arm-926ejs-linux-gnueabi-gcc: error: trig.c: No such file or directory
   arm-926ejs-linux-gnueabi-gcc: fatal error: no input files
   compilation terminated.
   Error: Command failed: 'LC_ALL=C /mnt/xfs/devel/oe-lite/tmp/work/machine/arm-926ejs-linux-gnueabi/trig-0.1/tmp/do_compile.20161102082713.run': 1
   
   CRITICAL: bake failed: error: 1

It can sometimes be difficult to see what the problem actually
is. Here the compiler complains that ``trig.c`` cannot be found - yet
we clearly listed that as a source file. We can also see that the
do_unpack task succeeded, so it *should* be there. The problem is,
what does *there* mean? Let's inspect the workdir:

.. code-block:: console

  $ tree -F -L 3 tmp/work/machine/arm-926ejs-linux-gnueabi/trig-0.1/
  tmp/work/machine/arm-926ejs-linux-gnueabi/trig-0.1/
  ├── fstage/
  ├── src/
  │   ├── patches/
  │   │   └── quiltrc
  │   ├── trig-0.1/
  │   └── trig.c
  ├── stage/
  │   ├── cross/
  │   │   ├── arm-926ejs-linux-gnueabi/
  │   │   ├── bin/
  │   │   ├── lib/
  │   │   ├── libexec/
  │   │   ├── OE-lite/
  │   │   └── x86_64-build_unknown-linux-gnu/
  │   ├── machine/
  │   │   ├── lib/
  │   │   ├── OE-lite/
  │   │   └── usr/
  │   └── native/
  │       ├── include/
  │       ├── lib/
  │       └── OE-lite/
  └── tmp/
      ├── do_compile.20161102082713.log
      ├── do_compile.20161102082713.run*
      ├── do_compile.log -> do_compile.20161102082713.log
      ├── do_compile.run -> do_compile.20161102082713.run*
      ├── do_stage.20161102082713.log
      ├── do_stage.log -> do_stage.20161102082713.log
      ├── do_unpack.20161102082713.log
      └── do_unpack.log -> do_unpack.20161102082713.log
  
  21 directories, 10 files

Here we see the problem: do_compile was run in the
``${WORKDIR}/src/trig-0.1/`` directory (aka ``${S}`` – see also the
section `task-directories`), but ``trig.c`` has been put in
``${WORKDIR}/src`` (aka ``${SRCDIR}``). The simplest fix is to make
``S`` and ``SRCDIR`` the same. So we change our recipe like this:

.. literalinclude:: examples/trig/2.diff
   :language: diff

With this in place, let's try again.

.. code-block:: console
   
   oe bake trig -y
   ...
   + cd /mnt/xfs/devel/oe-lite/tmp/work/machine/arm-926ejs-linux-gnueabi/trig-0.1/src
   + do_compile
   + for f in sin cos tan
   + arm-926ejs-linux-gnueabi-gcc -o sin -DFUNC=sin -O2 trig.c
   /tmp/ccrw5e1U.o: In function `main':
   trig.c:(.text.startup+0x2c): undefined reference to `sin'
   collect2: error: ld returned 1 exit status
   Error: Command failed: 'LC_ALL=C /mnt/xfs/devel/oe-lite/tmp/work/machine/arm-926ejs-linux-gnueabi/trig-0.1/tmp/do_compile.20161102091655.run': 1
   
   CRITICAL: bake failed: error: 1

Right, we didn't provide the ``-lm`` linker flag. OK, that's easy to fix.

.. literalinclude:: examples/trig/3.diff
   :language: diff

Once more. What can possibly go wrong now?

.. code-block:: console
   
   $ oe bake trig -y
   ...
   ERROR: machine:trig_0.1:do_compile failed  /mnt/xfs/devel/oe-lite/tmp/work/machine/arm-926ejs-linux-gnueabi/trig-0.1/tmp/do_compile.20161102092251.log
   > LC_ALL=C /mnt/xfs/devel/oe-lite/tmp/work/machine/arm-926ejs-linux-gnueabi/trig-0.1/tmp/do_compile.20161102092251.run
   + cd /mnt/xfs/devel/oe-lite/tmp/work/machine/arm-926ejs-linux-gnueabi/trig-0.1/src
   + do_compile
   + for f in sin cos tan
   + arm-926ejs-linux-gnueabi-gcc -o sin -DFUNC=sin -O2 trig.c -lm
   /mnt/xfs/devel/oe-lite/tmp/work/machine/arm-926ejs-linux-gnueabi/trig-0.1/stage/cross/bin/../lib/gcc/arm-926ejs-linux-gnueabi/5.4.0/../../../../arm-926ejs-linux-gnueabi/bin/ld: cannot find -lm
   collect2: error: ld returned 1 exit status
   Error: Command failed: 'LC_ALL=C /mnt/xfs/devel/oe-lite/tmp/work/machine/arm-926ejs-linux-gnueabi/trig-0.1/tmp/do_compile.20161102092251.run': 1
   
   CRITICAL: bake failed: error: 1

That this fails is actually a good thing, because it shows that
OE-lite works as expected! We've told the linker to link with
libm. But we haven't told OE-lite that that library is needed, so it
hasn't been `staged <staging>`. Telling OE-lite about build-time
dependencies is precisely what the ``DEPENDS`` variable is for. By
inheriting the ``c`` class, we've already told OE-lite that we depend
on the standard C library (and its header files), but libm is a
separate library. Now what we understand the problem, the fix is easy:

.. literalinclude:: examples/trig/4.diff
   :language: diff

The other variables we've added describes a *runtime
dependency*. Without that, the utilities would build just fine, but if
some image recipe then included the ``trig`` package, nothing has
informed OE-lite that it must also include ``libm.so`` in the
resulting image. So the binaries would be present but unrunnable. (Of
course, in a realistic full BSP, *some* recipe is bound to ensure that
libm gets included, but that's not necessarily the case for other
libraries, so it's better to always explicitly describe the exact
dependencies.)

Aside: dependency types
-----------------------

So why did we spell the runtime dependency ``RDEPENDS_${PN}`` and not
just ``RDEPENDS``? There are actually two kinds of build-time as well
as two types of run-time dependencies, *recipe dependencies* and
*package dependencies*. Recipe dependencies (given in the unsuffixed
``DEPENDS``, ``RDEPENDS`` variables) describe what is required to
build the recipe. Package dependencies, given in ``DEPENDS_<package
name>``, ``RDEPENDS_<package name``, describe what is needed to use
the contents of the package at build-time respectively run-time. Since
our utilities end up in the package by the same name as the recipe, we
tell OE-lite that anything that run-time depends on the ``trig``
*package* should also pull in libm.

An example where package build-time dependencies would come into play
is if we have two libraries, libfoo and libbar and a utility frob,
with libfoo depending on libbar and frob depending on libbar. In the
frob recipe, we would then have something like::

  DEPENDS += "libbar"
  RDEPENDS_${PN} += "libbar"

The frob utility probably does a ``#include <bar.h>`` somewhere, but
``bar.h`` contains a ``#include <foo.h>``. That libbar depends on
libfoo is an implementation detail of libbar, which frob doesn't care
about (and it may change with a different version of libbar), but in
this case we obviously need to ensure that ``foo.h`` gets staged when
building frob. The solution to this is to ensure that the package
providing libbar has a build-time dependency on libfoo. So the libbar
recipe might contain ::

  DEPENDS += "libfoo"
  DEPENDS_${PN} += "libfoo-dev"
  RDEPENDS_${PN} += "libfoo"

which says that (1) libfoo is necessary to build libbar, (2) to build
anything against libbar, you also need the libfoo-dev package, (3) if
you run-time depend on libbar, you also run-time depend on libfoo.
  
The alert reader may wonder how a *run-time dependency* for *building*
a recipe makes any sense. And in truth, most normal recipes do not
have those – a bare ``RDEPENDS`` in a recipe is usually an
error. However, there is one type of recipes which do have
``RDEPENDS``: Those that inherit image.oeclass, and hence describe a
complete file system image. While normal recipes have a do_stage task,
which pulls in all packages mentioned in the recipe's ``DEPENDS``
variable as well as their package dependencies (recursively), image
recipes have an do_rstage task which pulls in all the packages in the
recipe's ``RDEPENDS`` variable as well as their package rdependencies
(recursively). It is admittedly a stretch to call this run-time build
dependencies, but as the preceding sentence hopefully demonstrates,
this makes the handling of the two staging tasks nicely symmetric.

Back to the example
-------------------

While we can now succesfully build the trig utilities, the recipe is
not quite complete. Looking at the directory ``${WORKDIR}/packages``,
we see that all the packages are empty apart from some auto-generated
metadata. The problem is that we haven't described how to install the
utilities. Most »real« recipes get built using a Makefile (which may
be generated by autotools or whatnot), in which case there is usually
also an ``install`` target, and if we had inherited the ``make``
class, OE-lite would by default simply do ``make install``. We,
however, have to describe the install step manually, just as we
defined the do_compile function. So here goes


.. literalinclude:: examples/trig/5.diff
   :language: diff

If we then run ``oe bake trig -y`` and look at the directory ``${D}``
(aka ``${WORKDIR}/install``), we see that the three utilities are
there. Moreover, the do_install task by default strips debug symbols
and puts them in the ``.debug`` subdirectory:

.. code-block:: console

   $ tree -a -F tmp/work/machine/arm-926ejs-linux-gnueabi/trig-0.1/install/
   tmp/work/machine/arm-926ejs-linux-gnueabi/trig-0.1/install/
   └── usr/
       └── bin/
           ├── cos*
           ├── .debug/
           │   ├── cos*
           │   ├── sin*
           │   └── tan*
           ├── sin*
           └── tan*
   
   3 directories, 6 files

The next task is do_split, which takes the contents of the ``${D}``
directory and distributes the files in subdirectories of
``${WORKDIR}/packages`` according to the ``FILES_*`` variables. These
have reasonable default values, so we get this structure:

.. code-block:: console

   $ tree -a -F tmp/work/machine/arm-926ejs-linux-gnueabi/trig-0.1/packages/
   tmp/work/machine/arm-926ejs-linux-gnueabi/trig-0.1/packages/
   ├── trig/
   │   └── usr/
   │       └── bin/
   │           ├── cos*
   │           ├── sin*
   │           └── tan*
   ├── trig-dbg/
   │   └── usr/
   │       └── bin/
   │           └── .debug/
   │               ├── cos*
   │               ├── sin*
   │               └── tan*
   ├── trig-dev/
   ├── trig-doc/
   └── trig-locale/
   
   10 directories, 6 files

This allows one to RDEPEND on ``trig``, but if one also wants the
debug symbols, one should also add a run-time dependency on
``trig-dbg``. The final task is do_package, which adds an OE-lite
directory containing a little metadata (using the LICENSE and
DESCRIPTION variables), and then creates a tarball which is placed in
a subdirectory of ``tmp/packages``:


.. code-block:: console

   $ ls -F tmp/packages/machine/arm-926ejs-linux-gnueabi/trig*
   tmp/packages/machine/arm-926ejs-linux-gnueabi/trig_0.1_f7b2f5ade7888f1426ecbe773d909f0f.tar
   tmp/packages/machine/arm-926ejs-linux-gnueabi/trig_0.1.tar@
   tmp/packages/machine/arm-926ejs-linux-gnueabi/trig-dbg_0.1_f7b2f5ade7888f1426ecbe773d909f0f.tar
   tmp/packages/machine/arm-926ejs-linux-gnueabi/trig-dbg_0.1.tar@
   tmp/packages/machine/arm-926ejs-linux-gnueabi/trig-dev_0.1_f7b2f5ade7888f1426ecbe773d909f0f.tar
   tmp/packages/machine/arm-926ejs-linux-gnueabi/trig-dev_0.1.tar@
   tmp/packages/machine/arm-926ejs-linux-gnueabi/trig-doc_0.1_f7b2f5ade7888f1426ecbe773d909f0f.tar
   tmp/packages/machine/arm-926ejs-linux-gnueabi/trig-doc_0.1.tar@
   tmp/packages/machine/arm-926ejs-linux-gnueabi/trig-locale_0.1_f7b2f5ade7888f1426ecbe773d909f0f.tar
   tmp/packages/machine/arm-926ejs-linux-gnueabi/trig-locale_0.1.tar@

The long hex string is the metadata hash of the do_package task.

By now, we have a working recipe, and we can include the utilities on
our target by simply saying ::

  RDEPENDS += "trig"

in our root filesystem recipe. However, there are some things one
might want to improve.

- In a space-constrained root filesystem, it might be nice to be able
  to depend on the utilities individually, so that one doesn't have to
  include ``tan`` if one only needs ``cos``.

- One would not normally have the complete source code in the recipe
  directory, but instead have the SRC_URI point at a git repository or
  tar-ball containing it.

Instead of showing how to achieve this, we'll turn our attention to an
example from »real life«.
  
Dissection of an existing recipe
================================

