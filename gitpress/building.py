import os
import shutil
import tempfile
from git import Repo
from .config import content_config
from .helpers import copy_file_tree


default_theme_path = os.path.join(os.path.dirname(__file__), 'themes', 'default')


def build(directory=None, out_directory=None):
    """Builds the website, given the content and site configuration."""

    # Defaults
    if not directory:
        directory = '.'
    if not out_directory:
        out_directory = '_site'

    # Normalize
    directory = os.path.abspath(directory)
    out_directory = os.path.relpath(out_directory, directory)

    # Validate
    if not os.path.isdir(directory):
        raise ValueError('Directory not found: ' + repr(directory))
    if out_directory == '.':
        raise ValueError('Output directory must be different than the working directory: ' + repr(out_directory))

    # Configure
    config = content_config(directory)
    theme_source = config.get('theme')
    theme_branch = config.get('theme_branch')
    if theme_branch and not theme_source:
        theme_source = '.'

    # TODO: get installed themes
    installed_themes = []

    # TODO: optimize by directly using the directory where possible
    temp_theme_path = create_temp_dir()
    try:
        # Cache theme
        if theme_source in installed_themes:
            # TODO: use installed theme
            raise NotImplementedError()
        elif theme_source:
            theme_source = os.path.abspath(theme_source)
            repo = Repo.clone_from(theme_source, temp_theme_path)
            if theme_branch:
                if theme_branch in repo.heads:
                    repo.heads[theme_branch].checkout()
                else:
                    print 'Warning: No branch "%s"' % theme_branch
        else:
            copy_file_tree(default_theme_path, temp_theme_path)
        # TODO: implement
    finally:
        try:
            shutil.rmtree(temp_theme_path)
        except Exception as ex:
            print 'Warning: Could not clean up theme cache directory (%s)' % temp_theme_path
            print '        ', ex


def create_temp_dir():
    """Creates a new temporary directory and normalizes the resulting path, as necessary on Windows."""
    temp_dir = tempfile.mkdtemp()
    try:
        from ctypes import windll, create_string_buffer
        buf = create_string_buffer(500)
        rv = windll.kernel32.GetLongPathNameA(temp_dir, buf, 500)
        return buf.value if rv else temp_dir
    except Exception as ex:
        print ex
        return temp_dir
