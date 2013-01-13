import os
import errno
from collections import OrderedDict
try:
    import simplejson as json
except ImportError:
    import json
from .exceptions import ConfigSchemaError


config_file = '_config.json'


class Config(object):
    """Reads and writes the configuration."""
    def __init__(self, repo_directory, cached=True):
        self.path = os.path.join(repo_directory, config_file)
        self.cached = cached
        self._cache = None

    @staticmethod
    def read_dict(path):
        """Reads the configuration from disk as a dictionary."""
        try:
            with open(path, 'r') as f:
                return json.load(f, object_pairs_hook=OrderedDict)
        except IOError as ex:
            if ex != errno.ENOENT:
                raise
        return {}

    @staticmethod
    def write_dict(path, values):
        """Writes the specified dictionary configuration to disk."""
        contents = json.dumps(values, indent=4, separators=(',', ': ')) + '\n'
        try:
            with open(path, 'w') as f:
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
        values = Config.read_dict(self.path)
        if self.cached:
            self._cache = values
        return values

    def _write(self, values):
        """Writes the configuration to the disk and cache."""
        if self.cached:
            self._cache = values
        Config.write_dict(self.path, values)

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
        """Gets an individual value from the configuration."""
        values = self._read()
        value = values.get(key, default)
        if expect and key in values and not isinstance(value, expect):
            if silent:
                return default
            raise ConfigSchemaError('Expected config variable %s to be type %s, got %s'
                % (repr(key), repr(expect), repr(type(value))))
        return value

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
            return old

        # Check schema
        if strict and old is not None and not isinstance(old, type(value)):
            raise ConfigSchemaError('Expected config variable %s to be type %s, got %s'
                % (repr(key), repr(type(value)), repr(type(old))))

        # Set new value and save results
        values[key] = value
        self._write(values)
        return old

    def read(self, refresh=False):
        """\
        Returns a dictionary of the current configuration.
        Mutating the resulting dictionary will have no effect on this instance.
        """
        if refresh:
            self.invalidate()
        return self._read().copy()

    def write(self, values, overwrite=False, refresh=False):
        """Updates or overwrites the configuration with the specified dictionary."""
        if not overwrite:
            current = self.read(refresh)
            current.update(values)
            values = current
        self._write(values)
