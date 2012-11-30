import os
from flask import Flask


def preview(working_directory=None, host=None, port=None):
    """Runs a local server to preview the working directory of a repository."""

    # Flask application
    app = Flask('gitpress')
    app.config.from_pyfile('default_config.py')
    app.config.from_pyfile('local_config.py', silent=True)

    # Override default configuration
    config = {'HOST': host, 'PORT': port, 'WORKING_DIRECTORY': working_directory}
    app.config.update((k, v) for k, v in config.iteritems() if v is not None)

    # Normalize path
    app.config['WORKING_DIRECTORY'] = _normpath(app.config['WORKING_DIRECTORY'])

    # Views
    @app.route('/')
    @app.route('/<path:slug>')
    def index(slug=None):
        # TODO: implement
        return 'TODO: render %s' % (slug or '/')

    # Run local server
    app.run(app.config['HOST'], app.config['PORT'], debug=app.config['DEBUG'], use_reloader=app.config['DEBUG_GITPRESS'])


def _normpath(path):
    """Normalizes the specified path."""
    return os.path.abspath(os.path.normpath(path))
