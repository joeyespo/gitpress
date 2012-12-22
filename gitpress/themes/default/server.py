import os
from flask import Flask, render_template, abort
from helper import pages, page_for


# Flask application
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = os.environ.get('GITPRESS_BLOG_PREVIEW') in ['true', 'True']
app.config['BLOG_TITLE'] = os.environ.get('GITPRESS_BLOG_TITLE', '')
app.config['BLOG_DIRECTORY'] = os.environ.get('GITPRESS_BLOG_DIRECTORY', '.')
app.config['BLOG_PAGES'] = pages(os.environ.get('GITPRESS_BLOG_DIRECTORY', '.'))
application = app.wsgi_app


# Views
@app.route('/')
def index(slug=None):
    return render_template('index.html', site_title=app.config['BLOG_TITLE'], pages=app.config['BLOG_PAGES'])


@app.route('/<path:slug>')
def page(slug):
    page = page_for(app.config['BLOG_PAGES'], slug)
    # TODO: use Gitpress rules and Git for validation
    if not page:
        abort(404)
    return render_template('page.html', site_title=app.config['BLOG_TITLE'], page=page)
