from unittest.case import TestCase
from mock import Mock, call, ANY, MagicMock
from pyspecs import _runner as runner
from pyspecs._runner import SpecInitializationError
from pyspecs._should import ShouldError
from tests import examples


class TestSpecs(TestCase):
    def setUp(self):
        self.capture = MagicMock()
        self.loader = Mock()
        self.mock = Mock()
        self.calls = self.mock.mock_calls

    def run_spec(self, spec, spec_description):
        self.spec = spec_description
        self.loader.load_specs.return_value = spec
        runner.run_specs(self.loader, self.mock, self.capture)

    def _extract_exception_from_call(self, call_index):
        return self.calls[call_index][1][-1][1]

    def test_full_passing(self):
        self.run_spec(
            [examples.fully_implemented_and_passing],
            'fully implemented and passing'
        )
        self.mock.assert_has_calls([
            call.success(self.spec, 'given', 'some scenario'),
            call.success(self.spec, 'when', 'something is invoked'),
            call.success(self.spec, 'collect', 'results'),
            call.success(self.spec, 'then', 'something happens'),
            call.success(self.spec, 'then', 'something is calculated'),
            call.success(self.spec, 'after', 'cleanup')]
        )

    def test_spec_with_assertion_failure(self):
        self.run_spec([examples.spec_with_failure], 'spec with failure')

        self.mock.assert_has_calls([
            call.failure(self.spec, 'it should fail', ANY),
            call.success(self.spec, 'then', 'it should run other assertions')],
            any_order=True
        )
        self.assertIsInstance(self._extract_exception_from_call(0), ShouldError)

    def test_spec_with_assertion_error(self):
        self.run_spec(
            [examples.spec_with_assertion_error], 'spec with assertion error'
        )
        self.mock.assert_has_calls([
            call.error(self.spec, 'then', 'it should raise an error', ANY),
            call.success(self.spec, 'then', 'it should run other assertions'),
            call.success(self.spec, 'after', 'cleanup')
        ])
        self.assertIsInstance(self._extract_exception_from_call(0), KeyError)

    def test_spec_with_error_before_assertions(self):
        self.run_spec(
            [examples.spec_with_error_before_assertions],
            'spec with error before assertions'
        )
        self.mock.assert_has_calls([
            call.error(self.spec, 'given', 'an exception is raised', ANY),
            call.success(self.spec, 'after', 'should be executed to clean up')
        ])
        self.assertNotIn(call.success(ANY, 'when', ANY), self.calls)
        self.assertNotIn(call.success(ANY, 'collect', ANY), self.calls)
        self.assertNotIn(call.success(ANY, 'then', ANY), self.calls)
        self.assertIsInstance(self._extract_exception_from_call(0), KeyError)

    def test_spec_with_error_before_assertions_with_no_cleanup(self):
        self.run_spec(
            [examples.spec_with_error_before_assertions_without_cleanup],
            'spec with error before assertions without cleanup'
        )
        self.assertSequenceEqual(self.mock.mock_calls, [
            call.error(self.spec, 'when', 'an exception is raised', ANY),
        ])
        self.assertIsInstance(self._extract_exception_from_call(0), KeyError)

    def test_spec_with_error_after_assertions(self):
        self.run_spec(
            [examples.spec_with_error_after_assertions],
            'spec with error after assertions'
        )
        self.mock.assert_has_calls([
            call.success(self.spec, 'given', 'setup'),
            call.success(self.spec, 'when', 'action'),
            call.success(self.spec, 'collect', 'result'),
            call.success(self.spec, 'then', 'something'),
            call.success(self.spec, 'then', 'something else'),
            call.error(self.spec, 'after', 'an exception is raised', ANY)
        ])
        self.assertIsInstance(self._extract_exception_from_call(-1), KeyError)

    def test_spec_with_errors_before_and_after_assertions(self):
        self.run_spec(
            [examples.spec_with_error_before_and_after_assertions],
            'spec with error before and after assertions'
        )
        self.mock.assert_has_calls([
            call.success(self.spec, 'given', 'setup'),
            call.success(self.spec, 'when', 'action'),
            call.error(self.spec, 'collect', 'result', ANY),
            call.error(self.spec, 'after', 'an exception is raised', ANY)
        ])
        self.assertIsInstance(self._extract_exception_from_call(2), KeyError)
        self.assertIsInstance(self._extract_exception_from_call(3), ValueError)

    def test_spec_with_no_assertions(self):
        self.run_spec(
            [examples.spec_without_assertions],
            'spec without assertions'
        )
        self.assertEqual(
            self.mock.mock_calls[0],
            call.error(self.spec, 'collect steps', 'not implemented', ANY)
        )
        exception = self._extract_exception_from_call(0)
        self.assertIsInstance(exception, SpecInitializationError)
        self.assertEqual(
            'No assertions ("@then" decorators) found with '
            'the spec (spec without assertions).',
            exception.message)

    def test_spec_that_fails_initialization(self):
        self.run_spec(
            [examples.spec_that_fails_initialization],
            'spec that fails initialization'
        )
        self.mock.assert_has_calls([call.error(self.spec, ANY, ANY, ANY)])
        exception = self._extract_exception_from_call(0)
        self.assertIsInstance(exception, SpecInitializationError)
        self.assertEqual(
            'The spec (spec that fails initialization) could '
            'not be initialized (error in constructor).',
            exception.message)

    def test_excessive_use_of_spec_step_methods(self):
        self.run_spec(
            [examples.spec_with_multiple_givens,
             examples.spec_with_multiple_whens,
             examples.spec_with_multiple_collects,
             examples.spec_with_multiple_afters],
            ['spec with multiple givens',
             'spec with multiple whens',
             'spec with multiple collects',
             'spec with multiple afters',]
        )
        self.mock.assert_has_calls([
            call.error(self.spec[0], 'collect steps', 'extra steps', ANY),
            call.error(self.spec[1], 'collect steps', 'extra steps', ANY),
            call.error(self.spec[2], 'collect steps', 'extra steps', ANY),
            call.error(self.spec[3], 'collect steps', 'extra steps', ANY),
        ])
        exceptions = [self._extract_exception_from_call(x) for x in range(4)]
        self.assertTrue(
            all(isinstance(e, SpecInitializationError) for e in exceptions))
        expected_messages = [
            "The spec (spec with multiple givens) "
                "has extra steps (['given']).",
            "The spec (spec with multiple whens) "
                "has extra steps (['when']).",
            "The spec (spec with multiple collects) "
                "has extra steps (['collect']).",
            "The spec (spec with multiple afters) "
                "has extra steps (['after']).",
        ]
        self.assertSequenceEqual(
            expected_messages, [e.message for e in exceptions])

    def test_inheritance_of_steps(self):
        self.run_spec(
            [examples.child],
            'child spec, using a base spec'
        )
        self.mock.assert_has_calls([
            call.success(self.spec, 'given', 'setup'),
            call.success(self.spec, 'when', 'action'),
            call.success(self.spec, 'collect', 'results'),
            call.success(self.spec, 'then', 'something'),
            call.success(self.spec, 'then', 'something else'),
            call.success(self.spec, 'after', 'cleanup')
        ])