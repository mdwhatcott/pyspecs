from unittest.case import TestCase, skip
from mock import Mock, call
from pyspecs._loader import SpecLoader
from pyspecs._reporter import Reporter
from pyspecs._runner import SpecRunner
from tests import examples


class TestFullPassingSpec(TestCase):
    def setUp(self):
        self.spec = examples.fully_implemented_and_passing
        self.reporter = Mock(spec=Reporter)
        self.loader = Mock(spec=SpecLoader)
        self.loader.load_specs.return_value = [self.spec]
        self.runner = SpecRunner(self.loader, self.reporter)

    def test_result_populated_with_correct_statistics(self):
        self.runner.run_specs()
        spec_name = 'fully implemented and passing'
        self.reporter.assert_has_calls([
            call.success(spec_name, 'given', 'some scenario'),
            call.success(spec_name, 'when', 'something is invoked'),
            call.success(spec_name, 'collect', 'results'),
            call.success(spec_name, 'then', 'something happens'),
            call.success(spec_name, 'then', 'something is calculated'),
            call.success(spec_name, 'after', 'cleanup')
        ])


@skip
class TestSpecWithAssertionFailure(TestCase):
    def setUp(self):
        self.spec = examples.spec_with_failure

    def test_result_should_convey_failure(self): pass
    def test_result_should_contain_any_output(self): pass
    def test_it_should_run_fast(self): pass
    def test_stdout_should_have_been_restored(self): pass


@skip
class TestSpecWithAssertionError(TestCase):
    def setUp(self):
        self.spec = examples.spec_with_assertion_error

    def test_result_should_convey_the_exception(self): pass
    def test_result_should_contain_any_output_logged_before_exception(self): pass
    def test_remaining_assertions_are_invoked(self): pass
    def test_remaining_steps_are_invoked(self): pass


@skip
class TestSpecWithErrorBeforeAssertions(TestCase):
    def setUp(self):
        self.spec = examples.spec_with_error_before_assertions

    def test_result_should_convey_the_exception(self): pass
    def test_pre_assertion_steps_should_NOT_be_invoked(self): pass
    def test_assertions_should_NOT_be_invoked(self): pass
    def test_all_output_previous_to_exception_is_captured(self): pass
    def test_cleanup_attempted(self): pass


@skip
class TestSpecWithErrorAfterAssertions(TestCase):
    def setUp(self):
        self.spec = examples.spec_with_error_after_assertions

    def test_result_should_convey_the_exception(self): pass
    def test_all_output_previous_to_exception_is_captured(self): pass


@skip
class TestSpecWithErrorsBeforeAndAfterAssertions(TestCase):
    def setUp(self):
        self.spec = examples.spec_with_error_before_and_after_assertions

    def test_result_should_convey_pre_assertion_error(self): pass
    def test_result_should_convey_post_assertion_error(self): pass
    def test_all_output_previous_to_first_exception_is_captured(self): pass
    def test_no_assertions_attempted(self): pass
    def test_all_output_previous_to_second_exception_is_captured(self): pass


@skip
class TestSpecWithNoAssertions(TestCase):
    def setUp(self):
        self.spec = examples.spec_without_assertions

    def test_no_steps_should_be_executed(self): pass
    def test_result_should_indicate_that_the_spec_is_not_implemented(self): pass


@skip
class TestSpecThatFailsInitialization(TestCase):
    pass