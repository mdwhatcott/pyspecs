from unittest.case import TestCase
from pyspecs.should import ShouldError
from pyspecs.steps import \
    GIVEN_STEP, SPEC, WHEN_STEP, COLLECT_STEP, THEN_STEP, AFTER_STEP
from tests.examples import \
    fully_implemented_and_passing, spec_with_failure, spec_with_assertion_error


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
        self.assertAlmostEqual(0, self.result.duration.total_seconds(), 1)
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
        self.spec = spec_with_failure()
        self.result = self.spec.execute()

    def test_result_should_convey_failure(self):
        self.assertEqual(1, len(self.result.failures))
        name, error = self.result.failures[0]
        self.assertEqual('it should fail', name)
        self.assertIsInstance(error, ShouldError)

    def test_result_should_contain_any_output(self):
        self.assertEqual('Hello, World!\n', self.result.output)


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
    def test_result_should_convey_the_exception(self):
        pass

    def test_assertions_should_NOT_be_invoked(self):
        pass

    def test_all_output_previous_to_exception_is_captured(self):
        pass

    def test_cleanup_attempted(self):
        pass


class TestSpecWithStepErrorAfterAssertions(TestCase):
    def test_result_should_convey_the_exception(self):
        pass

    def test_all_output_previous_to_exception_is_captured(self):
        pass