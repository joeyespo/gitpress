"""\
gitpress.command
~~~~~~~~~~~~~~~~

Implements the command-line interface of Gitpress.


Usage:
  gitpress preview [--out <dir>] [<directory>] [<address>]
  gitpress build [-q] [--out <dir>] [<directory>]
  gitpress init [-q] [<directory>]
  gitpress themes [use <theme> | install <theme> | uninstall <theme>]
  gitpress plugins [add <plugin> | remove [-f] <plugin>]

Options:
  -h --help         Show this help.
  --version         Show version.
  -o --out <dir>    The directory to output the rendered site.
  -f                Force the command to continue without prompting.
  -q                Quiet mode, suppress all messages except errors.

Notes:
  <address> can take the form <host>[:<port>] or just <port>.
"""

import os
import sys
from docopt import docopt
from path_and_address import resolve, split_address
from .config import ConfigSchemaError
from .repository import init, RepositoryAlreadyExistsError, RepositoryNotFoundError
from .previewing import preview
from .building import build
from .themes import list_themes, use_theme, ThemeNotFoundError
from .plugins import list_plugins, add_plugin, remove_plugin, get_plugin_settings
from .helpers import yes_or_no
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
        error('No Gitpress repository found at', ex.directory)


def execute(args):
    """Executes the command indicated by the specified parsed arguments."""

    def info(*message):
        """Displays a message unless -q was specified."""
        if not args['-q']:
            print ' '.join(map(str, message))

    if args['init']:
        try:
            repo = init(args['<directory>'])
            info('Initialized Gitpress repository in', repo)
        except RepositoryAlreadyExistsError as ex:
            info('Gitpress repository already exists in', ex.repo)
        return 0

    if args['preview']:
        directory, address = resolve(args['<directory>'], args['<address>'])
        host, port = split_address(address)
        if address and not host and not port:
            error('Invalid address', repr(address))
        return preview(directory, host=host, port=port)

    if args['build']:
        info('Building site', os.path.abspath(args['<directory>'] or '.'))
        out_directory = build(args['<directory>'], args['--out'])
        info('Site built in', os.path.abspath(out_directory))
        return 0

    if args['themes']:
        theme = args['<theme>']
        if args['use']:
            try:
                switched = use_theme(theme)
            except ConfigSchemaError as ex:
                error('Could not modify config:', ex)
                return 1
            except ThemeNotFoundError as ex:
                error('Theme %s is not currently installed.' % repr(theme))
                return 1
            info('Switched to theme %s' if switched else 'Already using %s' % repr(theme))
        elif args['install']:
            # TODO: implement
            raise NotImplementedError()
        elif args['uninstall']:
            # TODO: implement
            raise NotImplementedError()
        else:
            themes = list_themes()
            if themes:
                info('Installed themes:')
                info('  ' + '\n  '.join(themes))
            else:
                info('No themes installed.')
        return 0

    if args['plugins']:
        plugin = args['<plugin>']
        if args['add']:
            try:
                added = add_plugin(plugin)
            except ConfigSchemaError as ex:
                error('Could not modify config:', ex)
                return 1
            info(('Added plugin %s' if added else
                'Plugin %s has already been added.') % repr(plugin))
        elif args['remove']:
            settings = get_plugin_settings(plugin)
            if not args['-f'] and settings and isinstance(settings, dict):
                warning = 'Plugin %s contains settings. Remove?' % repr(plugin)
                if not yes_or_no(warning):
                    return 0
            try:
                removed = remove_plugin(plugin)
            except ConfigSchemaError as ex:
                error('Error: Could not modify config:', ex)
            info(('Removed plugin %s' if removed else
                'Plugin %s has already been removed.') % repr(plugin))
        else:
            plugins = list_plugins()
            info('Installed plugins:\n  ' + '\n  '.join(plugins) if plugins else
                'No plugins installed.')
        return 0

    return 1


def error(*message):
    sys.exit('Error: ' + ' '.join(map(str, message)))


def gpp(argv=None):
    """Shortcut function for running the previewing command."""
    if argv is None:
        argv = sys.argv[1:]
    argv.insert(0, 'preview')
    return main(argv)
