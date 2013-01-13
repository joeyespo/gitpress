"""\
gitpress.presenters
~~~~~~~~~~~~~~~~~~~

Defines the built-in presenters.
"""

from .custom import CustomPresenter
from .default import DefaultPresenter


builtin_presenters = {
    'custom': CustomPresenter,
    'default': DefaultPresenter,
}
