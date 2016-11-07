# -*- coding: utf-8 -*-
"""
    oedomain
    ~~~~~~~~~~

    An OE-lite domain.

    This domain initially provides an `oe:var` role.

    Based on GNU Make domain from <https://bitbucket.org/birkenfeld/sphinx-contrib/src/55b13a74d56eebdbf3b6c11b1e73d2718ea51ab7/makedomain/?at=default>

"""

__version__ = "0.1.1"
# for this module's sphinx doc
release = __version__
version = release.rsplit('.', 1)[0]

from sphinxcontrib.domaintools import custom_domain
import re

def setup(app):
    app.add_domain(custom_domain('OEliteDomain',
        name  = 'oe',
        label = "OE-lite",

        elements = dict(
            var   = dict(
                objname = "OE-lite Variable",
                indextemplate = "pair: %s; OE-lite Variable"
            ),
        )))
