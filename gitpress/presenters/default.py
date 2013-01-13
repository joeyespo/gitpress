"""\
gitpress.presenters.default
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Defines the default presenter that builds the site.
"""

from ..presenter import Presenter


class DefaultPresenter(Presenter):
    """Runs an external application in a separate process to present the content."""
    def __init__(self):
        # TODO: read config
        super(DefaultPresenter, self).__init__()

    def build(self, out_directory=None):
        """Builds the Gitpress site."""
        # TODO: implement
