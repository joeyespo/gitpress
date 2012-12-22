import os
from werkzeug.serving import run_simple


def preview(working_directory=None, host=None, port=None, use_debugger=None):
    """Runs a local server to preview the working directory of a repository."""

    # Validation
    if working_directory and not os.path.isdir(working_directory):
        raise ValueError('Directory not found: ' + repr(working_directory))

    # Defaults
    working_directory = os.path.abspath(working_directory or '.')
    if not host:
        host = '127.0.0.1'
    if not port:
        port = 5000

    # Configuration
    os.environ['GITPRESS_BLOG_PREVIEW'] = 'True'
    os.environ['GITPRESS_BLOG_DIRECTORY'] = working_directory
    os.environ['GITPRESS_BLOG_TITLE'] = os.path.basename(working_directory).title()

    # TODO: themes
    # Get preview server
    from themes.default import application

    # Run preview server
    run_simple(host, port, application, use_debugger=True, use_reloader=True)
