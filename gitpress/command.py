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
"""

import os
import sys
from docopt import docopt
from .helpers import valid_address
from .server import preview
from . import __version__


def main(args=None):
    """The entry point of the application."""
    if args is None:
        args = sys.argv[1:]
    usage = '\n\n\n'.join(__doc__.split('\n\n\n')[1:])
    version = 'Gitpress ' + __version__
    args = docopt(usage, argv=args, version=version)

    if args['preview']:
        path, address = _resolve_address(args['<path>'], args['<address>'])
        if address and not valid_address(address):
            print 'Error: Invalid address', repr(address)
        host, port = _split_address(address)
        return preview(working_directory=path, host=host, port=port)

    return 0


def _resolve_address(path_or_address, address=None):
    """Returns (path, address) based on consecutive optional arguments, [path] [address]."""

    if path_or_address is None or address is not None:
        return path_or_address, address

    path = None
    if not valid_address(path_or_address) or os.path.exists(path_or_address):
        path = path_or_address
    else:
        address = path_or_address

    return path, address


def _split_address(address):
    """Returns (host, port) from the specified address."""
    # TODO: implement
    host = address
    port = None
    return host, port
