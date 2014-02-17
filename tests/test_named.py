import sys
from itertools import count
from unittest import TestCase
from pyspecs._step import _StepCounter, Step

if sys.version > '2':
    unichr = chr
    unicode = str


class FakeReporter(object):
    def __init__(self):
        self.received = None

    def report(self, step_report):
        self.received = step_report


class TestSingleNamedStep(TestCase):
    def test(self):
        timer = count()
        reporter = FakeReporter()
        counter = _StepCounter(reporter, timer.next if hasattr(timer, 'next') else timer.__next__)
        given = Step('given', counter)

        with given("something with spaces"):
            pass

        report = reporter.received
        self.assertEqual('given something with spaces', report.name)


class TestUnicodeNameStep(TestCase):
    def test(self):
        timer = count()
        reporter = FakeReporter()
        counter = _StepCounter(reporter, timer.next if hasattr(timer, 'next') else timer.__next__)
        given = Step('given', counter)

        with given(
                # tildes
                unichr(0xe1) +
                unichr(0xe9) +
                unichr(0xed) +
                unichr(0xf3) +
                unichr(0xfa) +
                ' ' +
                # circumflex
                unichr(0xe0) +
                unichr(0xe8) +
                unichr(0xec) +
                unichr(0xf2) +
                unichr(0xf9) +
                ' ' +
                # # dieresis
                unichr(0xe2) +
                unichr(0xea) +
                unichr(0xee) +
                unichr(0xf4) +
                unichr(0xfb) +
                ' ' +
                # # n tilde
                unichr(0xf1) +
                unichr(0xd1) +
                ' ' +
                # # c cedilla
                unichr(0xe7) +
                unichr(0xc7) +
                ''
        ):
            pass

        report = reporter.received
        self.assertEqual('given ----- ----- ----- -- --', report.name)


