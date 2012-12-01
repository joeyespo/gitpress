"""\
Gitpress
--------

Blissful blogging for hackers.


Links
`````

* `Website <http://gitpress.com/>`_
* `Documentation <http://gitpress.com/docs>`_
* `Source code <https://github.com/joeyespo/gitpress>`_

:copyright: (c) 2012 by Joe Esposito.
:license: MIT, see LICENSE for more details.
"""

__title__ = 'gitpress'
__version__ = '0.1'
__author__ = 'Joe Esposito'
__description__ = '\n\n'.join(__doc__.split('\n\n')[1:]).split('\n\n\n')[0]
__copyright__ = 'Copyright 2012 Joe Esposito'
__license__ = 'MIT'


from .runner import run
from .server import preview
from .helpers import parse_address
