.. // This is part of the OE-lite Developers Handbook
.. // Copyright (C) 2016
.. //   Rasmus Villemoes <ravi@prevas.dk>

*******
Recipes
*******

Recipes describe how to build stuff, both individual software
packages, complete root file systems as well as associated utilities
such as SDKs. This chapter gives a short introduction to the
conventions used as well as a short example.

When starting a build (``oe bake``), OE-lite starts by parsing all
recipe files in all registered layers, pruning recipes which are not
compatible with the current target architecture.


Naming conventions
==================

Recipe files end with the suffix ``.oe``, and should reside in
subdirectories of the ``recipes`` directory in one of the registered
OE-lite layers.

The filename must follow the format ``<name>_<version>.oe``, for example
``tcpdump_4.6.2.oe``, where ``<name>`` is the name of the item described
and ``<version>`` is the version of the software. The name part must not
contain an underscore, since everything after the first underscore is
taken to be the version. It is ok to omit the version part (including
the underscore) when it doesn't apply (e.g. in the case of recipes
describing an entire BSP root file system), in which case OE-lite will
simply pretend it is version "0".

Inside the recipe, the ``<name>`` is available as the variable ``${PN}``,
while the ``<version>`` is available as ``${PV}``.

Language
========

Recipes are written in a domain-specific language defined by
OE-lite. This is not as scary as it sounds. Essentially, the job of a
recipe is to set a bunch of variables. Each variable has a
well-defined semantic meaning to OE-lite. There are hundreds of
variables, but fortunately most retrieve their value more or less
automatically, and there is a lot of infrastructure for helping with
defining the rest.

A few examples of variables and their meaning:

SRC_URI
  Where to fetch the sources for the software.

DEPENDS
  Utilities and libraries necessary to build the recipe.

EXTRA_OECONF
  When using one of the autotools `classes <OE-lite
  class>`, this variable is appended to the ``./configure`` command
  line in the do_configure step.


include and require
===================

How a piece of software gets built usually doesn't change that much
from version to version, so it is quite common to put most of the
logic in ``.inc`` files which then get included from the recipe
files. A complete recipe file can be as small as:

.. code-block:: oe
   :caption: meta/base/recipes/vim/vim_7.4.oe

   require ${PN}.inc

The ``require`` directive instructs OE-lite to look for the given file
(``unzip.inc`` in the example above) and include it at that point. It
is a fatal error if the file is not found. The ``include`` directive
works similar to ``require``, but if the file cannot be found parsing
continues as if the ``include`` was not present.

Syntax
======

The syntax and semantics of defining and manipulating variables is
similar to the one used in Makefiles. For example, the right-hand side
of an ordinary assignment ``FOO = "BAR"`` is not expanded until
``FOO`` is expanded, whereas the ``:=`` operator causes immediate
expansion of the RHS. Also, the operator ``+=`` appends the RHS value
to the LHS variable, but also prepends a space if the variable was
non-empty.

Note, however, that OE-lite does not have the concept of variable
»flavors«, and that all right-hand sides should be properly quoted
strings.

See the appendix `chap_syntax` for a semi-formal survey of the various
allowed syntactic elements.

Variables
=========

This section describes some of the more common variables one needs to
define or which are just nice to know about.

Source code
-----------

.. oe:var:: SRC_URI

   A space-separated list of stuff to fetch to build the recipe. Each
   element should be a valid URI using one of the recognized
   schemes:

   - http\://
   - ftp\://
   - file\://
   - git\://

   The http and ftp schemes usually refer to (possibly compressed)
   tarballs. OE-lite recognizes these and automatically handles
   decompressing/unpacking in the do_unpack task.

   The file scheme is for local files included with the recipe,
   which may for example be a configuration file which should end up
   getting copied to /etc, or a patch which needs to be applied before
   building.

   The git scheme can be used to refer to a (local or remote) git
   repository. This scheme also accepts a number of parameters. These
   are given as key=value pairs separated from each other and the main
   uri by semicolons. The possible parameters are:

   - ``protocol`` the protocol which git will use when cloning from
     the given uri. The default is ``git``, but other possibilities
     are ``http`` and ``ssh``. Using the ``ssh`` protocol typically
     requires that public key authentification has been set up (that
     is, the user running OE-lite has a public key which allows
     password-less login to the remote server).

   - ``commit`` a sha1 to check out.

   - ``tag`` a tag to check out.

   - ``branch`` a branch to check out.

   The latter three are mutually exclusive.

   It is quite common for the :oe:var:`SRC_URI` variable to be defined
   in terms of the recipe version, ``${PV}``. A few examples::

     SRC_URI = "http://www.digip.org/jansson/releases/jansson-${PV}.tar.bz2"
     SRC_URI = "git://git.sv.gnu.org/libunwind.git;tag=v${PV}"
     SRC_URI = "git://github.com/kergoth/tslib.git;commit=f6c499a523bff845ddd57b1d96c9d1389f0df17b"
     SRC_URI = "${GNU_MIRROR}/autoconf/autoconf-${PV}.tar.bz2"

