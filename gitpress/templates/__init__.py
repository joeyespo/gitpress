"""\
gitpress.templates
~~~~~~~~~~~~~~~~~~

Defines the built-in templates.
"""

import os


templates_directory = os.path.dirname(__file__)
default_template = 'default'
builtin_templates = [
    'default',
    'external',
]


def resolve_template(name=None):
    """\
    Returns the path to the specified template name.
    Note that name can also be an absolute path.
    If a template is not found or the path does not exist, None is returned.
    """
    if name is None:
        name = default_template
    if not os.path.isabs(name):
        name = os.path.join(templates_directory, name)
    return name if os.path.exists(name) else None
