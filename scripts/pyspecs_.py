#!python


import os
import sys
from pyspecs import _step_runner


def main():
    working = os.getcwd()
    sys.path.append(working)
    _step_runner.load_steps(working)


if __name__ == '__main__':
    main()