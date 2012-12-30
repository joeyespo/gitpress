from .config import get_value, set_value


def list_plugins():
    """Gets a list of the installed themes."""
    plugins = get_value('plugins')
    if not plugins or not isinstance(plugins, dict):
        return None
    return plugins.keys()


def add_plugin(plugin):
    """Adds the specified plugin. This returns False if it was already added."""
    plugins = get_value('plugins', dict)
    if plugin in plugins:
        return False

    plugins[plugin] = {}
    set_value('plugins', plugins)
    return True


def remove_plugin(plugin):
    """Removes the specified plugin."""
    plugins = get_value('plugins', dict)
    if plugin not in plugins:
        return False

    del plugins[plugin]
    set_value('plugins', plugins)
    return True
