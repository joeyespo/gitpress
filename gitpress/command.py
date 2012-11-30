"""\
gitpress.command
~~~~~~~~~~~~~~~~

Implements the command-line interface of Gitpress.


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

import os
import sys
from docopt import docopt
from .helpers import parse_address, valid_address
from .server import preview
from . import __version__


def main(initial_args=None):
    """The entry point of the application."""
    if initial_args is None:
        initial_args = sys.argv[1:]
    version = 'Gitpress ' + __version__
    usage = '\n\n\n'.join(__doc__.split('\n\n\n')[1:])
    args = docopt(usage, argv=initial_args, version=version)

    if args['preview']:
        path, address = _resolve_address(args['<path>'], args['<address>'])
        if address and not valid_address(address):
            print 'Error: Invalid address', repr(address)
        host, port = parse_address(address)
        return preview(working_directory=path, host=host, port=port)

    return 0


def _resolve_address(path_or_address, address=None):
    """Returns (path, address) based on consecutive optional arguments, [path] [address]."""
    # TODO: return (path, host, port)

    if path_or_address is None or address is not None:
        return path_or_address, address

    path = None
    if not valid_address(path_or_address) or os.path.exists(path_or_address):
        path = path_or_address
    else:
        address = path_or_address

    return path, address