Checksums
~~~~~~~~~

To check the *integrity* of the downloaded files, OE-lite computes a
SHA1 checksum and compares it to value in recipe's *signature file* -
a file with the same name as the recipe file and ``.sig``
appended. For example:

.. literalinclude:: examples/jansson_2.9.oe.sig
   :caption: recipes/jansson/jansson_2.9.oe.sig

If the signature file does not exist, OE-lite creates one
automatically during do_fetch, but then deliberately causes the build
to fail to alert the user. This can be a useful way to create the
signature file for a new ingredient. The format of the signature files
is the same as the output from the standard ``sha1sum`` utility, so
another way is to download the file manually and run

.. code-block:: sh

   sha1sum jansson-2.9.tar.bz2 > /path/to/recipedir/jansson_2.9.oe.sig

However the signature file is generated, it is up to the creator of
the recipe to ensure its *authenticity*, e.g. by comparing a checksum
of the downloaded file to one provided by the upstream project (which
is not necessarily a SHA1).

.. _dependencies:

Dependencies
------------

There are a few different types of dependencies one needs to know
about – and these dependencies must be described to OE-lite using
these variables:

.. oe:var:: DEPENDS

   Describes recipe build dependencies – items that are necessary to
   build the recipe.

.. oe:var:: RDEPENDS

   Describes recipe runtime dependencies – not used in ordinary
   recipes (see below).

.. oe:var:: DEPENDS_foo

   Describes package build dependencies – additional items that are
   necessary to build something that depends on the foo package.

.. oe:var:: RDEPENDS_foo

   Describes package runtime dependencies – additional items that are
   necessary at runtime for using something that has a runtime
   dependency on the foo package.

OE-lite distinguishes between *build* and *runtime*
dependencies. A *build* dependency is something that is necessary to
build a given recipe, while a *runtime* dependency describes some
other item (typically a shared library) that is needed to actually run
the software.

These are further divided into *recipe* dependencies and *package*
dependencies. Recipe dependencies (given in the unsuffixed
``DEPENDS``, ``RDEPENDS`` variables) describe what is required to
build the recipe. Package dependencies, given in ``DEPENDS_<package
name>``, ``RDEPENDS_<package name>``, describe what is needed to use
the contents of the package at build-time respectively run-time.

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
variable as well as their package *build* dependencies (recursively),
image recipes have a do_rstage task which pulls in all the packages in
the recipe's ``RDEPENDS`` variable as well as their package *runtime*
dependencies (recursively). It is admittedly a stretch to call this
run-time build dependencies, but as the preceding sentence hopefully
demonstrates, this makes the handling of the two staging tasks nicely
symmetric.


USE flags
---------

To make it possible to tweak various aspects of a recipe without
having to modify the recipe itself, OE-lite has the concept of *USE
flags*. These are special variables, called ``USE_*``, which are not
set directly but rather receive their value from settings in various
configuration files. The value of ``USE_foo`` is the value of one of
these variables:

- ``DEFAULT_USE_foo`` (lowest priority)
- ``DISTRO_USE_foo`` (intended for distro configs)
- ``MACHINE_USE_foo`` (intended for machine configs)
- ``LOCAL_USE_foo`` (intended for local.conf)
- ``RECIPE_USE_foo`` (highest priority)

The idea is that one can, for example, have a generic setting
``DISTRO_USE_foo = "1"`` in a ``distro.conf`` file, while overriding
that with ``MACHINE_USE_foo = "0"`` in a machine-specific
configuration file.

.. oe:var:: RECIPE_FLAGS

   This is a space-separated list of USE flag names (without the
   ``USE_`` prefix) that apply to the recipe. Only those USE flags
   listed in :oe:var:`RECIPE_FLAGS` are available as variables.

Since USE flags are set globally, it is good practice to have the
first word of the name be the same as the recipe name.

A USE flag example
~~~~~~~~~~~~~~~~~~

