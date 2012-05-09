# Several flavors (
#   DotConsoleReporter,
#   StoryConsoleReporter,
#   HtmlReporter,
#
#   JsonReporter,
#   GrowlReporter,
#   etc...,
# )
# 1. receive standardized result object (aggregate required state)
# 2. formulate representation of result for report (text, html, etc...)
# 3. Show overview/stats


from abc import abstractmethod
from pyspecs.result import SpecResult, BrokenSpecResult, UnimplementedSpecResult


class Reporter(object):
    def report(self, result):
        if isinstance(result, SpecResult):
            self._report_spec(result)
        elif isinstance(result, BrokenSpecResult):
            self._report_broken_spec(result)
        elif isinstance(result, UnimplementedSpecResult):
            self._report_unimplemented_spec(result)

    @abstractmethod
    def _report_spec(self, result):
        pass

    @abstractmethod
    def _report_broken_spec(self, result):
        pass

    @abstractmethod
    def _report_unimplemented_spec(self, result):
        pass


class DotReporter(Reporter):
    def __init__(self):
        pass

    def _report_spec(self, result):
        pass

    def _report_broken_spec(self, result):
        pass

    def _report_unimplemented_spec(self, result):
        pass