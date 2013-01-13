import os
import shutil
import subprocess
from .config import Config
from .exceptions import RepositoryAlreadyExistsError, RepositoryNotFoundError, \
    InvalidRepositoryError, ThemeNotFoundError
from .templates import default_template, resolve_template
from .plugin import PluginRequirement


class Repository(object):
    """A Gitpress repository, which manages the containing Site."""
    def __init__(self, directory=None, content_directory=None, presenter=None):
        if directory is None:
            directory = '.'
        if content_directory is None:
            content_directory = os.path.join(directory, '..')
        directory = os.path.abspath(directory)
        content_directory = os.path.abspath(content_directory)
        config_file = os.path.join(directory, Config.config_file)

        if not os.path.isdir(directory):
            raise RepositoryNotFoundError(directory)
        if not os.path.exists(config_file):
            raise InvalidRepositoryError(directory, 'Config file not found: ' + config_file)

        config = Config(config_file)

        self.directory = directory
        self.content_directory = content_directory
        self.config = config
        self.presenter = presenter

    default_directory = '.gitpress'
    themes_directory = 'themes'
    default_theme = 'default'

    @staticmethod
    def from_content(content_directory=None, repo_directory=None, presenter=None):
        """Returns the repository of the specified content directory."""
        repo_directory = Repository.resolve(content_directory, repo_directory)
        return Repository(repo_directory, content_directory, presenter)

    @staticmethod
    def resolve(content_directory=None, repo_directory=None):
        """Resolves the repository directory from the specified locations."""
        if content_directory is None:
            content_directory = '.'
        if repo_directory is None:
            repo_directory = Repository.default_directory
        return os.path.join(content_directory, repo_directory)

    @staticmethod
    def init(self, content_directory=None, repo_directory=None, template=None):
        """\
        Initializes a new Gitpress repository by copying the files from the
        specified template, and returns the resulting Repository.
        The template can be a template name or an absolute path.
        """
        if template is None:
            template = default_template
        repo_directory = Repository.resolve(content_directory, repo_directory)

        if os.path.isdir(repo_directory):
            raise RepositoryAlreadyExistsError(content_directory, repo_directory)

        # Initialize repository with specified template
        template_path = resolve_template(template)
        shutil.copytree(template_path, repo_directory)

        # Copy over the requested template files
        message = '"Add %s presentation content."' % (template
            if template == default_template else repr(template))
        subprocess.call(['git', 'init', '-q', repo_directory])
        subprocess.call(['git', 'add', '.'], cwd=repo_directory)
        subprocess.call(['git', 'commit', '-q', '-m', message], cwd=repo_directory)

        return Repository(repo_directory, content_directory)

    @staticmethod
    def clone(self, content_directory, url):
        """Clones an existing repository to specified location."""
        # TODO: implement
        raise NotImplementedError()

    def preview(self, host=None, port=None):
        # TODO: return self.presenter.preview()
        from .previewer import preview
        return preview(self.content_directory, host, port)

    def build(self, out_directory=None, virtualenv=True):
        """Initiates a new isolated build and returns the output directory."""
        # TODO: return self.presenter.build()
        from .building import build
        return build(self.content_directory, out_directory)

    def plugins(self):
        """Gets a list of the installed themes."""
        plugins = self.config.get('plugins', {}, expect=dict, silent=True)
        return [PluginRequirement(plugin, plugins[plugin]) for plugin in plugins]

    def add_plugin(self, plugin):
        """Adds the specified plugin. This returns False if it was already added."""
        plugins = self.config.get('plugins', {}, expect=dict)
        if plugin in plugins:
            return False

        plugins[plugin] = {}
        self.config.set('plugins', plugins)
        return True

    def remove_plugin(self, plugin):
        """Removes the specified plugin."""
        plugins = self.config.get('plugins', {}, expect=dict)
        if plugin not in plugins:
            return False

        del plugins[plugin]
        self.config.set('plugins', plugins)
        return True

    def themes(self):
        """Gets a list of the installed themes."""
        path = os.path.join(self.directory, Repository.themes_directory)
        return os.listdir(path) if os.path.isdir(path) else None

    def use_theme(self, theme):
        """Switches to the specified theme. This returns False if switching to the already active theme."""
        if theme not in self.themes():
            raise ThemeNotFoundError(theme)
        return self.config.set('theme', theme) != theme

    def install_theme(self, theme):
        # TODO: implement
        raise NotImplementedError()

    def uninstall_theme(self, theme):
        # TODO: implement
        raise NotImplementedError()