An example from the `freetype` recipe::

  RECIPE_FLAGS += "freetype_bzip2"
  EXTRA_OECONF += "${EXTRA_OECONF_BZIP2}"
  EXTRA_OECONF_BZIP2 = "--without-bzip2"
  EXTRA_OECONF_BZIP2:USE_freetype_bzip2 = "--with-bzip2"
  DEPENDS:>USE_freetype_bzip2 = " libbz2"
  DEPENDS_${PN}:>USE_freetype_bzip2 = " libbz2"
  RDEPENDS_${PN}:>USE_freetype_bzip2 = " libbz2"

This defines a USE flag ``USE_freetype_bzip2`` which is used to decide
whether freetype should be compiled with support for bz2-compressed
fonts.

The logic in the three ``EXTRA_OECONF`` lines is that we append the
value of the ``EXTRA_OECONF_BZIP2`` variables to the ``EXTRA_OECONF``
variable - as explained below in the `autotools_class` section, the
contents of that variable is appended to the ``./configure`` command
line when a recipe uses the ``autotools`` class. The next line defines
the ``EXTRA_OECONF_BZIP2`` variable with the contents
``--without-bzip2``, while the third line uses the `override`
mechanism to set its value to ``--with-bzip2``. Altogether, this
ensures that freetype gets configured appropriately.

But the recipe author's job is not quite done yet. When the USE flag
is set, building the recipe also requires libbz2, so we need
to, conditionally, append libbz2 to the ``DEPENDS`` variable.

The freetype library ends up in the package also called freetype, so
we declare libbz2 as a build as well as runtime dependency of the
freetype package.

USE flag gotchas
~~~~~~~~~~~~~~~~

Most USE flags are boolean flags, so they are usually just assigned a
value of False or True, but they can really be any string. When used
in an override assignment, the strings ``""`` and ``"0"`` as well as
the value False are treated as false (that is, the override is not
applied), while all others are treated as true.

Due to a quirk of the current implementation, USE flag variables whose
final value is either the empty string or the string ``"0"`` end up
not being defined at all. This can unfortunately manifest itself as
rather obscure and hard-to-debug errors such as ``Exception: cannot
concatenate 'str' and 'NoneType' objects``, or worse not be detected
at build-time at all. It is also worth noting that using the tokens
``True`` and ``False`` on the right-hand side of assignments is
treated exactly as if one used ``"1"`` and ``"0"``, respectively.

.. _autotools_class:

autotools
---------

The autotools `class <OE-lite class>` is useful for software that uses
the `GNU Build System
<https://en.wikipedia.org/wiki/GNU_Build_System>`_, usually just known
as Autotools. It provides suitable implementations of
``do_configure``, ``do_compile`` and ``do_install`` (the latter two
being inherited from the `make_class` class) For example,
``do_configure`` invokes the autoconf ``configure`` script with all
the cross-compile relevant arguments (``--build``, ``--host``,
``--prefix``, ``cross_compiling=yes`` etc. etc.) set appropriately.

.. oe:var:: EXTRA_OECONF

One can augment the ``./configure`` commandline by setting the
:oe:var:`EXTRA_OECONF` variable – the value of this variable is simply
appended to the ``./configure`` invocation. We saw an example of this
in the USE flag example above, where ``EXTRA_OECONF`` was made to
contain either ``--with-bzip2`` or ``--without-bzip2`` depending on
the value of the ``USE_freetype_bzip2`` flag.

Since each piece of software has a different set of ``--enable-*``,
``--disable-*``, ``--with-*``, ``--without-*`` etc. flags, it is up to
the recipe author to add any appropriate options to
``EXTRA_OECONF``. Making each feature controllable with a USE flag can
be quite cumbersome, and there's nothing wrong with starting out with
just unconditionally adding e.g. ``--without-udev``.

.. _make_class:

make
----

The make `class <OE-lite class>` is useful for software that is built
and installed using standard ``make`` and ``make install``
commands. It provides suitable definitions of ``do_compile`` and
``do_install`` that, essentially, run ``make`` and ``make install``,
respectively.

.. oe:var:: EXTRA_OEMAKE
.. oe:var:: PARALLEL_MAKE
.. oe:var:: EXTRA_OEMAKE_COMPILE
.. oe:var:: EXTRA_OEMAKE_INSTALL
.. oe:var:: MAKE_DESTDIR

The contents of the :oe:var:`EXTRA_OEMAKE` variable is appended to the
``make`` command line in both cases. In addition,
:oe:var:`PARALLEL_MAKE` and :oe:var:`EXTRA_OEMAKE_COMPILE` are appended
in the ``do_compile`` case, while :oe:var:`EXTRA_OEMAKE_INSTALL` and
:oe:var:`MAKE_DESTDIR` are appended in the ``do_install`` case.

