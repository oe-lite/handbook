This chapter describes how to clone an existing OE-lite repository.

To create a local clone of an OE-lite repository for development and/or
build purposes, use the following command:

::

    oe clone <url> <path>

This will create a new OE-lite repository clone of <url> at the local
directory <path>. The <url> argument can be any valid git url. See
link:See git[git clone documentation] for more on this.

All git submodules and/or OE-lite layers specified will be (recursively)
cloned also.
