from unittest.case import TestCase
import sys
from pyspecs.result import UnimplementedSpecResult
from pyspecs.should import ShouldError
from pyspecs.steps import \
    GIVEN_STEP, SPEC, WHEN_STEP, COLLECT_STEP, THEN_STEP, AFTER_STEP
from tests import examples


class TestSpecMethodExecutionOrder(TestCase):
    def setUp(self):
        self.spec = examples.fully_implemented_and_passing()
        self.spec.execute()

    def test_methods_run_in_correct_order(self):
        self.assertSequenceEqual(
            ['given', 'when', 'collect', 'then1', 'then2', 'after'],
            self.spec.executed_steps
        )


class TestFullPassingSpec(TestCase):
    def setUp(self):
        self.spec = examples.fully_implemented_and_passing()
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
        self.spec = examples.spec_with_failure()
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

    def test_stdout_should_have_been_restored(self):
        self.assertIsInstance(sys.stdout, file)


class TestSpecWithAssertionError(TestCase):
    def setUp(self):
        self.spec = examples.spec_with_assertion_error()
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


class TestSpecWithErrorBeforeAssertions(TestCase):
    def setUp(self):
        self.spec = examples.spec_with_error_before_assertions()
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


class TestSpecWithErrorAfterAssertions(TestCase):
    def setUp(self):
        self.spec = examples.spec_with_error_after_assertions()
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


class TestSpecWithErrorsBeforeAndAfterAssertions(TestCase):
    def setUp(self):
        self.spec = examples.spec_with_error_before_and_after_assertions()
        self.result = self.spec.execute()
        self.output = self.result.output

    def test_result_should_convey_pre_assertion_error(self):
        self.assertTrue('collect' in self.result.errors)
        name, error = self.result.errors['collect']
        self.assertEqual('result', name)
        self.assertIsInstance(error, KeyError)

    def test_result_should_convey_post_assertion_error(self):
        self.assertTrue('after' in self.result.errors)
        name, error = self.result.errors['after']
        self.assertEqual('an exception is raised', name)
        self.assertIsInstance(error, ValueError)

    def test_all_output_previous_to_first_exception_is_captured(self):
        self.assertIn(GIVEN_STEP, self.output)
        self.assertIn(WHEN_STEP, self.output)
        self.assertIn(COLLECT_STEP, self.output)

    def test_no_assertions_attempted(self):
        self.assertNotIn(THEN_STEP, self.output)

    def test_all_output_previous_to_second_exception_is_captured(self):
        self.assertIn(AFTER_STEP, self.output)


class TestSpecWithNoAssertions(TestCase):
    def setUp(self):
        self.spec = examples.spec_without_assertions()
        self.result = self.spec.execute()

    def test_no_steps_should_be_executed(self):
        self.assertFalse(len(self.spec.executed))

    def test_result_should_indicate_that_the_spec_is_not_implemented(self):
        self.assertIsInstance(self.result, UnimplementedSpecResult)
        self.assertEqual(self.result.spec_name, 'spec without assertions')
