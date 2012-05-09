from unittest.case import TestCase
from mock import Mock
from pyspecs.result import SpecResult, UnimplementedSpecResult, BrokenSpecResult
from pyspecs.runner import SpecRunner
from pyspecs.spec import Spec
from pyspecs.steps import then


class TestSpecRunner(TestCase):
    def setUp(self):
        self.loader = Mock()
        self.reporter = FakeReporter()
        self.loader.load_specs.return_value = [successful, error]
        self.runner = SpecRunner(self.loader, self.reporter)

    def test_specs_loaded_and_executed_and_reported(self):
        self.runner.run_specs()
        self.assertIsInstance(self.reporter.results[0], SpecResult)
        self.assertIsInstance(self.reporter.results[1], BrokenSpecResult)


class successful(Spec):
    @then
    def action(self):
        pass


class error(Spec):
    def __init__(self):
        raise ValueError

    @then
    def action(self):
        pass


class FakeReporter(object):
    def __init__(self):
        self.results = []

    def report(self, result):
        self.results.append(result)