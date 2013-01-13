from .plugin import Plugin
from .exceptions import PresenterNotFoundError, BuildUnsupportedError, \
    ThemesNotSupportedException


class Presenter(Plugin):
    """Interprets the directory to present the site."""
    def __init__(self, repository, supports_themes=True, custom_server=False, custom_build=False):
        super(Presenter, self).__init__()
        self.repository = repository
        self.supports_themes = supports_themes
        self.custom_server = custom_server
        self.custom_build = custom_build

    default_presenter = 'default'

    @staticmethod
    def resolve(presenter=None):
        """\
        Returns a presenter object from the specified name.
        If a Presenter object is provided, it will be returned.
        The default presenter is 'default'.
        """
        from .presenters import builtin_presenters
        if presenter is None:
            presenter = Presenter.default_presenter
        if isinstance(presenter, Presenter):
            return presenter
        if not isinstance(presenter, basestring):
            raise TypeError('Presenter expected to be a string or a Presenter object, got %s.' % repr(type(presenter)))
        if presenter in builtin_presenters:
            return builtin_presenters[presenter]()
        # TODO: resolve import names
        raise PresenterNotFoundError(presenter)

    @property
    def is_static(self):
        """Returns whether the presenter generates static sites."""
        return self.custom_server is None

    @property
    def can_build(self):
        """Returns whether the presenter can build."""
        return self.is_static or self.custom_build

    def ensure_build(self):
        """Raises an exception if the presenter does not support builds."""
        if not self.can_build:
            raise BuildUnsupportedError()

    def ensure_themes(self):
        """Raises an exception if the presenter does not support themes."""
        if not self.supports_themes:
            raise ThemesNotSupportedException()

    def build(self, out_directory=None):
        """Initiates a new isolated build and returns the output directory."""
        self.ensure_build()
        return out_directory

    def read(self):
        """Reads the presentation directory."""
        # TODO: implement
        raise NotImplementedError()
