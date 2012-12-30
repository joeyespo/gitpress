import os
from .present import require_repo


themes_dir = '_themes'
default_theme = 'default'


def list_themes():
    """Gets a list of the installed themes."""
    repo = require_repo()
    path = os.path.join(repo, themes_dir)
    return os.listdir(path) if os.path.isdir(path) else None
