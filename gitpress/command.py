"""\
gitpress.command
~~~~~~~~~~~~~~~~

Implements the command-line interface of Gitpress.


Usage:
  gitpress init [-q] [<directory>]
  gitpress preview [--out <dir>] [<path>] [<address>]
  gitpress build [--out <dir>] [<path>]

Options:
  -h --help         Show this help.
  --version         Show version.

Notes:
  <address> can take the form <host>[:<port>] or just <port>.
"""

import sys
from docopt import docopt
from path_and_address import resolve, split_address
from .present import init, RepositoryAlreadyExistsError
from .previewing import preview
from .building import build
from . import __version__


def main(argv=None):
    """The entry point of the application."""
    if argv is None:
        argv = sys.argv[1:]
    usage = '\n\n\n'.join(__doc__.split('\n\n\n')[1:])
    version = 'Gitpress ' + __version__

    # Parse options
    args = docopt(usage, argv=argv, version=version)
    path = args['<path>']

    # Execute command
    if args['init']:
        try:
            repo = init(args['<directory>'])
            print 'Initialized Gitpress repository in', repo
        except RepositoryAlreadyExistsError as ex:
            if not args['-q']:
                print 'Gitpress repository already exists in', ex.repo
        return 0
    elif args['preview']:
        path, address = resolve(path, args['<address>'])
        host, port = split_address(address)
        if address and not host and not port:
            print 'Error: Invalid address', repr(address)
        return preview(working_directory=path, host=host, port=port)
    elif args['build']:
        return build(path, args['--out'])

    return 1


def gpp(argv=None):
    """Shortcut function for running the previewing command."""
    if argv is None:
        argv = sys.argv[1:]
    argv.insert(0, 'preview')
    return main(argv)
