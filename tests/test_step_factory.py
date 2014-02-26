from unittest import TestCase
from mock import Mock

from pyspecs._step import Step
from pyspecs._step import StepFactory


class StepFactoryTest(TestCase):
    def setUp(self):
        self.registry = Mock()

    def test_any_attribute_creates_a_new_step(self):
        kind = 'example'
        factory = StepFactory(kind, self.registry)

        step = factory.name

        self.assertIsInstance(step, Step)
        self.assertEqual(kind, step.kind)
        self.assertEqual('name', step.name)

    def test_replaces_underscores_by_spaces(self):
        kind = 'example'
        factory = StepFactory(kind, self.registry)

        step = factory.this_is_a_long_name

        self.assertEqual('this is a long name', step.name)

    def test_create_a_new_step_with_calls(self):
        kind = 'example'
        name = 'The new name'
        factory = StepFactory(kind, self.registry)

        step = factory(name)

        self.assertEqual(name, step.name)

    def test_accepts_just_one_argument_when_called(self):
        kind = 'example'
        name = 'The new name'
        factory = StepFactory(kind, self.registry)

        self.assertRaises(AttributeError, factory)
        self.assertRaises(AttributeError, factory, 'a', 'b')
