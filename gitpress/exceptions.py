import os


class RepositoryAlreadyExistsError(Exception):
    """Indicates a Gitpress repository already exists while attempting to create
    a new one."""
    def __init__(self, content_directory, repository_directory):
        content_directory = os.path.abspath(content_directory)
        repository_directory = os.path.abspath(repository_directory)
        super(RepositoryAlreadyExistsError, self).__init__(
            'Gitpress repository already exists in ' + repository_directory)
        self.content_directory = content_directory
        self.repository_directory = repository_directory


class RepositoryNotFoundError(Exception):
    """Indicates an existing Gitpress repository is required, but was not found."""
    def __init__(self, content_directory):
        directory = os.path.abspath(content_directory)
        super(RepositoryNotFoundError, self).__init__(
            'No Gitpress repository found at ' + directory)
        self.directory = directory


class InvalidRepositoryError(Exception):
    """Indicates a Gitpress repository was found, but not valid."""
    def __init__(self, repository_directory, message):
        super(InvalidRepositoryError, self).__init__(message)
        self.directory = os.path.abspath(repository_directory)


class ConfigSchemaError(Exception):
    """Indicates the configuration does not conform to the expected types."""
    def __init__(self, message):
        super(ConfigSchemaError, self).__init__(message)


class ThemeNotFoundError(Exception):
    """Indicates the requested theme was not found."""
    def __init__(self, theme):
        super(ThemeNotFoundError, self).__init__(
            'Theme %s is not currently installed.' % repr(theme))
        self.theme = theme


class NotADirectoryError(Exception):
    """Indicates a file was found when a directory was expected."""
    def __init__(self, directory, message=None):
        directory = os.path.abspath(directory)
        super(NotADirectoryError, self).__init__(
            'Expected a directory, found a file instead at ' + directory)
        self.directory = directory


class PresenterNotFoundError(Exception):
    """Indicates a presenter with the given name could not be found."""
    def __init__(self, presenter):
        super(PresenterNotFoundError, self).__init__(
            'Presenter %s could not be found.' % repr(presenter))
        self.presenter = presenter


class BuildUnsupportedError(Exception):
    """Indicates the current presenter does not support building."""
    def __init__(self):
        super(BuildUnsupportedError, self).__init__(
            'The current presenter does not support building.')


class ThemesNotSupportedException(Exception):
    """Indicates the current presenter does not support themes."""
    def __init__(self):
        super(ThemesNotSupportedException, self).__init__(
            'The current presenter does not support themes.')
