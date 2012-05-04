from unittest.case import TestCase
from pyspecs.steps import _step, PYSPECS_STEP


class TestStepAsDecorator(TestCase):
    def setUp(self):
        decorator = _step('the_name')

        @decorator
        def this_function_is_named_with_underscores():
            pass

        self.decorated = this_function_is_named_with_underscores

    def test_specified_attribute_is_set(self):
        attribute = getattr(self.decorated, PYSPECS_STEP)
        self.assertEqual('the_name', attribute)
