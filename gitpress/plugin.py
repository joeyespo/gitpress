# -*- coding: utf-8 -*-
"""
gitpress.plugin
~~~~~~~~~~~~~~~

Plugins are installable behavioral components to customize the build.

:copyright: (c) 2013 by Joe Esposito.
:license: MIT, see LICENSE for more details.
"""


class PluginRequirement(object):
    """Contains information about a particular plugin installed during a build."""
    def __init__(self, name, settings={}):
        self.name = name
        self.settings = settings
