from unittest.case import TestCase
from mock import Mock, call, ANY, MagicMock
from pyspecs import _runner as runner
from tests import examples


class TestSpecs(TestCase):
    def setUp(self):
        self.reporter = Mock()
        self.capture = MagicMock()
        self.loader = Mock()

    def test_full_passing(self):
        self.loader.load_specs.return_value = \
            [examples.fully_implemented_and_passing]
        runner.run_specs(self.loader, self.reporter, self.capture)
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
        runner.run_specs(self.loader, self.reporter, self.capture)
        spec = 'spec with failure'
        self.reporter.assert_has_calls([
                call.failure(spec, 'it should fail', ANY),
                call.success(spec, 'then', 'it should run other assertions')],
            any_order=True
        )
        # TODO: make assertions about the exception that was reported

    def test_spec_with_assertion_error(self):
        self.loader.load_specs.return_value = \
            [examples.spec_with_assertion_error]
        runner.run_specs(self.loader, self.reporter, self.capture)
        spec = 'spec with assertion error'
        self.reporter.assert_has_calls([
            call.error(spec, 'then', 'it should raise an error', ANY),
            call.success(spec, 'then', 'it should run other assertions'),
            call.success(spec, 'after', 'cleanup')
        ])
        # TODO: make assertions about the exception that was reported

    def test_spec_with_error_before_assertions(self):
        self.loader.load_specs.return_value = \
            [examples.spec_with_error_before_assertions]
        runner.run_specs(self.loader, self.reporter, self.capture)
        spec = 'spec with error before assertions'
        self.reporter.assert_has_calls([
            call.error(spec, 'given', 'an exception is raised', ANY),
            call.success(spec, 'after', 'should be executed to clean up')
        ])
        calls = self.reporter.mock_calls
        self.assertNotIn(call.success(ANY, 'when', ANY), calls)
        self.assertNotIn(call.success(ANY, 'collect', ANY), calls)
        self.assertNotIn(call.success(ANY, 'then', ANY), calls)
        # TODO: make assertions about the exception that was reported

    def test_spec_with_error_before_assertions_with_no_cleanup(self):
        self.loader.load_specs.return_value = \
            [examples.spec_with_error_before_assertions_without_cleanup]
        runner.run_specs(self.loader, self.reporter, self.capture)
        spec = 'spec with error before assertions without cleanup'
        self.assertSequenceEqual(self.reporter.mock_calls, [
            call.error(spec, 'when', 'an exception is raised', ANY),
        ])


    def test_spec_with_error_after_assertions(self):
        self.loader.load_specs.return_value = \
            [examples.spec_with_error_after_assertions]
        runner.run_specs(self.loader, self.reporter, self.capture)
        spec = 'spec with error after assertions'
        self.reporter.assert_has_calls([
            call.success(spec, 'given', 'setup'),
            call.success(spec, 'when', 'action'),
            call.success(spec, 'collect', 'result'),
            call.success(spec, 'then', 'something'),
            call.success(spec, 'then', 'something else'),
            call.error(spec, 'after', 'an exception is raised', ANY)
        ])
        # TODO: make assertions about the exception that was reported

    def test_spec_with_errors_before_and_after_assertions(self):
        self.loader.load_specs.return_value = \
            [examples.spec_with_error_before_and_after_assertions]
        runner.run_specs(self.loader, self.reporter, self.capture)
        spec = 'spec with error before and after assertions'
        self.reporter.assert_has_calls([
            call.success(spec, 'given', 'setup'),
            call.success(spec, 'when', 'action'),
            call.error(spec, 'collect', 'result', ANY),
            call.error(spec, 'after', 'an exception is raised', ANY)
        ])
        # TODO: make assertions about the exceptions that were reported

    def test_spec_with_no_assertions(self):
        self.loader.load_specs.return_value = \
            [examples.spec_without_assertions]
        runner.run_specs(self.loader, self.reporter, self.capture)
        self.assertEqual(
            self.reporter.mock_calls[0],
            call.error(
                'spec without assertions',
                'collect steps',
                'not implemented',
                ANY)
        )

        # TODO: exception should indicate that the spec is not implemented

    def test_spec_that_fails_initialization(self):
        self.loader.load_specs.return_value = \
            [examples.spec_that_fails_initialization]
        runner.run_specs(self.loader, self.reporter, self.capture)
        self.reporter.assert_has_calls([
            call.error('spec that fails initialization', ANY, ANY, ANY)
        ])

        # TODO: exception should indicate that spec steps were not applied correctly.

    def test_improper_use_of_spec_step_methods(self):
        pass
        # more than one given, when, collect, or after step

    def test_inheritance_of_steps(self):
        pass
        # base class defines given, when, collect, and after
        # child class makes assertions