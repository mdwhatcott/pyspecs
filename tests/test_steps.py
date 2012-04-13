from unittest.case import TestCase
from pyspecs.steps import _step, SPEC_DESCRIPTION, PYSPECS_STEP


class TestStepAsDecorator(TestCase):
  def setUp(self):
    decorator = _step('the_name')

    @decorator
    def this_function_is_named_with_underscores():
      pass

    self.decorated = this_function_is_named_with_underscores

  def test_description_matches_method_name_without_underscores(self):
    description = getattr(self.decorated, SPEC_DESCRIPTION)
    self.assertNotIn('_', description)
    self.assertEqual('this function is named with underscores', description)

  def test_specified_attribute_is_set(self):
    attribute = getattr(self.decorated, PYSPECS_STEP)
    self.assertEqual('the_name', attribute)
