class SpecRunner(object):
  def __init__(self, loader, executor, reporter):
    self.loader = loader
    self.executor = executor
    self.reporter = reporter

  def run_specs(self):
    for spec in self.loader.load_specs():
      result = self.executor.execute(spec)
      self.reporter.report(result)