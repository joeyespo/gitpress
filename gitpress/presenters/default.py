"""\
gitpress.presenters.default
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Defines the default presenter that builds the site.
"""

import os
from ..presenter import Presenter


class DefaultPresenter(Presenter):
    """Runs an external application in a separate process to present the content."""
    def __init__(self, repository):
        # TODO: read config
        super(DefaultPresenter, self).__init__(repository)

    def build(self, out_directory=None):
        """Builds the site from its content and presentation repository."""
        out_directory = os.path.abspath(out_directory or Presenter.default_output_directory)

        # Prevent user mistakes
        if out_directory == '.':
            raise ValueError('Output directory must be different than the source directory: ' + repr(out_directory))
        if os.path.basename(os.path.relpath(out_directory, self.repository.content_directory)) == '..':
            raise ValueError('Output directory must not contain the source directory: ' + repr(out_directory))

        # TODO: read config
        # TODO: use virtualenv
        # TODO: init and run plugins
        # TODO: process with active theme

        # TODO: Collect and copy files

        return out_directory
