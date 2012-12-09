import os
import misaka as m
from flask import Flask, render_template, abort


def preview(working_directory=None, host=None, port=None):
    """Runs a local server to preview the working directory of a repository."""

    # Check for working directory
    if working_directory and not os.path.isdir(working_directory):
        raise ValueError('Directory not found: ' + repr(working_directory))

    # Flask application
    app = Flask('gitpress')
    app.config.from_pyfile('default_config.py')
    app.config.from_pyfile('local_config.py', silent=True)

    # Override default configuration
    config = {'HOST': host, 'PORT': port, 'WORKING_DIRECTORY': working_directory}
    app.config.update((k, v) for k, v in config.iteritems() if v is not None)

    # Shared values
    working_directory = os.path.abspath(app.config['WORKING_DIRECTORY'])
    site_title = os.path.basename(working_directory).title()
    pages = _pages(working_directory)

    # Views
    @app.route('/')
    def index(slug=None):
        return render_template('index.html', site_title=site_title, pages=pages)

    @app.route('/<path:slug>')
    def page(slug):
        page = _page_for(pages, slug)
        # TODO: use Gitpress rules and Git for validation
        if not page:
            abort(404)
        return render_template('page.html', site_title=site_title, page=page)

    # Run local server
    app.run(app.config['HOST'], app.config['PORT'], debug=app.debug, use_reloader=app.config['DEBUG_GITPRESS'])


class _Page:
    """Represents a named or unordered page."""
    def __init__(self, root, path):
        self.root = root
        self.path = path
        self.fullpath = os.path.join(root, path)
        self.filename = os.path.basename(path)
        # TODO: use Gitpress with settings to transform paths into URLs
        self.url = _slugify(self.filename)
        self.title = self.url.replace('-', ' ').title()
        self.content = _read_file(self.fullpath)
        # TODO: Use smarter content cutoff
        self.summary = m.html(self.content[:300])
        self.content = m.html(self.content)


def _page_for(pages, slug):
    """Gets a page from the specified slug."""
    for page in pages:
        if page.url == slug:
            return page
    return None


def _read_file(path):
    """Reads a file and closes it."""
    with open(path) as f:
        return f.read()


def _slugify(path):
    """Returns a slug from the specified path."""
    path = os.path.normpath(path)
    path = os.path.splitext(path)[0]
    return '-'.join(path.split('-')[1:])


def _ordered_pages(path):
    """Returns all the ordered pages from the specified site."""
    # TODO: use Gitpress rules for page iteration
    posts = []
    for root, dirs, files in os.walk(path):
        if not _is_post_path(os.path.relpath(root, path)):
            continue
        posts += [os.path.join(root, filename) for filename in files if _starts_with_digit(filename)]
    return posts


def _named_pages(path):
    """Returns all the named pages from the specified site."""
    # TODO: get named pages
    return []


def _pages(path):
    """Gets a list of available named and ordered pages."""
    page_paths = _ordered_pages(path) + _named_pages(path)
    return map(lambda page_path: _Page(path, page_path), page_paths)


def _starts_with_digit(s):
    """Returns whether the specified string starts with a digit."""
    return len(s) > 1 and s[0].isdigit()


def _is_post_path(path):
    """Returns whether the specified path is valid for a post."""
    while path:
        path, directory = os.path.split(path)
        if not _starts_with_digit(directory):
            return False
    return True
