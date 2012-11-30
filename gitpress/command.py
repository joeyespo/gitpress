"""\
command.py
The command-line interface of Gitpress.

Usage:
  gitpress preview [<path>] [<address>]
  gitpress -h | --help
  gitpress --version

Where:
  <path> is the path to the working directory of a content repository
  <address> is what to listen on, of the form <host>[:<port>] or just <port>

Options:
  -h --help         Show this screen.
  --version         Show version.
"""

import sys
from docopt import docopt
from .helpers import resolve_address, parse_address, valid_address
from .server import preview
from . import __version__


def main(initial_args=None):
    """The entry point of the application."""
    if initial_args is None:
        initial_args = sys.argv[1:]
    version = 'Gitpress ' + __version__
    args = docopt(__doc__, argv=initial_args, version=version)

    if args['preview']:
        path, address = resolve_address(args['<path>'], args['<address>'])
        if address and not valid_address(address):
            print 'Error: Invalid address', repr(address)
        host, port = parse_address(address)
        return preview(working_directory=path, host=host, port=port)

    return 0
