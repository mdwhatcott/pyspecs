from itertools import count
from unittest import TestCase
from pyspecs._runner import _StepCounter, Step


class FakeReporter(object):
    def __init__(self):
        self.received = None

    def report(self, step_report):
        self.received = step_report


class TestSingleStep(TestCase):
    def test(self):
        timer = count()
        reporter = FakeReporter()
        counter = _StepCounter(reporter, timer.next)
        given = Step('given', counter)

        with given.something:
            pass

        report = reporter.received
        self.assertEqual('given something', report.name)
        self.assertEqual(0, report.started)
        self.assertEqual(1, report.finished)
        self.assertEqual(1, report.duration)
        self.assertEqual([], report.children)
        self.assertEqual(None, report.parent)


class TestNestedStep(TestCase):
    def test(self):
        timer = count()
        reporter = FakeReporter()
        counter = _StepCounter(reporter, timer.next)
        given = Step('given', counter)
        when = Step('when', counter)
        then = Step('then', counter)

        with given.something:
            with when.cause:
                with then.effect:
                    pass

        top = reporter.received
        middle = top.children[0]
        bottom = middle.children[0]

        self.assertIsNone(top.parent)
        self.assertTrue(middle.parent is top)
        self.assertTrue(bottom.parent is middle)
        self.assertEqual(top.children, [middle])
        self.assertEqual(middle.children, [bottom])
        self.assertEqual(bottom.children, [])

        self.assertEqual('given something', top.name)
        self.assertEqual('when cause', middle.name)
        self.assertEqual('then effect', bottom.name)

        self.assertEqual(0, top.started)
        self.assertEqual(1, middle.started)
        self.assertEqual(2, bottom.started)
        self.assertEqual(3, bottom.finished)
        self.assertEqual(4, middle.finished)
        self.assertEqual(5, top.finished)

        self.assertEqual(5, top.duration)
        self.assertEqual(3, middle.duration)
        self.assertEqual(1, bottom.duration)


class TestStepFailure(TestCase):
    def test(self):
        timer = count()
        reporter = FakeReporter()
        counter = _StepCounter(reporter, timer.next)
        given = Step('given', counter)

        with given.something:
            assert timer is None

        report = reporter.received
        self.assertEqual('given something', report.name)
        self.assertEqual(0, report.started)
        self.assertEqual(1, report.finished)
        self.assertEqual(1, report.duration)
        self.assertEqual([], report.children)
        self.assertEqual(None, report.parent)
        self.assertEqual(AssertionError, report.failure_type)
        self.assertIsNotNone(report.failure)
        self.assertIsNotNone(report.traceback)


class TestStepError(TestCase):
    def test(self):
        timer = count()
        reporter = FakeReporter()
        counter = _StepCounter(reporter, timer.next)
        given = Step('given', counter)

        with given.something:
            int('hi')

        report = reporter.received
        self.assertEqual('given something', report.name)
        self.assertEqual(0, report.started)
        self.assertEqual(1, report.finished)
        self.assertEqual(1, report.duration)
        self.assertEqual([], report.children)
        self.assertEqual(None, report.parent)
        self.assertEqual(ValueError, report.error_type)
        self.assertIsNotNone(report.error)
        self.assertIsNotNone(report.traceback)