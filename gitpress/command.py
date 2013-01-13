"""\
gitpress.command
~~~~~~~~~~~~~~~~

Implements the command-line interface of Gitpress.


Usage:
  gitpress preview [<directory>] [<address>]
  gitpress build [-q] [--out <dir>] [<directory>]
  gitpress init [-q] [<directory>]
  gitpress plugins [add <plugin> | remove [-f] <plugin>]  [<directory>]
  gitpress themes [use <theme> | install <theme> | uninstall <theme>] [<directory>]

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
from .exceptions import RepositoryAlreadyExistsError, RepositoryNotFoundError, ConfigSchemaError, ThemeNotFoundError, NotADirectoryError
from .repository import Repository
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
        return execute(args)
    except NotADirectoryError as ex:
        error(ex)
    except RepositoryNotFoundError as ex:
        error(ex)
    except ConfigSchemaError as ex:
        error(ex, header='Config schema error')


def execute(args):
    """Executes the command indicated by the specified parsed arguments."""

    def info(*message):
        """Displays a message unless -q was specified."""
        if not args['-q']:
            print ' '.join(map(str, message))

    if args['init']:
        try:
            repo = Repository.init(args['<directory>'])
            info('Initialized Gitpress repository in', repo.directory)
        except RepositoryAlreadyExistsError as ex:
            info(ex)
        return 0

    if args['preview']:
        directory, address = resolve(args['<directory>'], args['<address>'])
        host, port = split_address(address)
        if address and not host and not port:
            error('Invalid address', repr(address))
        repo = Repository.from_content(directory)
        return repo.preview(host=host, port=port)

    repo = Repository.from_content(args['<directory>'])

    if args['build']:
        info('Building site', os.path.abspath(args['<directory>'] or '.'))
        out_directory = repo.build(args['--out'])
        info('Site built in', os.path.abspath(out_directory))
        return 0

    if args['plugins']:
        plugin = args['<plugin>']
        if args['add']:
            added = repo.add_plugin(plugin)
            info(('Added plugin %s' if added
                else 'Plugin %s has already been added.') % repr(plugin))
        elif args['remove']:
            plugins = repo.plugins()
            settings = plugins[plugin].settings if plugin in plugins else None
            if not args['-f'] and settings and isinstance(settings, dict):
                warning = 'Plugin %s contains settings. Remove?' % repr(plugin)
                if not yes_or_no(warning):
                    return 0
            removed = repo.remove_plugin(plugin)
            info(('Removed plugin %s' if removed
                else 'No plugin %s found to remove.') % repr(plugin))
        else:
            plugins = repo.plugins()
            names = [plugin.name for plugin in plugins]
            info('Installed plugins:\n  ' + '\n  '.join(names) if plugins
                else 'No plugins installed.')
        return 0

    if args['themes']:
        theme = args['<theme>']
        if args['use']:
            try:
                switched = repo.use_theme(theme)
            except ThemeNotFoundError as ex:
                error(ex)
                return 1
            info(('Switched to theme %s' if switched
                else 'Already using %s') % repr(theme))
        elif args['install']:
            installed = repo.install_theme(theme)
            info(('Added theme %s' if installed
                else 'Theme %s has already been added.') % repr(theme))
        elif args['uninstall']:
            # TODO: check for settings like with plugins?
            uninstalled = repo.uninstall_theme(theme)
            info(('Removed theme %s' if uninstalled
                else 'No theme %s found to remove.') % repr(theme))
        else:
            themes = repo.themes()
            info('Installed themes:\n  ' + '\n  '.join(themes) if themes
                else 'No themes installed.')
        return 0

    return 1


def error(*message, **kwargs):
    """\
    Displays the specified error message and exits with error code 1.
    If the 'header' keyword argument is provided, it is used instead of 'Error:'.
    """
    sys.exit(kwargs.get('header', 'Error') + ': ' + ' '.join(map(str, message)))


def gpp(argv=None):
    """Shortcut function for running the previewing command."""
    if argv is None:
        argv = sys.argv[1:]
    argv.insert(0, 'preview')
    return main(argv)
