import os
from _runner import (
    given,
    provided,
    at,
    when,
    and_,
    then,
    so,
    therefore,
    however,
    as_well_as,
    the,
    it,
    this,
    _runner
)


__version__ = '2.0'


if __name__ == '__main__':
    _runner.load_steps(os.getcwd())