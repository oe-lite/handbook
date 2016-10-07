This chapter covers the various aspects related to making releases of
OE-lite based projects.

Some parts of this chapter is meant as a guideline and not something
that you need to follow.

Metadata Releases
=================

This section describes how to make releases of OE-lite metadata projects
(like OE-lite/core, OE-lite/base and so on).

Metadata Versioning
-------------------

For OE-lite.org metadata projects, the releases must be versioned
according to the scheme described in this section.

OE-lite.org metadata releases must follow the Semantic Versioning
specification (see http://semver.org). Briefly described, this means
that version numbers are formatted as X.Y.X, with X being major number,
Y being minor number, and Z being patch number.

For releases that only contains backwards compatible bugfixes (a bugfix
release) should be versioned with an increment to the patch number. A
bugfix release based on X.Y.Z would thus be X.Y.Z+1.

For release that contains new, backwards compatible functionality
(feature releases) should be versioned with an increment to the minor
number. A feature release based on X.Y.Z would thus be X.Y+1.0.

For releases that contains any backwards incompatile changes (major
releases) should be versioned with an increment to the major number. A
major release based on X.Y.Z would thus be X+1.0.0.

For more details, see http://semver.org

Metadata Release Branching
--------------------------

OE-lite.org metadata releases should be done from a release branch named
X.Y (for release version X.Y.Z).

When creating a new major release, a new release branch must be created.
This new X.0 branch should branch off of either the previous latest
release branch (ie. X-1.Y) or the master branch.

When creating a new feature release, a new release branch must be
created. This new X.Y branch should branch off of the previous release
branch (X.Y-1).

When creating a new bugfix release, the X.Y release branch should
already exist. It should have been created when the X.Y.0 feature
release (or major release if Y=0) was made.

Release branchs must be pushed to the official OE-lite.org upstream
repository (ie. git://oe-lite.org/oe-lite/core.git for OE-lite/core).
Release branches are considered permanent branches, and should not be
deleted, as they must be available for doing bugfix releases from.

    **Important**

    Public release branches must not be rebased, or the commit history
    in any other way be rewritten.

Metadata Release Tagging
------------------------

When a release is ready to go out of the door, it must be tagged.

OE-lite.org metadata project releases must contain a ``VERSION`` file
containing the release version number in plain text. So before making
the git tag, a new commit with this file should be created.

The following example shows how to create a release commit and tag:

.. code:: sh

    echo "3.4.1" > VERSION
    git add VERSION
    git commit -m "Release 3.4.1"
    git tag -a -m "Release 3.4.1" v3.4.1

After the release is done, the ``VERSION`` file should be removed, so
that only the actual release version carries it.

.. code:: sh

    git rm VERSION
    git commit -m "Unrelease"

The release branch (including both the release and unrelease commit) and
the release tag must of-course be pushed to the official OE-lite.org
upstream repository (ie. git://oe-lite.org/oe-lite/core.git for
OE-lite/core).

    **Important**

    Release tags must not be changed.

    **Note**

    The release and unrelease commits does not need a Signed-off-by
    line.

Metadata Release Tarballs
-------------------------

OE-lite.org metadata project releases must be available as tarball for
download on http://oe-lite.org/download/

To create release tarballs, use something like the following:

.. code:: sh

    git archive --prefix=core-3.4.1/ -o oe-lite-core-3.4.1.tar v3.4.1
    cat oe-lite-core-3.4.1.tar | gzip > oe-lite-core-3.4.1.tar.gz
    cat oe-lite-core-3.4.1.tar | xz > oe-lite-core-3.4.1.tar.xz

To put the tarballs on oe-lite.org, stuff them somewhere on the net and
send an email to esben@haabendal.dk (with cc to dev@oe-lite.org)
requesting copies to be placed on the oe-lite.org server.

Metadata Release Announcement
-----------------------------

When the OE-lite.org metadata project release is ready (ie. tarballs are
on oe-lite.org, and the release has been pushed to the official
oe-lite.org repository, the release must be announced to the OE-lite.org
community.

The release must be announced both on the dev@oe-lite.org mailing list
and the http://oe-lite.org site.

Metadata Release Email Announcement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The release announcement email could look something like
http://lists.oe-lite.org/pipermail/dev/2012-November/001222.html.

To generate the contributer contribution and the per-author shortlog
text, you can use the
http://oe-lite.org/download/scripts/release-mail.py script. It should be
called like this:

.. code:: sh

    release-mail.py v3.3.0 v3.4.0

With the first argument specifying the previous release, and the second
argument specifying the release you are announcing.

Metadata Relase Redmine Announcement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To announce the release on http://oe-lite.org, you must create a Redmine
news item, and it could look something like
http://oe-lite.org/redmine/news/11.

Metadata Release Checklist
--------------------------

1. Is the release created from a release branch according to the
   description in section `Metadata Release
   Branching <#metadata-release-branching>`__
   `section\_title <#metadata-release-branching>`__?

2. Is the release properly tagged according to the description in
   section `Metadata Release Tagging <#metadata-release-tagging>`__
   `section\_title <#metadata-release-tagging>`__?

3. Has tar-balls been created and uploaded to oe-lite.org according to
   the description in section `Metadata Release
   Tarballs <#metadata-release-tarballs>`__
   `section\_title <#metadata-release-tarballs>`__?

4. Has a release announcement mail been sent to the dev@oe-lite.org
   mailinglist according to the description in `Metadata Release
   Announcment <#metadata-release-announcement>`__
   `section\_title <#metadata-release-announcement>`__?

5. Has the http://oe-lite.org Redmine been updated with a News item
   according to the description in `Metadata Release
   Announcment <#metadata-release-announcement>`__
   `section\_title <#metadata-release-announcement>`__?

Release Cherry-Picking
======================

This section describes how to use the ``oe cherry`` command for
assistance in cherry picking commits to release branches.

To use the cherry command, you need OE-lite Bakery 4.0.0 or newer, and
OE-lite/core 3.3.0 or newer.

The idea with the cherry command is to help you keep track of which
commits eligible for a specific release branch.

You can fx. use the cherry command to find out which commits on the
master branch are eligible for being cherry picked to the 3.4 release
branch with the following command:

.. code:: sh

    oe cherry master 3.4

This will list all commits that are currently seen as eligible for the
3.4 release branch.

To remove commits from this list, you can run cherry in interactive
mode:

.. code:: sh

    oe cherry -i master 3.4

For each commit, you will be asked for the target version. The allowed
values are:

1. A release branch, ie. X.Y. Commits that you see as eligible for
   release branch X.Y (and newer) should be marked with target version
   X.Y (fx. "3.4", for release branch 3.4).

2. A major release version, ie. X. Commits that you see as eligible for
   a (most likely yet-to-come) major release, should be marked with
   target version X (fx. "4" for major release 4)

3. The master branch. Commits that is not eligible for any releases, and
   thus should stay on the master branch should be marked with target
   version "master".

Any target versions you set will be stored in your local git repository,
and will be used the next time you use the cherry command.

When you have trimmed down the list, you should cherry pick the commits
to the release branch you are working with.

    **Note**

    Remember to use the "-x" argument with the ``git cherry-pick``
    command, as it will help ``oe cherry`` in determining if a commit
    has already been cherry-picked.

BSP Versioning
==============

For OE-lite.org BSP projects, the releases must be versioned according
to the scheme described in this section.

An OE-lite.org BSP is specified by a version number, and an optional
release name. Notice that the version number is mandatory and must by
itself specify the release. The release name is optional and only meant
as a possibility of adding a short description (or perhaps for adding a
funny name…).

Currently, there is no rules or guidelines for the numbering scheme.
Suggestions and discussion related to this are welcome at
dev@oe-lite.org :-)

Branching and Tagging
=====================

TBD…
