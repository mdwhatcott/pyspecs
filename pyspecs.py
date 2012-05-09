# Initialization of components
# Run specs
# Optional: Idle (run on any change to .py files)

#from os import getcwd
#
#working_dir = getcwd()
#
#SpecRunner(
#    SpecLoader(
#        (Location(step) for step in walk(working_dir)),     # command line--where to start
#        Importer(working_dir)),  # command line--what to import
#    SpecExecutor(),
#    TerseConsoleReporter()   # command line--verbosity, type of report
#).run_specs()