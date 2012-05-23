from os import getcwd, walk
import sys
from pyspecs._loader import SpecLoader, Location, Importer
from pyspecs._reporter import DotReporter
from pyspecs._runner import run_specs


working_dir = getcwd()
walker = (Location(step) for step in walk(working_dir))
importer = Importer(working_dir)
loader = SpecLoader(walker, importer)
reporter = DotReporter(sys.__stdout__)
run_specs(loader, reporter, reporter)