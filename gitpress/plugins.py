from .config import Config
from .repository import require_repo


def list_plugins(directory=None):
    """Gets a list of the installed themes."""
    repo = require_repo(directory)
    plugins = Config(repo).get('plugins')
    if not plugins or not isinstance(plugins, dict):
        return None
    return plugins.keys()


def add_plugin(plugin, directory=None):
    """Adds the specified plugin. This returns False if it was already added."""
    repo = require_repo(directory)
    plugins = Config(repo).get('plugins', expect_type=dict)
    if plugin in plugins:
        return False

    plugins[plugin] = {}
    Config(repo).set('plugins', plugins)
    return True


def remove_plugin(plugin, directory=None):
    """Removes the specified plugin."""
    repo = require_repo(directory)
    plugins = Config(repo).get('plugins', expect_type=dict)
    if plugin not in plugins:
        return False

    del plugins[plugin]
    Config(repo).set('plugins', plugins)
    return True


def get_plugin_settings(plugin, directory=None):
    """Gets the settings for the specified plugin."""
    repo = require_repo(directory)
    plugins = Config(repo).get('plugins')
    return plugins.get(plugin) if isinstance(plugins, dict) else None
