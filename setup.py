"""\
Gitpress
--------

Blissful blogging for hackers.


Links
`````

* `Website <http://gitpress.com>`_
* `Documentation <http://docs.gitpress.com>`_
* `Source code <https://github.com/joeyespo/gitpress>`_

"""

import os
import sys
from setuptools import setup, find_packages


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='gitpress',
    version='0.3',
    description='Blissful blogging for hackers.',
    long_description=__doc__,
    author='Joe Esposito',
    author_email='joe@joeyespo.com',
    url='http://github.com/joeyespo/gitpress',
    license='MIT',
    platforms='any',
    packages=find_packages(),
    package_data={'': ['LICENSE'], 'gitpress': ['static/*', 'templates/*']},
    install_requires=read('requirements.txt'),
    zip_safe=False,
    entry_points={'console_scripts': ['gitpress = gitpress.command:main', 'gpp = gitpress.command:gpp']},
)
