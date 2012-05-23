from os import getcwd, walk
from sys import __stdout__ as console
from pyspecs._loader import Location, Importer, load_spec_classes
from pyspecs._reporter import DotReporter
from pyspecs._runner import run_specs


working_dir = getcwd()
walker = (Location(step) for step in walk(working_dir))
importer = Importer(working_dir)
loader = lambda: load_spec_classes(walker, importer)
reporter = DotReporter(console)
run_specs(loader, reporter, reporter)