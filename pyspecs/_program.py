import argparse
from os import getcwd, walk
from sys import __stdout__ as console
from pyspecs._loader import Location, Importer, load_spec_classes
from pyspecs._reporter import ConsoleReporter
from pyspecs import _spec as runner


def main():
    args = parse_args()
    working_dir = getcwd()
    walker = (Location(step) for step in walk(working_dir))
    importer = Importer(working_dir)
    loader = lambda: load_spec_classes(walker, importer)
    reporter = ConsoleReporter(console, verbosity=args.verbosity)
    runner.run_specs(loader, reporter, reporter)
    reporter.finish()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbosity', type=int,
                        help='0 for dots or 1 for full stories')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()