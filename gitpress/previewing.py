import os
from werkzeug.serving import run_simple


def preview(directory=None, host=None, port=None, use_debugger=None):
    """Runs a local server to preview the working directory of a repository."""

    # Defaults
    directory = os.path.abspath(directory or '.')
    if not host:
        host = '127.0.0.1'
    if not port:
        port = 5000

    # Validation
    if not os.path.isdir(directory):
        raise ValueError('Directory not found: ' + repr(directory))

    # Configuration
    os.environ['GITPRESS_BLOG_PREVIEW'] = 'True'
    os.environ['GITPRESS_BLOG_DIRECTORY'] = directory
    os.environ['GITPRESS_BLOG_TITLE'] = os.path.basename(directory).title()

    # TODO: themes
    # Get preview server
    from themes.default import application

    # Run preview server
    run_simple(host, port, application, use_debugger=True, use_reloader=True)
