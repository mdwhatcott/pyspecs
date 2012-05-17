from os import getcwd, walk
from pyspecs._loader import SpecLoader, Location, Importer
from pyspecs._reporter import DotReporter
from pyspecs._runner import SpecRunner


working_dir = getcwd()
walker = (Location(step) for step in walk(working_dir))
importer = Importer(working_dir)
loader = SpecLoader(walker, importer)
reporter = DotReporter()


SpecRunner(loader, reporter).run_specs()