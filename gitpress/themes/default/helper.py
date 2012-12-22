import os
from markdown2 import markdown

# TODO: use Gitpress to transform paths into URLs


class Page:
    """Represents a named or unordered page."""
    def __init__(self, root, path):
        self.root = root
        self.path = path
        self.fullpath = os.path.join(root, path)
        self.filename = os.path.basename(path)
        self.url = slugify(self.filename)
        self.title = self.url.replace('-', ' ').title()
        self.content = read_file(self.fullpath)
        # TODO: Use smarter content cutoff
        self.summary = markdown(self.content[:300])
        self.content = markdown(self.content)


def page_for(pages, slug):
    """Gets a page from the specified slug."""
    for page in pages:
        if page.url == slug:
            return page
    return None


def read_file(path):
    """Reads a file and closes it."""
    with open(path) as f:
        return f.read()


def slugify(path):
    """Returns a slug from the specified path."""
    path = os.path.normpath(path)
    path = os.path.splitext(path)[0]
    return '-'.join(path.split('-')[1:])


def ordered_pages(path):
    """Returns all the ordered pages from the specified site."""
    # TODO: use Gitpress rules for page iteration
    posts = []
    for root, dirs, files in os.walk(path):
        if not is_post_path(os.path.relpath(root, path)):
            continue
        posts += [os.path.join(root, filename) for filename in files if starts_with_digit(filename)]
    return posts


def named_pages(path):
    """Returns all the named pages from the specified site."""
    # TODO: get named pages
    return []


def pages(path):
    """Gets a list of available named and ordered pages."""
    page_paths = ordered_pages(path) + named_pages(path)
    return map(lambda page_path: Page(path, page_path), page_paths)


def starts_with_digit(s):
    """Returns whether the specified string starts with a digit."""
    return len(s) > 1 and s[0].isdigit()


def is_post_path(path):
    """Returns whether the specified path is valid for a post."""
    while path:
        path, directory = os.path.split(path)
        if not starts_with_digit(directory):
            return False
    return True
