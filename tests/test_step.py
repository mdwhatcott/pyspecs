from unittest import TestCase
from pyspecs._step import Step


class FakeCounter(object):
    def __init__(self):
        self.starts = []
        self.finished = False
        self.failures = []
        self.errors = []

    def start(self, name):
        self.starts.append(name)

    def finish(self):
        self.finished = True

    def error(self, exception_type, exception, traceback):
        self.errors.append((exception_type, exception, traceback))

    def fail(self, exception_type, exception, traceback):
        self.failures.append((exception_type, exception, traceback))


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
        self.name = self.step.name

    def test_should_start_the_counter_for_that_step(self):
        with self.step:
            pass

        self.assertEqual(self.counter.starts[0], 'my step is awesome')


class TestExitScope(TestCase):
    def setUp(self):
        self.counter = FakeCounter()
        self.step = Step('my step', self.counter).is_awesome
        self.name = self.step.name

    def test_success_should_finish_the_counter_for_that_step(self):
        try:
            with self.step:
                pass
        except Exception as e:
            raise AssertionError(
                'No exception expected but received a {0}'.format(type(e)))
        else:
            pass

        self.assertTrue(self.counter.finished)

    def test_assertion_error_should_log_failure(self):
        try:
            with self.step:
                assert self.step is None, 'blah blah'
        except Exception as e:
            raise AssertionError(
                'No exception expected but received a {0}'.format(type(e)))
        else:
            pass

        exception_type, exception, traceback = self.counter.failures[0]
        self.assertEqual(exception_type, type(AssertionError()))
        self.assertIsNotNone(exception)
        self.assertIn('blah blah', str(exception))
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

        exception_type, exception, traceback = self.counter.errors[0]
        self.assertEqual(exception_type, type(ZeroDivisionError()))
        self.assertIsNotNone(exception)
        self.assertIn('blah blah blah', str(exception))
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

    def test_exit_should_clear_the_description(self):
        with self.step:
            pass

        self.assertEqual('my step', self.step.name)
