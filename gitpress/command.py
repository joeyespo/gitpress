"""\
gitpress.command
~~~~~~~~~~~~~~~~

Implements the command-line interface of Gitpress.


Usage:
  gitpress preview [options] [<path>] [<address>]
  gitpress build [options] [<path>]

Options:
  -o, --out <path>  Use the specified relative path to render to.
  -h --help         Show this help.
  --version         Show version.

Notes:
  The <address> can take the form <host>[:<port>] or just <port>.
  Previewing content will use the built-in default theme.
  Previewing a theme will use the built-in default blog.
"""

import sys
from docopt import docopt
from path_and_address import resolve, split_address
from .previewing import preview
from .building import build
from . import __version__


def main(args=None):
    """The entry point of the application."""
    if args is None:
        args = sys.argv[1:]
    usage = '\n\n\n'.join(__doc__.split('\n\n\n')[1:])
    version = 'Gitpress ' + __version__

    # Parse options
    args = docopt(usage, argv=args, version=version)
    path = args['<path>']

    # Preview command
    if args['preview']:
        path, address = resolve(path, args['<address>'])
        host, port = split_address(address)

        if address and not host and not port:
            print 'Error: Invalid address', repr(address)

        try:
            return preview(working_directory=path, host=host, port=port)
        except ValueError as ex:
            print 'Error:', ex
            return 1

    # Build command
    if args['build']:
        try:
            return build(path, args['--out'])
        except ValueError as ex:
            print 'Error:', ex
            return 1

    return 0


def gpp(args=None):
    """Shortcut function for running the previewing command."""
    if args is None:
        args = sys.argv[1:]
    args.insert(0, 'preview')
    return main(args)
