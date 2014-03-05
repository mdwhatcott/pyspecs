from unittest import TestCase, skip
from mock import Mock, MagicMock

from pyspecs._step import Step


class test_giving_a_step_a_name(TestCase):
    def setUp(self):
        self.kind = 'step kind'
        self.name = 'step name'
        registry = Mock()
        step = Step(self.kind, self.name, registry)

        self.str_step = str(step)

    def test_step_string_is_prettified_with_the_step_type(self):
        self.assertTrue(self.str_step.startswith(self.kind))

    def test_step_string_includes_the_trailing_description(self):
        self.assertIn(self.name, self.str_step)

    def test_complete_step_string(self):
        self.assertEqual('%s %s' % (self.kind, self.name), self.str_step)


class TestEnterScope(TestCase):
    def setUp(self):
        self.registry = Mock()
        self.registry.push = MagicMock(return_value=None)

        self.step = Step('kind', 'name', self.registry)

    def test_should_register_that_step(self):
        with self.step:
            self.assertTrue(self.registry.push.called)


class TestExitScope(TestCase):
    def setUp(self):
        self.registry = Mock()
        self.registry.push = MagicMock(return_value=None)
        self.registry.pop = MagicMock(return_value=None)
        self.step = Step('kind', 'name', self.registry)

    def test_success_should_call_pop_and_finish(self):
        with self.step:
            pass
        self.assertTrue(self.registry.pop.called)
        self.assertTrue(self.step.result.is_success)

    def test_assertion_error_should_log_failure(self):
        with self.step:
            assert False, 'reason'

        self.assertTrue(self.registry.pop.called)
        self.assertTrue(self.step.result.is_failure)

    def test_error_should_log_error(self):
        with self.step:
            raise ZeroDivisionError('Fake zero division')

        self.assertTrue(self.registry.pop.called)
        self.assertTrue(self.step.result.is_error)

    def test_keyboard_interrupt_can_halt_execution(self):
        with self.assertRaises(KeyboardInterrupt):
            with self.step:
                raise KeyboardInterrupt()

        self.assertTrue(self.step.result.is_abort)
