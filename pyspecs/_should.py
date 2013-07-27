class _Should(object):
    """
    Should-style assertion class.
    """
    def __init__(self, value):
        self._value = value
        self._invert = None
        self._expect = None

    @property
    def should(self):
        self._invert = False
        self._expect = EXPECTED
        return self

    @property
    def should_NOT(self):
        self._invert = True
        self._expect = UNEXPECTED
        return self

    def equal(self, expected):
        self._assert(
            lambda: expected == self._value,
            lambda: (self._expect + EQUAL).format(self._value, expected)
        )

    def be_a(self, expected_type):
        self._assert(
            lambda: type(self._value) == expected_type,
            lambda: (self._expect + BE_A).format(
                self._value, expected_type, type(self._value))
        )

    def contain(self, item):
        self._assert(
            action=lambda: item in self._value,
            report=lambda: (self._expect + CONTAIN).format(self._value, item)
        )

    def be_in(self, collection):
        self._assert(
            action=lambda: self._value in collection,
            report=lambda: (self._expect + IN).format(self._value, collection)
        )

    def be_greater_than(self, lesser):
        self._assert(
            action=lambda: self._value > lesser,
            report=lambda: (
                self._expect + GREATER_THAN).format(self._value, lesser)
        )

    def be_less_than(self, greater):
        self._assert(
            action=lambda: self._value < greater,
            report=lambda: (
                self._expect + LESS_THAN).format(self._value, greater)
        )

    def be_greater_than_or_equal_to(self, lesser):
        self._assert(
            action=lambda: self._value >= lesser,
            report=lambda: (
                self._expect + GREATER_THAN_EQUAL).format(self._value, lesser)
        )

    def be_less_than_or_equal_to(self, greater):
        self._assert(
            action=lambda: self._value <= greater,
            report=lambda: (
                self._expect + LESS_THAN_EQUAL).format(self._value, greater)
        )

    def be(self, thing):
        self._assert(
            action=lambda: self._value is thing,
            report=lambda: (self._expect + BE).format(self._value, thing)
        )

    def be_between(self, first, last):
        self._assert(
            action=lambda: first < self._value < last,
            report=lambda: (
                self._expect + BETWEEN).format(self._value, first, last)
        )

    def be_empty(self):
        self._assert(
            action=lambda: not len(self._value),
            report=lambda: (self._expect + BE_EMPTY).format(self._value)
        )

    def raise_a(self, exception, message=None):
        try:
            self._value()

        except exception as e:
            if message is not None and message != e.message:
                raise AssertionError(INCORRECT_EXCEPTION_MESSAGE.format(
                    exception.__name__, message, e.message))

        except Exception as e:
            raise AssertionError(INCORRECT_EXCEPTION.format(
                exception.__name__, e.__class__.__name__))

        else:
            raise AssertionError(NO_EXCEPTION.format(
                self._value.__name__, exception.__name__))

    def raise_an(self, exception, message=None):
        """
        This is merely a grammatical equivalent of self.raise_a(...)
        """
        self.raise_a(exception, message)

    def _assert(self, action, report):
        if self._invert is None:
            raise AssertionError(PREPARATION_ERROR)

        result = action()
        assert (result and not self._invert) or (not result and self._invert), \
            report()


NO_EXCEPTION = "'{0}' executed successfully but should have raised '{1}'!"
INCORRECT_EXCEPTION = "Should have raised '{0}' but raised '{1}' instead."
INCORRECT_EXCEPTION_MESSAGE = "Raised '{0}' as expected but with an " + \
                              "incorrect error message:\n" + \
                              "Expected: '{1}'\n" + \
                              "Received: '{2}'"
BETWEEN = "to be between '{1}' and '{2}'."
BE = "to be '{1}'."
LESS_THAN_EQUAL = "to be less than or equal to '{1}'."
GREATER_THAN_EQUAL = "to be greater than or equal to '{1}'."
LESS_THAN = "to be less than '{1}'."
GREATER_THAN = "to be greater than '{1}'."
IN = "to be in '{1}'."
CONTAIN = "to contain '{1}'."
BE_A = "to be a {1} (was a {2})."
EQUAL = "to equal '{1}'."
BE_EMPTY = "to be empty."
PREPARATION_ERROR = 'You must add calls to .should and .NOT in '\
    'order to execute an assertion!'
EXPECTED = "Expected '{0}' "
UNEXPECTED = EXPECTED + "NOT "


def should_expectation(function):
    setattr(_Should, function.__name__, function)
    return function