.. // This is part of the OE-lite Developers Handbook
.. // Copyright (C) 2016
.. //   Rasmus Villemoes <ravi@prevas.dk>

*****
Tasks
*****

OE-lite divides the job of building software into a number of
(interdependent) tasks, each with a well-defined purpose. For example,
one task is responsible for fetching the source code, another for
unpacking it, a third for applying local patches, a fourth for doing
the actual compilation, and so on and so forth.

Most recipes end up being split into about 13 tasks. The section
`task_types` below briefly explains the purpose of the various tasks.

Environment
===========

The filename of a recipe implicitly defines two variables, ``PN`` and
``PV``, which are used in the definition of lots of other
variables. ``PN`` is the name of the recipe, while ``PV`` is the
version. For a recipe file called ``openssh_7.1p2.oe``, these would be
``openssh`` and ``7.1p2``, respectively. Moreover, ``P`` is a
shorthand for ``${PN}-${PV}``. These should never be changed from
within a recipe.

.. _task-directories:

Directories
-----------

The directory containing the `OE-lite manifest` is available as the
variable ``TOPDIR``. Two other standard variables are defined in terms
of this, ``INGREDIENTS`` (``${TOPDIR}/ingredients``) and ``TMPDIR``
(``${TOPDIR}/tmp``).

Every recipe gets built in a dedicated subdirectory of
``${TMPDIR}/work``, named according to the recipe's type, the target
architecture and the recipe version. Examples are
``${TMPDIR}/work/machine/arm-cortexa9neon-linux-gnueabi/openssh-7.1p2``
and
``${TMPDIR}/work/native/x86_64-build_unknown-linux-gnu/gmp-6.0.0a``. This
is the contents of the ``${WORKDIR}`` variable.

There are a number of other standard variables defined in terms of
``WORKDIR``, ``PN`` and ``PV`` which one should know about.

- SRCDIR ``${WORKDIR}/src``
- S ``${SRCDIR}/${P}``
- B ``${S}``
- D ``${WORKDIR}/install``
- T ``${WORKDIR}/tmp``
- PKGD ``${WORKDIR}/packages``

Their default values are shown above, but that may be overridden by
classes or the recipe itself. We give a few examples of when this
might be necessary in the task descriptions below.


Logging
-------

The output from each task gets written to a log file in
``${WORKDIR}/tmp``. The files are called
``<taskname>.<datetime>.log``, e.g. ``do_compile.20161013074154.log``,
and there is a symbolic link ``<taskname>.log`` pointing to the most
recent log file.

Empty log files get deleted automatically.

Scripts
-------

Some tasks are implemented as bash functions. OE-lite runs these by
writing a complete bash script to ``${WORKDIR}/tmp`` called
``<taskname>.<datetime>.run`` (again, with ``<taskname>.run`` being a
symlink to the most recent) containing all the necessary environment
settings, function definitions etc., then executes it, with stdout and
stderr redirected to the ``.log`` file.

These scripts can also be run manually, which can be very useful as a
debugging tool.


.. _task_metadata:

Metadata
========

A task is completely controlled by its associated *metadata*, which is
essentially a set of key-value pairs. This metadata is copied from the
metadata for the parent recipe, filtering away variables which are not
relevant to the specific task.

Metadata hashing
----------------

In order to know whether a task needs to be redone and to facilitate
use of `prebakes <prebake>`, OE-lite assigns a hash value to every
task. This hash value is computed from two sources: The hash values of
all tasks which this task depends on, and the set of key-value pairs
constituting the task's metadata. The former ensures that any change
in the dependency chain (e.g. a change of compiler) causes a rebuild.

A variable can be exempt from affecting the computed hash value by
setting the ``[nohash]`` flag. This should be done with great care,
since it is only safe if it is known not to affect the binaries
generated, and it is only very rarely set in classes or recipes.


.. _task_types:

Task types
==========

Common tasks types
------------------

These tasks are performed for almost all recipes during a normal
build. Note that for the configure, compile and install tasks, if a
recipe does not define a corresponding ``do_`` function (and does not
inherit a class defining it), it is implicitly assumed that the step
is irrelevant to the recipe, so a dummy no-op function is used.

