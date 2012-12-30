import os
import subprocess
from .helpers import copy_files


repo_dir = '.gitpress'
templates_path = os.path.join(os.path.dirname(__file__), 'templates')
default_template_path = os.path.join(templates_path, 'default')


class RepositoryAlreadyExistsError(Exception):
    """Indicates 'repo_dir' already exists while attempting to create a new one."""
    def __init__(self, directory=None, repo=None):
        super(RepositoryAlreadyExistsError, self).__init__()
        self.directory = os.path.abspath(directory) if directory else os.getcwd()
        self.repo = repo or repo_path(self.directory)


class RepositoryNotFoundError(Exception):
    """Indicates an existing 'present_dir' is required, but was not found."""
    def __init__(self, directory=None):
        super(RepositoryNotFoundError, self).__init__()
        self.directory = os.path.abspath(directory) if directory else os.getcwd()


def require_repo(directory=None):
    """Checks for a presentation repository and raises an exception if not found."""
    if directory and not os.path.isdir(directory):
        raise ValueError('Directory not found: ' + repr(directory))
    repo = repo_path(directory)
    if not os.path.isdir(repo):
        raise RepositoryNotFoundError(directory)
    return repo


def repo_path(directory=None):
    """Gets the presentation repository from the specified directory."""
    return os.path.join(directory, repo_dir) if directory else repo_dir


def init(directory=None):
    """Initializes a Gitpress presentation repository at the specified directory."""
    repo = repo_path(directory)
    if os.path.isdir(repo):
        raise RepositoryAlreadyExistsError(directory, repo)

    # Initialize repository with default template
    copy_files(default_template_path, repo)

    message = '"Default presentation content."'
    subprocess.call(['git', 'init', '-q', repo])
    subprocess.call(['git', 'add', '.'], cwd=repo)
    subprocess.call(['git', 'commit', '-q', '-m', message], cwd=repo)

    return repo


def presentation_files(directory=None):
    """Gets a list of the repository presentation files relative to 'directory'."""
    return list(iterate_presentation_files(directory))


def iterate_presentation_files(directory=None):
    """Iterates the repository presentation files relative to 'directory'."""
    repo = require_repo(directory)
    for root, dirs, files in os.walk(repo):
        for f in files:
            yield os.path.join(root, f)
