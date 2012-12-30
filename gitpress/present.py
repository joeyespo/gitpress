import os
import subprocess
from .helpers import copy_files


repo_dir = '.gitpress'
config_file = '_config.json'
templates_path = os.path.join(os.path.dirname(__file__), 'templates')
default_template_path = os.path.join(templates_path, 'default')


class RepositoryAlreadyExistsError(Exception):
    """Indicates 'repo_dir' already exists while attempting to create a new one."""
    def __init__(self, directory=None, repo=None):
        super(RepositoryAlreadyExistsError, self).__init__()
        self.directory = os.path.abspath(directory or '.')
        self.repo = repo or repo_path(self.directory)


class RepositoryNotFoundError(Exception):
    """Indicates an existing 'present_dir' is required, but was not found."""
    pass


def require_repo(directory=None):
    """Checks for a presentation repository and raises an exception if not found."""
    if directory and not os.path.isdir(directory):
        raise ValueError('Directory not found: ' + repr(directory))
    repo = repo_path(directory)
    if not os.path.isdir(repo):
        raise RepositoryNotFoundError()
    return repo


def repo_path(directory=None):
    """Gets the presentation repository from the specified directory."""
    return os.path.join(directory or '.', repo_dir)


def init(directory=None):
    """Initializes a Gitpress presentation repository at the specified directory."""
    repo = os.path.abspath(repo_path(directory))
    if os.path.isdir(repo):
        raise RepositoryAlreadyExistsError(directory, repo)

    # Create repository with default template
    copy_files(default_template_path, repo)

    # Initialize repository
    message = '"Default presentation content."'
    subprocess.call(['git', 'init', '-q', repo])
    subprocess.call(['git', 'add', '.'], cwd=repo)
    subprocess.call(['git', 'commit', '-q', '-m', message], cwd=repo)

    return repo
