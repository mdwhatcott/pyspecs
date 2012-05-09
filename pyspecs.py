# Optional: Idle (run on any change to .py files)

from os import getcwd, walk
from pyspecs.loader import SpecLoader, Location, Importer
from pyspecs.runner import SpecRunner

working_dir = getcwd()

SpecRunner(
    SpecLoader(
        (Location(step) for step in walk(working_dir)),
        Importer(working_dir)),
    None  #    TerseConsoleReporter()
).run_specs()