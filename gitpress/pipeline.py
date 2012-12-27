import os
import errno
import shutil
import tempfile


def run(content_url=None, presentation_url=None, target_path=None):
    """Runs the Gitpress Pipeline on over the specified content and theme repositories."""
    is_temp = target_path is None

    if is_temp:
        target_path = tempfile.mkdtemp()
    elif not os.path.isdir(target_path):
            raise ValueError('Target directory not found: ' + repr(target_path))
    elif not os.listdir(target_path):
            raise ValueError('Target directory not empty: ' + repr(target_path))

    target_path = os.path.abspath(target_path)
    try:
        _apply_pipeline(target_path, content_url, presentation_url)
    finally:
        if is_temp:
            shutil.rmtree(target_path)


def _apply_pipeline(path, content_url, presentation_url):
    """Applies the Gitpress Pipeline."""

    # TODO: Try presentation_url with git first
    _copydir(presentation_url, os.path.join(path, 'presentation'))
    
    # TODO: Read presentation config

    if not os.path.isdir(content_url):
        raise ValueError('Content directory not found: ' + repr(content_url))

    # TODO: Try content_url with git first, or use it directly if it is a directory
    _copydir(content_url, os.path.join(path, 'content'))

    #site_title = os.path.basename(working_directory).title()
    #pages = _pages(working_directory)


def _copydir(source, dest):
    """Copies the contents of one directory to another."""
    try:
        shutil.copytree(source, dest)
    except OSError as exc:
        if exc.errno != errno.ENOTDIR:
            raise
        shutil.copy(source, dest)
