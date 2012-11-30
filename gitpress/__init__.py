"""\
Gitpress
--------

Blissful blogging for hackers.


Links
`````

* `Website <http://gitpress.com/>`_
* `Documentation <http://gitpress.com/docs>`_
* `Source code <https://github.com/joeyespo/gitpress>`_
"""

__title__ = 'gitpress'
__version__ = '0.1'
__author__ = 'Joe Esposito'
__description__ = '\n\n'.join(__doc__.split('\n\n')[1:]).split('\n\n\n')[0]
__license__ = 'MIT'
__copyright__ = 'Copyright 2012 Joe Esposito'


from .server import preview
from .runner import run
