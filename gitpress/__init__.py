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

import command
from helper import run


__all__ = ['command', 'run']

__version__ = '0.1'
__description__ = '\n\n'.join(__doc__.split('\n\n')[1:]).split('\n\n\n')[0]
