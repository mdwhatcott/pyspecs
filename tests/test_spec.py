from unittest.case import TestCase
from pyspecs.should import ShouldError
from pyspecs.steps import GIVEN_STEP, SPEC, WHEN_STEP, COLLECT_STEP, THEN_STEP, AFTER_STEP
from tests.examples import fully_implemented_and_passing, spec_with_failure


class TestSpecMethodExecutionOrder(TestCase):
  def setUp(self):
    self.spec = fully_implemented_and_passing()
    steps = self.spec.collect_steps()
    self.spec.execute_steps(steps)

  def test_methods_run_in_correct_order(self):
    self.assertSequenceEqual(
      ['given', 'when', 'collect', 'then1', 'then2', 'after'],
      self.spec.executed_steps
    )


class TestFullPassingSpec(TestCase):
  def setUp(self):
    self.spec = fully_implemented_and_passing()
    steps = self.spec.collect_steps()
    self.result = self.spec.execute_steps(steps)

  def test_result_populated_with_correct_statistics(self):
    self.assertAlmostEqual(0, self.result.duration.total_seconds(), 1)
    self.assertFalse(any(self.result.errors.values()))
    self.assertFalse(any(self.result.output.values()))
    self.assertEqual('fully implemented and passing', self.result.names[SPEC])
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
    steps = self.spec.collect_steps()
    self.result = self.spec.execute_steps(steps)

  def test_result_should_convey_failure_and_log_output(self):
    self.assertEqual(1, len(self.result.errors['then']))
    name, error = self.result.errors['then'][0]
    self.assertEqual('it should fail', name)
    self.assertIsInstance(error, ShouldError)


class TestSpecWithAssertionError(TestCase):
  pass


class TestSpecWithStepError(TestCase):
  pass


class TestSpecThatFailsInitialization(TestCase):
  pass