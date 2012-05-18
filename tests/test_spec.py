from unittest.case import TestCase, skip
from mock import Mock, call, MagicMock
from pyspecs._loader import SpecLoader
from pyspecs._reporter import Reporter
from pyspecs._runner import SpecRunner
from tests import examples


def context_wrap(wrapped_calls):
    for wrapped_call in wrapped_calls:
        yield call.__enter__()
        yield wrapped_call
        yield call.__exit__(None, None, None)


class TestSpecs(TestCase):
    def setUp(self):
        self.reporter = MagicMock(spec=Reporter)
        self.report_capture = Mock()
        self.loader = Mock(spec=SpecLoader)
        self.runner = SpecRunner(self.loader, self.reporter)

    def test_full_passing(self):
        self.loader.load_specs.return_value = [examples.fully_implemented_and_passing]
        self.runner.run_specs()
        subject = 'fully implemented and passing'
        self.reporter.assert_has_calls(list(context_wrap([
            call.success(subject, 'given', 'some scenario'),
            call.success(subject, 'when', 'something is invoked'),
            call.success(subject, 'collect', 'results'),
            call.success(subject, 'then', 'something happens'),
            call.success(subject, 'then', 'something is calculated'),
            call.success(subject, 'after', 'cleanup')]
        )))

    @skip
    def test_spec_with_assertion_failure(self):
        self.loader.load_specs.return_value = [examples.spec_with_failure]
        # test_result_should_convey_failure
        # test_result_should_contain_any_output
        # test_it_should_run_fast
        # test_stdout_should_have_been_restored

    @skip
    def test_spec_with_assertion_error(self):
        self.loader.load_specs.return_value = [examples.spec_with_assertion_error]
        # test_result_should_convey_the_exception
        # test_result_should_contain_any_output_logged_before_exception
        # test_remaining_assertions_are_invoked
        # test_remaining_steps_are_invoked

    @skip
    def test_spec_with_error_before_assertions(self):
        self.loader.load_specs.return_value = [examples.spec_with_error_before_assertions]
        #    def test_result_should_convey_the_exception(self): pass
        #    def test_pre_assertion_steps_should_NOT_be_invoked(self): pass
        #    def test_assertions_should_NOT_be_invoked(self): pass
        #    def test_all_output_previous_to_exception_is_captured(self): pass
        #    def test_cleanup_attempted(self): pass

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