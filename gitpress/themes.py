import os
from .present import require_repo


themes_dir = '_themes'
default_theme = 'default'


def list_themes():
    """Gets a list of the installed themes."""
    repo = require_repo()
    themes = os.path.join(repo, themes_dir)
    return os.listdir(themes) if os.path.isdir(themes) else None
