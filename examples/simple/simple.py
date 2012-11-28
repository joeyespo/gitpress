"""\
Simple
Gitpress Example

An example website that uses Gitpress to listen for and serve a blog.
"""

import os
import gitpress


if __name__ == '__main__':
    gitpress.run(port=os.environ.get('PORT'))
