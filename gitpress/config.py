import os
try:
    import simplejson as json
except ImportError:
    import json


content_config_file = 'gitpress.json'
theme_config_file = 'gitpress_theme.json'


def content_config(path):
    """Returns the configuration for the specified working directory."""
    return from_file(os.path.join(path, content_config_file))


def theme_config(path):
    """Returns the configuration for the specified theme directory."""
    return from_file(os.path.join(path, theme_config_file))


def from_file(config_file):
    """Returns the configuration from the specified file."""
    if not os.path.exists(config_file):
        return {}
    with file(config_file) as f:
        return json.load(f)
