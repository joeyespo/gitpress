"""\
gitpress.presenters.application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Defines a presenter for using a non-Python application to present content with.
"""

from ..presenter import Presenter


class ApplicationPresenter(Presenter):
    """Runs an external application in a separate process to present the content."""
    def __init__(self, repository):
        # TODO: read config to determine if it can also build
        super(ApplicationPresenter, self).__init__(repository, False, False, True, False)
        # TODO: if '' not in self.config: raise
        # TODO: read configuration

    def serve(self):
        """Serves the site."""
        # TODO: os.system(self.config[''])