The ``EXTRA_OEMAKE*`` variables are for recipe-specific tweaks; often
they are not needed at all.

:oe:var:`PARALLEL_MAKE` is typically defined in ``local.conf`` and
hence applies to all recipes, containing something like ``-j8`` or
however many cpu cores one has (or wishes to use). Some software is
known not to support parallel builds – in those cases, one can set
``PARALLEL_MAKE = ""`` or more explicitly ``PARALLEL_MAKE = "-j1"`` in
the recipe file to force a serial build.

:oe:var:`MAKE_DESTDIR` usually contains the value ``DESTDIR=${D}``, and
thus serves to ensure that the ``DESTDIR`` variable is defined
appropriately.

.. _pkgconfig_class:

pkgconfig
---------

Many autotools configure scripts rely on pkg-config to figure out the
proper compiler/linker flags for various needed libraries (or to
detect if those libraries are even present). To make sure pkg-config
picks up libraries and headers from the staging area rather than the
host, you should inherit the :oe:cls:`pkgconfig` class.

.. _auto_package_libs_class:

auto-package-libs
-----------------

Some recipes provide multiple (more or less related) libraries. The
auto-package-libs `class <OE-lite class>` provides a convenient way to
split those libraries into separate `packages <OE-lite package>`. It
is easiest to look at an example to to explain how it is used.

The mosquitto recipe generates two libraries libmosquitto and
libmosquittopp, the latter being a C++ version. In ``mosquitto.inc``
we find::

  inherit auto-package-libs
  AUTO_PACKAGE_LIBS = "mosquitto mosquittopp"

That is, the :oe:var:`AUTO_PACKAGE_LIBS` variable should contain the
list of library names, each without the ``lib`` prefix. For each
library name X, this automatically creates the packages
mosquitto-libX, mosquitto-libX-dev and mosquitto-libX-dbg [»creating«
a package is really just a matter of adding a word to the
:oe:var:`PACKAGES` variable], and also creates corresponding
``FILES_*`` variables naming the files which belong to those
packages. For example, for the three mosquittopp packages, the
``FILES_*`` variables contain::

  FILES_mosquitto-libmosquittopp='/usr/lib/libmosquittopp.so.*'
  FILES_mosquitto-libmosquittopp-dbg='/usr/lib/.debug/libmosquittopp.so.*'
  FILES_mosquitto-libmosquittopp-dev='/usr/lib/libmosquittopp.so /usr/lib/libmosquittopp.la /usr/lib/libmosquittopp.a /usr/lib/pkgconfig/mosquittopp.pc'

The `do_split_task` task puts every file matching those glob patterns
into the corresponding package.

Unfortunately, the two lines above are not quite sufficient to explain
everything to OE-lite - in particular, we need to define the `package
dependencies <dependencies>` for the individual packages, so that a
build or run-time dependency on e.g. libmosquittopp automatically
pulls in anything else that that library needs. For convenience, four
variables are available that can be set to common dependencies for all
the libX and libX-dev packages:

.. oe:var:: AUTO_PACKAGE_LIBS_DEPENDS

   automatically added to each package build dependency DEPENDS_foo-libX.

.. oe:var:: AUTO_PACKAGE_LIBS_RDEPENDS

   automatically added to each package run-time dependency variable RDEPENDS_foo-libX.

.. oe:var:: AUTO_PACKAGE_LIBS_DEV_DEPENDS

   automatically added to each package build dependency DEPENDS_foo-libX-dev.

.. oe:var:: AUTO_PACKAGE_LIBS_DEV_RDEPENDS

   automatically added to each package run-time dependency variable RDEPENDS_foo-libX-dev.

For example, the mosquitto.inc file contains::

  AUTO_PACKAGE_LIBS_DEPENDS = "libpthread librt libz libm openssl"
  AUTO_PACKAGE_LIBS_RDEPENDS = "libc libcrypto libpthread librt libssl"

In addition, the C++ library depends on the C library, so we additionally have::

  DEPENDS_mosquitto-libmosquittopp += "libmosquitto libstdc++"
  RDEPENDS_mosquitto-libmosquittopp += "libmosquitto libgcc libstdc++"

For hopefully obvious reasons, libmosquitto cannot be added to the
common dependency variable AUTO_PACKAGE_LIBS_DEPENDS, but on the other
hand it is crucial that depending on libmosquittopp in some other
recipe also implies a dependency on libmosquitto. One could add
libstdc++ to the common dependency variable, but that would
unnecessarily pollute the staging area for recipes that only depend on
the C library.

