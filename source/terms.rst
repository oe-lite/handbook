.. // This is part of the OE-lite Developers Handbook
.. // Copyright (C) 2013
.. //   Esben Haabendal <esben@haabendal.dk>

*******************
OE-lite Terminology
*******************

.. glossary::

   OE-lite manifest
      A git repository used as top-level for the project, containing
      as a minimum the definition of OE-lite stack used in the project
      (the conf/bakery.conf file). It typically also contains other
      project specific parts, such as project specific configuration
      files, and OE-lite recipes, scripts and documentation.

   OE-lite stack
      An ordered list of OE-lite layers, and various properties
      assigned to these.

   OE-lite layer
      A subdirectory of the OE-lite manifest, holding either OE-lite
      metadata or Python library code. An OE-lite layer is typically
      contained in its own git repository.

   OE-lite layer, external layer
      An OE-lite layer hosted in a git repository not related to the
      projects OE-lite repository. When creating clones of the OE-lite
      repository, the layer will be cloned from the (external) git
      repository. Using OE-lite/core directly from
      git://oe-lite.org/oe-lite/core.git is an example of an external
      layer.

   OE-lite layer, internal layer
      An OE-lite layer hosted in a git repository which is placed
      under the manifest repository using the same relative path as is
      used in the OE-lite stack, and is referenced in the OE-lite
      manifest using relative paths. An example of an internal layer
      is an OE-lite project with the manifest repository hosted at
      git://oe-lite.org/bsp/foobar.git has an OE-lite/core layer at
      meta/core hosted at git://oe-lite.org/bsp/foobar.git/meta/core,
      and referenced in the manifest using the url ./meta/core .

   OE-lite layer, embedded layer
      An OE-lite layer contained directly in the OE-lite manifest
      repository, and is as such indivisible from the manifest. This
      should normally only be used for layers that has no re-use
      potential for other projects, now and in the future. The top of
      the OE-lite manifest is always treated as an implicit embedded
      layer. Other than this implicit top-level embedded layer, this
      layer type is not advisable.

   OE-lite repository
      A bare clone of the OE-lite manifest git repository, and bare
      clones of any OE-lite layers using relative paths.
