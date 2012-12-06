"""\
Gitpress
--------

Blissful blogging for hackers.


Links
`````

* `Website <http://gitpress.com>`_
* `Documentation <http://docs.gitpress.com>`_
* `Source code <https://github.com/joeyespo/gitpress>`_

:copyright: (c) 2012 by Joe Esposito.
:license: MIT, see LICENSE for more details.
"""

__version__ = '0.1'
__description__ = '\n\n'.join(__doc__.split('\n\n')[1:]).split('\n\n\n')[0]


import os
from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='gitpress',
    version=__version__,
    description=__description__,
    long_description=__doc__,
    author='Joe Esposito',
    author_email='joe@joeyespo.com',
    url='http://github.com/joeyespo/gitpress',
    license='MIT',
    platforms='any',
    packages=find_packages(),
    package_data={'': ['LICENSE'], 'gitpress': ['static/*', 'templates/*']},
    include_package_data=True,
    install_requires=read('requirements.txt'),
    zip_safe=False,
    entry_points={'console_scripts': ['gitpress = gitpress.command:main']},
)
