"""\
gitpress.command
~~~~~~~~~~~~~~~~

Implements the command-line interface of Gitpress.


Usage:
  gitpress preview [--out <dir>] [<path>] [<address>]
  gitpress build [--out <dir>] [<path>]
  gitpress init [-q] [<directory>]
  gitpress themes [use <theme> | install <theme> | uninstall <theme>]

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
from .themes import list_themes
from . import __version__


def main(argv=None):
    """The entry point of the application."""
    if argv is None:
        argv = sys.argv[1:]
    usage = '\n\n\n'.join(__doc__.split('\n\n\n')[1:])
    version = 'Gitpress ' + __version__

    # Parse options
    args = docopt(usage, argv=argv, version=version)

    # Execute command
    execute(args)


def execute(args):
    """Executes the command indicated by the specified parsed arguments."""
    if args['init']:
        try:
            repo = init(args['<directory>'])
            print 'Initialized Gitpress repository in', repo
        except RepositoryAlreadyExistsError as ex:
            if not args['-q']:
                print 'Gitpress repository already exists in', ex.repo
        return 0

    if args['preview']:
        path, address = resolve(args['<path>'], args['<address>'])
        host, port = split_address(address)
        if address and not host and not port:
            print 'Error: Invalid address', repr(address)
        return preview(working_directory=path, host=host, port=port)

    if args['build']:
        return build(args['<path>'], args['--out'])

    if args['themes']:
        # TODO: implement
        if args['use']:
            pass
        elif args['install']:
            pass
        elif args['uninstall']:
            pass
        else:
            themes = list_themes()
            if themes:
                print 'Installed themes:'
                print '  ' + '\n  '.join(themes)
            else:
                print 'No themes installed.'

    return 1


def gpp(argv=None):
    """Shortcut function for running the previewing command."""
    if argv is None:
        argv = sys.argv[1:]
    argv.insert(0, 'preview')
    return main(argv)
