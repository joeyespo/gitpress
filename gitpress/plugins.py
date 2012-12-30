from .config import get_value


def list_plugins():
    """Gets a list of the installed themes."""
    plugins = get_value('plugins')
    if not plugins or not isinstance(plugins, dict):
        return None
    return plugins.keys()
