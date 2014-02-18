#!python


import os
import argparse
from pyspecs import _idle


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pyspecs test runner')
    parser.add_argument('path', nargs='?', default=os.getcwd(),
                        help='Directory to be processed')
    parser.add_argument('-w', '--watch', action='store_true', default=False,
                        help='watch files and run tests under any change')

    args = parser.parse_args()

    if args.watch:
        _idle.watch(args.path)
    else:
        _idle.run(args.path)
