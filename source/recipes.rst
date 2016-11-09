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

