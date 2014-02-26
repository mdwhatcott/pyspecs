import logging
log = logging.getLogger(__name__)

from ._should import _Should
from ._step import StepFactory


def framework(registry):
    return dict(
        given = StepFactory('given', registry),
        provided = StepFactory('provided', registry),
        at = StepFactory('at', registry),
        when = StepFactory('when', registry),
        and_ = StepFactory('and', registry),
        then = StepFactory('then', registry),
        so = StepFactory('so', registry),
        therefore = StepFactory('therefore', registry),
        however = StepFactory('however', registry),
        as_well_as = StepFactory('as well as', registry),

        the = _Should,
        it = _Should,
        this = _Should,
        that = _Should,
        )