.. _auto_package_utils_class:

auto-package-utils
------------------

A companion to the `auto_package_libs_class` class, the
auto-package-utils class is useful for splitting utilities into
separate packages. In principle, the usage is as simple as::

  inherit auto-packages-utils
  AUTO_PACKAGE_UTILS = "bzip2 bzdiff bzgrep bzip2recover bzmore"

This example is from the bzip2 recipe. The above creates packages
bzip2-X and bzip2-X-doc for each X in the ``AUTO_PACKAGE_UTILS``
variable. The corresponding ``FILES_*`` automatically get sensible
values, e.g. ::

  FILES_bzip2-bzdiff = "/sbin/bzdiff /bin/bzdiff /usr/sbin/bzdiff /usr/bin/bzdiff /usr/libexec/bzdiff"
  FILES_bzip2-bzdiff-doc = "/usr/share/man/man?/bzdiff.*"

ensures that the bzdiff binary, whereever it might get installed, ends
up in the bzip2-bzdiff package, and its documentation goes into
bzip2-bzdiff-doc.

There are also corresponding ``PROVIDES_*`` settings::

  PROVIDES_bzip2-bzdiff = "util/bzdiff"

The ``util/`` prefix is a convention used to designate »utilities«
(anything executable) for dependency purposes. By default, a package
provides an item with the same name as the package, so if one writes ::

  RDEPENDS += "bzip2"

one would get whatever got packaged in the main ``bzip2`` package,
which doesn't necessarily (and in fact, not in this case) include the
``bzip2`` binary. Hence if one needs the ``bzip2`` utility, one should
spell it ::

  RDEPENDS += "util/bzip2"

That will make OE-lite find and stage the package which actually
provides the ``bzip2`` binary, and other recipes do not need to know
about how the bzip2 recipe is being split.

Some utilities behave differently depending on how they are invoked
(i.e., based on ``argv[0]``). This is typically implemented by making
each of the alternate names a symlink to the main binary. Since these
symlinks would be useless by themselves, it is better to package them
together with the binary they point to. The
:oe:cls:`auto-package-utils` class provides a simple mechanism for
this: Set ``AUTO_PACKAGE_UTILS_SYMLINKS_foo`` to the list for
alternate names for the ``foo`` utility. For example, in the bzip2
recipe, we have::

  AUTO_PACKAGE_UTILS_SYMLINKS_bzip2 = "bunzip2 bzcat"
  AUTO_PACKAGE_UTILS_SYMLINKS_bzdiff = "bzcmp"
  AUTO_PACKAGE_UTILS_SYMLINKS_bzgrep = "bzegrep bzfgrep"
  AUTO_PACKAGE_UTILS_SYMLINKS_bzmore = "bzless"

and the above ``FILES_*`` and ``PROVIDES_*`` were slightly lying;
their real values are::

  FILES_bzip2-bzdiff = "/sbin/bzdiff /bin/bzdiff /usr/sbin/bzdiff /usr/bin/bzdiff /usr/libexec/bzdiff /sbin/bzcmp /bin/bzcmp /usr/sbin/bzcmp /usr/bin/bzcmp /usr/libexec/bzcmp"
  FILES_bzip2-bzdiff-doc = "/usr/share/man/man?/bzdiff.* /usr/share/man/man?/bzcmp.*"
  PROVIDES_bzip2-bzdiff = "util/bzdiff util/bzcmp"

Just as for auto-package-libs, one also needs to define the package
dependencies for the packages created by the auto-package-utils class,
and there are similar convenience variables for defining common
dependencies:

.. oe:var:: AUTO_PACKAGE_UTILS_DEPENDS

   automatically added to each package build dependency DEPENDS_foo-X.

.. oe:var:: AUTO_PACKAGE_UTILS_RDEPENDS

   automatically added to each package run-time dependency variable RDEPENDS_foo-X.

In the bzip2 case, all the utilities depend on the libbz2.so shared library, so we have::

  AUTO_PACKAGE_UTILS_RDEPENDS = "libbz2"

..
  TODO: Document AUTO_PACKAGE_UTILS_PACKAGES and
  AUTO_PACKAGE_UTILS_PROVIDES. They seem to be used for the same
  purpose, namely making the main package (or an extra special-purpose
  foo-utils package) RDEPEND on all the utilities. In practice,
  there's probably no difference between

  RDEPENDS_${PN} += "${AUTO_PACKAGE_UTILS_PROVIDES}"

  and

  RDEPENDS_${PN} += "${AUTO_PACKAGE_UTILS_PACKAGES}"
