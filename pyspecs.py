# Done: setup.py
# TODO: test installation and usage (bowling game)
# TODO: catalog bowling game example
# TODO: documentation
# TODO: decide on name and location on github
# TODO: publish to pypi


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


def main():
    _runner.load_steps(os.getcwd())


if __name__ == '__main__':
    main()
