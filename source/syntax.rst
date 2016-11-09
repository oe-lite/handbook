.. // This is part of the OE-lite Developers Handbook
.. // Copyright (C) 2016
.. //   Rasmus Villemoes <ravi@prevas.dk>

.. _chap_syntax:

******
Syntax
******

This appendix contains a rough sketch of the formal syntax used to
define OE-lite recipes.

Formal grammar
==============

The BNF grammar below is extracted from the actual source code used to
parse recipes. On the one hand, that makes it quite authoritative. On
the other hand, it might have been more readable if it was a little
less formal. Also, not all terminals (productions in uppercase) are
defined below [#f1]_ – but at least some of the missing ones should be
obvious, and we explain a few more (e.g. what constitutes a valid
variable name) in the `semantics`_ section below.

.. include:: syntax.bnf

.. _semantics:

Semantics
=========

This section describes the semantics of the most important top-level
productions in the above grammar.

Assignment
----------

The most common statement in a recipe is some form of assignment. The
LHS must be a valid variable name, which means that it must match the
regular expression ``[a-zA-Z_][a-zA-Z0-9_\-\${}\+\.]*``. In other
words, it must start with a letter or underscore, and otherwise
consist of alphanumeric characters, along with ``-${}+.``.

The characters ``${}`` are not part of the actual variable name, but
can be used to substitute the value of another variable. For example,
if ``PN`` contains ``openssh``, ``RDEPENDS_${PN} = "something"`` would
assign the value ``something`` to ``RDEPENDS_openssh``. In practice,
``${PN}`` is the only variable one will ever use in this context.

The RHS should normally consist of a quoted string. References to
other variables can be done by wrapping them in ``${}`` (this differs
from Makefile syntax where ``$()`` is used).

The semantics of the various operators is as follows:

``LHS = "RHS"``: Assign ``RHS`` to the variable ``LHS``.

``LHS .= "RHS"``: Append ``RHS`` to the current value of ``LHS`` – if
``LHS`` was not defined, it is treated as if it was defined to the
empty string.

``LHS =. "RHS"``: This works just like ``.=`` except that it prepends
rather than appends.

``LHS += "RHS"``: If LHS is not currently defined or is the empty
string, this works just as ``LHS = "RHS"``. Otherwise, this appends a
space and then ``RHS`` to the value of ``LHS``.

``LHS =+ "RHS"``: This works just like ``+=`` except that it prepends
rather than appends.

``LHS := "RHS"``: Expand all variables appearing in ``RHS``
(recursively) and assign the result to ``LHS``. It is an error if the
RHS, or any of the text it expands to, refers to undefined variables.

``LHS ?= "RHS"``: If ``LHS`` is already defined (even as the empty
string), this does nothing. Otherwise, it works just as ``LHS =
"RHS"``.

Flags
-----

Apart from its value, a variable can also have a number of attributes,
or flags. It is rarely necessary to set flags in recipes, but you may
encounter the syntax in classes and configuration files.

In general, the syntax for flag settings is just as for variable settings:

.. code-block:: oe

   varname[flag] = "value"

Some flags just serve as boolean flags (hence the name) and are hence
normally only set using the ``=``, ``?=`` and ``:=`` operators, while
others are treated as a whitespace separated list of words.

nohash
~~~~~~

This flag indicates that the variable it is attached to should not be
part of the `metadata hashing <metadatahash>`_.

export
~~~~~~

When a shell function is executed as part of a task, most of the
task's metadata variables [#f2]_ are written to the shell script. Only those
variables with the ``export`` flag set are further exported to the
commands executed by the script.

Instead of setting this flag using the ``varname[export] = "1"``
syntax, an alternative is to use the ``export varname`` statement.

unexport
~~~~~~~~

A variable with this flag does not get exported to the shell
environment when a shell function is run. It is thus not quite the
opposite of the *export* flag.

emit
~~~~

This flag is used to limit the tasks which a given variable gets
copied to. If set, the variable is only emitted to the metadata
instances for the tasks listed, e.g.

.. code-block:: oe

   PACKAGES[emit] = "do_split do_package"




.. rubric:: Footnotes

.. [#f1] Automatically extracting the regexps definining the various
         tokens and presenting them in a reasonable way is not easy.
.. [#f2] Variables names which are not valid as shell variables,
         e.g. those containing ``-``, are not exported.
