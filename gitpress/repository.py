import os
import re
import shutil
import fnmatch
import subprocess


repo_dir = '.gitpress'
templates_path = os.path.join(os.path.dirname(__file__), 'templates')
default_template_path = os.path.join(templates_path, 'default')
specials = ['.*', '_*']
specials_re = re.compile('|'.join([fnmatch.translate(x) for x in specials]))


class RepositoryAlreadyExistsError(Exception):
    """Indicates 'repo_dir' already exists while attempting to create a new one."""
    def __init__(self, directory=None, repo=None):
        super(RepositoryAlreadyExistsError, self).__init__()
        self.directory = os.path.abspath(directory if directory else os.getcwd())
        self.repo = os.path.abspath(repo or repo_path(self.directory))


class RepositoryNotFoundError(Exception):
    """Indicates an existing 'present_dir' is required, but was not found."""
    def __init__(self, directory=None):
        super(RepositoryNotFoundError, self).__init__()
        self.directory = os.path.abspath(directory if directory else os.getcwd())


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
    shutil.copytree(default_template_path, repo)

    message = '"Default presentation content."'
    subprocess.call(['git', 'init', '-q', repo])
    subprocess.call(['git', 'add', '.'], cwd=repo)
    subprocess.call(['git', 'commit', '-q', '-m', message], cwd=repo)

    return repo


def presentation_files(path=None, excludes=None, includes=None):
    """Gets a list of the repository presentation files relative to 'path',
    not including themes. Note that 'includes' take priority."""
    return list(iterate_presentation_files(path, excludes, includes))


def iterate_presentation_files(path=None, excludes=None, includes=None):
    """Iterates the repository presentation files relative to 'path',
    not including themes. Note that 'includes' take priority."""

    # Defaults
    if includes is None:
        includes = []
    if excludes is None:
        excludes = []

    # Transform glob patterns to regular expressions
    includes_pattern = r'|'.join([fnmatch.translate(x) for x in includes]) or r'$.'
    excludes_pattern = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'
    includes_re = re.compile(includes_pattern)
    excludes_re = re.compile(excludes_pattern)

    def included(root, name):
        """Returns True if the specified file is a presentation file."""
        full_path = os.path.join(root, name)
        # Explicitly included files takes priority
        if includes_re.match(full_path):
            return True
        # Ignore special and excluded files
        return (not specials_re.match(name)
            and not excludes_re.match(full_path))

    # Get a filtered list of paths to be built
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if included(root, d)]
        files = [f for f in files if included(root, f)]
        for f in files:
            yield os.path.relpath(os.path.join(root, f), path)
