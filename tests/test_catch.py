from unittest import TestCase
import sys
from pyspecs import catch


class TestCatch(TestCase):
    def test_without_exception_returns_None(self):
        info = catch(lambda: sum([0]))
        self.assertIsNone(info)

    def test_with_exception_returns_exception_value(self):
        def throw():
            raise ZeroDivisionError('No can do!')

        info = catch(throw)
        self.assertIsInstance(info, ZeroDivisionError)
        self.assertEqual('No can do!', info.message)

    def test_exception_info_reset(self):
        def throw():
            raise ZeroDivisionError('No can do!')

        catch(throw)
        self.assertEqual((None, None, None), sys.exc_info())