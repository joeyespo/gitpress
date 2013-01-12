import os
import errno
from collections import OrderedDict
try:
    import simplejson as json
except ImportError:
    import json
from .exceptions import ConfigSchemaError


config_file = '_config.json'


def read_config(repo_directory):
    """Returns the configuration from the presentation repository."""
    return read_config_file(os.path.join(repo_directory, config_file))


def read_config_file(path):
    """Returns the configuration from the specified file."""
    try:
        with open(path, 'r') as f:
            return json.load(f, object_pairs_hook=OrderedDict)
    except IOError as ex:
        if ex != errno.ENOENT:
            raise
    return {}


def write_config(repo_directory, config):
    """Writes the specified configuration to the presentation repository."""
    return write_config_file(os.path.join(repo_directory, config_file), config)


def write_config_file(path, config):
    """Writes the specified configuration to the specified file."""
    contents = json.dumps(config, indent=4, separators=(',', ': ')) + '\n'
    try:
        with open(path, 'w') as f:
            f.write(contents)
        return True
    except IOError as ex:
        if ex != errno.ENOENT:
            raise
    return False


def get_value(repo_directory, key, expect_type=None):
    """Gets the value of the specified key in the config file."""
    config = read_config(repo_directory)
    value = config.get(key)
    if expect_type and value is not None and not isinstance(value, expect_type):
        raise ConfigSchemaError('Expected config variable %s to be type %s, got %s'
            % (repr(key), repr(expect_type), repr(type(value))))
    return value


def set_value(repo_directory, key, value, strict=True):
    """Sets the value of a particular key in the config file. This has no effect when setting to the same value."""
    if value is None:
        raise ValueError('Argument "value" must not be None.')

    # Read values and do nothing if not making any changes
    config = read_config(repo_directory)
    old = config.get(key)
    if old == value:
        return old

    # Check schema
    if strict and old is not None and not isinstance(old, type(value)):
        raise ConfigSchemaError('Expected config variable %s to be type %s, got %s'
            % (repr(key), repr(type(value)), repr(type(old))))

    # Set new value and save results
    config[key] = value
    write_config(repo_directory, config)
    return old
