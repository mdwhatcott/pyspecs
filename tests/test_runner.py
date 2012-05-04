from unittest.case import TestCase
from mock import Mock, call
from pyspecs.runner import SpecRunner

class TestSpecRunner(TestCase):
    def setUp(self):
        self.loader = Mock()
        self.executor = Mock()
        self.reporter = Mock()
        self.specs = [Mock(), Mock()]
        self.result = Mock()

        self.loader.load_specs.return_value = self.specs
        self.executor.execute.return_value = self.result
        self.runner = SpecRunner(self.loader, self.executor, self.reporter)

    def test_specs_loaded_and_executed_and_reported(self):
        self.runner.run_specs()
        self.reporter.assert_has_calls(
            [
                call.report(self.result),
                call.report(self.result)
            ]
        )