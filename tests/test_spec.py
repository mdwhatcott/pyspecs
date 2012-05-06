from unittest.case import TestCase, skip
import sys
from pyspecs.should import ShouldError
from pyspecs.steps import \
    GIVEN_STEP, SPEC, WHEN_STEP, COLLECT_STEP, THEN_STEP, AFTER_STEP
from tests.examples import \
    fully_implemented_and_passing, \
    spec_with_failure, \
    spec_with_assertion_error, \
    spec_with_error_before_assertions, \
    spec_with_error_after_assertions


class TestSpecMethodExecutionOrder(TestCase):
    def setUp(self):
        self.spec = fully_implemented_and_passing()
        self.spec.execute()

    def test_methods_run_in_correct_order(self):
        self.assertSequenceEqual(
            ['given', 'when', 'collect', 'then1', 'then2', 'after'],
            self.spec.executed_steps
        )


class TestFullPassingSpec(TestCase):
    def setUp(self):
        self.spec = fully_implemented_and_passing()
        self.result = self.spec.execute()

    def test_result_populated_with_correct_statistics(self):
        self.assertAlmostEqual(0, self.result.duration().total_seconds(), 1)
        self.assertFalse(any(self.result.errors.values()))
        self.assertEqual(str(), self.result.output)
        self.assertEqual(
          'fully implemented and passing', self.result.names[SPEC])
        self.assertEqual('some scenario', self.result.names[GIVEN_STEP])
        self.assertEqual('something is invoked', self.result.names[WHEN_STEP])
        self.assertEqual('results', self.result.names[COLLECT_STEP])
        self.assertSequenceEqual(
            ['something happens', 'something is calculated'],
            self.result.names[THEN_STEP]
        )
        self.assertEqual('cleanup', self.result.names[AFTER_STEP])

class TestSpecWithAssertionFailure(TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        self.spec = spec_with_failure()
        self.result = self.spec.execute()

    def test_result_should_convey_failure(self):
        self.assertEqual(1, len(self.result.failures))
        name, error = self.result.failures[0]
        self.assertEqual('it should fail', name)
        self.assertIsInstance(error, ShouldError)

    def test_result_should_contain_any_output(self):
        self.assertEqual('Hello, World!\n', self.result.output)

    def test_it_should_run_fast(self):
        self.assertAlmostEqual(0, self.result.duration().total_seconds(), 1)

    @skip('It feels like the python unittest framework is swapping stdout.')
    def test_stdout_should_have_been_restored(self):
        self.assertEqual(sys.stdout, self.result._output)
        self.assertIsInstance(sys.stdout, file)

    def tearDown(self):
        sys.stdout = self.stdout

class TestSpecWithAssertionError(TestCase):
    def setUp(self):
        self.spec = spec_with_assertion_error()
        self.result = self.spec.execute()

    def test_result_should_convey_the_exception(self):
        self.assertEqual(1, len(self.result.errors['then']))
        name, error = self.result.errors['then'][0]
        self.assertEqual('it should raise an error', name)
        self.assertIsInstance(error, Exception)

    def test_result_should_contain_any_output_logged_before_exception(self):
        self.assertTrue(self.result.output.startswith("Hello, World!\n"))

    def test_remaining_assertions_are_invoked(self):
        self.assertTrue(self.spec.other_assertion)

    def test_remaining_steps_are_invoked(self):
        self.assertTrue(self.result.output.endswith(AFTER_STEP))


class TestSpecWithStepErrorBeforeAssertions(TestCase):
    def setUp(self):
        self.spec = spec_with_error_before_assertions()
        self.result = self.spec.execute()

    def test_result_should_convey_the_exception(self):
        self.assertTrue('given' in self.result.errors)
        name, error = self.result.errors['given']
        self.assertEqual('an exception is raised', name)
        self.assertIsInstance(error, KeyError)

    def test_pre_assertion_steps_should_NOT_be_invoked(self):
        self.assertNotIn(WHEN_STEP, self.result.output)
        self.assertNotIn(COLLECT_STEP, self.result.output)

    def test_assertions_should_NOT_be_invoked(self):
        self.assertNotIn(WHEN_STEP, self.result.output)

    def test_all_output_previous_to_exception_is_captured(self):
        self.assertIn(GIVEN_STEP, self.result.output)

    def test_cleanup_attempted(self):
        self.assertIn(AFTER_STEP, self.result.output)


class TestSpecWithStepErrorAfterAssertions(TestCase):
    def setUp(self):
        self.spec = spec_with_error_after_assertions()
        self.result = self.spec.execute()

    def test_result_should_convey_the_exception(self):
        self.assertTrue('after' in self.result.errors)
        name, error = self.result.errors['after']
        self.assertEqual('an exception is raised', name)
        self.assertIsInstance(error, KeyError)

    def test_all_output_previous_to_exception_is_captured(self):
        self.assertIn(GIVEN_STEP, self.result.output)
        self.assertIn(WHEN_STEP, self.result.output)
        self.assertIn(COLLECT_STEP, self.result.output)
        self.assertTrue(self.result.output.count(THEN_STEP) == 2)
        self.assertNotIn(AFTER_STEP, self.result.output)