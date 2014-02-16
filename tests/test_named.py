import sys
from itertools import count
from unittest import TestCase
from pyspecs._step import _StepCounter, Step


class FakeReporter(object):
    def __init__(self):
        self.received = None

    def report(self, step_report):
        self.received = step_report


class TestSingleNamedStep(TestCase):
    def test(self):
        timer = count()
        reporter = FakeReporter()
        counter = _StepCounter(reporter, timer.next)
        given = Step('given', counter)

        with given("something with spaces"):
            pass

        report = reporter.received
        self.assertEqual('given something with spaces', report.name)


class TestUnicodeNameStep(TestCase):
    def test(self):
        timer = count()
        reporter = FakeReporter()
        counter = _StepCounter(reporter, timer.next)
        given = Step('given', counter)

        with given(
                u"\xe1\xe9\xed\xf3\xfa "  # tilde
                u"\xe0\xe8\xec\xf2\xf9 "  # back tilde
                u"\xe2\xea\xee\xf4\xfb "  # circumflex
                u"\xe4\xeb\xef\xf6\xff "  # dieresis
                u"\xf1\xd1 " # n tilde
                u"\xe7\xc7 " # c cedilla
                u"\xdf\xa7"  # B umlaud
        ):
            pass

        report = reporter.received
        self.assertEqual('given ----- ----- ----- ----- -- -- --', report.name)


