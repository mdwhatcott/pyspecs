from unittest.case import TestCase
from pyspecs.steps import GIVEN_STEP, SPEC, WHEN_STEP, COLLECT_STEP, THEN_STEP, AFTER_STEP
from tests.examples import FullyImplementedPassing


class TestSpecMethodExecutionOrder(TestCase):
  def setUp(self):
    self.spec = FullyImplementedPassing()
    self.spec.collect_steps()
    self.spec.execute_steps()

  def test_methods_run_in_correct_order(self):
    self.assertSequenceEqual(
      ['given', 'when', 'collect', 'then1', 'then2', 'after'],
      self.spec.executed_steps
    )


class TestFullPassingSpec(TestCase):
  def setUp(self):
    self.spec = FullyImplementedPassing()
    self.spec.collect_steps()
    self.result = self.spec.execute_steps()

  def test_result_populated_with_correct_statistics(self):
    self._assert_descriptions()
    self.assertAlmostEqual(0, self.result.duration.total_seconds(), 1)
    # TODO: assert no errors
    # TODO: assert no output?

  def _assert_descriptions(self):
    self.assertEqual(FullyImplementedPassing.__name__, self.result.names[SPEC])
    self.assertEqual('some scenario', self.result.names[GIVEN_STEP])
    self.assertEqual('something is invoked', self.result.names[WHEN_STEP])
    self.assertEqual('results', self.result.names[COLLECT_STEP])
    self.assertSequenceEqual(
      ['something happens', 'something is calculated'],
      self.result.names[THEN_STEP]
    )
    self.assertEqual('cleanup', self.result.names[AFTER_STEP])
