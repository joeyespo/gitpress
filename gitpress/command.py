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
from .config import ConfigSchemaError
from .present import init, RepositoryAlreadyExistsError, RepositoryNotFoundError
from .previewing import preview
from .building import build
from .themes import list_themes, use, ThemeNotFoundError
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
    try:
        execute(args)
    except RepositoryNotFoundError as ex:
        print 'Error: No Gitpress repository found at', ex.directory


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
        theme = args['<theme>']
        if args['use']:
            try:
                switched = use(theme)
            except ConfigSchemaError as ex:
                print 'Error: Could not set config value:', ex
                return 1
            except ThemeNotFoundError as ex:
                print 'Error: Theme %s is not currently installed.' % repr(theme)
                return 1
            if switched:
                print 'Switched to theme %s.' % repr(theme)
            else:
                print 'Already using %s.' % repr(theme)
        elif args['install']:
            # TODO: implement
            raise NotImplementedError()
        elif args['uninstall']:
            # TODO: implement
            raise NotImplementedError()
        else:
            themes = list_themes()
            if themes:
                print 'Installed themes:'
                print '  ' + '\n  '.join(themes)
            else:
                print 'No themes installed.'
        return 0

    return 1


def gpp(argv=None):
    """Shortcut function for running the previewing command."""
    if argv is None:
        argv = sys.argv[1:]
    argv.insert(0, 'preview')
    return main(argv)
