from unittest import TestCase
from mock import Mock
from pyspecs._registry import Registry


class RegistryTests(TestCase):
    def test_has_no_root_steps_by_default(self):
        registry = Registry()

        self.assertEquals([], registry.root_steps)

    def test_support_adding_steps(self):
        registry = Registry()
        step = Mock()

        ret_value = registry.push(step)

        self.assertEquals([step], registry.root_steps)
        self.assertEquals(None, ret_value)

    def test_adding_a_descendant_step_returns_the_parent(self):
        registry = Registry()
        step1 = Mock()
        step2 = Mock()

        ret_value1 = registry.push(step1)
        ret_value2 = registry.push(step2)

        self.assertEquals(None, ret_value1)
        self.assertEquals(step1, ret_value2)
        self.assertEquals([step1], registry.root_steps)

    def test_pop_returns_none_if_no_steps(self):
        registry = Registry()

        self.assertEquals(None, registry.pop())

    def test_pop_does_not_fail_if_step_has_no_parent(self):
        registry = Registry()
        step = Mock()
        step.parent = None
        registry.push(step)

        self.assertEquals(None, registry.pop())

    def test_pushing_after_popping_creates_a_new_root_step(self):
        registry = Registry()
        step1 = Mock()
        step1.parent = None
        step2 = Mock()
        step2.parent = None

        registry.push(step1)
        registry.pop()
        registry.push(step2)

        self.assertEquals([step1, step2], registry.root_steps)
