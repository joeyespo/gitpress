"""\
gitpress.presenters
~~~~~~~~~~~~~~~~~~~

Defines the built-in presenters.
"""

from .application import ApplicationPresenter
from .custom import CustomPresenter
from .default import DefaultPresenter


builtin_presenters = {
    'application': ApplicationPresenter,
    'custom': CustomPresenter,
    'default': DefaultPresenter,
}
