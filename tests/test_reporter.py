from StringIO import StringIO
from unittest.case import TestCase
from pyspecs._reporter import DotReporter


ASSERTION_PASSED = '.'
FAILURE = 'X'
ERROR = 'E'


class TestDotReporter(TestCase):
    def setUp(self):
        self.console = StringIO()
        self.capture = StringIO()
        self.reporter = DotReporter(self.console, self.capture)

    def test_capture_of_output(self):
        with self.reporter:
            message = "Hello, World!"
            print message

        self.assertEqual(message + '\n', self.capture.getvalue())

    def test_success(self):
        self.reporter.success(str(), 'given', str())
        self.assertEqual(self.console.getvalue(), str())
        self.console.buf = str()

        self.reporter.success(str(), 'when', str())
        self.assertEqual(self.console.getvalue(), str())
        self.console.buf = str()

        self.reporter.success(str(), 'collect', str())
        self.assertEqual(self.console.getvalue(), str())
        self.console.buf = str()

        self.reporter.success(str(), 'then', str())
        self.assertEqual(self.console.getvalue(), ASSERTION_PASSED)
        self.console.buf = str()

        self.reporter.success(str(), 'after', str())
        self.assertEqual(self.console.getvalue(), str())
        self.console.buf = str()

    def test_error(self):
        self.reporter.error(str(), 'given', str(), None)
        self.assertEqual(self.console.getvalue(), ERROR)
        self.console.buf = str()

        self.reporter.error(str(), 'when', str(), None)
        self.assertEqual(self.console.getvalue(), ERROR)
        self.console.buf = str()

        self.reporter.error(str(), 'collect', str(), None)
        self.assertEqual(self.console.getvalue(), ERROR)
        self.console.buf = str()

        self.reporter.error(str(), 'then', str(), None)
        self.assertEqual(self.console.getvalue(), ERROR)
        self.console.buf = str()

        self.reporter.error(str(), 'after', str(), None)
        self.assertEqual(self.console.getvalue(), ERROR)
        self.console.buf = str()

    def test_failure(self):
        self.reporter.failure(str(), 'then', None)
        self.assertEqual(self.console.getvalue(), FAILURE)
        self.console.buf = str()