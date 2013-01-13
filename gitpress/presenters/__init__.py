"""\
gitpress.presenters
~~~~~~~~~~~~~~~~~~~

Defines the built-in presenters.
"""

from .default import DefaultPresenter


builtin_presenters = {
    'default': DefaultPresenter,
}
