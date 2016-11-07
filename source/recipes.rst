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
