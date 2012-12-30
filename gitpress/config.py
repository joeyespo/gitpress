import os
from collections import OrderedDict
try:
    import simplejson as json
except ImportError:
    import json
from .present import require_repo


config_file = '_config.json'
theme_config_file = 'gitpress_theme.json'


class ConfigSchemaError(Exception):
    """Indicates the config does not conform to the expected types."""
    pass


def content_config(path):
    """Returns the configuration for the specified working directory."""
    return from_file(os.path.join(path, config_file))


def theme_config(path):
    """Returns the configuration for the specified theme directory."""
    return from_file(os.path.join(path, theme_config_file))


def from_file(config_file):
    """Returns the configuration from the specified file."""
    if not os.path.exists(config_file):
        return {}
    with file(config_file, 'r') as f:
        return json.load(f)


def get_value(key):
    """Gets the value of the specified key in the config file."""
    repo = require_repo()
    path = os.path.join(repo, config_file)

    with open(path, 'r') as f:
        config = json.load(f, object_pairs_hook=OrderedDict)
    return config.get(key)


def set_value(key, value, strict=True):
    """Sets the value of a particular key in the config file. This has no effect when setting to the same value."""
    if value is None:
        raise ValueError('Argument "value" must not be None.')
    repo = require_repo()
    path = os.path.join(repo, config_file)

    # Read values and short circuit if no value is effectively being set
    with open(path, 'r') as f:
        config = json.load(f, object_pairs_hook=OrderedDict)
    old = config.get(key)
    if old == value:
        return value

    # Check schema
    if strict and old is not None and not isinstance(old, type(value)):
        raise ConfigSchemaError('Expected config variable %s to be type %s, got %s'
            % (repr(key), repr(type(value)), repr(type(old))))

    # Set new value and save results
    config[key] = value
    contents = json.dumps(config, indent=4, separators=(',', ': ')) + '\n'
    with open(path, 'w') as f:
        f.write(contents)
    return old
