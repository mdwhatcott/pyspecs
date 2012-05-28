from unittest.case import TestCase
from pyspecs import skip, then
from pyspecs._steps import _step, PYSPECS_STEP, PYSPECS_SKIPPED


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


class TestSkipDecorator(TestCase):
    def test_skip_attribute_set(self):
        @skip
        @then
        def method(self):
            pass

        @skip
        class spec_(object):
            pass

        self.assertTrue(getattr(method, PYSPECS_SKIPPED))
        self.assertTrue(getattr(spec_, PYSPECS_SKIPPED))