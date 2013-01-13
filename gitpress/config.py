import errno
from copy import deepcopy
from collections import OrderedDict
try:
    import simplejson as json
except ImportError:
    import json
from .exceptions import ConfigSchemaError


class Config(object):
    """Reads and writes configuration files."""
    def __init__(self, config_file, cached=True):
        # TODO: validate file
        self.config_file = config_file
        self.cached = cached
        self._cache = None

    config_file = '_config.json'
    theme_config_file = 'theme.json'

    @staticmethod
    def read_dict(config_file):
        """Reads the configuration from disk as a dictionary."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f, object_pairs_hook=OrderedDict)
        except IOError as ex:
            if ex != errno.ENOENT:
                raise
        return {}

    @staticmethod
    def write_dict(config_file, values):
        """Writes the specified dictionary configuration to disk."""
        contents = json.dumps(values, indent=4, separators=(',', ': ')) + '\n'
        try:
            with open(config_file, 'w') as f:
                f.write(contents)
            return True
        except IOError as ex:
            if ex != errno.ENOENT:
                raise
        return False

    def _read(self):
        """Reads or re-reads the configuration if out of date."""
        if self._cache is not None:
            return self._cache
        values = Config.read_dict(self.config_file)
        if self.cached:
            self._cache = values
        return values

    def _write(self, values):
        """Writes the configuration to the disk and cache."""
        if self.cached:
            self._cache = values
        Config.write_dict(self.config_file, values)

    def invalidate(self):
        """Invalidates the cache, causing it to reload on the next read."""
        self._cache = None

    def refresh(self):
        """\
        Refreshes the cache by reloading the values from disk.
        This call has no effect if caching is turned off.
        """
        if not self.caching:
            return
        self.invalidate()
        self._read()

    def get(self, key, default=None, expect=None, silent=False):
        """\
        Gets an individual value from the configuration, or default if not found.
        If expect is given and the value is not an instance of 'expect', an
        exception is raised. If silent is given, the default is returned instead of
        raising an exception.
        """
        values = self._read()
        value = values.get(key, default)
        if expect and key in values and not isinstance(value, expect):
            if silent:
                return default
            raise ConfigSchemaError('Expected config variable %s to be type %s, got %s'
                % (repr(key), repr(expect), repr(type(value))))
        return deepcopy(value) if self.cached else value

    def set(self, key, value, strict=True):
        """\
        Writes an individual value from the configuration and return the old value.
        This has no effect when setting to the same value.
        """
        if value is None:
            raise ValueError('Argument "value" must not be None.')

        # Read values and do nothing if not making any changes
        values = self._read()
        old = values.get(key)
        if old == value:
            return deepcopy(old) if self.cached else old

        # Check schema
        if strict and old is not None and not isinstance(old, type(value)):
            raise ConfigSchemaError('Expected config variable %s to be type %s, got %s'
                % (repr(key), repr(type(value)), repr(type(old))))

        # Set new value and save results
        values[key] = value
        self._write(values)
        return deepcopy(old) if self.cached else old

    def read(self, refresh=False):
        """\
        Returns a dictionary of the current configuration.
        Mutating the resulting dictionary will have no effect on this instance.
        """
        if refresh:
            self.invalidate()
        values = self._read()
        return deepcopy(values) if self.cached else values

    def write(self, values, overwrite=False, overwrite_refreshed=False):
        """Updates or overwrites the configuration with the specified dictionary."""
        if not overwrite:
            current = self.read(overwrite_refreshed)
            current.update(values)
            values = current
        self._write(values)
