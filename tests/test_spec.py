from unittest.case import TestCase, skip
from mock import Mock, call, ANY, MagicMock
from pyspecs._runner import SpecRunner
from tests import examples


class TestSpecs(TestCase):
    def setUp(self):
        self.reporter = Mock()
        self.capture = MagicMock()
        self.loader = Mock()
        self.runner = SpecRunner(self.loader, self.reporter, self.capture)

    def test_full_passing(self):
        self.loader.load_specs.return_value = [examples.fully_implemented_and_passing]
        self.runner.run_specs()
        subject = 'fully implemented and passing'
        self.reporter.assert_has_calls([
            call.success(subject, 'given', 'some scenario'),
            call.success(subject, 'when', 'something is invoked'),
            call.success(subject, 'collect', 'results'),
            call.success(subject, 'then', 'something happens'),
            call.success(subject, 'then', 'something is calculated'),
            call.success(subject, 'after', 'cleanup')]
        )

    def test_spec_with_assertion_failure(self):
        self.loader.load_specs.return_value = [examples.spec_with_failure]
        self.runner.run_specs()
        spec = 'spec with failure'
        self.reporter.assert_has_calls([
                call.failure(spec, 'it should fail', ANY),
                call.success(spec, 'then', 'it should run other assertions')],
            any_order=True
        )
        # TODO: make assertions about the exception that was reported

    def test_spec_with_assertion_error(self):
        self.loader.load_specs.return_value = [examples.spec_with_assertion_error]
        self.runner.run_specs()
        spec = 'spec with assertion error'
        self.reporter.assert_has_calls([
            call.error(spec, 'then', 'it should raise an error', ANY),
            call.success(spec, 'then', 'it should run other assertions'),
            call.success(spec, 'after', 'cleanup')
        ])
        # TODO: make assertions about the exception that was reported

    def test_spec_with_error_before_assertions(self):
        self.loader.load_specs.return_value = [examples.spec_with_error_before_assertions]
        self.runner.run_specs()
        spec = 'spec with error before assertions'
        self.reporter.assert_has_calls([
            call.error(spec, 'given', 'an exception is raised', ANY),
            call.success(spec, 'after', 'should be executed to clean up')
        ])
        self.assertNotIn(call.success(ANY, 'when', ANY), self.reporter.mock_calls)
        self.assertNotIn(call.success(ANY, 'collect', ANY), self.reporter.mock_calls)
        self.assertNotIn(call.success(ANY, 'then', ANY), self.reporter.mock_calls)
        # TODO: make assertions about the exception that was reported


    @skip
    def test_spec_with_error_after_assertions(self):
        self.loader.load_specs.return_value = [examples.spec_with_error_after_assertions]
        #    def test_result_should_convey_the_exception(self): pass
        #    def test_all_output_previous_to_exception_is_captured(self): pass

    @skip
    def test_spec_with_errors_before_and_after_assertions(self):
        self.loader.load_specs.return_value = [examples.spec_with_error_before_and_after_assertions]
        #    def test_result_should_convey_pre_assertion_error(self): pass
        #    def test_result_should_convey_post_assertion_error(self): pass
        #    def test_all_output_previous_to_first_exception_is_captured(self): pass
        #    def test_no_assertions_attempted(self): pass
        #    def test_all_output_previous_to_second_exception_is_captured(self): pass

    @skip
    def test_spec_with_no_assertions(self):
        self.loader.load_specs.return_value = [examples.spec_without_assertions]
        #    def test_no_steps_should_be_executed(self): pass
        #    def test_result_should_indicate_that_the_spec_is_not_implemented(self): pass

    @skip
    def test_spec_that_fails_initialization(self):
        self.loader.load_specs.return_value = [examples.spec_that_fails_initialization]