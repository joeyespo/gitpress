import os
import subprocess


repo_dir = '.gitpress'
config_file = '_config.json'
default_config = """\
{
    "title": "",
    "author": "",
    "theme": "default",
    "plugins": {},
    "include": [],
    "exclude": []
}
"""


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
    if not os.path.isdir(directory):
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

    # Create presentation repository with initial content
    subprocess.call(['git', 'init', '-q', repo])

    with open(os.path.join(repo, config_file), 'w') as f:
        f.write(default_config)
    subprocess.call(['git', 'add', '.'], cwd=repo)
    subprocess.call(['git', 'commit', '-q', '-m', '"Default presentation."'], cwd=repo)

    return repo
