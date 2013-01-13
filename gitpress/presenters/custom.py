"""\
gitpress.presenters.custom
~~~~~~~~~~~~~~~~~~~~~~~~~~

Allows external Python scripts to present the content.
"""

from ..presenter import Presenter


class CustomPresenter(Presenter):
    """Runs an external application in a separate process to present the content."""
    def __init__(self, repository):
        # TODO: read config to determine if it can also build, defaulted to False
        super(CustomPresenter, self).__init__(repository)

    def build(self):
        """Delegates the build process to a custom Python script."""
        # TODO: os.system(self.config[''])

    def serve(self):
        """Delegates the server to a custom Python script."""
        # TODO: os.system(self.config[''])
