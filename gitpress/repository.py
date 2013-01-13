import os
import shutil
import subprocess
from .config import Config
from .exceptions import RepositoryAlreadyExistsError, RepositoryNotFoundError, \
    InvalidRepositoryError
from .building import build
from .templates import default_template, resolve_template


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

    def build(self, out_directory=None, virtualenv=True):
        """Initiates a new isolated build and returns the output directory."""
        # TODO: return self.presenter.build()
        return build(self.directory, out_directory)
