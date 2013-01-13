import os
from .repository import Repository


default_out_directory = '_site'


def build(content_directory=None, out_directory=None):
    """Builds the site from its content and presentation repository."""
    content_directory = content_directory or '.'
    out_directory = os.path.abspath(out_directory or default_out_directory)
    repo = Repository.from_content(content_directory)

    # Prevent user mistakes
    if out_directory == '.':
        raise ValueError('Output directory must be different than the source directory: ' + repr(out_directory))
    if os.path.basename(os.path.relpath(out_directory, repo.content_directory)) == '..':
        raise ValueError('Output directory must not contain the source directory: ' + repr(out_directory))

    # TODO: read config
    # TODO: use virtualenv
    # TODO: init and run plugins
    # TODO: process with active theme

    # TODO: Collect and copy files

    return out_directory
