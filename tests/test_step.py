from unittest import TestCase
from spec import Step


class FakeCounter(object):
    def __init__(self):
        self.starts = []
        self.finishes = []
        self.failures = []
        self.errors = []

    def start(self, step, name):
        self.starts.append((step, name))

    def finish(self, name):
        self.finishes.append(name)

    def error(self, name, exception_type, exception, traceback):
        self.errors.append((name, exception_type, exception, traceback))

    def fail(self, name, exception_type, exception, traceback):
        self.failures.append((name, exception_type, exception, traceback))


class test_giving_a_step_a_name(TestCase):
    def setUp(self):
        self.counter = FakeCounter()
        step = Step('my step', self.counter).is_awesome
        self.name = step.name

    def test_name_is_prettified_with_the_step_type(self):
        self.assertTrue(self.name.startswith('my step'))

    def test_name_includes_the_trailing_description(self):
        self.assertTrue(self.name.endswith('is awesome'))

    def test_complete_name(self):
        self.assertEqual('my step is awesome', self.name)


class TestOneNamingOnly(TestCase):
    def setUp(self):
        self.counter = FakeCounter()
        self.step = Step('my step', self.counter).is_awesome

    def test_additional_names_are_prohibited(self):
        self.assertRaises(AttributeError, lambda: self.step.blah)


class TestEnterScope(TestCase):
    def setUp(self):
        self.counter = FakeCounter()
        self.step = Step('my step', self.counter).is_awesome

    def test_should_start_the_counter_for_that_step(self):
        with self.step:
            pass

        self.assertEqual(self.counter.starts[0], ('my step', self.step.name))


class TestExitScope(TestCase):
    def setUp(self):
        self.counter = FakeCounter()
        self.step = Step('my step', self.counter).is_awesome

    def test_success_should_finish_the_counter_for_that_step(self):
        try:
            with self.step:
                pass
        except Exception as e:
            raise AssertionError(
                'No exception expected but received a {0}'.format(type(e)))
        else:
            pass

        self.assertEqual(self.counter.finishes[0], self.step.name)

    def test_assertion_error_should_log_failure(self):
        try:
            with self.step:
                assert self.step is None, 'blah blah'
        except Exception as e:
            raise AssertionError(
                'No exception expected but received a {0}'.format(type(e)))
        else:
            pass

        name, exception_type, exception, traceback = self.counter.failures[0]
        self.assertEqual(name, self.step.name)
        self.assertEqual(exception_type, type(AssertionError()))
        self.assertIsNotNone(exception)
        self.assertIn('blah blah', exception.message)
        self.assertIsNotNone(traceback)

    def test_error_should_log_error(self):
        try:
            with self.step:
                raise ZeroDivisionError('blah blah blah')
        except Exception as e:
            raise AssertionError(
                'No exception expected but received a {0}'.format(type(e)))
        else:
            pass

        name, exception_type, exception, traceback = self.counter.errors[0]
        self.assertEqual(name, self.step.name)
        self.assertEqual(exception_type, type(ZeroDivisionError()))
        self.assertIsNotNone(exception)
        self.assertIn('blah blah blah', exception.message)
        self.assertIsNotNone(traceback)

    def test_keyboard_interrupt_can_halt_execution(self):
        try:
            with self.step:
                raise KeyboardInterrupt()
        except KeyboardInterrupt:
            pass  # execution could be halted here.
        else:
            raise AssertionError('Should have caught a KeyboardInterrupt!')

        self.assertEqual(0, len(self.counter.errors))
