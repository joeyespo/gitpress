import os
from .repository import require_repo, presentation_files
from .helpers import copy_files, remove_directory


default_out_directory = '_site'


def build(directory=None, out_directory=None):
    """Builds the site from its content and presentation repository."""
    directory = directory or '.'
    out_directory = os.path.abspath(out_directory or default_out_directory)
    repo = require_repo(directory)

    # Prevent user mistakes
    if out_directory == '.':
        raise ValueError('Output directory must be different than the source directory: ' + repr(out_directory))
    if os.path.basename(os.path.relpath(out_directory, directory)) == '..':
        raise ValueError('Output directory must not contain the source directory: ' + repr(out_directory))

    # TODO: read config
    # TODO: use virtualenv
    # TODO: init and run plugins
    # TODO: process with active theme

    # Collect and copy static files
    files = presentation_files(repo)
    remove_directory(out_directory)
    copy_files(files, out_directory, repo)

    return out_directory
