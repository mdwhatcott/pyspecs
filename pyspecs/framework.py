from ._should import _Should
from ._step import StepFactory


given = StepFactory('given')
provided = StepFactory('provided')
at = StepFactory('at')
when = StepFactory('when')
and_ = StepFactory('and')
then = StepFactory('then')
so = StepFactory('so')
therefore = StepFactory('therefore')
however = StepFactory('however')
as_well_as = StepFactory('as well as')

the = _Should
it = _Should
this = _Should
that = _Should


def framework():
    return dict(
        given=given,
        provided=provided,
        at=at,
        when=when,
        and_=and_,
        then=then,
        so=so,
        therefore=therefore,
        however=however,
        as_well_as=as_well_as,
        the=the,
        it=it,
        this=this,
        that=that,
    )
