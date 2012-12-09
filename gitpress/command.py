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

import sys
from path_and_address import resolve, split_address
from docopt import docopt
from .server import preview
from . import __version__


def main(args=None):
    """The entry point of the application."""
    if args is None:
        args = sys.argv[1:]
    usage = '\n\n\n'.join(__doc__.split('\n\n\n')[1:])
    version = 'Gitpress ' + __version__

    # Parse options
    args = docopt(usage, argv=args, version=version)

    # Parse arguments
    path, address = resolve(args['<path>'], args['<address>'])
    host, port = split_address(address)

    # Validate address
    if address and not host and not port:
        print 'Error: Invalid address', repr(address)

    # Run command
    if args['preview']:
        try:
            return preview(working_directory=path, host=host, port=port)
        except ValueError as ex:
            print 'Error:', ex
            return 1

    return 0