The listed task dependencies are those that must have completed
succesfully before the task is started. OE-lite does a ``chdir`` to
the given working directory before starting the task.

do_fstage
~~~~~~~~~

TBD.

do_fetch
~~~~~~~~

This task downloads the necessary source code to the local
`ingredients directory`. This is typically in the form of
compressed tar-balls, but it can also perform cloning of git
repositories.

Task dependencies: fstage

Working directory: ``${INGREDIENTS}``

do_unpack
~~~~~~~~~

This extracts the source code from the local `ingredients directory`
to ``${WORKDIR}/src``. For a tarball, this consists of (uncompressing
and) extracting the file, but it can also consist of checking out a
specific commit from a git repository. It also copies local patches
(files mentioned in ``SRC_URI`` ending with ``.patch``) to
``${WORKDIR}/patches``.

Task dependencies: fetch

Working directory: ``${SRCDIR}``

do_patch
~~~~~~~~

This applies the local patches, if any, to the source code.

Task dependencies: unpack

Working directory: ``${PATCHDIR}``

do_stage
~~~~~~~~

This populates the directory ``${WORKDIR}/stage`` with all the
necessary build-time dependencies as described by the recipe's
``DEPENDS`` variable.

Task dependencies: do_stage depends on the existence of all the
`packages <OE-lite package>` providing the items defined in the
``DEPENDS`` variable. If a necessary package does not already exist in
the ``tmp/packages`` directory or can be found as a prebake, the
recipe providing that package will automatically get built, in which
case do_stage depends on the do_package task of the other recipe. 

Working directory: ``${STAGE_DIR}``

do_configure
~~~~~~~~~~~~

This is responsible for configuring the software. In many cases this
is the classic ``./configure`` step. When a recipe uses an appropriate
`class <OE-lite class>`, OE-lite automatically constructs and passes
the relevant command line parameters to the configure script.

Task dependencies: patch and stage

Working directory: ``${B}``

do_compile
~~~~~~~~~~

This task is where the software actually gets built. In many cases
this is just calling ``make``. The working directory is ``${S}``.

Task dependencies: configure

Working directory: ``${B}``

do_install
~~~~~~~~~~

This installs the software under ``${WORKDIR}/install``, often just by
invoking ``make install``. During

Task dependencies: compile

Working directory: ``${B}``

do_split
~~~~~~~~

This splits the files installed under ``${WORKDIR}/install`` into
packages. Files belonging to the package ``foo`` gets copied to a
directory tree under ``${PKGD}/foo``. The splitting is governed by the
``FILES_*`` variables. These contain space-separated lists of glob
patterns. For example, ``FILES_${PN}-dev`` contain (among other
things) ``/lib/lib*.so /usr/include``, so all

Task dependencies: install

Working directory: ``${D}``

do_package
~~~~~~~~~~

This adds some metadata (descripton, license, version etc.) to the
packages created by do_split, and then wraps the directories up in a
tarball.

Task dependencies: split

Working directory: ``${PKGD}``

Other tasks
-----------

These are usually only run when requested explicitly on the command line, e.g.

.. code:: sh

   oe bake openssl -t packageqa

packageqa
~~~~~~~~~

Perform a number of Quality Assurance checks, for example:

- For shared libraries, check that the so-name matches the ``LIBRARY_VERSION`` version.

- For binaries and shared libraries, check that all
  runtime-dependencies are actually listed in the ``RDEPENDS``
  variable.

Task dependencies: package

Working directory: ``${PKGD}``
  
clean
~~~~~

Remove the entire ``${WORKDIR}`` as well as the ``${STAMPDIR}`` – the
former ensures that there are no leftovers from earlier attempts to
build the recipe, while the latter prevents OE-lite from believing
that certain tasks are already succesfully completed and thus eliding
them. Hence a subsequent ``oe bake foo`` should do all tasks related
to the foo recipe.

Task dependencies: none

Working directory: ``${TOPDIR}``
