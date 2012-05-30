import argparse
from os import getcwd, walk
from sys import __stdout__ as console
import sys
from pyspecs._loader import Location, Importer, load_spec_classes
from pyspecs._reporter import ConsoleReporter
from pyspecs import _spec as runner


def main():
    args = parse_args()
    working_dir = getcwd()
    sys.path.append(working_dir)
    walker = (Location(step) for step in walk(working_dir))
    importer = Importer(working_dir)
    loader = lambda: load_spec_classes(walker, importer)
    reporter = ConsoleReporter(console, verbose=args.verbosity == 'story')
    runner.run_specs(loader, reporter, reporter)
    reporter.finish()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbosity', default='dot',
                        help="'dot' or 'story'")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()