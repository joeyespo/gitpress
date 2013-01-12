import os


class RepositoryAlreadyExistsError(Exception):
    """Indicates a Gitpress repository already exists while attempting to create
    a new one."""
    def __init__(self, content_directory, repository_directory):
        super(RepositoryAlreadyExistsError, self).__init__()
        self.content_directory = os.path.abspath(content_directory)
        self.repository_directory = os.path.abspath(repository_directory)


class RepositoryNotFoundError(Exception):
    """Indicates an existing Gitpress repository is required, but was not found."""
    def __init__(self, content_directory):
        super(RepositoryNotFoundError, self).__init__()
        self.directory = os.path.abspath(content_directory)


class ConfigSchemaError(Exception):
    """Indicates the configuration does not conform to the expected types."""
    pass


class ThemeNotFoundError(Exception):
    """Indicates the requested theme was not found."""
    def __init__(self, theme):
        super(ThemeNotFoundError, self).__init__()
        self.theme = theme


class NotADirectoryError(Exception):
    """Indicates a file was found when a directory was expected."""
    def __init__(self, directory, message=None):
        super(NotADirectoryError, self).__init__(
            'Expected a directory, found a file instead at ' + directory)
        self.directory = os.path.abspath(directory)
